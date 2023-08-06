"""Features for defining drivers (:mod:`fluidlab.instruments.features`)
=======================================================================

.. todo:: Work on the documentation of :mod:`fluidlab.instruments.features`.

Provides:

.. autoclass:: Feature
   :members:
   :private-members:

.. autoclass:: WriteCommand
   :members:
   :private-members:

.. autoclass:: QueryCommand
   :members:
   :private-members:

.. autoclass:: Value
   :members:
   :private-members:

.. autoclass:: BoolValue
   :members:
   :private-members:

.. autoclass:: StringValue
   :members:
   :private-members:

.. autoclass:: NumberValue
   :members:
   :private-members:

.. autoclass:: IntValue
   :members:
   :private-members:

.. autoclass:: FloatValue
   :members:
   :private-members:

.. autoclass:: RegisterValue
   :members:
   :private-members:

"""
import warnings, time
import six


def custom_formatwarning(message, category, filename, lineno, line=None):
    return f"{filename}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = custom_formatwarning
warnings.simplefilter("always", UserWarning)
# warnings.simplefilter('always', Warning)
# warnings.simplefilter('always')


class Feature:
    def __init__(self, name, doc=""):
        self._name = name
        self.__doc__ = doc


class WriteCommand(Feature):
    def __init__(self, name, doc="", command_str=""):
        super().__init__(name, doc)
        self.command_str = command_str

    def _build_driver_class(self, Driver):
        """Add a "write function" to the driver class

        """
        command_str = self.command_str

        def func(self):
            self._interface.write(command_str)

        func.__doc__ = self.__doc__
        setattr(Driver, self._name, func)


class QueryCommand(Feature):
    def __init__(self, name, doc="", command_str="", parse_result=None):
        super().__init__(name, doc)
        self.command_str = command_str
        self.parse_result = parse_result

    def _build_driver_class(self, Driver):
        """Add a "query function" to the driver class

        """
        command_str = self.command_str

        parse_result = self.parse_result

        if parse_result is None:

            def func(self):
                return self._interface.query(command_str)

        else:

            def func(self):
                return parse_result(self._interface.query(command_str))

        func.__doc__ = self.__doc__
        setattr(Driver, self._name, func)


class SuperValue(Feature):
    def _build_driver_class(self, Driver):
        name = self._name
        setattr(Driver, name, self)


class Value(SuperValue):
    _fmt = "{}"

    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        check_instrument_value=True,
        pause_instrument=0.0,
        channel_argument=False,
    ):
        super().__init__(name, doc)
        self.command_set = command_set
        self.check_instrument_value_after_set = check_instrument_value

        self.pause_instrument = pause_instrument
        # certains appareils plantent si on leur parle sans faire de pauses

        self.channel_argument = channel_argument
        # if true, then get() and set() needs a channel argument
        # in that case, command_get and command_set strings are provided
        # with python string format arguments {channel} and {value}

        if command_get is None and command_set is not None:
            command_get = command_set + "?"

        self.command_get = command_get

    def _check_value(self, value):
        pass

    def _check_instrument_value(self, value):
        pass

    def _convert_from_str(self, value):
        return value.strip()

    def _convert_as_str(self, value):
        return self._fmt.format(value)

    def get(self, channel=0):
        """Get the value from the instrument.
           Optional argument 'channel' is used for multichannel instrument.
           Then command_get should include '{channel:}'
        """
        if isinstance(channel, list) or isinstance(channel, tuple):
            return [self.get(c) for c in channel]
        if self.pause_instrument > 0:
            time.sleep(self.pause_instrument)
        command = self.command_get
        if self.channel_argument:
            command = command.format(channel=channel)
        if self.pause_instrument > 0:
            result = self._convert_from_str(
                self._interface.query(command, time_delay=self.pause_instrument)
            )
        else:
            result = self._convert_from_str(self._interface.query(command))
        self._check_value(result)
        return result

    def set(self, value, channel=0):
        """Set the value in the instrument.
           Optional argument 'channel' is used for multichannel instrument.
           Then command_set argument should include '{channel:}' and '{value:}'
        """
        if self.pause_instrument > 0:
            time.sleep(self.pause_instrument)
        self._check_value(value)
        if self.channel_argument:
            # here we don't call _convert_as_str to allow the user to choose
            # the desired format in the command_set string
            command = self.command_set.format(channel=channel, value=value)
        else:
            command = self.command_set + " " + self._convert_as_str(value)
        self._interface.write(command)
        if self.check_instrument_value_after_set:
            self._check_instrument_value(value)


