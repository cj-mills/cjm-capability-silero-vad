# Tombstone — `test_reconfigure.py` (RETIRED 2026-06-18, stage 9)

**Origin:** `cjm-media-plugin-silero-vad/tests_manual/test_reconfigure.py` (pre-overhaul).
**Retired because:** imported `MediaAnalysisStorage` from the now-dissolved `cjm-media-plugin-system` (GitHub-archived 2026-06-18; the import was largely vestigial — the test's real subject is a **substrate** contract). Per the stage-9 decision the pre-overhaul `tests_manual` cohort is **retired, not patched**.

**What it validated (substrate CR-4 reconfigure-delta contract, in-process on a real model + real audio):**
1. `execute()` loads the model (`use_onnx=True` backend).
2. `reconfigure(use_onnx` flip`)` must hit a `RELOAD_TRIGGER` → `_release_model` and re-apply via `_apply_config` (the exact behavior CR-4 wired into `PluginManager.update_plugin_config`).
3. The next `execute()` reloads a fresh model on the flipped backend.
4. A **non-trigger** field change (`threshold`) must **NOT** release the model.

**Coverage status:** UNIQUE — the cores' happy-path e2e do NOT exercise the reconfigure delta path. This is the [[contract_level_reconfigure_tests]] pattern.

**Reimplementation target (first principles):** this is a **substrate-behavior** test that happened to live in the silero repo. Reimplement against the **substrate (`cjm-substrate`)** itself — a `_Fake*` tool exercising RELOAD_TRIGGER vs non-trigger deltas — rather than re-homing a tool-specific script. Preserve the trigger-vs-non-trigger release assertion as the key invariant.
