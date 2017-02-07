import time


class WorkManager(object):
    """ Manage work time

    This class will start by reading the worktime file
    that will hold sessions, and then you will be able to
    create new sessions and manage your time.
    """
    prompt = ">> "

    def __init__(self, ses_file, hourly_price):
        self.ses_file = ses_file
        self.hourly_price = hourly_price
        self.running = False
        self.startTime = None

    def start(self):
        while 1:
            cmd = input(self.prompt)
            try:
                funct = getattr(self, "command_{command}".format(command=cmd))
                funct()
            except AttributeError:
                print("Non-existent command.")

    # Methods that user can use.
    def command_help(self):
        print("help")

    def command_ses_start(self):
        if self.running is False:
            self.running = True

    def command_ses_stop(self):
        if self.running is True:
            self.running = False


def main():
    """Initialize the work manager """
    try:

        hourly_price = float( # noqa
                            input("Enter hourly price for today's session : ") # noqa
                       ) # noqa
        session_file = input("Enter session file name : ")
        WM = WorkManager(session_file, hourly_price)
        WM.start()
    except ValueError:
        print("Wrong input type.")


if __name__ == "__main__":

    main()
