
'''

This script will handle setting and getting the ABSOLUTE MINIMUM parameters required to control the CNT alignment system.
Different lab power supplies may be used, but which one is used will be abstracted to the main script.

'''

# standard python libraries #
import logging
logging.basicConfig(level=logging.WARNING)		# enable debug messages
import time
import sys

# pip installed libraries #
# import serial           # the function generator works with serial port communication (over USB)

# custom submodule libraries #

from soft_lib_scpi_device.scpi_serial_device import scpi_serial_device

# custom project libraries #
import config as config

# from scpi_serial_device import scpi_serial_device                # parent class to inherit from in the case of the supply and function generators

class ea_ps2042(scpi_serial_device):

    device_id = "EA Elektro-Automatik GmbH & Co. KG, PS 2042-20 B"

    def __init__(self):
        super().__init__()

# class methods #########################


    def set_volt(self, voltage = 2):
        command = "voltage "
        command = command + str(voltage)
        self.send_command(command)
    def set_current(self, current = 1):
        command = "current "
        command = command + str(current)
        self.send_command(command)
    def set_output(self, state = "on"):
        command = "output: "
        if state == "on":
            command = command + "on"
        elif state == "off":
            command = command + "off"
        self.send_command(command)

        # else:
        #     print("invalid state")

    def set_default_values(self):
        self.reset()
        self.set_volt(20)
        self.set_current(2)
        self.set_output("off")
        # self.set_output("on")
        # self.reset()
        # self.reset()
        # self.set_output("on")

    def get_set_volt(self):
        command = "voltage?"
        self.send_command(command)
        time.sleep(self.t)
        response = self.receive_response()
        logging.debug(response)
        response = response.split(" ")  # data after the first space is the units, so we remove
        response = response[0]          # we get only the number on the response
        response = float(response)      # convert to floating number
        return(response)

    def get_set_curr(self):
        command = "current?"
        self.send_command(command)
        time.sleep(self.t)
        response = self.receive_response()
        logging.debug(response)
        response = response.split(" ")  # data after the first space is the units, so we remove
        response = response[0]          # we get only the number on the response
        response = float(response)      # convert to floating number
        return(response)

    def get_volt(self):
        command = "measure:voltage?"
        self.send_command(command)
        time.sleep(self.t)
        response = self.receive_response()
        logging.debug(response)
        response = response.split(" ")  # data after the first space is the units, so we remove
        response = response[0]          # we get only the number on the response
        response = float(response)      # convert to floating number
        return(response)

    def get_current(self):
        command = "measure:current?"
        self.send_command(command)
        time.sleep(self.t)
        response = self.receive_response()
        logging.debug(response)
        response = response.split(" ")  # data after the first space is the units, so we remove
        response = response[0]          # we get only the number on the response
        response = float(response)      # convert to floating number
        return(response)

def test_sweep():
    for i in range(1,20):
        t = 1
        supply.set_output("on")
        time.sleep(t)
        supply.set_output("off")
        supply.set_volt(i)
        print("voltage set to " + str(i))
        supply.set_current(i/10)
        print("current set to " + str(i/10))
        time.sleep(t)


# MAIN FUNCTION ########################################################

if __name__ == "__main__":

    supply = ea_ps2042()
    supply.serial_connect(config.serial_port)
    print("Device id confirmation:")
    print(supply.confirm_device_id())
    time.sleep(1)
    print("resetting power supply")
    supply.reset()
    time.sleep(1)

    print("setting 'default' values: (required by minipuls back then)")
    supply.set_default_values()
    time.sleep(1)

    print("switching on: ")
    supply.set_output("on")
    time.sleep(1)

    print("current voltage:")
    print(supply.get_volt())
    print("current intensity:")
    print(supply.get_current())
    time.sleep(1)

    print("Varying voltage and current max vals.")
    test_sweep()

    print("switching off:")
    supply.set_output("off")
