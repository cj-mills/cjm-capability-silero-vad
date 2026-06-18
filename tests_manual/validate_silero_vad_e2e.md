# Tombstone — `validate_silero_vad_e2e.py` (RETIRED 2026-06-18, stage 9)

**Origin:** `cjm-media-plugin-silero-vad/tests_manual/validate_silero_vad_e2e.py` (Phase-3-bundle era).
**Retired because:** imported `MediaAnalysisResult` from the now-dissolved `cjm-media-plugin-system.core` shim (GitHub-archived 2026-06-18; the VAD result DTO is now `VADResult` in `cjm-capability-primitives`). Per the stage-9 decision the pre-overhaul `tests_manual` cohort is **retired, not patched**.

**What it validated:** the v2.0 manifest carries a non-empty `description`, binary-only resources (no quantitative `min_*_mb`), and the WORKER_ENV with a static `OMP_NUM_THREADS` default + empty `install.env_vars` (var moved onto the class); a real VAD analysis via `JobQueue.submit → wait_for_job` through a spawned worker (proving WORKER_ENV is composed + injected at `Popen`), asserting speech ranges detected; CPU-plugin empirical rows (gpu peak 0).

**Coverage status:** SUPERSEDED — all three cores exercise the VAD path on the task channel (silero = the first `vad` task family); schema-v2 validation covers the manifest.

**Reimplementation target:** none required (cores are the standing harness).
