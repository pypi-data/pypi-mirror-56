"""

Name: IOTBit Library compatible with all versions up to IoTBit V1.7
i.e industrial variant
Purpose: Library to interface with the IOTBit HAT on the Raspberry Pi,
tested on the latest version of Raspbian using a Raspberry Pi 3b.
classes Modem
requirements pyserial module, RPI.GPIO

"""

import serial
import time
import serial.tools.list_ports
import RPi.GPIO as GPIO
import logging


class IotModem:
    """
    Set up the system only works if no other ttyUSB ports are on board
    """

    def __init__(self, apn=None, device='4G', uartenable=False, usbenable=True, logtofile=False):
        # Set logging type either to file of on screen
        if logtofile == True:
            logging.basicConfig(filename='IOT-Bit-Library-logfile.txt', level=logging.DEBUG,
                                format=' %(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

        self.apn = apn
        self.end = '\r'
        self.response = ''
        self.device = device
        self.uartenable = uartenable
        self.usbenable = usbenable

        # Pins connected to 40 Pin header BCM style pin numbering
        self.modempowerpin = 13
        self.chargerenablepin = 6
        self.levelshifterpin = 24

        # Logging Strings
        self.commandstring = ' Command string: {} \n Response given: \n {}'
        self.pinstatestring = 'Set pin: {} to GPIO state: {}'
        self.portstring = 'COM port for {} found at {}'

        if self.device == '4GIND':
            self.gpioconfig()

        if self.device == '4G':
            self.configureport()

    ##Function to get the current time in milliseconds. Required for timeout implementation.
    # @param self The object pointer.
    def getmills(self):
        mills = int(round(time.time() * 1000))
        return mills

    ##Function to configure pins 6,13,24 used by the IoTBit.
    # @param self The object pointer.
    def gpioconfig(self):
        # Intialise the GPIO pins as output pins
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.modempowerpin, GPIO.OUT)
        GPIO.setup(self.chargerenablepin, GPIO.OUT)
        GPIO.setup(self.levelshifterpin, GPIO.OUT)
        logging.debug('GPIO Pins are set up')

    ##Function to configure the usb and/or the uart ports used by the IOTbit.
    # @param self The object pointer.
    def configureport(self):
        # Get a list of currently available usb comports
        USB_ports = list(serial.tools.list_ports.comports())
        # Configure the usb ports
        if self.device == '4G':
            if self.usbenable:
                # If the usb is connected assign the ports the correct names.
                gps = USB_ports[3].device
                logging.debug(self.portstring.format('GPS', gps))
                at = USB_ports[2].device
                logging.debug(self.portstring.format('AT', at))
                ppp = USB_ports[1].device
                logging.debug(self.portstring.format('PPP', ppp))
                audio = USB_ports[0].device
                logging.debug(self.portstring.format('Audio', audio))
                # Configure the found ports so they can be used by the pyserial module
                self.GPSPort = serial.Serial(gps, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                self.ATPort = serial.Serial(at, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                            rtscts=True,
                                            dsrdtr=True)
                self.PPPPort = serial.Serial(ppp, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                self.AudioPort = serial.Serial(audio, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                               rtscts=True, dsrdtr=True)
                logging.debug('Serial Ports are set up')

        elif self.device == '3G':
            if self.usbenable:
                # If the usb is connected assign the ports the correct names.
                gps = USB_ports[2].device
                logging.debug(self.portstring.format('GPS', gps))
                at = USB_ports[1].device
                logging.debug(self.portstring.format('AT', at))
                ppp = USB_ports[0].device
                logging.debug(self.portstring.format('PPP', ppp))
                # Configure the found ports so they can be used by the pyserial module
                self.GPSPort = serial.Serial(gps, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                self.ATPort = serial.Serial(at, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                            rtscts=True,
                                            dsrdtr=True)
                self.PPPPort = serial.Serial(ppp, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                logging.debug('Serial Ports are set up')
        elif self.device == 'GSM':
            if self.uartenable:
                uart = '/dev/serial0'  # Serial Port for Raspbian Stretch and higher
                # Configure the port so it can be used by the pyserial module
                self.PassthroughPort = serial.Serial(uart, baudrate=115200, bytesize=8, parity='N', stopbits=1,
                                                     timeout=1, rtscts=True, dsrdtr=True)
                logging.debug('Serial Ports are set up')
            else:
                logging.warning('Use raspi-config to enable UART in interfacing options.')
                
        elif self.device == '4GIND':
            if self.usbenable:
                # If the usb is connected assign the ports the correct names.
                gps = USB_ports[3].device
                logging.debug(self.portstring.format('GPS', gps))
                at = USB_ports[2].device
                logging.debug(self.portstring.format('AT', at))
                ppp = USB_ports[1].device
                logging.debug(self.portstring.format('PPP', ppp))
                audio = USB_ports[0].device
                logging.debug(self.portstring.format('Audio', audio))
                # Configure the found ports so they can be used by the pyserial module
                self.GPSPort = serial.Serial(gps, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                self.ATPort = serial.Serial(at, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                            rtscts=True,
                                            dsrdtr=True)
                self.PPPPort = serial.Serial(ppp, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                             rtscts=True, dsrdtr=True)
                self.AudioPort = serial.Serial(audio, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1,
                                               rtscts=True, dsrdtr=True)
            if self.uartenable:
                uart = '/dev/serial0'  # Serial Port for Raspbian Stretch and higher
                self.UARTPort = serial.Serial(uart, baudrate=115200, bytesize=8, parity='N', stopbits=1,
                                              timeout=1, rtscts=True, dsrdtr=True)
            logging.debug('Serial Ports are set up')

    ##Function encode the AT command string given to be sent to the modem via the usb AT port
    # @param self The object pointer.
    # @param ATcmd The command to be sent to the modem.
    # @param timeout How long in millisecond(ms) to wait for a response.
    def sendatcmd(self, ATcmd, timeout):
        # Modify the ATcmd so that it has the end of line '\r' character
        cmd = ATcmd + self.end
        # Send the modified command to the device , '.encode required for Python 3 and higher
        self.ATPort.write(cmd.encode())
        time.sleep(0.01)
        # Check the serial buffer to see if there is a response waiting
        bytestoread = self.ATPort.inWaiting()
        logging.debug('First try - Bytes to be read: %d' % bytestoread)
        # While timeout not reached keep checking buffer
        if bytestoread == 0:
            currenttime = self.getmills()

            while (bytestoread == 0) and ((self.getmills() - currenttime) < timeout):
                bytestoread = self.ATPort.inWaiting()
            logging.debug('Bytes to be read: %d' % bytestoread)
            # Store the response, '.decode' required for Python 3 and higher
            self.response = self.ATPort.read(bytestoread).decode("utf-8")
            logging.debug(self.commandstring.format(cmd, self.response))
        else:
            self.response = self.ATPort.read(bytestoread).decode("utf-8")
            logging.debug(self.commandstring.format(cmd, self.response))

    ##Function to read the a port to see if there data is waiting to be read.
    # @param self The object pointer.
    # @param port Configured ports are USB: ATPort, GPSPort, PPPPort, AudioPort UART: UARTPort, PassthroughPort.(V1.6)
    # @param timeout How long in millisecond(ms) to wait for a response.
    def readPort(self, port, timeout):
        # Check the serial buffer to see if there is a response waiting
        bytestoread = port.inWaiting()
        logging.debug('First try - Bytes to be read: %d' % bytestoread)
        # While timeout not reached keep checking buffer
        if bytestoread == 0:
            # Get the current time
            currenttime = self.getmills()
            # If the there is nothing to read and the timeout hasn't been reached.
            while (bytestoread == 0) and ((self.getmills() - currenttime) < timeout):
                # Chech the port for new data.
                bytestoread = port.inWaiting()
            logging.debug('Bytes to be read: %d' % bytestoread)
            # Store the response
            self.response = port.read(bytestoread).decode("utf-8")
        else:
            self.response = port.read(bytestoread).decode("utf-8")
        return self.response

    ##Function
    # @param self The object pointer.
    # @param ATcmd The command to be sent to the modem.
    # @param timeout How long in millisecond(ms) to wait for a response.
    def sendATcmdUART(self, ATcmd, timeout):
        # Modify the ATcmd so that it has the end of line character
        cmd = ATcmd + self.end
        # Send the cmd to the device
        self.UARTPort.write(cmd.encode())
        time.sleep(0.01)

        # Check the serial buffer to see if there is a response waiting
        bytestoread = self.UARTPort.inWaiting()
        logging.debug('First try - Bytes to be read: %d' % bytestoread)
        # While timeout not reached keep checking buffer
        if bytestoread == 0:
            currenttime = self.getmills()

            while (bytestoread == 0) and ((self.getmills() - currenttime) < timeout):
                bytestoread = self.UARTPort.inWaiting()
            logging.debug('Bytes to be read: %d' % bytestoread)
            # Store the response
            self.response = self.UARTPort.read(bytestoread).decode("utf-8")
            logging.debug(self.commandstring.format(cmd, self.response))
        else:
            self.response = self.UARTPort.read(bytestoread).decode("utf-8")
            logging.debug(self.commandstring.format(cmd, self.response))

    ##Function to Send commands via the serial interface
    ##Waits for a response and returns the response if there is one.
    ##Timeout length is variable.
    ##Usable only with firmware verison 1.5 and v1.6
    ##To test your firmare version use the function VersionCheck().
    ##version 1.7 i.e IoTBit Industrial uses sendATcmdUART
    # @param self The object pointer.
    # @param ATcmd The command to be sent to the modem.
    # @param timeout How long in millisecond(ms) to wait for a response.
    def sendATcmdPassthrough(self, ATcmd, Timeout):

        self.PassthroughPort.flushInput()
        self.PassthroughPort.flushOutput()

        # Modify the ATcmd so that it has the end of line character
        cmd = ATcmd + self.end
        time2send = str(Timeout)

        # Wait for modem to be ready
        ready = self.PassthroughPort.readline().decode("utf-8")
        logging.debug(self.commandstring.format('No cmd', ready))
        if 'Modem Ready' in ready:
            pcmd = 'P'
            self.PassthroughPort.write(pcmd.encode())
            sendTimeout = self.PassthroughPort.readline().decode("utf-8")
            logging.debug(self.commandstring.format(pcmd, sendTimeout))
            if 'Send Timeout' in sendTimeout:
                self.PassthroughPort.write(time2send.encode())
                sendCmd = self.PassthroughPort.readline().decode("utf-8")
                logging.debug(self.commandstring.format(time2send, sendCmd))
                if 'Send CMD' in sendCmd:
                    # Send the cmd to the device
                    self.PassthroughPort.write(cmd.encode())

                    # Check the serial buffer to see if there is a response waiting
                    bytestoread = self.PassthroughPort.inWaiting()
                    logging.debug('First try - Bytes to be read: %d' % bytestoread)
                    # While timeout not reached keep checking buffer
                    if (bytestoread == 0):
                        # time.sleep((Timeout+500)/1000)
                        curtime = self.getmills()

                        while (bytestoread == 0) or ((self.getmills() - curtime) < Timeout):
                            bytestoread = self.PassthroughPort.inWaiting()
                            time.sleep(0.01)
                        logging.debug('Bytes to be read: %d' % bytestoread)
                        # Store the response
                        self.response = self.PassthroughPort.read(bytestoread).decode("utf-8")
                        logging.debug(self.commandstring.format(cmd, self.response))
                    else:
                        self.response = self.PassthroughPort.readline().decode("utf-8")
                        logging.debug(self.commandstring.format(cmd, self.response))
                else:
                    print ('Command not sent')
            else:
                print('Timeout not sent')
        else:
            print ('Modem not ready')

    ########################################### BOARD FUNCTIONS ##########################################################################

    ##########################  V 1.5 and 1.6  #######################

    ##Function to reset the whole board including the Raspberry pi
    ##if it is drawing power from the IOTBit. Make sure to save before
    ##using this function
    # @param self The object pointer.
    def ResetAll(self):
        # Wait for modem to be ready
        saved = input('Doing this may reset your Raspberry Pi are you sure? Y/N\n')
        if saved == 'Y':
            ready = self.PassthroughPort.readline()
            if 'Modem Ready' in ready:
                self.PassthroughPort.write('S')
        elif saved == 'N':
            print('Please save you work before running this function.')
        else:
            print('Please type Y or N')

    ##Function to check the firmware version if you get no response this means
    ##the firmware version is older than 1.5. or the IoT industrial version.
    # @param self The object pointer.

    def versioncheck(self):
        # Wait for modem to be ready
        ready = self.PassthroughPort.readline()
        if 'Modem Ready' in ready:
            self.PassthroughPort.write('V')
            self.response = self.PassthroughPort.readline()

    ##########################  V 1.7  ###############################

    ##Function to turn on the modem
    # @param self The object pointer.
    def turnonmodem(self):
        # Set the modem power pin high
        GPIO.output(self.modempowerpin, GPIO.HIGH)
        logging.debug(self.pinstatestring.format(self.modempowerpin, GPIO.HIGH))
        time.sleep(1)
        # Set low after a 1 second.
        GPIO.output(self.modempowerpin, GPIO.LOW)
        logging.debug(self.pinstatestring.format(self.modempowerpin, GPIO.LOW))

    ##Function to turn on the level shifter
    # @param self The object pointer.
    def turnonlevelshifter(self):
        GPIO.output(self.levelshifterpin, GPIO.HIGH)
        logging.debug(self.pinstatestring.format(self.levelshifterpin, GPIO.HIGH))

    ##Function to setup the battery charger
    # @param self The object pointer.
    def setbatterycharger(self):
        GPIO.output(self.chargerenablepin, GPIO.LOW)
        logging.debug(self.pinstatestring.format(self.chargerenablepin, GPIO.HIGH))

    ## Function to configure iotbit board
    # @param self The object pointer.
    def hardwareconfig(self):
        self.setbatterycharger()
        self.turnonlevelshifter()
        self.turnonmodem()

    ########################################### MODULE FUNCTIONS ##########################################################################

    ##Function to reset the modem
    # @param self The object pointer.
    def modemReset(self):
        print('Resetting...')
        cmd = 'AT+CRESET'
        self.sendatcmd(cmd, 100)


    ##Function to check signal quality
    # @param self The object pointer.
    def signalCheck(self):
        """See Signal Quality"""
        cmd = 'AT+CSQ'
        self.sendatcmd(cmd, 1000)
        signal = self.response

        if ',' in self.response[8:10]:
            signal = signal.replace(',', '')
            signal = int(signal[8:9])
        else:
            signal = int(self.response[8:10])

        if signal < 10:
            signal = "Poor Signal"
        elif 10 < signal < 14:
            signal = "OK Signal"
        elif 14 < signal < 20:
            signal = "Good Signal"
        elif 20 <= signal < 99:
            signal = "Exceptional Signal"
        elif signal >= 99:
            signal = "No Connection"
        return signal

    ##Function test the modem is working and a sim card has been inserted
    # @param self The object pointer.
    def setupTest(self):

        # command to stop the echo on the modem
        cmd = 'ATE0'
        self.sendatcmd(cmd, 100)

        if 'OK' in self.response:
            print('Modem command echo Disabled')
        # Command to get general informtion from the modem
        cmd = 'ATI'
        self.sendatcmd(cmd, 100)
        if 'OK' in self.response:
            print('Modem responding')
        # command to check the sim card is inserted
        cmd = 'AT+CPIN?'
        self.sendatcmd(cmd, 100)
        if 'READY' in self.response:
            print('Sim card detected')
        elif 'CME ERROR' in self.response:
            print('Response Error: ' + self.response)
        # Check the signal quality of the modem.
        self.signal = self.signalCheck()
        logging.debug('Signal Response given: %s' % self.signal)
        print(self.signal)

    ########################################### SMS FUNCTIONS ##########################################################################

    ##Function to configure SMS
    # @param self The object pointer.

    def smsconfig(self):
        logging.debug('Configuring Modem for SMS...')
        self.sendatcmd('AT+CMGF=1', 100)
        time.sleep(0.01)
        # SM stands for SIM message storage since there is no external storage  we set all memory options to SM
        cmd = 'AT+CPMS="SM","SM","SM"'
        self.sendatcmd(cmd, 100)
        time.sleep(0.01)
        self.sendatcmd('AT+CNMI=2,1', 100)
        time.sleep(0.01)
        if 'OK' in self.response:
            logging.debug('Setup Complete')

    ##Function to Send an SMS
    # @param self The object pointer.
    # @param number The number as a string the message is being sent to.
    # @param message The message to be sent.

    def sendsms(self, number, message):
        print ('Sending SMS ...')
        # AT command to send an sms
        smssendformat = 'AT+CMGSO="{}","{}"'
        cmd = smssendformat.format(number, message)
        self.sendatcmd(cmd, 16000)
        if 'OK' in self.response:
            print (' Sending successful')
        else:
            print (' Sending Unsuccessful')

    ##Function to read the sms in storage, if index is 0 print all msgs
    # @param self The object pointer.
    # @param index The position of the message you want to read the higher the number the newer the message. Default 0
    # @param allmessages Set this to true for modem to display all messages. Default False
    # TODO: Add max number limit for max message to be stored.

    def readsms(self, index=0, allmessages=False):
        if allmessages == True:
            # command to read all available messages
            self.sendatcmd('AT+CMGL="ALL"', 3000)
        else:
            # command to read a specific message the higher thr number the newer the message
            cmd = 'AT+CMGR={}'
            self.sendatcmd(cmd.format(index), 3000)
        return self.response

    ##Function to delete an sms in storage, index refers to the position of the message
    # @param self The object pointer.
    # @param index The position of the message you want to delete the bigger the number the newer the message.
    def deleteSMS(self, index):
        cmd = 'AT+CMGD={}'
        self.sendatcmd(cmd.format(index), 3000)
        return self.response

    ########################################### GPS FUNCTIONS ##########################################################################

    ##Function to start the GPS make sure the GPS antenna is connected and near a window
    # @param self The object pointer.
    # @param mode 0 for default AT+CGPS=1 1 for AT+CGPSCOLD (Cold start) 2 for AT+CGPSHOT (Hot start)

    def startGPS(self, mode=0):

        print (' Configuring ....')

        # TODO: Add options for more types of data output using .format string modifer
        # Set the NMEA port to output GLNOass and GPRS data
        cmd = 'AT+CGPSNMEA=3'
        self.sendatcmd(cmd, 100)
        if 'OK' in self.response:
            print ('NMEA Port configured')
        else:
            print (self.response)

        time.sleep(0.01)

        # Make sure the GPS is actually off
        cmd = 'AT+CGPS=0'
        self.sendatcmd(cmd, 100)
        if 'OK' in self.response:
            print ('Resetting GPS')
        else:
            print (self.response)

        time.sleep(0.01)

        # Check which mode has been chosen to turn on GPS
        if mode == 0:
            cmd = 'AT+CGPS=1'
            self.sendatcmd(cmd, 100)
            if 'OK' in self.response:
                print (' Starting GPS')
            else:
                print (self.response)

        elif mode == 1:
            cmd = 'AT+CGPSHOT'
            self.sendatcmd(cmd, 100)
            if 'OK' in self.response:
                print (' Hot starting GPS')
            else:
                print (self.response)

        elif mode == 2:
            cmd = 'AT+CGPSCOLD'
            self.sendatcmd(cmd, 100)
            if 'OK' in self.response:
                print (' Cold starting GPS')
            else:
                print (self.response)
        else:
            print ("Mode not set correctly ")

        time.sleep(0.01)

    ##Function to stop the GPS
    # @param self The object pointer.

    def stopGPS(self):
        self.sendatcmd('AT+CGPS=0', 100)
        if 'OK' in self.response:
            print (' Stopping GPS')
        else:
            print (self.response)
        time.sleep(0.01)

    # TODO: Use regex to parse GPS signal and get long lat and time as variables
    ##Function to get the raw GPS information.
    # @param self The object pointer.

    def getrawGPSposition(self):
        self.sendatcmd('AT+CGPSINFO', 1)
        logging.debug('Raw GPS postion: {}'.format(self.response))
        return self.response


