import logging
import random
import re
import collections
import queue


class MockDmm:
    """
    Mock Digital Multimeter with serial interface.

    End-of-message is ASCII 0x0A.

    Commands
    --------
    * VER: Get Version
    * SN: Get Serial Number
    * RD: Read Voltage
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    EOM = "\n"
    Command = collections.namedtuple("Command", ["regex", "cmd_func"])

    SYNTAX_ERROR = "SYNTAX ERROR"
    EXECUTE_ERROR = "EXECUTE ERROR"

    def __init__(self):
        """
        Init
        """
        self._cmds = [
            self.Command(re.compile("RD"), self._read_volts),
            self.Command(re.compile("SN"), self._serial_number),
            self.Command(re.compile("VER"), self._version),
        ]

        self._msg_queue = queue.Queue()

        print('Started')

    def do_write(self, input_data: bytes):
        """
        Peform a simulated write.

        Takes an input and pushes bytes to a queue. Processes a message if EOM
        is detected.

        SYNTAX_ERROR is returned if EOM is detected, but command is invalid.

        @param input: Stream of bytes received by Mock DMM
        @return: Stream of bytes. Empty bytes-object if no command yet 
                 received to parse.
        """
        logging.debug("Input {}".format(input_data))
        rsp = bytes()

        msgs = []
        for c in input_data.decode("ascii"):
            if c == self.EOM:
                # Get Message since EOM is found
                msg = ""
                while True:
                    try:
                        msg += self._msg_queue.get_nowait()

                    except queue.Empty:
                        break

                msgs.append(msg)

            else:
                self._msg_queue.put(c)

        for msg in msgs:
            # New Message exists -> Parse
            logging.debug("Parsing {}...".format(msg))
            cmd_rsp = self.SYNTAX_ERROR
            for regex, cmd_func in self._cmds:
                if regex.fullmatch(msg):
                    cmd_rsp = cmd_func() + self.EOM

            logging.debug("Response {}".format(cmd_rsp))
            rsp += cmd_rsp.encode("ascii")

        return rsp

    def _version(self):
        return "1.0.0"

    def _serial_number(self):
        return "10203040"

    def _read_volts(self):
        return "{:.6E}".format(random.random() * 10.0)
