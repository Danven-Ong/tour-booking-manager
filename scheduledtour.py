from tour import Tour, tour1, tour2, tour3
from datetime import datetime

class ScheduledTour:

    _HANDLING_FEE = 120

    @classmethod
    def getHandlingFee(cls):
        return cls._HANDLING_FEE

    def __init__(
        self,
        scheduleCode: str,
        tour: Tour,
        departureDatetime: datetime,
        lang: str,
        capacity: int,
    ):
        self._scheduleCode = scheduleCode
        self._tour = tour
        self._departureDatetime = departureDatetime
        self._lang = lang
        self._capacity = capacity
        self._seatsAvailable = self.capacity
        self._status = True

    @property
    def departureDatetime(self) -> datetime:
        return self._departureDatetime

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def seatsAvailable(self) -> int:
        return self._seatsAvailable

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, newStatus: bool) -> bool:
        self._status = newStatus

    @property
    def code(self) -> str:
        return self._tour.code + "-" + self._scheduleCode

    @property
    def cost(self) -> float:
        return self._tour.cost

    def bookSeats(self, qty: int) -> bool:
        if self._seatsAvailable - qty >= 0:
            self._seatsAvailable -= qty
            return True
        return False

    def cancelSeats(self, qty: int) -> bool:
        if self._seatsAvailable + qty <= self.capacity:
            self._seatsAvailable += qty
            return True
        return False

    def getPenaltyRate(self, days: int) -> float:
        if days >= 46:
            penalty = 0.1
        elif days > 14:
            penalty = 0.25
        elif days > 7:
            penalty = 0.5
        else:
            penalty = 1
        return penalty

    def __str__(self) -> str:
        return (
            f"Name: {self._tour.name} {self._tour.daysNight:<10}Base Cost: ${self.cost:,.2f}\n"
            f"Code: {self.code:<20}Depature: {self._departureDatetime.strftime('%d-%m-%Y %H:%M'):<25}Language: {self._lang}\n"
            f"Capacity: {self.capacity:<7}Available: {self.seatsAvailable:<7}Open: {'Yes' if self.status else 'No'}\n"
        )


class PeakScheduledTour(ScheduledTour):
    _HANDLING_FEE = 200
    _SURCHARGE = 0.15

    @property
    def cost(self) -> float:
        return self._tour.cost * (1 + PeakScheduledTour._SURCHARGE)

    def getPenaltyRate(self, days: int) -> float:
        if days >= 46:
            penalty = 0.2
        elif days > 14:
            penalty = 0.35
        elif days > 7:
            penalty = 0.6
        else:
            penalty = 1
        return penalty


st1 = ScheduledTour(
    "505",
    tour1,
    datetime.strptime("5-May-2024 10:30", "%d-%b-%Y %H:%M"),
    "English",
    30,
)
st2 = ScheduledTour(
    "408",
    tour1,
    datetime.strptime("8-Apr-2024 8:45", "%d-%b-%Y %H:%M"),
    "English",
    25,
)
st3 = ScheduledTour(
    "503",
    tour2,
    datetime.strptime("3-May-2024 8:05", "%d-%b-%Y %H:%M"),
    "English",
    32,
)
st4 = ScheduledTour(
    "403",
    tour2,
    datetime.strptime("3-Apr-2024 10:05", "%d-%b-%Y %H:%M"),
    "Mandarin",
    25,
)
st5 = ScheduledTour(
    "503",
    tour3,
    datetime.strptime("3-May-2024 11:08", "%d-%b-%Y %H:%M"),
    "Mandarin",
    28,
)
if __name__ == "__main__":
    print(st1)
    print(st2)
    print(st3)
    print(st4)
    print(st5)
