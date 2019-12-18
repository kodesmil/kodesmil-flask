from enum import Enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


class ChatRoomRoles(Enum):
    Admin = 1
    User = 2


class ChatRoomSchema(Schema):
	_id = fields.Str()
	updated_at = fields.Date()


class ChatRoomParticipationSchema(Schema):
	_id = fields.Str()
	user_id = fields.Str()
	role = EnumField(ChatRoomRoles)
	chatroom_id = fields.Str()
	updated_at = fields.Date()


class ChatRoomMessageSchema(Schema):
	_id = fields.Str()
	text = fields.Str()
	author_id = fields.Str()
	chatroom_id = fields.Str()
	created_at = fields.Date()
	updated_at = fields.Date()
