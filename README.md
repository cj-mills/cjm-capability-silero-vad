# cjm-capability-silero-vad

<!-- generated from the context graph by `cjm-context-graph readme` — do not edit by hand; edit the graph (the urge to hand-edit = move it on-graph) -->

A Silero-based Voice Activity Detection (VAD) capability for the cjm-substrate runtime that provides high-accuracy speech segmentation.

## Modules

- **`cjm_capability_silero_vad.__init__`**
- **`cjm_capability_silero_vad.capability`** — Pure-compute voice-activity-detection tool capability using Silero VAD (Option C, stage 8).

## API

### `cjm_capability_silero_vad.capability`

- `SileroVADCapability` _class_ — Voice Activity Detection tool capability using Silero VAD (stage 8: pure compute).
- `SileroVADConfig` _class_ — Configuration for Silero VAD parameters.

## Dependencies

**Depends on:** `cjm-capability-primitives`, `cjm-substrate`, `numpy`, `onnxruntime`, `silero-vad`, `soundfile`
