from customer import Customer
from tour import Tour 
from scheduledtour import ScheduledTour
from booking import Booking, BookingException, IndividualBooking, GroupBooking


class TourAgency:

    def __init__(self):
        self._tours = []
        self._customers = []
        self._scheduledTours = []
        self._bookings = []

    def searchCustomer(self, passportNumber: str) -> Customer:
        for customer in self._customers:
            if passportNumber == customer.passportNumber:
                return customer
        return None

    def searchTour(self, code: str) -> Tour:
        for tour in self._tours:
            if code == tour.code:
                return tour
        return None

    def searchScheduledTour(self, code: str) -> ScheduledTour:
        for st in self._scheduledTours:
            if code == st.code:
                return st
        return None

    def searchBooking(self, bookingId: int) -> Booking:
        for booking in self._bookings:
            if bookingId == booking.bookingId:
                return booking
        return None

    def listTours(self) -> str:
        string = ""
        for tour in self._tours:
            string += f"{tour}\n"
        return string

    def listBookings(self) -> str:
        string = ""
        for booking in self._bookings:
            string += f"{booking}\n"
        return string

    def listScheduledTours(self) -> str:
        string = ""
        for st in self._scheduledTours:
            string += f"{st}\n"
        return string

    def listOpenScheduledTours(self) -> str:
        string = ""
        for ost in self._scheduledTours:
            if ost.status:
                string += f"{ost}\n"
        return string

    def addCustomer(self, customer: Customer):
        if customer in self._customers:
            raise BookingException("Customer already exists")
        else:
            self._customers.append(customer)

    def addTour(self, tour: Tour):
        if tour in self._tours:
            raise BookingException("Tour already exists")
        else:
            self._tours.append(tour)

    def addScheduledTour(self, st: ScheduledTour):
        if st in self._scheduledTours:
            raise BookingException("Scheduled Tour already exists")
        else:
            self._scheduledTours.append(st)

    def removeScheduledTour(self, code: str):
        st = self.searchScheduledTour(code)
        for bookings in self._bookings:
            if st == bookings.scheduleTour:
                raise BookingException("Scheduled tour has bookings")
        self._scheduledTours.remove(st)

    def addBooking(
        self, st: ScheduledTour, customers: list, type: str, single: bool
    ) -> Booking:
        if st.status:
            for booking in self._bookings:
                if booking.scheduleTour == st:
                    for customer in customers:
                        if customer in booking.customers:
                            raise BookingException(
                                "Customer has already booked for this scheduled tour"
                            )
            if type == "I":
                ibook = IndividualBooking(st, customers[0], single)
                self._bookings.append(ibook)
                return ibook
            else:
                gbook = GroupBooking(st, customers)
                self._bookings.append(gbook)
                return gbook
        else:
            raise BookingException("Scheduled tour is not open for booking")

    def cancelBooking(self, bookingId: int):
        cancelledbook = self.searchBooking(bookingId)
        if not cancelledbook:
            raise BookingException("No booking found from this id")
        if cancelledbook.scheduleTour.cancelSeats(len(cancelledbook.customers)):
            self._bookings.remove(cancelledbook)
        else:
            raise BookingException("Cancelling failed")

    def addSeats(self, bookingId: int, customers: list) -> float:
        booking = self.searchBooking(bookingId)
        if not booking:
            raise BookingException("No booking found from this id")
        if booking.scheduleTour.status:
            oldcost = booking.cost()
            if booking.addSeats(customers):
                return booking.cost() - oldcost
        else:
            raise BookingException("Scheduled tour is not open for booking")
