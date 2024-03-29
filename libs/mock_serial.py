import logging
import queue


class SerialException(Exception):
    pass

class ReadTimeout(SerialException):
    pass


class MockSerial:
    """
    A simple Mock Serial port implementation.

    Takes a fake device that receives messages and returns responses. Responses
    are pushed onto a queue one byte at a time to simulate a serial port.
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, port_name : str, mock_device):
        """
        Init
        @param port_name: Name of port; unused, but simulates many serial
                          abstractions
        @param mock_device: A fake device containing a do_write(bytes) method
                            that returns a bytes-like object response or None
        @return:
        """
        assert mock_device is not None

        self._dev = mock_device
        self._recv_queue = queue.Queue()
        self._is_open = False

        print(mock_device)

    def open(self):
        self._is_open = True

    def close(self):
        self._is_open = False

    def write(self, msg: bytes):
        """
        Write message to device
        @param msg: Message to write to device
        @return: Number of bytes written
        """
        if not self._is_open:
            raise SerialException("Port not open!")

        print(self._dev)
        rsp = self._dev.do_write(msg)

        logging.debug("Sent {}".format(msg))

        if rsp is not None:
            for b in rsp:
                self._recv_queue.put(bytes([b]))

        return len(msg)

    def read(self, num_bytes: int, timeout_s: float):
        """
        Read a number of bytes from the receive buffer until timeout
        @param num_bytes: Number of bytes to read
        @param timeout_s: Inter-byte timeout in seconds. How long to wait for
                          a byte to be received.
        @return: Bytes stream
        """
        if not self._is_open:
            raise SerialException("Port not open!")

        msg = bytes()
        for _ in range(num_bytes):
            try:
                b = self._recv_queue.get(timeout=timeout_s)
                msg += b

            except queue.Empty:
                raise ReadTimeout()

        logging.debug("Received {}".format(msg))

        return msg
