"""Explicit model and pricing configuration for external teacher workflows."""
from __future__ import annotations

import json
import math
import os


TEACHER_ENV = {
    "teacher-a": "QREFLECTOR_TEACHER_MODEL",
    "teacher-b": "QREFLECTOR_CORRECTION_MODEL",
}


def resolve_teacher_model(model):
    """Resolve public role names before building a request or freezing a run."""
    if not isinstance(model, str) or not model.strip():
        raise ValueError("A teacher model ID must be configured")
    model = model.strip()
    if model not in TEACHER_ENV:
        return model
    variable = TEACHER_ENV[model]
    configured = os.environ.get(variable, "").strip()
    if not configured or configured in TEACHER_ENV:
        raise ValueError(f"Set {variable} to an actual model ID before running this workflow")
    return configured


def configured_prices(role):
    """Optional user-supplied USD-per-million rates; never assume model prices."""
    raw = os.environ.get("QREFLECTOR_TEACHER_PRICES_JSON", "")
    if not raw:
        return None
    values = json.loads(raw)
    if not isinstance(values, dict):
        raise ValueError("QREFLECTOR_TEACHER_PRICES_JSON must be an object keyed by teacher role")
    rates = values.get(role)
    if rates is not None:
        validate_prices(rates)
    return rates


def validate_prices(rates):
    keys = {"input", "cached_input", "cache_write", "output"}
    if not isinstance(rates, dict) or set(rates) != keys:
        raise ValueError("Supply input, cached_input, cache_write, and output prices")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or
           not math.isfinite(v) or v < 0 for v in rates.values()):
        raise ValueError("Teacher prices must be finite nonnegative numbers")


def usage_cost(counts, rates):
    if rates is None:
        return None
    validate_prices(rates)
    inp = counts.get("input_tokens", 0)
    cached = counts.get("cached_tokens", counts.get("cached_input_tokens", 0))
    writes = counts.get("cache_write_tokens", 0)
    if cached + writes > inp:
        raise ValueError("Cached and cache-write tokens exceed input tokens")
    return ((inp - cached - writes) * rates["input"] +
            cached * rates["cached_input"] + writes * rates["cache_write"] +
            counts.get("output_tokens", 0) * rates["output"]) / 1e6
