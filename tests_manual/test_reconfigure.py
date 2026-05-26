"""Real-world CR-4 reconfigure validation for the Silero VAD plugin.

Exercises the substrate's reconfigure delta path against a REAL model on REAL
audio (in-process; no worker required):

  1. execute() loads the model (use_onnx=True backend)
  2. reconfigure(use_onnx flip) must RELEASE the model (RELOAD_TRIGGER ->
     _release_model) and RE-APPLY the new config (_apply_config) -- the exact
     behavior CR-4 wired into PluginManager.update_plugin_config
  3. next execute() reloads a fresh model on the flipped backend
  4. a non-trigger field change (threshold) must NOT release the model

Requires the gitignored test_files/ audio + the substrate version with the
two-phase reconfigure (CR-4). Run from the repo root in the plugin's env:

    conda run -n cjm-media-plugin-silero-vad --no-capture-output \
        python tests_manual/test_reconfigure.py

Becomes a pytest (with @pytest.mark.real_data) under Track 17.
"""
import os
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(REPO_ROOT, "test_files", "short_test_audio.mp3")


def main() -> int:
    if not os.path.exists(AUDIO):
        print(f"SKIP: test audio not found at {AUDIO} (test_files/ is gitignored)")
        return 0

    from cjm_media_plugin_silero_vad.plugin import SileroVADPlugin
    from cjm_media_plugin_system.storage import MediaAnalysisStorage

    p = SileroVADPlugin()
    if not p.is_available():
        print("SKIP: silero-vad not installed in this env")
        return 0

    from silero_vad import load_silero_vad
    avail = {}
    for onnx in (True, False):
        try:
            load_silero_vad(onnx=onnx); avail[onnx] = True
        except Exception:
            avail[onnx] = False
    print("backends available (onnx, torch):", avail)
    start = True if avail.get(True) else False
    flip = not start

    fd, dbp = tempfile.mkstemp(suffix=".db"); os.close(fd)
    try:
        # minimal in-process init (skip get_plugin_metadata; use a temp store)
        p._apply_config({"use_onnx": start})
        p.storage = MediaAnalysisStorage(dbp)

        r1 = p.execute(AUDIO, force=True)
        assert p._model is not None, "model should be loaded after execute"
        m1 = id(p._model)
        print(f"[1] loaded onnx={start}: {len(r1.ranges)} segments")

        # CR-4 discriminating assertion: reconfigure releases + re-applies
        p.reconfigure({"use_onnx": start}, {"use_onnx": flip})
        assert p._model is None, "RELOAD_TRIGGER must fire _release_model on use_onnx change"
        assert p.config.use_onnx is flip, "reconfigure must re-apply the new config (CR-4)"
        print(f"[2] reconfigure use_onnx {start}->{flip}: released + applied  OK")

        if avail.get(flip):
            r2 = p.execute(AUDIO, force=True)
            assert p._model is not None and id(p._model) != m1, "must reload a fresh model"
            print(f"[3] reloaded onnx={flip}: {len(r2.ranges)} segments  OK")
        else:
            print(f"[3] backend onnx={flip} unavailable; release validated, reload skipped")

        # non-trigger field must NOT release
        p._apply_config({"use_onnx": p.config.use_onnx, "threshold": 0.5})
        p._model = object()
        p.reconfigure({"use_onnx": p.config.use_onnx, "threshold": 0.5},
                      {"use_onnx": p.config.use_onnx, "threshold": 0.7})
        assert p._model is not None, "non-trigger (threshold) change must NOT release the model"
        assert p.config.threshold == 0.7, "config still applied on non-trigger change"
        print("[4] threshold change (non-trigger): model retained + applied  OK")
    finally:
        try:
            os.unlink(dbp)
        except OSError:
            pass

    print("REAL-WORLD RECONFIGURE VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
