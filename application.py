from datetime import datetime
import csv
from customer import Customer
from tour import Tour
from scheduledtour import ScheduledTour, PeakScheduledTour
from booking import BookingException
from touragency import TourAgency
import re


touragency = TourAgency()
with open("./data/customers.csv") as f:
    reader = csv.reader(f)
    next(reader)

    for passno, name, dob, contact in reader:
        parseddob = datetime.strptime(dob, "%Y%m%d")
        touragency.addCustomer(Customer(passno, name, parseddob, int(contact)))

with open("./data/tours.csv") as f:
    reader = csv.reader(f)
    next(reader)

    for tc, name, days, nights, cost in reader:
        touragency.addTour(Tour(tc, name, int(days), int(nights), float(cost)))

with open("./data/scheduledTours.csv") as f:
    reader = csv.reader(f)
    next(reader)

    for tc, stc, lg, depdt, cap, pk in reader:
        searchtour = touragency.searchTour(tc)
        parseddepdt = datetime.strptime(depdt, "%d-%b-%Y %H:%M")
        cap = int(cap)
        if pk == "Yes":
            touragency.addScheduledTour(
                PeakScheduledTour(stc, searchtour, parseddepdt, lg, cap)
            )
        else:
            touragency.addScheduledTour(
                ScheduledTour(stc, searchtour, parseddepdt, lg, cap)
            )


def schedule_tour():
    print("\nList of available tours:")
    print("=" * 30)
    print(touragency.listTours())

    while True:
        tourcode = input("Enter Tour Code:")

        if not touragency.searchTour(tourcode.upper()):
            print("Tour code does not exist")
            continue
        break

    while True:
        scode = input("Enter Schedule Code:")

        if not re.match("^[1-9][0-9]{2}$", scode):
            print("Schedule code must be a 3 number code")

        elif not touragency.searchScheduledTour(f"{tourcode}-{scode}".upper()):
            break

        else:
            print("Schedule tour code exists")

    while True:
        departuredatetime = input("Enter Departure Datetime in (yyyy-mm-dd HH:MM):")

        try:
            parseddatetime = datetime.strptime(departuredatetime, "%Y-%m-%d %H:%M")
            break
        except ValueError as ex:
            print(ex)
            print("Enter appropriate time format")

    while True:
        lang = input("Language used to conduct the tour:")

        if lang.casefold() not in ["english", "mandarin"]:
            print("Language is not available")
            continue
        lang = lang.capitalize()
        break
    while True:

        capacity = input("Enter capacity:")
        if not re.match(r"^[1-9]+$", capacity):
            print("Invalid capacity number")
            continue
        capacity = int(capacity)
        break

    while True:
        peaknorm = input("(P)eak or (N)ormal:")
        peaknorm = peaknorm.casefold()

        if peaknorm not in ["p", "n"]:
            print("Please enter P or N")
            continue
        break
    searchtour = touragency.searchTour(tourcode.upper())

    try:
        touragency.addScheduledTour(
            ScheduledTour(scode, searchtour, parseddatetime, lang, capacity)
            if peaknorm == "n"
            else PeakScheduledTour(scode, searchtour, parseddatetime, lang, capacity)
        )
        print("Setup complete...\n")
        print(
            ScheduledTour(scode, searchtour, parseddatetime, lang, capacity)
            if peaknorm == "n"
            else PeakScheduledTour(scode, searchtour, parseddatetime, lang, capacity)
        )
    except BookingException as ex:
        print(ex)

def open_close_st():

    if touragency.listScheduledTours() == "":
        print("No scheduled tours to update")
        return
    
    while True:
        stcode = input("Enter Scheduled tour Code to update:").upper()
        searchtour = touragency.searchScheduledTour(stcode)

        if not searchtour:
            print("Scheduled tour not found")
            continue
        print(touragency.searchScheduledTour(stcode))
        break

    while True:
        update = input(
            f"{'Close? (Y/N):' if searchtour.status else 'Open? Y/N:'}"
        ).casefold()

        if update not in ["y", "n"]:
            print("Please enter Y or N")
            continue

        elif update == "y":
            print("Status updated!!")
            searchtour.status = not searchtour.status
            print(searchtour)
        break


def remove_st():

    if not touragency._scheduledTours:
        print("There are no scheduled tours to remove")
        return
    
    while True:
        stcode = input("Enter Scheduled tour Code to remove:").upper()
        searchtour = touragency.searchScheduledTour(stcode)
         
        if not searchtour:
            print("Scheduled tour not found")
            continue
        print(searchtour)
        break

    while True: 
        remove = input("Remove? (Y/N):").casefold()

        if remove not in ["y", "n"]:
            print("Please enter Y or N")
            continue

        elif remove == "y":
            try:
                touragency.removeScheduledTour(stcode)
                print("Removal done...")
            except BookingException as ex:
                print(ex)
        break


def list_st():
    touragency._scheduledTours = sorted(
        touragency._scheduledTours,
        key=lambda st: st.departureDatetime,
    )
    print(f"\n{touragency.listScheduledTours()}")


def validate_input(input_string) -> bool:
    pattern = r"^[A-Za-z]\d{7}[A-Za-z]$"
    return True if re.match(pattern, input_string) else False


