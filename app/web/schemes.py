from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str()


class ServiceSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    duration = fields.Int(required=True)


class DepartmentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    hairdressers = fields.Nested(UserSchema, many=True)
    administrators = fields.Nested(UserSchema, many=True)
    services = fields.Nested(ServiceSchema, many=True)


class DepartmentGeneralSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)


class ShiftSchema(Schema):
    id = fields.Int(required=True)
    start_day_time = fields.Int(required=True)
    end_day_time = fields.Int(required=True)
    day = fields.Int(required=True)
    hairdressers = fields.Nested(UserSchema, required=True, many=True)


class ScheduleItemSchema(Schema):
    start_day_time = fields.Int(required=True)
    end_day_time = fields.Int(required=True)
    day = fields.Int(required=True)


class SessionSchema(Schema):
    id = fields.Int(required=True)
    user_type = fields.Str(required=True)
    user_id = fields.Int(required=True)
    die_time = fields.Int(required=True)


class ReceptionSchema(Schema):
    id = fields.Int(required=True)
    department = fields.Nested(DepartmentGeneralSchema)
    services = fields.Nested(ServiceSchema, many=True)
    hairdresser = fields.Nested(UserSchema)
    customer = fields.Nested(UserSchema)
    year = fields.Int(required=True)
    month = fields.Int(required=True)
    day = fields.Int(required=True)
    day_time = fields.Int(required=True)
