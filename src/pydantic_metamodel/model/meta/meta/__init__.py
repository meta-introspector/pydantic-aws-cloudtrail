# generated by datamodel-codegen:
#   filename:  <dict>

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class EventVersion(BaseModel):
    title: str
    type: str


class UserIdentity(BaseModel):
    field_ref: str = Field(..., alias='$ref')


class EventTime(BaseModel):
    title: str
    type: str


class EventSource(BaseModel):
    title: str
    type: str


class EventName(BaseModel):
    title: str
    type: str


class EventId(BaseModel):
    title: str
    type: str


class ReadOnly(BaseModel):
    title: str
    type: str


class EventType(BaseModel):
    title: str
    type: str


class EventCategory(BaseModel):
    title: str
    type: str


class AnyOfItem(BaseModel):
    type: str


class ErrorCode(BaseModel):
    any_of: List[AnyOfItem] = Field(..., alias='anyOf')
    default: None
    title: str


class ErrorMessage(BaseModel):
    any_of: List[AnyOfItem] = Field(..., alias='anyOf')
    default: None
    title: str


class SharedEventId(BaseModel):
    any_of: List[AnyOfItem] = Field(..., alias='anyOf')
    default: None
    title: str


class Properties(BaseModel):
    event_version: EventVersion = Field(..., alias='eventVersion')
    user_identity: UserIdentity = Field(..., alias='userIdentity')
    event_time: EventTime = Field(..., alias='eventTime')
    event_source: EventSource = Field(..., alias='eventSource')
    event_name: EventName = Field(..., alias='eventName')
    event_id: EventId = Field(..., alias='eventID')
    read_only: ReadOnly = Field(..., alias='readOnly')
    event_type: EventType = Field(..., alias='eventType')
    event_category: EventCategory = Field(..., alias='eventCategory')
    error_code: ErrorCode = Field(..., alias='errorCode')
    error_message: ErrorMessage = Field(..., alias='errorMessage')
    shared_event_id: SharedEventId = Field(..., alias='sharedEventID')


class ModelItem(BaseModel):
    properties: Properties
    required: List[str]
    title: str
    type: str


class Secret(BaseModel):
    title: str


class Properties1(BaseModel):
    secret: Secret


class UserIdentity1(BaseModel):
    properties: Properties1
    required: List[str]
    title: str
    type: str


class FieldDefs(BaseModel):
    model_item: ModelItem = Field(..., alias='ModelItem')
    user_identity: UserIdentity1 = Field(..., alias='UserIdentity')


class Items(BaseModel):
    field_ref: str = Field(..., alias='$ref')


class Model(BaseModel):
    field_defs: FieldDefs = Field(..., alias='$defs')
    items: Items
    title: str
    type: str