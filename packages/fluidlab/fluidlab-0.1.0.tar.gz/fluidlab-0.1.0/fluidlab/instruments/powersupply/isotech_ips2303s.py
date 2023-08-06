"""Iso-tech IPS 2303S
=====================

.. autoclass:: IsoTechIPS2303S
   :members:
   :private-members:

"""

__all__ = ["IsoTechIPS2303S"]

from serial.tools.list_ports import comports

from fluidlab.instruments.drivers import Driver
from fluidlab.interfaces.serial_inter import SerialInterface

from fluidlab.instruments.features import QueryCommand, FloatValue


class FloatValueIPS(FloatValue):
    """Particular value for the driver IsoTechIPS2303S."""

    _fmt = "{:5.3f}"

    def __init__(self, name, doc="", command_set=None):

        if command_set is None:
            raise ValueError("command_set should be a string.")

        command_get = command_set + "?\r\n"

        super().__init__(
            name=name, doc=doc, command_set=command_set, command_get=command_get
        )

    def _convert_from_str(self, value):
        return float(value[:-1])

    def get(self):
        """Get the value from the instrument."""
        result = self._convert_from_str(self._interface.query(self.command_get))
        self._check_value(result)
        return result

    def set(self, value, warn=True):
        """Set the value in the instrument."""
        self._check_value(value)
        self._interface.write(
            self.command_set + ":" + self._convert_as_str(value) + "\n"
        )
        if warn:
            self._check_instrument_value(value)


class IsoTechIPS2303S(Driver):
    """Driver for the power supply IPS 2303S.

    Parameters
    ----------

    baudrate : {9600, 57600, 115200}

      The baud rate (symbol per second). Warning: it is written in the
      documentation of the device that the baudrate has to be equal to
      57600 or 115200. Actually, before I modified this parameter I
      was able to communicate with the device only with a baud rate of
      9600 Bd.

    """

    def __init__(self, baudrate=115_200):

        if baudrate not in [9600, 57600, 115_200]:
            raise ValueError("baudrate has to be in [9600, 57600, 115200].")

        port = None
        for info_port in comports():
            if "0403" in info_port[2] and "6001" in info_port[2]:
                port = info_port[0]

        if port is None:
            raise ValueError("The device does not seem to be plugged.")

        interface = SerialInterface(
            port, baudrate=baudrate, bytesize=8, parity="N", stopbits=1, timeout=1
        )

        super().__init__(interface)

    def set_beep(self, ok_for_beep=True):
        """Set beep on or off."""
        if ok_for_beep:
            value = 1
        else:
            value = 0
        self.interface.write(f"BEEP{value}\n")

    def set_output_state(self, on=True):
        """Set output state on or off.

        If the output state is off, there is no output.

        """
        if on:
            value = 1
        else:
            value = 0
        self.interface.write(f"OUT{value}\n")

    def set_operation_mode(self, tracking="independent"):
        """Set the operation mode (tracking).

        Parameters
        ----------

        tracking : {'independent', 'series', 'parallel'}

          The tracking mode.

        """

        if tracking == "independent":
            value = 0
        elif tracking == "series":
            value = 1
        elif tracking == "parallel":
            value = 2
        else:
            raise ValueError(
                "tracking has to be in ['independent', 'series', 'parallel']"
            )

        self.interface.write(f"TRACK{value}\n")

    def set_baud(self, baud=115_200):
        """Set baud rate for the serial communication.

        parameters
        ----------

        baud : {115200, 57600}
          The baud rate (symbol per second).

        """
        if baud == 115_200:
            value = 0
        elif baud == 57600:
            value = 1
        else:
            raise ValueError("baud has to be in [115200, 57600]")

        self.interface.write(f"BAUD{value}\n")
        self.interface.serial_port.baudrate = baud

    def print_device_help(self):
        """Print internal help."""
        print(
            self._query_help()
            + "\n\nMost of the command are implemented in this driver. "
            "For them, you do not need to know the exact internal command."
        )


def _parse_status_code(code):
    status = {}
    if code[0] == "0":
        status["mode_CH1"] = "CC"
    else:
        status["mode_CH1"] = "CV"
    if code[1] == "0":
        status["mode_CH2"] = "CC"
    else:
        status["mode_CH2"] = "CV"

    tracking = code[2:4]
    if tracking == "01":
        status["tracking"] = "independent"
    elif tracking == "11":
        status["tracking"] = "series"
    elif tracking == "10":
        status["tracking"] = "parallel"
    else:
        status["tracking"] = "?"

    if code[4] == "0":
        status["beep"] = "off"
    else:
        status["beep"] = "on"

    if code[6] == "0":
        status["output"] = "off"
    else:
        status["output"] = "on"

    return status


def _parse_to_float(s):
    return float(s[:-1])


features = [
    QueryCommand(
        "query_identification", "Identification query", command_str="*IDN?\r\n"
    ),
    QueryCommand(
        "query_status",
        "Query status\n\n"
        "Return a dictionary containing information of the device.",
        command_str="STATUS?\r\n",
        parse_result=_parse_status_code,
    ),
    QueryCommand(
        "_query_help", "Query help (list of commands).", command_str="HELP?\r\n"
    ),
    QueryCommand(
        "query_error_message", "Query error message.", command_str="ERR?\r\n"
    ),
]

for channel in [1, 2]:
    features.extend(
        [
            FloatValueIPS(
                f"iset{channel}",
                doc=f"Target output current for channel {channel} (A).",
                command_set=f"ISET{channel}",
            ),
            FloatValueIPS(
                f"vset{channel}",
                doc=f"Target output voltage for channel {channel} (V).",
                command_set=f"VSET{channel}",
            ),
            QueryCommand(
                f"get_iout{channel}",
                f"Get the actual current for channel {channel} (A).",
                f"IOUT{channel}?\r\n",
                parse_result=_parse_to_float,
            ),
            QueryCommand(
                f"get_vout{channel}",
                f"Get the actual voltage for channel {channel}. (V)",
                f"VOUT{channel}?\r\n",
                parse_result=_parse_to_float,
            ),
        ]
    )


IsoTechIPS2303S._build_class_with_features(features)


def for_dev_idn_with_serial():
    import serial

    port = None
    for info_port in comports():
        if "0403:6001" in info_port[2]:
            port = info_port[0]

    if port is None:
        raise ValueError("The device does not seem to be plugged.")

    sp = serial.Serial(
        port=port,
        baudrate=9600,  # warning: does work for higher baudrate!
        timeout=1,
        bytesize=8,
        parity="N",
        stopbits=1,
    )

    sp.readline()
    sp.write("*IDN?\r\n")
    print(sp.readline())

    return sp


def for_dev_idn_with_visa():
    import visa

    rm = visa.ResourceManager("@py")

    # for r in rm.list_resources():
    #     if 'ttyUSB' in r:
    #         resource_name = r

    # print(resource_name)

    resource_name = "ASRL/dev/ttyUSB0::INSTR"
    instr = rm.open_resource(resource_name)
    instr.write("*IDN?\r\n")
    print(instr.read())


if __name__ == "__main__":
    # sp = for_dev_idn_with_serial()
    # for_dev_idn_with_visa()

    pwrsupp = IsoTechIPS2303S()