def create_book():
    passportnolist = []
    while True:

        passportno = input("Enter passport number:").upper()

        if not validate_input(passportno):
            print("Not valid passport number")

        elif not touragency.searchCustomer(passportno):
            print("Passport number does not exist in tour agency")

        else:
            passportnolist.append(passportno)
            touragency._scheduledTours = sorted(
                touragency._scheduledTours,
                key=lambda st: st.departureDatetime,
            )
            break

    print("List of open scheduled tours:")
    print("=" * 30)
    print(touragency.listOpenScheduledTours())

    while True:
        stcode = input("Enter Schedule Tour Code:").upper()
        searchtour = touragency.searchScheduledTour(stcode)

        if not searchtour or searchtour.status == False:
            print("There are no open scheduled tour with this code")
            continue
        break

    while True:
        igbook = input("(I)ndividual (G)roup Booking?").casefold()

        if igbook not in ["i", "g"]:
            print("Please enter I or G")
            continue

        elif igbook == "i":
            while True:
                single = input("Single Room (Y/N):").casefold()
                if single not in ["y", "n"]:
                    print("Please enter Y or N")
                    continue
                single = True if single == "y" else False
                break

        else:
            while True:
                single = False
                data = input("Enter passport number <enter to stop>").upper()

                if not data:
                    break

                elif not validate_input(data):
                    print("Not valid passport number")

                elif not touragency.searchCustomer(data):
                    print("Passport number does not exist in tour agency")

                elif data in passportnolist:
                    print("Customer already exists")
                        
                else:
                    passportnolist.append(data)

        customerlist = [touragency.searchCustomer(num) for num in passportnolist]

        try:
            bk = touragency.addBooking(searchtour, customerlist, igbook.upper(), single)
            print(f"Booking is added...\n\n{bk}")
        except BookingException as ex:
            print(ex)
        break


def cancel_book():

    if touragency.listBookings() == "":
        print("No bookings to cancel")
        return
    
    while True:
        bookingid = input("Enter booking Id:")

        if not re.match("^[1-9]+$", bookingid):
            print("Booking Id must be a number")
            continue
        searchbook = touragency.searchBooking(int(bookingid))

        if not searchbook:
            print("There is no bookings associated with this Id")
        else:
            print(
                f"{searchbook}\n"
                f"Penalty for cancellation: ${searchbook.getPenaltyAmount():,.2f}"
            )
            break

    while True:
        cancel = input("Proceed to cancel (Y/N):").casefold()

        if cancel not in ["y", "n"]:
            print("Please enter Y or N")
            continue

        if cancel == "y":
            try:
                touragency.cancelBooking(int(bookingid))
                print(
                    f"Cancellation done... "
                    f"Please pay ${searchbook.getPenaltyAmount():,.2f}"
                )
            except BookingException as ex:
                print(ex)
        break


def addseats_book():

    if touragency.listBookings() == "":
        print("No bookings to add seats")
        return
    
    passportnolist = []

    while True:
        bookingid = input("Enter booking Id:")

        if not re.match("^[1-9]+$", bookingid):
            print("Booking Id must be a number")
            continue

        searchbook = touragency.searchBooking(int(bookingid))
        if not searchbook:
            print("There is no bookings associated with this Id")

        elif not searchbook.scheduleTour.status:
            print("Booking is not open for this associated schedule tour")

        else:
            break
    while True:
        data = input("Enter passport number <enter to stop>").upper()

        if not data:
            break

        elif not validate_input(data):
            print("Not valid passport number")

        elif not touragency.searchCustomer(data):
            print("Passport number does not exist in tour agency")

        elif len(searchbook.customers) == 1:
            print("Individual booking cannot add traveller...")
            break

        else:
            passportnolist.append(data)
    customerlist = [touragency.searchCustomer(num) for num in passportnolist]
    try:
        addcost = touragency.addSeats(int(bookingid), customerlist)
        print(f"Seats added, please pay ${addcost:,.2f}")
    except BookingException as ex:
        print(ex)


def list_book():
    touragency._bookings = sorted(
        touragency._bookings,
        key=lambda bk: bk.scheduleTour.code,
    )
    print(touragency.listBookings())


if __name__ == "__main__":
    while True:
        print(
            """<<<< Main Menu >>>>
        1. Tour Management
        2. Book Management
        0. Quit"""
        )

        choice = input("Enter choice:")

        if choice not in ["0", "1", "2"]:
            print("No option")
            continue

        print("")

        if choice == "1":
            while True:

                if choice == "0":
                    print("")
                    break

                print(
                    """<<<< Tour Menu >>>>
            1. Schedule Tour
            2. Open/Close Scheduled Tour
            3. Remove Scheduled Tour
            4. List Scheduled Tours
            0. Back to main menu"""
                )
                choice = input("Enter choice:")

                if choice not in ["0", "1", "2", "3", "4"]:
                    print("No option")
                    continue

                while True:

                    if choice == "1":
                        schedule_tour()
                        break

                    elif choice == "2":
                        open_close_st()
                        break

                    elif choice == "3":
                        remove_st()
                        break

                    elif choice == "4":
                        list_st()
                        break

                    elif choice == "0":
                        break

        elif choice == "2":
            while True:

                if choice == "0":
                    break

                print(
                    """<<<< Booking Menu >>>>
    1. Create Booking
    2. Cancel Booking
    3. Add Seats to Booking
    4. List Bookings
    0. Back to main menu"""
                )
                choice = input("Enter choice:")

                if choice not in ["0", "1", "2", "3", "4"]:
                    print("No option")
                    continue
                while True:

                    if choice == "1":
                        create_book()
                        break

                    elif choice == "2":
                        cancel_book()
                        break

                    elif choice == "3":
                        addseats_book()
                        break

                    elif choice == "4":
                        list_book()
                        break

                    elif choice == "0":
                        break

        elif choice == "0":
            break
