from dataclasses import dataclass

from app.store.database.gino import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String())
    phone = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)


class Hairdresser(db.Model):
    __tablename__ = 'hairdressers'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(), unique=True)
    phone = db.Column(db.String(), unique=True)
    password = db.Column(db.String())


class Administrator(db.Model):
    __tablename__ = 'administrators'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String())
    phone = db.Column(db.String(), unique=True)
    password = db.Column(db.String())


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(), unique=True)
    price = db.Column(db.Integer())
    duration = db.Column(db.Integer())


class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    department = db.Column(db.ForeignKey('departments.id', ondelete="CASCADE"))
    start_day_time = db.Column(db.Integer())
    end_day_time = db.Column(db.Integer())
    day = db.Column(db.Integer())
    hairdressers = []
    _uix = db.UniqueConstraint('department', 'start_day_time', 'end_day_time', 'day', name='uix_shifts')


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String(), unique=True)
    hairdressers = []
    administrators = []
    schedule = None


class Reception(db.Model):
    __tablename__ = 'receptions'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    department = db.Column(db.ForeignKey('departments.id', ondelete="CASCADE"))
    hairdresser = db.Column(db.ForeignKey('hairdressers.id', ondelete="CASCADE"))
    customer = db.Column(db.ForeignKey('customers.id', ondelete="CASCADE"))
    year = db.Column(db.Integer())
    month = db.Column(db.Integer())
    day = db.Column(db.Integer())
    day_time = db.Column(db.Integer())
    services = []


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    key = db.Column(db.String(), unique=True)
    user_type = db.Column(db.String())
    user_id = db.Column(db.Integer())
    die_time = db.Column(db.Integer())


class ReceptionXService(db.Model):
    __tablename__ = 'reception_x_service'

    reception = db.Column(db.ForeignKey('receptions.id', ondelete="CASCADE"))
    service = db.Column(db.ForeignKey('services.id', ondelete="CASCADE"))
    _uix = db.UniqueConstraint('reception', 'service', name='uix_reception_x_service')


class DepartmentXService(db.Model):
    __tablename__ = 'department_x_service'

    department = db.Column(db.ForeignKey('departments.id', ondelete="CASCADE"))
    service = db.Column(db.ForeignKey('services.id', ondelete="CASCADE"))
    _uix = db.UniqueConstraint('department', 'service', name='uix_department_x_service')


class DepartmentXAdministrator(db.Model):
    __tablename__ = 'department_x_administrator'

    department = db.Column(db.ForeignKey('departments.id', ondelete="CASCADE"))
    administrator = db.Column(db.ForeignKey('administrators.id', ondelete="CASCADE"))
    _uix = db.UniqueConstraint('department', 'administrator', name='uix_department_x_administrator')


class DepartmentXHairdresser(db.Model):
    __tablename__ = 'department_x_hairdresser'

    department = db.Column(db.ForeignKey('departments.id', ondelete="CASCADE"))
    hairdresser = db.Column(db.ForeignKey('hairdressers.id', ondelete="CASCADE"))
    _uix = db.UniqueConstraint('department', 'hairdresser', name='uix_department_x_hairdresser')


class ShiftXHairdresser(db.Model):
    __tablename__ = 'shift_x_hairdresser'

    hairdresser = db.Column(db.ForeignKey('hairdressers.id', ondelete="CASCADE"))
    shift = db.Column(db.ForeignKey('shifts.id', ondelete="CASCADE"))
    _uix = db.UniqueConstraint('hairdresser', 'shift', name='uix_shift_x_hairdresser')


@dataclass
class Organization:
    name: str
    password: str
    email: str
