from marshmallow import Schema, fields


class AdministratorGetCustomerSchema(Schema):
    id = fields.Int()


class AdministratorGetHairdresserSchema(Schema):
    id = fields.Int()


class AdministratorGetAdministratorSchema(Schema):
    id = fields.Int()


class AdministratorGetDepartmentSchema(Schema):
    id = fields.Int()


class AdministratorGetReceptionSchema(Schema):
    id = fields.Int(attribute="id_")


class AdministratorGetShiftSchema(Schema):
    id = fields.Int()


class AdministratorGetSessionSchema(Schema):
    id = fields.Int(attribute="id_")


class AdministratorDeleteSessionSchema(Schema):
    id = fields.Int(required=True, attribute="key_or_id")


class AdministratorGetServiceSchema(Schema):
    id = fields.Int()


class AdministratorDeleteShiftSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class AdministratorDeleteReceptionSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class AdministratorPostShiftSchema(Schema):
    id = fields.Int(required=True, attribute="id_")
    new_start_day_time = fields.Int()
    new_end_day_time = fields.Int()
    new_day = fields.Int()
    new_hairdressers = fields.List(fields.Int)


class AdministratorPutShiftSchema(Schema):
    department = fields.Int(required=True)
    start_day_time = fields.Int(required=True)
    end_day_time = fields.Int(required=True)
    day = fields.Int(required=True)
    hairdressers = fields.List(fields.Int, required=True)


class AdministratorPostDepartmentSchema(Schema):
    id = fields.Int(required=True)
    new_hairdressers = fields.List(fields.Int)
    new_services = fields.List(fields.Int)


class AdministratorAuthorizationSchema(Schema):
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
