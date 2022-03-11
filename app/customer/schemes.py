from marshmallow import Schema, fields


class CustomerRegistrationSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=True)


class CustomerGetRecoverPasswordSchema(Schema):
    email = fields.Str(required=True)


class CustomerEditSchema(Schema):
    new_name = fields.Str()
    new_password = fields.Str()
    new_email = fields.Str()
    new_phone = fields.Str()


class CustomerPostRecoverPasswordSchema(Schema):
    key = fields.Str()
    new_password = fields.Str()


class CustomerAuthorizationSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class CustomerPutReceptionSchema(Schema):
    department = fields.Int(required=True)
    services = fields.List(fields.Int, required=True)
    hairdresser = fields.Int(required=True)
    year = fields.Int(required=True)
    month = fields.Int(required=True)
    day = fields.Int(required=True)
    day_time = fields.Int(required=True)


class CustomerPostReceptionSchema(Schema):
    department = fields.Int(required=True)
    services = fields.List(fields.Int, default=fields.List)
    hairdresser = fields.Int()
    year = fields.Int(required=True)
    month = fields.Int(required=True)
    day = fields.Int(required=True)
    day_time = fields.Int()


class CustomerDeleteReceptionSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class CustomerGetAdministratorSchema(Schema):
    id = fields.Int()


class CustomerGetHairdresserSchema(Schema):
    id = fields.Int()


class CustomerGetDepartmentSchema(Schema):
    id = fields.Int()
    day = fields.Int()
