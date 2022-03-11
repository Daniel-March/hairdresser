from marshmallow import Schema, fields


class HairdresserAuthorizationSchema(Schema):
    phone = fields.Str(required=True)
    password = fields.Str(required=True)


class HairdresserDeleteReceptionSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class HairdresserGetReceptionSchema(Schema):
    id = fields.Int()


class HairdresserGetDepartmentSchema(Schema):
    id = fields.Int()


class HairdresserGetScheduleSchema(Schema):
    day = fields.Int()


class HairdresserGetShiftSchema(Schema):
    day = fields.Int()


class HairdresserGetCustomerSchema(Schema):
    day = fields.Int(required=True, attribute="id_")


class HairdresserGetAdministratorSchema(Schema):
    day = fields.Int(attribute="id_")


class HairdresserGetServiceSchema(Schema):
    day = fields.Int(attribute="id_")
