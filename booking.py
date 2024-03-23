from abc import ABC, abstractmethod
from customer import Customer
from scheduledtour import ScheduledTour, st1
from datetime import datetime, timezone
import csv


class BookingException(Exception):
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class Booking(ABC):
    _NEXT_ID = 1

    def __init__(self, scheduleTour: ScheduledTour, customers: list):
        if scheduleTour.seatsAvailable >= len(customers):
            self._scheduleTour = scheduleTour
            self._customers = customers
            self._bookingId = Booking._NEXT_ID
            Booking._NEXT_ID += 1
            self.scheduleTour.bookSeats(len(customers))
        else:
            raise BookingException("Not enough seats for customers")

    @property
    def bookingId(self) -> int:
        return self._bookingId

    @property
    def scheduleTour(self) -> ScheduledTour:
        return self._scheduleTour

    @property
    def customers(self) -> list:
        return self._customers

    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def addSeats(self):
        pass

    def searchCustomer(self, passportNumbers: list) -> bool:
        for passportNumber in passportNumbers:
            if passportNumber in self.customers:
                return True
        return False

    def getPenaltyAmount(self) -> float:
        days = datetime.now(timezone.utc).day - self.scheduleTour.departureDatetime.day
        penalty_amount = (
            self.scheduleTour._HANDLING_FEE
            + self.scheduleTour.cost * self.scheduleTour.getPenaltyRate(days)
        )
        if penalty_amount > self.cost():
            return self.cost()
        else:
            return penalty_amount

    def __str__(self) -> str:
        def customerinfo():
            string = ""
            for customer in self.customers:
                string += f"Passport: {customer.passportNumber:<15}Name: {customer.name:<20}Age:{customer.getAge():<8}Contact:{customer.contact}\n"
            return string

        return (
            f"Booking Id: {self.bookingId:< 6}Seats: {len(self.customers):< 6}Final Cost: ${self.cost():,.2f}\n"
            f"{str(self.scheduleTour)}"
            f"{customerinfo()}"
        )


class IndividualBooking(Booking):
    _SINGLE = 0.5

    def __init__(self, scheduledTour: ScheduledTour, customer: Customer, single: bool):
        if customer.getAge() < 20:
            raise BookingException("Customer is less than 20 years old")
        super().__init__(scheduledTour, [customer])
        self._single = single

    def cost(self) -> float:
        if self._single:
            return self.scheduleTour.cost * 1.5

    def addSeats(self) -> bool:
        raise BookingException("Not possible to add seats for individual booking")


class GroupBooking(Booking):
    _DISCOUNT = {10: 0.1, 6: 0.05}

    def __init__(self, scheduledTour: ScheduledTour, customers: list):
        if len(customers) < 2:
            raise BookingException("Group size must be 2 or more")
        new_customers = list(
            filter(lambda customer: customer.getAge() >= 20, customers)
        )
        if not new_customers:
            raise BookingException("All customers are less than 20 years old")
        super().__init__(scheduledTour, customers)

    def getDiscount(self) -> float:
        if len(self._customers) >= 10:
            discount = 10
        elif len(self._customers) >= 6:
            discount = 6
        else:
            discount = None
        return GroupBooking._DISCOUNT.get(discount, 0)

    def cost(self) -> float:
        return len(self.customers) * (self.scheduleTour.cost * (1 - self.getDiscount()))

    def addSeats(self, customers: list) -> bool:
        for customer in customers:
            if customer in self.customers:
                raise BookingException("Customer has already booked")

        if self.scheduleTour.bookSeats(len(customers)):
            self.customers.extend(customers)
            return True
        else:
            raise BookingException("Scheduled tour have reached full capacity")


def main():
    with open("customers.csv") as f:
        customerlist = []
        reader = csv.reader(f)
        next(reader)
        for passno, name, dob, contact in reader:
            parseddob = datetime.strptime(dob, "%Y%m%d")
            customerlist.append(Customer(passno, name, parseddob, int(contact)))

    above20list = list(filter(lambda customer: customer.getAge() > 20, customerlist))
    below20list = list(filter(lambda customer: customer.getAge() < 20, customerlist))
    sortedlist = sorted(customerlist, key=lambda customer: customer.getAge())

    try:
        Bk1 = IndividualBooking(st1, above20list[0], True)
        print(Bk1)
        print("=" * 50)
        print(Bk1.getPenaltyAmount())
        print("=" * 50)
        Bk1.addSeats()
    except BookingException as ex:
        print(ex)
        print("=" * 50)
    try:
        Bk2 = IndividualBooking(st1, below20list[0], True)
    except BookingException as ex:
        print(ex)
        print("=" * 50)
    try:
        Bk3 = GroupBooking(st1, below20list[:2])
    except BookingException as ex:
        print(ex)
        print("=" * 50)
    try:
        bklist = sortedlist[0:4]
        bklist.append(sortedlist[-1])
        Bk4 = GroupBooking(st1, bklist)
        print(Bk4)
        print("=" * 50)
        Bk4.addSeats(sortedlist[4:6])
        print(Bk4)
        print("=" * 50)
    except BookingException as ex:
        print(ex)


if __name__ == "__main__":
    main()