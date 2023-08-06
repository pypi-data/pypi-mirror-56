"""module used for defining puzzle decorator for submiting or solving problem"""
from .cache_file import cache_file_data
from .config_file import get_all_session
from .server_action import submit_output


class _Puzzle:
    """Puzzle class for handling out a puzzle decorator"""

    def __init__(
        self, function, operation_type, year, day, part, session=None, input_file=None
    ):
        """Initialize _Puzzle class"""
        self.function = function
        self.year = year
        self.day = day
        self.part = part
        if session is None:
            self.session = get_all_session()
        else:
            if isinstance(session, list):
                self.session = session
            else:
                self.session = [session]
        self.operation_type = operation_type
        self.input_file = input_file

    def __call__(self):
        """Caller for _Puzzle class"""
        for session_list in self.session:
            if self.input_file is None:
                input_data = cache_file_data(self.year, self.day, session_list)
            else:
                with open(self.input_file) as opened_file:
                    input_data = opened_file.read()
            answer = self.function(input_data)
            if answer is not None:
                if self.operation_type == "submit":
                    message = submit_output(
                        self.year, self.day, self.part, session_list, answer
                    )
                    if message.contains("Congratulation"):
                        print(
                            "{}:{}-{}-{}: {} {} {}".format(
                                session_list,
                                self.year,
                                self.day,
                                self.part,
                                answer,
                                u"\u2713",
                                message,
                            )
                        )
                    else:
                        print(
                            "{}:{}-{}-{}: {} {} {}".format(
                                session_list,
                                self.year,
                                self.day,
                                self.part,
                                answer,
                                u"\u274C",
                                message,
                            )
                        )
                elif self.operation_type == "solve":
                    print(
                        "{}:{}-{}-{}: {}".format(
                            session_list, self.year, self.day, self.part, answer
                        )
                    )


def submit(year, day, part, session=None, input_file=None):
    """
    Puzzle decorator used to submit a solution to advent_of_code server and provide
    result. If input_file is not present then it tries to download file and cache it
    for submiting solution else it require to be provided with input_file path which
    input it can use out
    """

    def _action(function):
        operation_type = "submit"
        return _Puzzle(function, operation_type, year, day, part, session, input_file)

    return _action


def solve(year, day, part, session=None, input_file=None):
    """
    Puzzle decorator used to only solve a solution & print output value. It doesn't
    submit output to advent of code server to validate out whether an answer is correct
    or not. By default it downloads out input file from advent-of-code server. Puzzle
    can also be solved by using custom file location with help of input_file parameter
    while using input_file year, day, part are required even if they are not used for
    only reference purpose of printing output.
    """

    def _action(function):
        operation_type = "solve"
        return _Puzzle(function, operation_type, year, day, part, session, input_file)

    return _action
