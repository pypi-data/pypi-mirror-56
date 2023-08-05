import json

import pytest

from mythx_models.exceptions import ValidationError
from mythx_models.response import Analysis, AnalysisStatusResponse
from mythx_models.util import serialize_api_timestamp

from . import common as testdata


def assert_analysis_data(expected, analysis: Analysis):
    assert expected["apiVersion"] == analysis.api_version
    assert expected["maruVersion"] == analysis.maru_version
    assert expected["mythrilVersion"] == analysis.mythril_version
    assert expected["harveyVersion"] == analysis.harvey_version
    assert expected["queueTime"] == analysis.queue_time
    assert expected["runTime"] == analysis.run_time
    assert expected["status"] == analysis.status
    assert expected["submittedAt"] == serialize_api_timestamp(analysis.submitted_at)
    assert expected["submittedBy"] == analysis.submitted_by
    assert expected["uuid"] == analysis.uuid


def test_analysis_list_from_valid_json():
    resp = AnalysisStatusResponse.from_json(
        json.dumps(testdata.ANALYSIS_STATUS_RESPONSE_DICT)
    )
    assert_analysis_data(testdata.ANALYSIS_STATUS_RESPONSE_DICT, resp.analysis)


def test_analysis_list_from_empty_json():
    with pytest.raises(ValidationError):
        AnalysisStatusResponse.from_json("{}")


def test_analysis_list_from_valid_dict():
    resp = AnalysisStatusResponse.from_dict(testdata.ANALYSIS_STATUS_RESPONSE_DICT)
    assert_analysis_data(testdata.ANALYSIS_STATUS_RESPONSE_DICT, resp.analysis)


def test_analysis_list_from_empty_dict():
    with pytest.raises(ValidationError):
        AnalysisStatusResponse.from_dict({})


def test_analysis_list_to_dict():
    d = testdata.ANALYSIS_STATUS_RESPONSE_OBJECT.to_dict()
    assert d == testdata.ANALYSIS_STATUS_RESPONSE_DICT


def test_analysis_list_to_json():
    json_str = testdata.ANALYSIS_STATUS_RESPONSE_OBJECT.to_json()
    assert json.loads(json_str) == testdata.ANALYSIS_STATUS_RESPONSE_DICT
