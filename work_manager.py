from datetime import datetime
from crypto import Crypto
from simplecrypt import DecryptionException
from commands import CommandProcessor
import helper_methods
import json
from getpass import getpass
import os

prompt = "--> "
sessions_storage = "session_files/{filename}"
"""
Do ne

"""
datetime_format = "%d/%m/%Y %H:%M:%S"
date_format = "%d/%m/%Y"
time_format = "%H:%M:%S"


class Session(object):
    """Manages a single work session"""

    def __init__(self, session_manager, startTime=None, endTime=None,
                 paid=None):
        """Initialize a singe session

        Params:
            startTime -> string -> This is string in format datetime_format
            endTime -> string -> This is string in format datetime_format
            paid -> string -> This is true/false
            session_manager -> SessionManager -> This is sessaion manager
            for session

        Internals:
            start_time -> datetime
            end_time -> datetime
            paid -> boolean
            session_manager -> SessionManager

        This function initializes session. It can be unstarted session,
        or a complete session

        """
        self.start_time, self.end_time = None, None
        self.session_manager = session_manager
        # if supplied check parameter integrity
        if startTime is not None and endTime is not None:
            self.start_time = datetime.strptime(startTime.replace("-", " "),
                                                datetime_format)
            self.end_time = datetime.strptime(endTime.replace("-", " "),
                                              datetime_format)
        self.paid = False
        if paid is not None:
            if paid == "true":
                self.paid = True

    def is_finished(self):
        """Check if this session is ended"""
        if self.end_time is not None:
            return True
        return False

    def is_started(self):
        """Check if this session is started"""
        if self.start_time is not None:
            return True
        return False

    def start(self):
        """Start the session with current time"""
        if self.is_started() is False:
            self.start_time = datetime.today()
            helper_methods.log(3, "Session started!")
        else:
            helper_methods.log(2, "Trying to start already started session")

    def stop(self):
        """Stop the session with current time"""
        if self.is_finished() is False:
            self.end_time = datetime.today()
            helper_methods.log(3, "Session stopped!")
        else:
            helper_methods.log(2, "Trying to stop already stopped session!")

    def total_time(self):
        """Return timedelta between beginning and end"""
        if self.is_started():
            if self.is_finished():
                if self.end_time < self.start_time:
                    raise Exception("End time must be after start time")
                return self.end_time - self.start_time
            else:
                return self.current_time()
        else:
            raise Exception("This session is unstarted !")

    def current_time(self):
        """Return time difference from now to start of session"""
        if self.is_started():
            return helper_methods.chop_microseconds(
                datetime.now() - self.start_time
            )
        else:
            helper_methods.log(1, "This session is unstarted!")

    def date(self):
        """Get session date"""
        if self.is_started():
            return self.start_time.strftime(date_format)
        else:
            helper_methods.log(1, "This session is unstarted")

    def total_hours(self):
        """ Return total amount of hours in this session"""
        return self.total_time().total_seconds() / (60 * 60)

    def __str__(self):
        """String reperesentation of session object"""
        if self.end_time is None:
            endTime = "Unfinished"
        else:
            endTime = self.end_time.strftime(datetime_format)

        return "Session(START: {start_time}, END: {end_time})".format(
            start_time=self.start_time.strftime(datetime_format),
            end_time=endTime

        )

    def timerange(self):
        if self.is_finished():
            next_day = ""
            if self.end_time.day > self.start_time.day:
                next_day = "Next day : "  # noqa

            return "%s - %s%s" % (self.start_time.strftime(time_format),
                                  next_day,
                                  self.end_time.strftime(time_format)
                                  )
        else:
            return "Unfinished session"

    def serialize(self):
        """Serializer of the class

        This is used for json encoding the object, for saving
        the sessions data, each class that should be saved should
        have serialize, and deserialize methods
        """

        return {
            "start_time": self.start_time.strftime(datetime_format),
            "end_time": self.end_time.strftime(datetime_format),
            "paid": str(self.paid).lower()
        }

    def deserialize(self, dct):
        """Parse a dict with info about session

        Return serialized data back to create instance of
        Session object
        """
        self.start_time = datetime.strptime(dct['start_time'], datetime_format)
        self.end_time = datetime.strptime(dct['end_time'], datetime_format)
        self.paid = True if dct['paid'] == "true" else False
        return self


