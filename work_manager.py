import documentation
from datetime import datetime
import helper_methods
import pickle

prompt = ">> "


class Session(object):
    """Manages a single work session"""

    time_format = "%d/%m/%Y %H:%M:%S"  # Time format for session

    def __init__(self, startTime=None, endTime=None):
        """Initialize a singe session

        Params:
            startTime -> string -> This is string in format time_format
            endTime -> string -> This is string in format time_format

        Internals:
            start_time -> datetime
            end_time -> datetime

        This function initializes unstarted session, that can be started
        and stopped externaly.
        """
        self.start_time, self.end_time = None, None

        # if supplied check parameter integrity
        if startTime is not None:
            self.start_time = datetime.strptime(startTime, self.time_format)

        if endTime is not None:
            self.end_time = datetime.strptime(endTime, self.time_format)

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
        """ Set's the start time to current time"""
        if self.is_started() is False:
            self.start_time = datetime.today()
            helper_methods.log(3, "Session started!")
        else:
            helper_methods.log(2, "Trying to start already started session")

    def stop(self):
        if self.is_finished() is False:
            self.end_time = datetime.today()
            helper_methods.log(3, "Session stopped!")
        else:
            helper_methods.log(2, "Trying to stop already stopped session!")

    def total_time(self):
        """Return timedelta between beginning and end"""
        if self.is_finished() and self.is_started():
            if self.end_time < self.start_time:
                raise Exception("End time must be after start time")
            return self.end_time - self.start_time
        else:
            helper_methods.log(2, "This session is unfinished !")

    def total_hours(self):
        """ Return total amount of hours in this session"""
        return self.total_time() / (60 * 60)

    def __str__(self):
        return "Session(START: {start_time}, END: {end_time})".format(
            start_time=self.start_time.strftime(self.time_format),
            end_time=self.end_time.strftime(self.time_format)
        )


class CommandProcessor(object):
    """Process the user command

    This class will manage command
    interpretation and will call right
    method to handle it.

    If you add a method to the class that
    can handle some user command, then register
    it here. Your method must be in format
    cmd_[method_name]. You can't duplicate methods
    because  it will create confusion. After you
    register your method, do so in the doc
    """

    def __init__(self, method_handlers):
        """Initialize command processor

        Params:
            * method_handlers -> list -> Objects that may
        contain appropriate methods.

        """
        self.method_handlers = method_handlers
        self.cmds = [
            "save",
            "start_session",
            "stop_session",
            "load_sessions",
            "clear_session",
            "in_memory_sessions"
        ]

    def call(self, user_input):
        """Call appropriate method

        Params:
            * user_input -> string
        """
        cmd_parts = user_input.split(" ")
        cmd = cmd_parts[0]
        arguments = None if len(cmd_parts) == 1 else cmd_parts[1:]
        if cmd.strip().lower() in self.cmds:
            for potential_handler in self.method_handlers:
                funct = getattr(
                    potential_handler,
                    "cmd_{command}".format(command=cmd),
                    None  # default if attr not existent
                )
                if funct is not None:
                    funct(arguments)
                    return
            helper_methods.log(1, "Command registered but unexistent")
        else:
            helper_methods.log(3, "The command doesn't exist")


class WorkManager(object):
    """ Manage work time

    This class will start by reading the worktime file
    that will hold sessions, and then you will be able to
    create new sessions and manage your time. We'll load all
    sessions in memory and then we'll modify it, and save the
    result at exit or at save.
    """

    def __init__(self, ses_file, hourly_price):
        self.ses_file = ses_file
        self.hourly_price = hourly_price
        self.sessions = []
        self.current_session = None

    def save(self, destination=None):
        if destination is None:
            print("Enter the file name to save sessions")
            destination = input(prompt)

        helper_methods.log(3, "Saving the sessions")
        pass

    def cmd_save(self, arguments):
        if len(arguments) != 1:
            helper_methods.log(2, "You should only supply file name")
            return
        file_name = helper_methods.check_file_name(
            allowed_extensions=['time', 'sessions']
        )

        self.save()

    def cmd_start_session(self, arguments):
        """Issue a new session if no session is currently active.currently

        This will start session with this date

        """
        if self.current_session is None:
            self.current_session = Session()
            self.current_session.start()
            self.sessions.append(self.current_session)
        else:
            helper_methods.log(2, "One session is currently active")

    def cmd_stop_session(self, arguments):
        if self.current_session is not None:
            self.current_session.stop()
            self.current_session = None
        else:
            helper_methods.log(2, "No session is started")

    def cmd_load_all(self):
        """TODO : Load session from file """
        pass

    def cmd_in_memory_sessions(self, arguments):
        for session in self.sessions:
            helper_methods.log(3, str(session))


def main():
    """Initialize the work manager """
    try:

        hourly_price = float(
            input("Enter hourly price for today's session : ")
        )
        session_file = input("Enter session file name : ")
        WM = WorkManager(session_file, hourly_price)
        CP = CommandProcessor([WM])
        while 1:
            try:
                CP.call(input(prompt))
            except KeyboardInterrupt:
                WM.save()
                helper_methods.log(3, "\nBye bye")
                break
    except ValueError:
        print("Wrong input type.")


if __name__ == "__main__":

    main()
