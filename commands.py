import helper_methods


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
            "ttime",
            "start",
            "change_h_price",
            "clear_sessions",
            "add_session",
            "print_sessions",
            "stop",
            "load",
            "clear",
            "calc",
            "ims"
        ]

    def call(self, user_input):
        """Call appropriate method

        Params:
            * user_input -> string

        Split user command into parts, find
        appropriate method to call from parts[0],
        and call it with arguments parts[1:]
        """
        cmd_parts = user_input.split(" ")
        cmd = cmd_parts[0]
        arguments = [] if len(cmd_parts) == 1 else cmd_parts[1:]
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