class SessionManager(object):
    """Manager of session objects

    This class has interfaces for stopping and starting
    session, and interface to commands with sessions
    """

    def __init__(self):
        self.sessions = {}
        self.current_session = None

    def start_session(self):
        """Start the session

        Before starting the session make sure that
        no session is started. otherwise log a notice
        Register session to a sessions dictionary
        """
        if self.current_session is None:
            self.current_session = Session(self)
            self.current_session.start()
            ses_date = self.current_session.date()
            if ses_date in self.sessions:
                self.sessions[ses_date].append(self.current_session)
            else:
                self.sessions[ses_date] = [self.current_session]

        else:
            helper_methods.log(2, "One session is currently active")

    def stop_session(self):
        """Stop a session

        If there is a session running then stop it
        """
        if self.current_session is not None:
            self.current_session.stop()
            self.current_session = None
        else:
            helper_methods.log(2, "No session is started")

    def current_session_time(self):
        """Get time of current running session"""
        if self.current_session is not None:
            return self.current_session.current_time()
        else:
            return "No session is running at a time"

    def calc_range(self, per_hour, d1, d2):
        """Calulate price and total hours of date range

        Find all sessions that fit in date range, and calc
        price and total working hours for them.
        """
        final_price = 0.0
        total_hours = 0.0
        for date, sessions in self.sessions.items():
            if (datetime.strptime(date, date_format) > d1 and
                    datetime.strptime(date, date_format) < d2):
                for session in sessions:
                    if session.paid is False:
                        total_hours += session.total_hours()
                        final_price += session.total_hours() * per_hour

        return (total_hours, final_price)

    def calc_all(self, per_hour):
        """Calculate all from beginning"""
        final_price = 0.0
        total_hours = 0.0
        for date, sessions in self.sessions.items():
            for session in sessions:
                if session.paid is False:
                    total_hours += session.total_hours()
                    final_price += session.total_hours() * per_hour

        return (total_hours, final_price)

    def calc_one(self, per_hour, date):
        """Get time of just one session"""
        date_str = datetime.strftime(date, date_format)
        total_hours = 0
        total_price = 0
        if date_str in self.sessions:
            for session in self.sessions[date_str]:
                if session.paid is False:
                    total_hours += session.total_hours()
                    total_price += session.total_hours() * per_hour

            return (total_hours, total_price)
        else:
            return (0, 0)

    def calculate_price(self, per_hour, date1=None, date2=None):
        """Calculate price for sessions in date1
        if date2 defined then use date range date1 to date2

        Params:
            * per_hour -> float -> Price per hour
            * date1 -> string -> String in format date_format
            * date2 -> string -> String in format date_format

        This is interface to above functions
        """
        if date1 is not None and date2 is not None:
            d1 = datetime.strptime(date1, date_format)
            d2 = datetime.strptime(date2, date_format)
            return self.calc_range(per_hour, d1, d2)
        elif date1 is not None and date2 is None:
            d1 = datetime.strptime(date1, date_format)
            return self.calc_one(per_hour, d1)
        else:
            return self.calc_all(per_hour)

    def ps_range(self, d1, d2):
        for date, sessions in self.sessions.items():
            if (datetime.strptime(date, date_format) > d1 and
                    datetime.strptime(date, date_format) < d2):
                print("Date: %s" % date)
                for session in sessions:
                    print(" |---%s , %s" % (
                        session.timerange(),
                        "Paid" if session.paid else "Unpaid"
                    ))

    def ps_one(self, date):
        date_str = datetime.strftime(date, date_format)
        if date_str in self.sessions:
            print("Date: %s" % date_str)
            for session in self.sessions[date_str]:
                print(" |---%s , %s" % (
                    session.timerange(),
                    "Paid" if session.paid else "Unpaid"
                ))
        else:
            print("No sessions are registered at that date")

    def ps_all(self):
        for date, sessions in self.sessions.items():
            print("Date: %s" % date)
            for session in sessions:
                print(" |---%s , %s" % (
                    session.timerange(),
                    "Paid" if session.paid else "Unpaid"
                ))

    def print_sessions(self, date1=None, date2=None):
        if date1 is not None and date2 is not None:
            d1 = datetime.strptime(date1, date_format)
            d2 = datetime.strptime(date2, date_format)
            self.ps_range(d1, d2)
        elif date1 is not None and date2 is None:
            d1 = datetime.strptime(date1, date_format)
            self.ps_one(d1)
        else:
            self.ps_all()

    def mp_range(self, d1, d2, paid):
        for date, sessions in self.sessions.items():
            if (datetime.strptime(date, date_format) > d1 and
                    datetime.strptime(date, date_format) < d2):
                for session in sessions:
                    session.paid = paid
        print("Sessions marked as %s" % ("paid" if paid else "unpaid"))

    def mp_one(self, date, paid):
        date_str = datetime.strftime(date, date_format)
        if date_str in self.sessions:
            for session in self.sessions[date_str]:
                session.paid = paid
            print("Sessions marked as %s" % ("paid" if paid else "unpaid"))
        else:
            print("No sessions are registered at that date")

    def mp_all(self, paid):
        for date, sessions in self.sessions.items():
            for session in sessions:
                session.paid = paid
        print("Sessions marked as %s" % ("paid" if paid else "unpaid"))

    def mark_paid(self, date1=None, date2=None):
        if date1 is not None and date2 is not None:
            d1 = datetime.strptime(date1, date_format)
            d2 = datetime.strptime(date2, date_format)
            self.mp_range(d1, d2, True)
        elif date1 is not None and date2 is None:
            d1 = datetime.strptime(date1, date_format)
            self.mp_one(d1, True)
        else:
            self.mp_all(True)

    def mark_unpaid(self, date1=None, date2=None):
        if date1 is not None and date2 is not None:
            d1 = datetime.strptime(date1, date_format)
            d2 = datetime.strptime(date2, date_format)
            self.mp_range(d1, d2, False)
        elif date1 is not None and date2 is None:
            d1 = datetime.strptime(date1, date_format)
            self.mp_one(d1, False)
        else:
            self.mp_all(False)

    def add_session(self, startTime=None, endTime=None, paid=None):
        if startTime is not None and endTime is not None and paid is not None:
            session = Session(self, startTime, endTime, paid)
            date = session.date()
            if date not in self.sessions:
                self.sessions[date] = [session]
                print("Session added successfully!")
            else:
                contains = False
                for ses in self.sessions[date]:
                    if ses.start_time == session.start_time:
                        contains = True
                if not contains:
                    self.sessions[date].append(session)
                    print("Session added successfully!")
                else:
                    print("Session with same start time already exists!")

        else:
            print("Please specify start and end time")

    def remove_sessions(self, date):
        if date in self.sessions:
            mapper = {}
            print("Here are sessions for this date:")
            for i in range(0, len(self.sessions[date])):
                session = self.sessions[date][i]
                print(" " * 4 + str(i) + " -> " + session.timerange())
                mapper[i] = self.sessions[date][i]
            print("Enter , separated numbers of sessions")
            delete = [int(a.strip()) for a in input(prompt).split(',')]
            for d in delete:
                if d in mapper:
                    self.sessions[date].remove(mapper[d])
            if len(self.sessions[date]) == 0:
                del self.sessions[date]

    def serialize(self):
        """Serializer of the class"""
        return {date: [session.serialize() for session in lst] for
                (date, lst) in self.sessions.items()}

    def deserialize(self, dct):
        """Deserializer of the class"""
        self.sessions = {
            date: [Session(session_manager=self).deserialize(session_data) for
                   session_data in lst] for (date, lst) in dct.items()}
        return self


