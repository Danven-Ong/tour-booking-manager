from datetime import datetime, timezone


class Customer:
    def __init__(self, passportNumber: str, name: str, dob: datetime, contact: int):
        self._passportNumber = passportNumber
        self._name = name
        self._dob = dob
        self._contact = contact

    @property
    def passportNumber(self) -> str:
        return self._passportNumber

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact(self) -> int:
        return self._contact

    @property
    def dob(self) -> datetime:
        return self._dob

    @contact.setter
    def contact(self, newContact: int) -> int:
        self._contact = newContact

    def getAge(self) -> int:
        return datetime.now(timezone.utc).year - self.dob.year

    def __str__(self) -> str:
        return f"Passport: {self.passportNumber:<15}Name: {self.name:<20}Age: {self.getAge():<6}Contact: {self.contact}"
