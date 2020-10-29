# -*- coding: utf-8 -*-
#
#  Copyright 2020 pietroro
#  ------------
#  Based on the 2017 original work by uberdaff
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import sys
import time

import serial


class ka3305pInstrument:
    # Status variables
    isConnected = False
    psu_com = None
    status = {}

    # Helper variables for command sanity check
    channels = [1,2]
    modes = [0,1,2]
    panels = [1,2,3,4,5]
    
    def __init__(self, psu_com):
        """Constructor

        Args:
            psu_com (string): COM port on which serial is connected
        """
        try:
            psu_com = serial.Serial(
                port=psu_com,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            psu_com.isOpen()
            self.psu_com = psu_com
            self.isConnected = True
            self.status=self.getStatus()
        except:
            print("COM port failure:")
            print(sys.exc_info())
            self.psu_com = None
            self.isConnected = False
    
    def close(self):
        """Closes connection to the PSU
        """
        self.psu_com.close()
    
    def serWriteAndRecieve(self, data, delay=0.05):
        """Helper function to write to serial adapter and read from buffer

        Args:
            data (string): Data to write to serial adapter
            delay (float, optional): Delay between request and reply. Defaults to 0.05.

        Returns:
            latin-1 encoded chars: Reply from PSU
        """
        self.psu_com.write(data.encode())
        out = ''
        time.sleep(delay)
        while self.psu_com.inWaiting() > 0:
            out += self.psu_com.read(1).decode("latin-1")
        if out != '':
            return out	# Store measurements
        return None
    
    def getIdn(self):
        """Gets instrument identification

        Returns:
            Example output: "KORAD KD3005P V2.0 (Manufacturer, model name,)"
        """
        return self.serWriteAndRecieve("*IDN?", 0.3)
    
    def setVolt(self, channel, voltage, delay=0.1):
        """Sets output voltage on channel

        Args:
            channel (int): Channel on which to set voltage (either 1 or 2)
            voltage (float): Voltage to be set [V]
            delay (float, optional): Delay allows PSU to set voltage. Defaults to 0.1.
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        self.serWriteAndRecieve("VSET{}:{:1.2f}".format(channel,voltage))
        time.sleep(delay) 
    
    def getVolt(self, channel):
        """Gets "set" voltage on channel

        Args:
            channel (int): Channel from which to read voltage

        Returns:
            float: Requested voltage on channel [V]
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        return self.serWriteAndRecieve("VSET{}?".format(channel))
    
    def readVolt(self, channel):
        """Requests voltage measurement on channel

        Args:
            channel (int): Channel from which to measure voltage

        Returns:
            float: Measured voltage value on channel [V]
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        return self.serWriteAndRecieve("VOUT{}?".format(channel))
    
    def setAmp(self, channel, amp, delay=0.1):
        """Sets output current on channel

        Args:
            channel (int): Channel on which to set current (either 1 or 2)
            amp (float): Current to be set [A]
            delay (float, optional): Delay allows PSU to set current. Defaults to 0.1.
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        self.serWriteAndRecieve("ISET{}:{:1.3f}".format(channel,amp))
        time.sleep(delay) 
    
    def getAmp(self, channel):
        """Gets "set" current on channel

        Args:
            channel (int): Channel from which to read current

        Returns:
            float: Requested current on channel [A]
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        return self.serWriteAndRecieve("ISET{}?".format(channel))
    
    def readAmp(self, channel):
        """Requests current measurement on channel

        Args:
            channel (int): Channel from which to measure current

        Returns:
            float: Measured current value on channel [A]
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        return self.serWriteAndRecieve("IOUT{}?".format(channel))
    
    def setOut(self, state):
        """Turns output ON or OFF

        Args:
            state (bool): True to turn on, False to turn off
        """
        if(state == True):
            self.serWriteAndRecieve("OUT1")
        elif(state == False):
            self.serWriteAndRecieve("OUT0")
    
    def toggleOcp(self, state):
        """Turns the Over Current Protection ON or OFF

        Args:
            state (bool): True to turn on, False to turn off
        """
        if(state == True):
            self.serWriteAndRecieve("OCP1")
        elif(state == False):
            self.serWriteAndRecieve("OCP0")

    def setOcp(self, channel, amp, delay=0.1):
        """Sets Over Current Protection value on channel

        Args:
            channel (int): Channel on which to set OCP value (either 1 or 2)
            amp (float): OCP current [A]
            delay (float, optional): Delay allows PSU to set OCP value. Defaults to 0.1.
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        self.serWriteAndRecieve("OCPSTE{}:{:1.3f}".format(channel,amp))
        time.sleep(delay)
    
    def toggleOvp(self, state):
        """Turns the Over Voltage Protection ON or OFF

        Args:
            state (bool): True to turn on, False to turn off
        """
        if(state == True):
            self.serWriteAndRecieve("OVP1")
        elif(state == False):
            self.serWriteAndRecieve("OVP0")

    def setOvp(self, channel, voltage, delay=0.1):
        """Sets Over Voltage Protection value on channel

        Args:
            channel (int): Channel on which to set OVP value (either 1 or 2)
            voltage (float): OCP voltage [V]
            delay (float, optional): Delay allows PSU to set OVP value. Defaults to 0.1.
        """
        assert channel in self.channels, "Channel {} does not exist".format(channel)
        self.serWriteAndRecieve("OVPSTE{}:{:1.3f}".format(channel,voltage))
        time.sleep(delay)
    
    def getStatus(self):
        """Returns the PSU's status

        Returns:
            dict: Dictionary containing the current mode (CC - current, CV - voltage) and output status
        """
        stat = ord(self.serWriteAndRecieve("STATUS?")[0])
        if (stat&(1 << 0))==0:
            self.status["Mode"]="CC"
        else:
            self.status["Mode"]="CV"
        if (stat&(1 << 6))==0:
            self.status["Output"]="Off"
        else:
            self.status["Output"]="On"
        return self.status

    def recallPanel(self, panel):
        """Recalls panel setting to slot panel

        Args:
            panel (int): Panel setting to recall, an integer between 1 and 5
        """
        assert panel in self.panels, "Panel {} does not exist".format(panel)
        self.serWriteAndRecieve("RCL{}".format(panel))

    def savePanel(self, panel):
        """Saves panel setting to slot panel

        Args:
            panel (int): Panel setting to overwrite, an integer between 1 and 5
        """
        assert panel in self.panels, "Panel {} does not exist".format(panel)
        self.serWriteAndRecieve("SAV{}".format(panel))

    def setMode(self,mode):
        """Sets the output of the power supply working on indepent or tracking mode

        Args:
            mode (int): Possibilities are 0=INDEP, 1=SER, 2=PARA
        """
        assert mode in self.modes, "Mode {} does not exist".format(mode)
        self.serWriteAndRecieve("TRACK{}".format(mode))

if __name__ == "__main__":
    # This example is for Ubuntu, in Windows the port will most likely be COM*
    psu = ka3305pInstrument('/dev/ttyUSB0')
    # Connect to PSU
    if psu.isConnected == True:
        # Get ID
        print(psu.getIdn())
        # Request voltage on channel 1
        psu.setVolt(1,13.37)
        # Request voltage measurement on channel 1
        print(psu.readVolt(1))
        # Get PSU status
        print(psu.status)
    psu.close()
