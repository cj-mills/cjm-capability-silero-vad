"""Tests for cjm_capability_silero_vad.capability — pure-compute VAD tool.

Projected from the capability notebook's test cells at the c25780e8 flip
(hermetic: no model download/inference; the detect_speech path is exercised
by the e2e harnesses in tests_manual/)."""
from dataclasses import fields

import pytest

from cjm_capability_silero_vad.capability import SileroVADCapability, SileroVADConfig
from cjm_substrate.core.capability import ToolCapability
from cjm_substrate.utils.validation import SCHEMA_TITLE, dict_to_config


def test_capability_identity_and_availability():
    capability = SileroVADCapability()
    assert isinstance(capability, ToolCapability)
    assert capability.config_class.__name__ == "SileroVADConfig"
    # silero-vad is a hard dependency of this lib's env
    assert capability.is_available() is True
    # identity derives from the installed distribution (PILLAR 1c) — resolvable
    # here because tests run against the installed package, unlike notebook __main__
    assert capability.version


def test_config_fields_stage8_shape():
    names = {f.name for f in fields(SileroVADConfig)}
    # sampling_rate dropped (stage 8 — the upstream ffmpeg convert owns the rate)
    assert "sampling_rate" not in names
    assert {"threshold", "min_speech_duration_ms", "min_silence_duration_ms",
            "speech_pad_ms", "use_onnx"} <= names
    # every field carries a schema title for UI generation
    for f in fields(SileroVADConfig):
        assert f.metadata.get(SCHEMA_TITLE)


def test_config_validation():
    cfg = dict_to_config(SileroVADConfig, {"threshold": 0.5}, validate=True)
    assert cfg.threshold == 0.5
    with pytest.raises(ValueError):
        dict_to_config(SileroVADConfig, {"threshold": 1.5}, validate=True)
    with pytest.raises(ValueError):
        dict_to_config(SileroVADConfig, {"min_speech_duration_ms": -5}, validate=True)


def test_config_schema_for_ui():
    schema = SileroVADCapability().get_config_schema()
    assert schema["name"] == "SileroVADConfig"
    assert len(schema["properties"]) == len(fields(SileroVADConfig))
