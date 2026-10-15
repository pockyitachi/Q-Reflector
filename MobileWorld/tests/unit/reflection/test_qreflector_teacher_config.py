"""Teacher role configuration never leaks a placeholder into an API request."""
import json
import importlib
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from qreflector_teacher_config import configured_prices, resolve_teacher_model, usage_cost


def test_missing_model_fails_before_an_api_request(monkeypatch):
    monkeypatch.delenv('QREFLECTOR_TEACHER_MODEL', raising=False)
    with pytest.raises(ValueError, match='QREFLECTOR_TEACHER_MODEL'):
        resolve_teacher_model('teacher-a')


def test_roles_resolve_independently_and_explicit_ids_are_preserved(monkeypatch):
    monkeypatch.setenv('QREFLECTOR_TEACHER_MODEL', 'custom-model-a')
    monkeypatch.setenv('QREFLECTOR_CORRECTION_MODEL', 'custom-model-b')
    assert resolve_teacher_model('teacher-a') == 'custom-model-a'
    assert resolve_teacher_model('teacher-b') == 'custom-model-b'
    assert resolve_teacher_model('explicit-model') == 'explicit-model'


@pytest.mark.parametrize('value', ['', ' ', 'teacher-a', 'teacher-b'])
def test_configuration_requires_actual_model_ids(monkeypatch, value):
    monkeypatch.setenv('QREFLECTOR_TEACHER_MODEL', value)
    with pytest.raises(ValueError):
        resolve_teacher_model('teacher-a')


def test_prices_are_optional_explicit_and_checked(monkeypatch):
    monkeypatch.delenv('QREFLECTOR_TEACHER_PRICES_JSON', raising=False)
    assert configured_prices('teacher-a') is None
    assert usage_cost({'input_tokens': 100}, None) is None
    rates = {'input': 1, 'cached_input': .1, 'cache_write': 2, 'output': 3}
    monkeypatch.setenv('QREFLECTOR_TEACHER_PRICES_JSON', json.dumps({'teacher-a': rates}))
    assert configured_prices('teacher-a') == rates
    assert configured_prices('teacher-b') is None
    with pytest.raises(ValueError, match='exceed'):
        usage_cost({'input_tokens': 10, 'cached_tokens': 11}, rates)
    monkeypatch.setenv('QREFLECTOR_TEACHER_PRICES_JSON', '{"teacher-a": {"input": -1}}')
    with pytest.raises(ValueError):
        configured_prices('teacher-a')


@pytest.mark.parametrize('module_name', [
    'eval_qreflector_teacher', 'qreflector_condition_check_data',
    'qreflector_v9_distill_dpo', 'qreflector_correction_round1',
    'qreflector_correction_round2', 'qreflector_teacher_pilot_v9',
])
def test_missing_teacher_does_not_leave_a_partially_prepared_run(monkeypatch, tmp_path, module_name):
    monkeypatch.delenv('QREFLECTOR_TEACHER_MODEL', raising=False)
    monkeypatch.delenv('QREFLECTOR_CORRECTION_MODEL', raising=False)
    module = importlib.import_module(module_name)
    output = tmp_path / 'run'
    with pytest.raises(ValueError, match='actual model ID'):
        module.prepare(output)
    assert not output.exists()
