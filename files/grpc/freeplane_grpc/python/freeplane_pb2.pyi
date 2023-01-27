from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateChildRequest(_message.Message):
    __slots__ = ["name", "parent_node_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    parent_node_id: str
    def __init__(self, name: _Optional[str] = ..., parent_node_id: _Optional[str] = ...) -> None: ...

class CreateChildResponse(_message.Message):
    __slots__ = ["node_id", "node_text"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_TEXT_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    node_text: str
    def __init__(self, node_id: _Optional[str] = ..., node_text: _Optional[str] = ...) -> None: ...

class DeleteChildRequest(_message.Message):
    __slots__ = ["node_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: str
    def __init__(self, node_id: _Optional[str] = ...) -> None: ...

class DeleteChildResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GroovyRequest(_message.Message):
    __slots__ = ["groovy_code"]
    GROOVY_CODE_FIELD_NUMBER: _ClassVar[int]
    groovy_code: str
    def __init__(self, groovy_code: _Optional[str] = ...) -> None: ...

class GroovyResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class NodeAttributeAddRequest(_message.Message):
    __slots__ = ["attribute_name", "attribute_value", "node_id"]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    attribute_name: str
    attribute_value: str
    node_id: str
    def __init__(self, node_id: _Optional[str] = ..., attribute_name: _Optional[str] = ..., attribute_value: _Optional[str] = ...) -> None: ...

class NodeAttributeAddResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class NodeBackgroundColorSetRequest(_message.Message):
    __slots__ = ["alpha", "blue", "green", "node_id", "red"]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    RED_FIELD_NUMBER: _ClassVar[int]
    alpha: int
    blue: int
    green: int
    node_id: str
    red: int
    def __init__(self, node_id: _Optional[str] = ..., red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ..., alpha: _Optional[int] = ...) -> None: ...

class NodeBackgroundColorSetResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class NodeColorSetRequest(_message.Message):
    __slots__ = ["alpha", "blue", "green", "node_id", "red"]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    RED_FIELD_NUMBER: _ClassVar[int]
    alpha: int
    blue: int
    green: int
    node_id: str
    red: int
    def __init__(self, node_id: _Optional[str] = ..., red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ..., alpha: _Optional[int] = ...) -> None: ...

class NodeColorSetResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class NodeDetailsSetRequest(_message.Message):
    __slots__ = ["details", "node_id"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    details: str
    node_id: str
    def __init__(self, node_id: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class NodeDetailsSetResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class NodeLinkSetRequest(_message.Message):
    __slots__ = ["link", "node_id"]
    LINK_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    link: str
    node_id: str
    def __init__(self, node_id: _Optional[str] = ..., link: _Optional[str] = ...) -> None: ...

class NodeLinkSetResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
