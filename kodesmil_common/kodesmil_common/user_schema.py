from kodesmil_common.object_id import ObjectId
from marshmallow import Schema, fields
import datetime as dt


class UserSchema(Schema):
    _id = ObjectId()
    auth_user_id = fields.Str()
    last_synced_at = fields.DateTime()


def get_user(db, request_data):
    user_id = request_data['user_id']
    match = {'auth_user_id': user_id}
    user = db.users.find_one(match)
    user_schema = UserSchema().load({
        'auth_user_id': user_id,
        'last_synced_at': dt.datetime.now().isoformat(),
    })
    if not user:
        db.users.insert_one(user_schema)
        return db.users.find_one(match)
    else:
        db.users.replace_one(
            match,
            user_schema,
            True,
        )
        return db.users.find_one(match)