# -*- coding: utf-8 -*-
"""
Implements axes3DSpec for lulzbot taz 6 with modified firmware.

| First created on Sat Oct 19 20:39:58 2019
| Revised: 23/10/2019 14:06:59
| Author: Bijal Patel

"""
import serial
import io
import time
from polychemprint3.utility.serialDeviceSpec import serialDeviceSpec
from polychemprint3.axes.axes3DSpec import Axes3DSpec
import logging


class lulzbotTaz6_BP(serialDeviceSpec, Axes3DSpec):
    """Implemented interface for Lulzbot Taz 6 with BP modified firmware."""

    def __init__(self,
                 name='LulzbotTaz6',
                 posMode='relative',
                 devAddress="/dev/ttyACM0",
                 baudRate="115200",
                 commsTimeOut=0.5,
                 __verbose__=0,
                 firmwareVers='BP'):
        """*Initializes object with default params DOESNT ACTIVATE*.

        Parameters
        ----------
        name: String
            name of printer
        devAddress: String
            location of serial device for communication
        baudRate: String
            baudrate for serial communication
        commsTimeout: int
            how long to wait for serial device
        firmwareVers: String
            version of marlin firmware to validate against in handshake
            unique to this implementation to make sure
            people use modified firmware
        __verbose__: bool
            whether details should be printed to cmd line
        posMode: String
            Current active positioning mode, relative or absolute
        """
        self.firmwareVers = firmwareVers
        kwargs = {'name': name,
                  'posMode': posMode,
                  'devAddress': devAddress,
                  'baudRate': baudRate,
                  'commsTimeOut': commsTimeOut,
                  '__verbose__': __verbose__}
        super().__init__(**kwargs)

    #########################################################################
    ### Axes3DSpecMethods
    #########################################################################
    def activate(self):
        """*Makes required connections and returns status bool*.

        Returns
        -------
        bool
            True if ready to use
            False if not ready
        """
        passed = False
        # Start Serial Device
        [status, message] = self.startSerial()
        print("\t\t\t" + message)
        if status == 1:
            # Try initial handshake
            [status, message] = self.handShakeSerial()
            print("\t\t\t" + message)
            if status == 1:
                passed = True

        return passed

    def deactivate(self):
        """*Closes communication and returns status bool*.

        Returns
        -------
        bool
            True if closed succesfully
            False if failed
        """
        passed = False
        # Stop Serial Device
        [status, message] = self.stopSerial()
        print("\t\t\t" + message)
        if status == 1:
            passed = True

        return passed

    def setPosMode(self, newPosMode):
        """*Sets positioning mode to relative or absolute*.

        Parameters
        ----------
        newPosMode: String
            Positioning mode to use for future move cmds
        """
        try:
            if newPosMode == 'relative':
                self.writeReady("G91\n")
                self.posMode = newPosMode
            elif newPosMode == 'absolute':
                self.writeReady("G90\n")
                self.posMode = newPosMode
            else:
                print("Error setting position mode to axes")

        except Exception as inst:
            logging.exception(inst)
            print("Error setting position mode to axes")

    def move(self, gcodeString):
        """*Initializes Axes3D object*.

        Parameters
        ----------
        gCodeString: String
            Motion command in terms of Gcode G0/G1/G2/G3 supported

        | *Returns*
        |   none
        """
        self.writeReady(gcodeString)

    def sendCmd(self, command):
        """*Writes command to axes device when ready*.

        Parameters
        ----------
        command: String
            to write to axes
        """
        self.writeReady(command)

    def poll(self, command):
        """*Sends message to axes and parses response*.

        Parameters
        ----------
        command: String
            to write to axes

        Return
        ------
        String
            Response from axes
        """
        return self.writeReady(command)

    def getAbsPosXY(self):
        """*Gets the current position (absolute) and return XY positions*.

        Parameters
        ----------
        command: String
            Gcode to write to axes

        Returns
        -------
        String
            [X, Y] X and Y positions as strings
        """
        self.writeReady('M114\n')
        m114Call = self.waitReady()
        m114Split = m114Call.split(' ')
        x = m114Split[0][2:]
        y = m114Split[1][2:]
        return[x, y]

    #########################################################################
    ### SerialDevice Methods
    #########################################################################
    def startSerial(self):
        """*Creates pySerial device*.

        Returns
        -------
        [1, "Terminated successfully"]
            started succesfully
        [-1, 'Failed Creating pySerial...']
            could not start
        """
        if self.checkIfSerialConnectParamsSet():
            # Try to connect, catch errors and return to user
            try:
                self.ser = serial.Serial(port=self.devAddress,
                                         baudrate=self.baudRate,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         timeout=1,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False,
                                         writeTimeout=2)

                # Use ser for writing
                # Use sReader for buffered read
                self.sReader = io.TextIOWrapper(io.BufferedReader(self.ser))

                # Clear initial garbage text in output buffer
                self.ser.reset_output_buffer()

                time.sleep(0.25)
                lineIn = self.sReader.readlines()
                linesIn = [lineIn]

                # keep reading until empty
                while lineIn != []:
                    time.sleep(0.25)
                    lineIn = self.sReader.readlines()
                    linesIn.extend(lineIn)

            except Exception as inst:
                return [-1, 'Failed Creating pySerial... ' + inst.__str__()]

        else:  # Not all params were set
            return [0, 'Not all connection parameters set']

    def stopSerial(self):
        """*Closes serial devices*.

        Returns
        -------
        [1, "Terminated successfully"]
            started succesfully
        [-1, "Error: Serial Device could not be stopped + error text"]
        """
        try:
            self.ser.close()
            self.sReader.close()
            return [1, "Terminated successfully"]
        except Exception:
            return [-1, "Error: Serial Device could not be stopped"]

    def handShakeSerial(self):
        """*Perform communications handshake with serial device*.

        Returns
        -------
        [1, "Handshake Successful"]
            success occured
        [0, 'Handshake Failed, Rcvd + message received']
            failure occured
        [-1, "Error: Handshake with Tool Failed + error text"]
            Error received
        """
        try:
            self.ser.write(b"M115\n")
            readInput = self.sReader.readlines()
            print(readInput)
            wrongVers = (-1 == readInput[0].find(self.firmwareVers))
            if (wrongVers):
                return [-1, 'Wrong Firmware Version']
            else:
                return [1, 'Handshake Success']
        except Exception as inst:
            return [-1, 'Error on Handshake: ' + inst.__str__()]

    def __writeSerial__(self, command):
        """*Writes text to serial device*.

        Parameters
        ----------
        text: String
            message to send

        Returns
        -------
        [1, 'Text Sent + text']
            succesfull 2-way communication
        [-1, 'Write Failed + Error']
            Exception caught
        """
        try:
            self.ser.write(command)
            if (self.verbose):
                print('\tCommand Sent: ' + command)
            return [1, 'Command Sent' + command]
        except Exception as inst:
            return [-1, 'Error on Write: ' + inst.__str__()]

    def readTime(self):
        """*Reads in from serial device until timeout*.

        Returns
        -------
        String
            All text read in, empty string if nothing
        """
        inp = ''  # input string
        ins = ''  # read in
        tEnd = time() + self.commsTimeOut

        # Reads input until timeout
        while (time() < tEnd):
            ins = self.ser.read()
            if (ins != ""):
                inp += ins

        inp = inp.strip  # removes any newlines
        if self.verbose:
            print('\tReceived    : ' + inp + '\n')
        return (inp)

    #########################################################################
    ### Unique Methods
    #########################################################################
    def waitReady(self):
        """*Looks for "ok" in input, waits indefinitely*.

        Returns
        -------
        String
            All text read in, empty string if nothing
        """
        notReady = True
        i = 0  # loop increments
        while (notReady):
            inp = self.readTime()  # read buffer
            if (i % 10 == 0 and self.verbose):
                print('\tWaiting for axes... ... ...\n')
            if ('ok' in inp):
                notReady = False
        return inp

    def writeReady(self, command):
        """*Sends command only after receiving ok message*.

        | *Parameters*
        |   command, string to write to axes

        | *Returns*
        |   inp, String read in
        """
        self.write(command)
        return self.waitReady()