class WorkManager(object):
    """ Main class for CMD and managing files"""

    def __init__(self):
        self.password_tries = 3
        print(
            "Please enter the name of your session "
            "file or name of one you want to create:"
        )
        self.ses_file = sessions_storage.format(
            filename=input(prompt)
        )
        if(os.path.exists(self.ses_file)):
            print("Enter your password")
            self.new_user = False
        else:
            print(
                "Enter your new password for "
                "encrypting/decrypting of this file"
            )
            self.new_user = True

        self.password = getpass(prompt)
        if self.new_user is True:
            print("Enter your hourly price without currency")
            self.hourly_price = float(input(prompt))
            print("Enter currency")
            self.currency = input(prompt)
            self.session_manager = SessionManager()
            self.saved = 0
        else:
            self.load()

    def serialize(self):
        """Class serializer"""
        ret = {
            "last_modified": datetime.now().strftime(datetime_format),
            "hourly_price": self.hourly_price,
            "sessions": self.session_manager.serialize(),
            "currency": self.currency
        }
        return ret

    def deserialize(self, dct):
        """Class deserializer"""
        print(dct)
        self.last_modified = dct['last_modified']
        self.session_manager = SessionManager().deserialize(dct['sessions'])
        self.saved = 0
        self.currency = dct['currency']
        self.hourly_price = float(dct['hourly_price'])
        return self
        # print(self.sessions)

    def save(self):
        print(self.serialize())
        Crypto.write_to_file(
            json.dumps(obj=self.serialize()),
            self.ses_file,
            self.password
        )

    def load(self):
        try:
            decrypted = Crypto.read_from_file(
                self.ses_file,
                self.password
            )
            self.deserialize(json.loads(decrypted))
            helper_methods.log(3, "Loaded config from file")
        except DecryptionException as e:  # noqa
            self.password_tries -= 1
            if self.password_tries == 0:
                exit("File you try to open is corrupt or password "
                     "is incorrect")

            print(str(e) + (" Please type password again,"
                            "you can do it {tries} more times").format(
                tries=self.password_tries
            ))
            self.password = getpass(prompt)
            self.load()

    def cmd_save(self, arguments):
        """Save working state"""
        self.save()

    def cmd_change_h_price(self, arguments):
        try:
            cijena = float(arguments[0])
            self.hourly_price = cijena
            print("Hourly price changed to %s %s" %
                  (self.hourly_price, self.currency)
                  )
        except:
            print("Price must be int of floating point number")

    def cmd_print_sessions(self, arguments):
        self.session_manager.print_sessions(*arguments)

    def cmd_start(self, arguments):
        """Start a new session"""
        self.session_manager.start_session()

    def cmd_stop(self, arguments):
        "Stop current session"
        self.session_manager.stop_session()

    def cmd_ttime(self, arguments):
        print(self.session_manager.current_session_time())

    def cmd_load(self, arguments):
        "Load session from file"
        self.load()

    def cmd_calc(self, arguments):
        """Calculate price

        Params:
            arguments -> string -> for this function can be
                None,
                Single date,
                Date range

        Result contains a tuple with working hours number
        and price with the given hourly_price.
        """
        result = self.session_manager.calculate_price(
            self.hourly_price,
            *arguments
        )
        print("You worked {hours} hours, and earned {amount} "
              "{currency} ".format(
                  hours=round(result[0], 2),
                  amount=round(result[1], 2),
                  currency=self.currency
              ))

    def cmd_add_session(self, arguments):

        self.session_manager.add_session(
            *arguments
        )

    def cmd_remove_sessions(self, arguments):
        self.session_manager.remove_sessions(
            *arguments
        )

    def cmd_mark_paid(self, arguments):
        self.session_manager.mark_paid(*arguments)

    def cmd_mark_unpaid(self, arguments):
        self.session_manager.mark_unpaid(*arguments)

    def cmd_ims(self, arguments):
        for date, session in self.session_manager.sessions.items():
            helper_methods.log(3, date + "===" + str([
                str(ses) for ses in session
            ]))


def main():
    """Initialize the work manager """
    try:

        WM = WorkManager()
        CP = CommandProcessor([WM])
        while 1:
            try:
                cmd = input(prompt)
                if cmd == "exit":
                    raise KeyboardInterrupt()
                CP.call(cmd)
            except KeyboardInterrupt:
                print()
                if WM.saved == 0:
                    WM.save()
                helper_methods.log(3, "\nBye bye")
                break
    except ValueError:
        print("Wrong input type.")


if __name__ == "__main__":
    main()
