# Copyright 2026 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI

from app.telemetry.otel import otel

# `app.telemetry` re-exports the singleton under the name `otel`, which shadows the submodule.
otel_module = importlib.import_module("app.telemetry.otel")


@pytest.fixture
def isolated_otel(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Reset the singleton's providers and keep the process-global OTel state untouched."""
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:1")
    monkeypatch.setattr(otel, "_meter_provider", None)
    monkeypatch.setattr(otel, "_tracer_provider", None)
    monkeypatch.setattr(otel_module.metrics, "set_meter_provider", MagicMock())
    monkeypatch.setattr(otel_module.trace, "set_tracer_provider", MagicMock())
    monkeypatch.setattr(otel_module.FastAPIInstrumentor, "instrument_app", MagicMock())
    yield
    if otel._meter_provider is not None:
        otel._meter_provider.shutdown()


def test_instrumenting_the_app_configures_the_meter_provider(
    isolated_otel: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The HTTP metrics of the FastAPI instrumentation go nowhere without a meter provider."""
    monkeypatch.setattr(otel, "telemetry_enabled", True)

    otel.instrument_fastapi_app(FastAPI())

    assert otel._meter_provider is not None
    otel_module.metrics.set_meter_provider.assert_called_once_with(otel._meter_provider)


def test_instrumenting_the_app_leaves_the_meter_provider_unset_when_telemetry_is_disabled(
    isolated_otel: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(otel, "telemetry_enabled", False)

    otel.instrument_fastapi_app(FastAPI())

    assert otel._meter_provider is None
    otel_module.metrics.set_meter_provider.assert_not_called()
