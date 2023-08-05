"""
Tests for the response_encoders library
"""
from dataclasses import dataclass
from pydantic.dataclasses import dataclass as pydantic_dataclass

import pytest

from gqlclient import dataclass_encoder, json_encoder, dict_encoder


@dataclass
class ChildResponseModel:
    s: str
    i: int


@dataclass
class ParentResponseModel:
    a: str
    c: ChildResponseModel


@dataclass
class MutationResponseModel:
    mutation_response: ParentResponseModel


@pydantic_dataclass
class PydanticChildResponseModel:
    s: str
    i: int


@pydantic_dataclass
class PydanticParentResponseModel:
    a: str
    c: PydanticChildResponseModel


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance",
    [
        (  # dataclass query response without a list
            "call",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            ParentResponseModel,
            ParentResponseModel(a="foo", c=ChildResponseModel(s="bar", i=1)),
        ),
        (  # dataclass query response with a list
            "call",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            ParentResponseModel,
            [
                ParentResponseModel(a="foo1", c=ChildResponseModel(s="bar1", i=1)),
                ParentResponseModel(a="foo2", c=ChildResponseModel(s="bar2", i=2)),
            ],
        ),
        (  # pydantic dataclass query response without a list
            "call",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            PydanticParentResponseModel,
            PydanticParentResponseModel(a="foo", c=PydanticChildResponseModel(s="bar", i=1)),
        ),
        (  # pydantic dataclass query response with a list
            "call",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            PydanticParentResponseModel,
            [
                PydanticParentResponseModel(a="foo1", c=PydanticChildResponseModel(s="bar1", i=1)),
                PydanticParentResponseModel(a="foo2", c=PydanticChildResponseModel(s="bar2", i=2)),
            ],
        ),
        (  # dataclass mutation response without a list
            "call",
            {"call": {"mutation_response": {"a": "foo", "c": {"s": "bar", "i": 1}}}},
            MutationResponseModel,
            MutationResponseModel(
                mutation_response=ParentResponseModel(a="foo", c=ChildResponseModel(s="bar", i=1))
            ),
        ),
    ],
)
def test_dataclass_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert dataclass_encoder(call_base, response, response_cls) == expected_response_cls_instance


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance",
    [
        (  # response without a list
            "foo",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            ParentResponseModel,
            '{"call": {"a": "foo", "c": {"s": "bar", "i": 1}}}',
        ),
        (  # response with a list
            "foo",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            ParentResponseModel,
            '{"call": [{"a": "foo1", "c": {"s": "bar1", "i": 1}}, {"a": "foo2", "c": {"s": "bar2", "i": 2}}]}',
        ),
    ],
)
def test_json_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert json_encoder(call_base, response, response_cls) == expected_response_cls_instance


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance",
    [
        (  # response without a list
            "foo",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            ParentResponseModel,
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
        ),
        (  # response with a list
            "foo",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            ParentResponseModel,
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
        ),
    ],
)
def test_dict_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert dict_encoder(call_base, response, response_cls) == expected_response_cls_instance
