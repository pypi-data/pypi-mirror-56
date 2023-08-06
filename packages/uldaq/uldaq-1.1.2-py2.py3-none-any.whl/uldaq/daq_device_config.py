"""
Created on Feb 17 2018

@author: MCC
"""

from ctypes import create_string_buffer, c_uint, byref, c_longlong, c_bool
from .ul_exception import ULException
from .ul_c_interface import lib, UlInfoItem, DevConfigItem
from .ul_enums import DevVersionType


class DaqDeviceConfig:
    """
    An instance of the DaqDeviceConfig class is obtained by calling
    :func:`DaqDevice.get_config`.
    """

    def __init__(self, handle):
        self.__handle = handle

    def get_version(self, version_type):
        # type: (DevVersionType) -> str
        """
        Gets the version of the firmware specified on the device
        referenced by the :class:`DaqDevice` object, specified
        by :class:`DevVersionType`, and returns it as a string.

        Args:
            version_type (DevVersionType): The type of firmware.

        Returns:
            str:
            
            The version of the specified type of firmware.

        Raises:
            :class:`ULException`
        """
        string_len = c_uint(100)
        info_str = create_string_buffer(string_len.value)
        err = lib.ulDevGetConfigStr(self.__handle, UlInfoItem.VER_STR,
                                    version_type, info_str, byref(string_len))
        if err != 0:
            raise ULException(err)
        return info_str.value.decode('utf-8')

    def has_exp(self):
        # type: () -> bool
        """
        Determines whether the device referenced by the :class:`DaqDevice`
        object has an expansion board attached.

        Returns:
            bool:

            True if an expansion board is attached.
            False if no expansion board is attached.

        Raises:
            :class:`ULException`
        """
        has_exp = c_longlong()
        err = lib.ulDevGetConfig(self.__handle, DevConfigItem.HAS_EXP, 0,
                                 byref(has_exp))
        if err != 0:
            raise ULException(err)
        return c_bool(has_exp).value
