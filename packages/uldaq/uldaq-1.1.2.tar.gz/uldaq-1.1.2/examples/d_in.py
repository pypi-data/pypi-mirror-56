#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        dio_device.d_in()

    Purpose:                          Reads the value of the first supported
                                      digital port

    Demonstration:                    Displays the value of the first digital
                                      port
    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Verify that the DAQ device has a digital input subsystem
    4. Call daq_device.connect() to establish a UL connection to the DAQ device
    5. Get the supported port types
    6. Call dio_device.d_config_port() to configure the port for input
    7. Call dio_device.d_in() to read the data for the digital port
    8. Display the data for the port
    9. Call daq_device.disconnect() and daq_device.release() before exiting the process.
"""
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   DigitalDirection, DigitalPortIoType)


def main():
    daq_device = None

    interface_type = InterfaceType.USB
    descriptor_index = 0
    port_types_index = 0

    try:
        # Get descriptors for all of the available DAQ devices.
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)
        if number_of_devices == 0:
            raise Exception('Error: No DAQ devices found')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('  ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        # Create the DAQ device object associated with the specified descriptor index.
        daq_device = DaqDevice(devices[descriptor_index])

        # Get the DioDevice object and verify that it is valid.
        dio_device = daq_device.get_dio_device()
        if dio_device is None:
            raise Exception('Error: The DAQ device does not support digital input')

        # Establish a connection to the DAQ device.
        descriptor = daq_device.get_descriptor()
        print('\nConnecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()

        # Get the port types for the device(AUXPORT, FIRSTPORTA, ...)
        dio_info = dio_device.get_info()
        port_types = dio_info.get_port_types()

        if port_types_index >= len(port_types):
            port_types_index = len(port_types) - 1

        port_to_read = port_types[port_types_index]

        # Configure the port for input.
        port_info = dio_info.get_port_info(port_to_read)
        if (port_info.port_io_type == DigitalPortIoType.IO or
                port_info.port_io_type == DigitalPortIoType.BITIO):
            dio_device.d_config_port(port_to_read, DigitalDirection.INPUT)

        print('\n', descriptor.dev_string, ' ready', sep='')
        print('    Function demonstrated: dio_device.d_in()')
        print('    Port: ', port_to_read.name)
        try:
            input('\nHit ENTER to continue\n')
        except (NameError, SyntaxError):
            pass

        system('clear')

        try:
            while True:
                try:
                    reset_cursor()
                    print('Please enter CTRL + C to terminate the process\n')
                    print('Active DAQ device: ', descriptor.dev_string, ' (',
                          descriptor.unique_id, ')\n', sep='')

                    # Read the first port.
                    data = dio_device.d_in(port_to_read)

                    clear_eol()
                    print('Port(', port_to_read.name, ') Data: ', data)

                    sleep(0.1)
                except (ValueError, NameError, SyntaxError):
                    break
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


def reset_cursor():
    stdout.write('\033[1;1H')


def clear_eol():
    stdout.write('\x1b[2K')


if __name__ == '__main__':
    main()
