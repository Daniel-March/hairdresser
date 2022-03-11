from app.web.app import Application
from app.web.models import Shift, Department, Service


class MainManager:
    @staticmethod
    async def make_schedule(app: Application, department: Department | int, day: int = None):
        if type(department) is not Department:
            department = await app.store.department_accessor.get_by_id(department)
        if day is not None:
            day = int(day)

        shifts = await app.store.shift_accessor.get_by_department(department)
        shifts_by_id: dict[int:list[int, int, int]] = {}
        shifts_by_day: dict[int:list[int, int, int]] = {n: [] for n in range(7)}
        schedule = []

        for shift in shifts:
            shifts_by_id[shift.id] = [shift.start_day_time, shift.end_day_time, shift.day]

        for shift in shifts_by_id.values():
            shifts_by_day[shift[2]].append(shift)

        for shifts in shifts_by_day.values():
            shifts = sorted(shifts)
            for i in range(len(shifts) - 1, 0, -1):
                if shifts[i - 1][1] < shifts[i][0]:
                    continue
                if shifts[i - 1][0] <= shifts[i][0] <= shifts[i - 1][1]:
                    shifts[i - 1][1] = shifts[i][1]
                    del shifts[i]
                if shifts[i - 1][0] >= shifts[i][0] <= shifts[i - 1][1]:
                    shifts[i - 1][0] = shifts[i][0]
                    shifts[i - 1][1] = shifts[i][1]
                    del shifts[i]

        for shifts in shifts_by_day.values():
            for shift in shifts:
                schedule.append(Shift(start_day_time=shift[0],
                                      end_day_time=shift[1],
                                      day=shift[2]))
        if day is None:
            return schedule
        return [shift for shift in schedule if shift.day == day]

    @staticmethod
    async def get_available_time_for_reception(app: Application,
                                               department: int,
                                               services: list[int] | list[Service],
                                               hairdresser: int | None,
                                               year: int,
                                               month: int,
                                               day: int):
        if len(services) > 0 and type(services[0]) is int:
            services: list[Service] = [await app.store.service_accessor.get_by_id(service) for service in services]
        required_time = sum([service.duration for service in services])
        available_time = []
        if hairdresser is None:
            for hairdresser in await app.store.hairdresser_accessor.get_by_department(department):
                receptions = await app.store.reception_accessor.get_by_date(day=day, month=month, year=year)
                receptions = [reception for reception in receptions if reception.hairdresser.id == hairdresser.id]
                shifts = await app.store.shift_accessor.get_by_hairdresser(hairdresser)
                shifts = [[shift.start_day_time, shift.end_day_time] for shift in shifts]
                for reception in receptions:
                    r_required_time = sum([service.duration for service in reception.services])
                    for shift in shifts:
                        if shift[0] <= reception.day_time <= shift[1]:
                            if shift[0] != reception.day_time:
                                shifts.append([shift[0], reception.day_time])
                            if shift[1] != reception.day_time + r_required_time:
                                shifts.append([reception.day_time + r_required_time, shift[1]])
                            shifts.remove(shift)
                            break
                for shift in shifts:
                    if shift[1] - shift[0] >= required_time:
                        available_time.append(shift)
        else:
            receptions = await app.store.reception_accessor.get_by_date(day=day, month=month, year=year)
            receptions = [reception for reception in receptions if reception.hairdresser.id == hairdresser]
            shifts = await app.store.shift_accessor.get_by_hairdresser(hairdresser)
            shifts = [[shift.start_day_time, shift.end_day_time] for shift in shifts]
            for reception in receptions:
                r_required_time = sum([service.duration for service in reception.services])
                for shift in shifts:
                    if shift[0] <= reception.day_time < shift[1]:
                        if shift[0] != reception.day_time:
                            shifts.append([shift[0], reception.day_time])
                        if shift[1] != reception.day_time + r_required_time:
                            shifts.append([reception.day_time + r_required_time, shift[1]])
                        shifts.remove(shift)
                        break
            for shift in shifts:
                if shift[1] - shift[0] >= required_time:
                    available_time.append(shift)
        available_time.sort()
        for i in range(len(available_time) - 1, 0, -1):
            if available_time[i - 1][0] <= available_time[i][0] <= available_time[i - 1][1]:
                if available_time[i][1] <= available_time[i - 1][1]:
                    del available_time[i]
                else:
                    available_time[i-1][1] = available_time[i][1]
                    del available_time[i]
            available_time[i][1] -= required_time
        available_time[0][1] -= required_time
        return available_time

    @staticmethod
    async def get_available_services_for_reception(app: Application,
                                                   department: int,
                                                   services: list[int],
                                                   hairdresser: int | None,
                                                   year: int,
                                                   month: int,
                                                   day: int,
                                                   day_time: int | None):
        services = [await app.store.service_accessor.get_by_id(service) for service in services]
        required_time = sum([service.duration for service in services])
        all_services = [i for i in await app.store.service_accessor.get_by_department(department) if
                        i.id not in services]
        available_services = []
        if hairdresser is None:
            available_time = await MainManager.get_available_time_for_reception(app=app,
                                                                                department=department,
                                                                                services=services,
                                                                                hairdresser=hairdresser,
                                                                                year=year,
                                                                                month=month,
                                                                                day=day)
            for time in available_time:
                for service in all_services:
                    if day_time is None:
                        if time[1] - time[0] >= required_time + service.duration:
                            available_services.append(service)
                    else:
                        if day_time >= time[0] and day_time + required_time + service.duration <= time[1]:
                            available_services.append(service)
        else:
            hairdresser = await app.store.hairdresser_accessor.get_by_id(hairdresser)
            receptions = await app.store.reception_accessor.get_by_date(day=day, month=month, year=year)
            receptions = [reception for reception in receptions if reception.hairdresser.id == hairdresser.id]
            shifts = await app.store.shift_accessor.get_by_hairdresser(hairdresser)
            shifts = [[shift.start_day_time, shift.end_day_time] for shift in shifts]
            for reception in receptions:
                r_required_time = sum([service.duration for service in reception.services])
                for shift in shifts:
                    if shift[0] <= reception.day_time <= shift[1]:
                        if shift[0] != reception.day_time:
                            shifts.append([shift[0], reception.day_time])
                        if shift[1] != reception.day_time + r_required_time:
                            shifts.append([reception.day_time + r_required_time, shift[1]])
                        shifts.remove(shift)
                        break
            for shift in shifts:
                for service in all_services:
                    if day_time is None:
                        if shift[1] - shift[0] >= required_time + service.duration:
                            available_services.append(service)
                    else:
                        if day_time >= shift[0] and day_time + required_time + service.duration <= shift[1]:
                            available_services.append(service)

        return available_services

    @staticmethod
    async def get_available_hairdressers_for_reception(app: Application,
                                                       department: int,
                                                       services: list[int],
                                                       year: int,
                                                       month: int,
                                                       day: int,
                                                       day_time: int | None):
        services = [await app.store.service_accessor.get_by_id(service) for service in services]
        required_time = sum([service.duration for service in services])
        hairdressers = await app.store.hairdresser_accessor.get_by_department(department)
        available_hairdressers = []
        for hairdresser in hairdressers:
            receptions = await app.store.reception_accessor.get_by_date(day=day, month=month, year=year)
            receptions = [reception for reception in receptions if reception.hairdresser.id == hairdresser.id]
            shifts = await app.store.shift_accessor.get_by_hairdresser(hairdresser)
            shifts = [[shift.start_day_time, shift.end_day_time] for shift in shifts]

            for reception in receptions:
                r_required_time = sum([service.duration for service in reception.services])
                for shift in shifts:
                    if shift[0] <= reception.day_time <= shift[1]:
                        if shift[0] != reception.day_time:
                            shifts.append([shift[0], reception.day_time])
                        if shift[1] != reception.day_time + r_required_time:
                            shifts.append([reception.day_time + r_required_time, shift[1]])
                        shifts.remove(shift)
                        break
            for shift in shifts:
                if day_time is None:
                    if shift[1] - shift[0] >= required_time:
                        available_hairdressers.append(hairdresser)
                        break
                else:
                    if day_time >= shift[0] and day_time + required_time <= shift[1]:
                        available_hairdressers.append(hairdresser)
                        break

        return available_hairdressers
