from marshmallow import Schema, fields


class OrganizationAuthorizationSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class OrganizationGetCustomerSchema(Schema):
    id = fields.Int()


class OrganizationGetHairdresserSchema(Schema):
    id = fields.Int()


class OrganizationPutHairdresserSchema(Schema):
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)


class OrganizationPostHairdresserSchema(Schema):
    id = fields.Int(required=True)
    new_name = fields.Str()
    new_phone = fields.Str()
    new_password = fields.Str()


class OrganizationDeleteHairdresserSchema(Schema):
    id = fields.Int(required=True)


class OrganizationGetAdministratorSchema(Schema):
    id = fields.Int()


class OrganizationPutAdministratorSchema(Schema):
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)


class OrganizationPostAdministratorSchema(Schema):
    id = fields.Int(required=True)
    new_name = fields.Str()
    new_phone = fields.Str()
    new_password = fields.Str()


class OrganizationDeleteAdministratorSchema(Schema):
    id = fields.Int(required=True)


class OrganizationGetSessionSchema(Schema):
    id = fields.Int(attribute="id_")


class OrganizationGetServiceSchema(Schema):
    id = fields.Int()


class OrganizationPutServiceSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    duration = fields.Int(required=True)


class OrganizationPostServiceSchema(Schema):
    id = fields.Int(required=True, attribute="id_")
    new_name = fields.Str()
    new_price = fields.Int()
    new_duration = fields.Int()


class OrganizationDeleteServiceSchema(Schema):
    id = fields.Int(required=True)


class OrganizationGetDepartmentSchema(Schema):
    id = fields.Int()
    day = fields.Int()


class OrganizationGetReceptionSchema(Schema):
    id = fields.Int()


class OrganizationDeleteReceptionSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class OrganizationGetShiftSchema(Schema):
    id = fields.Int()


class OrganizationPutShiftSchema(Schema):
    department = fields.Int(required=True)
    start_day_time = fields.Int(required=True)
    end_day_time = fields.Int(required=True)
    day = fields.Int(required=True)
    hairdressers = fields.List(fields.Int, required=True)


class OrganizationPostShiftSchema(Schema):
    id = fields.Int(required=True, attribute="id_")
    new_start_day_time = fields.Int()
    new_end_day_time = fields.Int()
    new_day = fields.Int()
    new_hairdressers = fields.List(fields.Int)


class OrganizationDeleteShiftSchema(Schema):
    id = fields.Int(required=True, attribute="id_")


class OrganizationDeleteSessionSchema(Schema):
    id = fields.Int(required=True, attribute="key_or_id")


class OrganizationPutDepartmentSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    administrators = fields.List(fields.Int, required=True, default=[])
    hairdressers = fields.List(fields.Int, required=True, default=[])
    services = fields.List(fields.Int, required=True, default=[])


class OrganizationPostDepartmentSchema(Schema):
    id = fields.Int(required=True, attribute="id_")
    new_name = fields.Str()
    new_address = fields.Str()
    new_administrators = fields.List(fields.Int)
    new_hairdressers = fields.List(fields.Int)
    new_services = fields.List(fields.Int)


class OrganizationDeleteDepartmentSchema(Schema):
    id = fields.Int(required=True)
