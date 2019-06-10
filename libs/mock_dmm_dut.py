import logging
import mock_dmm
import mock_serial


class MockDmmDut:
    def __init__(self, port_name : str):
        self._ser = mock_serial.MockSerial(port_name, mock_dmm.MockDmm())
        self._ser.open()

    def write(self, msg : str):
        return self._ser.write("{}{}".format(msg, mock_dmm.MockDmm.EOM).encode("ascii"))

    def read(self, timeout_s : float):
        rsp = ""
        eom = mock_dmm.MockDmm.EOM
        while True:
            c = self._ser.read(1, timeout_s).decode("ascii")
            rsp += c

            if len(rsp) >= len(eom) and rsp[-len(eom)] == eom:
                rsp = rsp[:-len(eom)]
                break

        return rsp