class ReadOnlyBoolValue(Value):
    def get(self):
        return self._interface.read_readonlybool(self._adress)


class BoolValue(Value):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        check_instrument_value=True,
        pause_instrument=0.0,
        channel_argument=False,
        true_string="1",
        false_string="0",
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
        self.true_string = true_string
        self.false_string = false_string

    def _convert_from_str(self, value):
        value = value.strip()
        if value == self.false_string:
            return False

        else:
            return True

    def _convert_as_str(self, value):
        if value:
            return self.true_string

        else:
            return self.false_string

    def _check_instrument_value(self, value):
        instr_value = self.get()
        if instr_value != value:
            msg = (
                self._name
                + " could not be set to "
                + str(value)
                + " and was set to "
                + str(instr_value)
                + " instead"
            )
            warnings.warn(msg, UserWarning)


class StringValue(Value):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        valid_values=None,
        check_instrument_value=True,
        pause_instrument=0.0,
        channel_argument=False,
    ):
        super().__init__(
            name,
            doc,
            command_set=command_set,
            command_get=command_get,
            check_instrument_value=check_instrument_value,
            pause_instrument=pause_instrument,
            channel_argument=channel_argument,
        )
        self.valid_values = valid_values

    def _check_value(self, value):
        value = value.lower()
        if self.valid_values is not None and value not in self.valid_values:
            raise ValueError(
                'Value "{}" not in valid_values, which is equal to {}'.format(
                    value, repr(self.valid_values)
                )
            )

    def _check_instrument_value(self, value):
        value = value.lower()
        instr_value = self.get().lower()
        if not (value.startswith(instr_value)):
            msg = (
                self._name
                + " could not be set to "
                + str(value)
                + " and was set to "
                + str(instr_value)
                + " instead"
            )
            warnings.warn(msg, UserWarning)


class ReadOnlyInt16Value(Value):
    def get(self):
        return self._interface.read_readonlyint16(self._adress)


class Int16Value(Value):
    def get(self):
        return self._interface.read_int16(self._adress)

    def set(self, value, signed=False):
        self._interface.write_int16(self._adress, value, signed)


class DecimalInt16Value(Int16Value):
    def __init__(self, name, doc="", address=0, number_of_decimals=0):
        self._number_of_decimals = number_of_decimals
        super().__init__(name, doc, address)

    def get(self):
        raw_value = super().get()

        if self._number_of_decimals == 0:
            return raw_value

        else:
            return float(raw_value) / 10 ** self._number_of_decimals

    def set(self, value, check=True, signed=False):
        """Set the Value to value.

        If check, checks that the value was properly set.
        """
        if self._number_of_decimals == 0:
            raw_int = int(value)
        else:
            raw_int = int(value * 10 ** self._number_of_decimals)

        super().set(raw_int, signed)

        if check:
            self._check_value(value)

    def _check_value(self, value):
        """After a value is set, checks the instrument value and
        sends a warning if it doesn't match."""
        instr_value = self.get()
        if instr_value != value:
            msg = (
                "Value {} could not be set to {} and was set " "to {} instead"
            ).format(self._name, value, instr_value)
            warnings.warn(msg, UserWarning)


class Int16StringValue(SuperValue):
    def __init__(self, name, doc="", int_dict=None, adress=0):
        self._adress = adress
        self._int_dict = int_dict
        string_dict = {}
        for k in int_dict:
            string_dict[int_dict[k]] = k
        self._string_dict = string_dict
        super().__init__(name, doc)

    def get(self):
        return self._int_dict[self._interface.read_int16(self._adress)]

    def set(self, string):
        self._interface.write_int16(self._adress, self._string_dict[string])


class ReadOnlyFloat32Value(Value):
    def get(self):
        return self._interface.read_readonlyfloat32(self._adress)


