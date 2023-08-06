"""lauda
========

.. autoclass:: Lauda
   :members:
   :private-members:


"""

__all__ = ["Lauda"]

from fluidlab.instruments.drivers import Driver
from fluidlab.interfaces import PhysicalInterfaceType
from fluidlab.instruments.features import Value
from time import sleep


class LaudaException(Exception):
    pass


class LaudaValue(Value):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        check_instrument_value=False,
        pause_instrument=0.5,
        channel_argument=False,
    ):
        super().__init__(
            name,
            doc,
            command_set,
            command_get,
            check_instrument_value,
            pause_instrument,
            channel_argument,
        )

    def get(self):
        result = super().get()
        if len(result) < 3:
            print(result.decode("ascii"))
            raise LaudaException("Erreur de communication")

        elif result.startswith(b"ERR"):
            raise LaudaException("Erreur Lauda: " + result)

        else:
            return float(result)

    def set(self, value):
        command = self.command_set.format(value).encode("ascii")
        self._interface.write(command)
        sleep(self.pause_instrument)
        confirmation = self._interface.read()
        if confirmation != b"OK":
            print(confirmation.decode("ascii"))
            raise LaudaException("Erreur de communication")


class LaudaOnOffValue(LaudaValue):
    Supported_ROM = [1200]

    def __init__(self):
        super().__init__(name="onoff", command_get="IN_MODE_02\r")

    def get(self):
        if self._driver.rom in LaudaOnOffValue.Supported_ROM:
            resultat = super().get()
            return True if (resultat == "1") else False

        else:
            return True

    def set(self, value):
        if value:
            self._interface.write(b"START\r")
            sleep(self.pause_instrument)


class LaudaStatValue(Value):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        check_instrument_value=False,
        pause_instrument=0.5,
        channel_argument=False,
    ):
        super().__init__(
            name,
            doc,
            command_set,
            command_get,
            check_instrument_value,
            pause_instrument,
            channel_argument,
        )

    def get(self):
        result = super().get().decode("ascii")
        if len(result) < 3:
            raise LaudaException("Erreur de communication")

        elif result.startswith("ERR"):
            raise LaudaException("Erreur Lauda: " + result)

        else:
            print(result)
            return {
                "overheat": True if (result[0] == "1") else False,
                "lowlevel": True if (result[1] == "1") else False,
                "pumperr": True if (result[2] == "1") else False,
                "controllererror1": True if (result[3] == "1") else False,
                "controllererror2": True if (result[4] == "1") else False,
            }


class Lauda(Driver):
    # Below is the list of models which has been tested
    # Your model has to be in the list, otherwise a NotImplemented
    # will be raised. This is to avoid to inadvertantly use
    # untested model without knowning.
    Models = {"RP  845": 845, "RP  855": 855, "E200": 200, "VC": 1200}
    default_physical_interface = PhysicalInterfaceType.Serial
    default_inter_params = {
        "baudrate": 9600,
        "bytesize": 8,
        "parity": "N",
        "stopbits": 1,
        "timeout": 1,
        "xonxoff": False,
        "rtscts": False,
        "dsrdtr": False,
    }

    def __enter__(self):
        super().__enter__()
        identification = self.interface.query(b"TYPE\r").decode("ascii")
        if identification not in Lauda.Models:
            if len(identification) > 0:
                raise LaudaException("Unsupported model: " + identification)

            else:
                raise LaudaException(
                    "Cannot communicate with Lauda on " + str(self.port)
                )

        else:
            self.rom = Lauda.Models[identification]
            print("Identification: " + identification)
        return self


features = [
    LaudaValue(
        "setpoint", command_get="IN_SP_00\r", command_set="OUT_SP_00 {:.2f}\r"
    ),
    LaudaStatValue("stat", command_get="STAT\r"),
    LaudaValue("temperature", command_get="IN_PV_00\r"),
    LaudaValue("waterlevel", command_get="IN_PV_05\r"),
    LaudaOnOffValue(),
]

Lauda._build_class_with_features(features)

if __name__ == "__main__":
    lauda = Lauda("/dev/ttyS0")
    lauda.setpoint.set(15.0)
    try:
        while True:
            print(lauda.temperature.get())
            sleep(1.0)
    except KeyboardInterrupt:
        pass