class Float32Value(Value):
    def get(self):
        return self._interface.read_float32(self._adress)

    def set(self, value):
        self._interface.write_float32(self._adress, value)


class NumberValue(Value):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        limits=None,
        check_instrument_value=True,
        pause_instrument=0.0,
        channel_argument=False,
    ):
        super().__init__(
            name,
            doc,
            command_set=command_set,
            command_get=command_get,
            check_instrument_value=check_instrument_value,
            pause_instrument=pause_instrument,
            channel_argument=channel_argument,
        )

        if limits is not None and len(limits) != 2:
            raise ValueError("limits have to be a sequence of length 2 or None")

        self.limits = limits

    def _check_value(self, value):
        if self.limits is None:
            return

        lim_min = self.limits[0]
        lim_max = self.limits[1]

        if lim_min is not None and value < lim_min:
            raise ValueError(
                f"Value ({value}) is smaller than lim_min ({lim_min})"
            )

        if lim_max is not None and value > lim_max:
            raise ValueError(
                f"Value ({value}) is larger than lim_max ({lim_max})"
            )

    def _check_instrument_value(self, value):
        instr_value = self.get()
        if abs(instr_value - value) > 0.001 * abs(value):
            msg = (
                self._name
                + " could not be set to "
                + str(value)
                + " and was set to "
                + str(instr_value)
                + " instead"
            )
            warnings.warn(msg, UserWarning)


class FloatValue(NumberValue):
    _fmt = "{:f}"

    def _convert_from_str(self, value):
        return float(value)


class FloatScientificValue(NumberValue):
    _fmt = "{:.5e}"

    def _convert_from_str(self, value):
        return float(value)


class IntValue(NumberValue):
    _fmt = "{:d}"

    def _convert_from_str(self, value):
        return int(value)


class RegisterValue(NumberValue):
    def __init__(
        self,
        name,
        doc="",
        command_set=None,
        command_get=None,
        keys=None,
        default_value=0,
        check_instrument_value=True,
        pause_instrument=0.0,
        channel_argument=False,
    ):

        if keys is None:
            raise ValueError("Keys has to contain the keys of the register.")

        self.keys = keys
        self.nb_bits = len(keys)

        limits = (0, 2 ** self.nb_bits)

        super().__init__(
            name,
            doc,
            command_set=command_set,
            command_get=command_get,
            limits=limits,
            check_instrument_value=check_instrument_value,
            pause_instrument=pause_instrument,
            channel_argument=channel_argument,
        )

        if isinstance(default_value, int):
            self.default_value = self.compute_dict_from_number(default_value)
        elif isinstance(default_value, dict):
            for k in default_value.keys():
                if k not in keys:
                    raise ValueError(f"key {k} not in keys")

            for k in keys:
                default_value.setdefault(k, False)
            self.default_value = default_value
        else:
            raise ValueError("default_value has to be an int or a dict.")

    def _build_driver_class(self, Driver):
        name = self._name
        setattr(Driver, name, self)

    def get_as_number(self):
        """Get the register as number."""
        value = self._interface.query(self.command_get)
        self._check_value(value)
        return value

    def get(self):
        """Get the register as dictionary."""
        number = self.get_as_number()
        return self.compute_dict_from_number(number)

    def set(self, value):
        """Set the register.

        Parameters
        ----------

        value : {dict, int}
           The value as a dictionnary or an integer.

        """

        if isinstance(value, dict):
            value = self.compute_number_from_dict(value)

        self._check_value(value)
        self._interface.write(self.command_set + f" {value}")

    def compute_number_from_dict(self, d):
        for k in d.keys():
            if k not in self.keys:
                raise ValueError(f"key {k} not in keys")

        self._complete_dict_with_default(d)

        number = 0
        for i, k in enumerate(self.keys):
            if d[k]:
                number += 2 ** i
        return number

    def compute_dict_from_number(self, number):
        s = bin(number)[2:].zfill(self.nb_bits)

        d = {}
        for i, k in enumerate(self.keys):
            d[k] = s[-1 - i] == "1"

        return d

    def _complete_dict_with_default(self, d):
        for k, v in self.default_value.items():
            d.setdefault(k, v)
