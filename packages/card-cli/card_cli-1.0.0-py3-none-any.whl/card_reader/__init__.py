#!/usr/bin/env python3
from argparse import ArgumentParser
from threading import Event, Timer
from time import sleep

from smartcard.AbstractCardRequest import AbstractCardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.Exceptions import CardRequestException, ListReadersException
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard.pcsc.PCSCContext import PCSCContext
from smartcard.CardConnectionObserver import CardConnectionObserver
from smartcard.util import toHexString

from smartcard.scard import (
    INFINITE, 
    SCardListReaders, 
    SCardGetStatusChange, 
    SCardGetErrorMessage,
    SCARD_E_NO_READERS_AVAILABLE, 
    SCARD_E_TIMEOUT,
    SCARD_E_UNKNOWN_READER,
    SCARD_STATE_UNAWARE, 
    SCARD_STATE_CHANGED,
    SCARD_STATE_PRESENT,
)

import usb.core
import usb.util

import json

__VERSION__ = 'v1.0.0'

# APDU confriguration settings
APDU = {
	'ISO7816': {
		'getserial': [0xFF, 0xCA, 0x00, 0x00, 0x00], # ACS ACR122U - see API docs p.11 
		'status-success': {
			'sw1': 0x90,
			'sw2': 0x00
		},
		'status-failed': {
			'sw1': 0x63,
			'sw2': 0x00
		},
		'observer-status': [0xFF, 0xCA, 0x00, 0x00, 0x00],
		'observer-get': [0x00, 0x00, 0x00, 0x00, 0x00] # Not correct - See documentation
	}
}

class MsrCli:
    def __init__(self, device_vendor_id, device_product_id, debug = False):
        """Constructor."""
        self.debug = debug
        self.device_vendor_id = device_vendor_id
        self.device_product_id = device_product_id
        self.data_length = 537

    def load_device_endpoint(self):
        """Initialize the device and load the correct endpoint."""
        self.device = usb.core.find(idVendor=self.device_vendor_id, idProduct=self.device_product_id)

        if not self.device:
            print("No MSR device connected!")
            return True

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                raise e
                # sys.exit("Could not detatch kernel driver: %s" % str(e))

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            raise e
            # sys.exit("Could not set configuration: %s" % str(e))

        self.device_endpoint = self.device[0][(0, 0)][0]
        return self.device_endpoint


    def process_data(self, data):
        """Process magnetic card strip data."""
        encoding_formats = ['ISO/ABA', 'AAMVA', 'CADL', 'Blank', 'Other', 'Undetermined', 'None']

        parsed = {}
        parsed['encoding_type'] = encoding_formats[data[6]]
        parsed['tracks'] = [{}, {}, {}]

        data_offset = 9

        # Process all 3 tracks
        for i in range(0, 3):
            track = {}
            parsed['tracks'][i] = track

            track['length'] = data[i + 3]

            if not track['length']:
                continue

            track['raw'] = ''.join(map(chr, data[data_offset:data_offset + track['length'] + 1]))
            track['data'] = track['raw'].strip('\x10\t\n\r\0')

            data_offset += track['length'] + 1

            # Remove raw data
            track.pop('raw', None)

            # Skip empty tracks
            if not len(track['data']):
                continue

            if parsed['encoding_type'] == 'ISO/ABA':
                if i == 0:
                    format_code_offset = track['data'].find('%', 0)
                    primary_account_number_offset = format_code_offset + 1
                    name_offset = track['data'].find('^', format_code_offset + 1)
                    additional_data_offset = track['data'].find('^', name_offset + 1)

                    track['format_code'] = track['data'][format_code_offset + 1]
                    track['primary_account_number'] = track['data'][primary_account_number_offset + 1:name_offset]

                    track['name'] = track['data'][name_offset + 1:additional_data_offset]
                    track['last_name'], track['first_name'] = track['name'].split('/')

                    track['expiration_year'] = track['data'][additional_data_offset + 1:additional_data_offset + 3]
                    track['expiration_month'] = track['data'][additional_data_offset + 3:additional_data_offset + 5]
                elif i == 1:
                    primary_account_number_offset = track['data'].find(';', 0)
                    additional_data_offset = track['data'].find('=', primary_account_number_offset + 1)

                    track['primary_account_number'] = track['data'][primary_account_number_offset + 1:
                                                                    additional_data_offset]

                    track['expiration_year'] = track['data'][additional_data_offset + 1:additional_data_offset + 3]
                    track['expiration_month'] = track['data'][additional_data_offset + 3:additional_data_offset + 5]

        return parsed

class TracerAndSELECTInterpreter(CardConnectionObserver):
	"""This observer will interprer SELECT and GET RESPONSE bytes
	and replace them with a human readable string."""
	def __init__(self, nc=False):
		self.nc = True

	def update(self, cardconnection, ccevent):
		if not self.nc:
			if 'connect' == ccevent.type:
				print('connecting to ' + cardconnection.getReader())

			elif 'disconnect' == ccevent.type:
				print('disconnecting from ' + cardconnection.getReader())

			elif 'command' == ccevent.type:
				str = toHexString(ccevent.args[0])
				print('>', str)

			elif 'response' == ccevent.type:
				if [] == ccevent.args[0]:
					print('<  []', '%-2X %-2X' % tuple(ccevent.args[-2:]))
				else:
					print('<',
						toHexString(ccevent.args[0]),
						'%-2X %-2X' % tuple(ccevent.args[-2:]))


def signalEvent(evt, isInfinite):
    if not isInfinite:
        evt.set()

class PCSCCardRequest(AbstractCardRequest):
    def __init__(self, newcardonly=False, readers=None,
                 cardType=None, cardServiceClass=None, timeout=1):
        """Construct new PCSCCardRequest.
        @param newcardonly: if True, request a new card default is
        False, i.e. accepts cards already inserted
        @param readers: the list of readers to consider for requesting a
        card default is to consider all readers
        @param cardType: the CardType class to wait for; default is
        AnyCardType, i.e.  the request will returns with new or already
        inserted cards
        @param cardServiceClass: the specific card service class to
        create and bind to the card default is to create and bind a
        PassThruCardService
        @param timeout: the time in seconds we are ready to wait for
        connecting to the requested card.  default is to wait one second
        to wait forever, set timeout to None
        """
        AbstractCardRequest.__init__(
            self, newcardonly, readers, cardType, cardServiceClass, timeout)

        # polling interval in s for SCardGetStatusChange
        self.pollinginterval = 0.05 # normal 0.1

        # if timeout is None, translate to scard.INFINITE
        if None == self.timeout:
            self.timeout = INFINITE
        # otherwise, from seconds to milliseconds
        else:
            self.timeout = int(self.timeout)

        self.hcontext = PCSCContext().getContext()

    def getReaderNames(self):
        """Returns the list or PCSC readers on which to wait for cards."""

        # get inserted readers
        hresult, pcscreaders = SCardListReaders(self.hcontext, [])
        if 0 != hresult and SCARD_E_NO_READERS_AVAILABLE != hresult:
            raise ListReadersException(hresult)

        readers = []

        # if no readers asked, use all inserted readers
        if None == self.readersAsked:
            readers = pcscreaders

        # otherwise use only the asked readers that are inserted
        else:
            for reader in self.readersAsked:
                if not isinstance(reader, type(str)):
                    reader = str(reader)
                if reader in pcscreaders:
                    readers = readers + [reader]

        return readers

    def serialObject(self, data):
        data = ';' + toHexString(data).replace(' ', '') + '?'
        return ({
            'encoding_type': 'Other',
            'tracks': [
                {'length': 0},
                {'length': len(data), 'data': data},
                {'length': 0}
            ]
        })

    def cardservice(self, reader):
        cardservice = self.cardServiceClass(reader.createConnection())
        cardservice.connection.connect()
        # attach the console tracer
        observer = TracerAndSELECTInterpreter()
        cardservice.connection.addObserver(observer)
        data, sw1, sw2 = cardservice.connection.transmit(APDU['ISO7816']['getserial'])
        return self.serialObject(data)
    
    def readCard(self, dend, msr):
        """Wait for card insertion and returns a card service."""
        msr_active = True
        if type(dend) == bool:
            msr_active = False
        
        AbstractCardRequest.waitforcard(self)
        cardfound = False

        data = []
        swiped = False

        # for non infinite timeout, a timer will signal
        # the end of the time-out by setting the evt event
        evt = Event()
        if INFINITE == self.timeout:
            timertimeout = 1
        else:
            timertimeout = self.timeout
        timer = Timer(
            timertimeout, signalEvent, [evt, INFINITE == self.timeout])

        # create a dictionary entry for new readers
        readerstates = {}
        readernames = self.getReaderNames()
        for reader in readernames:
            if not reader in readerstates:
                readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

        # remove dictionary entry for readers that disappeared
        for oldreader in list(readerstates.keys()):
            if oldreader not in readernames:
                del readerstates[oldreader]

        # call SCardGetStatusChange only if we have some readers
        if {} != readerstates:
            hresult, newstates = SCardGetStatusChange(
                self.hcontext, 0, list(readerstates.values()))
        else:
            hresult = 0
            newstates = []

        # we can expect normally time-outs or reader
        # disappearing just before the call
        # otherwise, raise execption on error
        if 0 != hresult and \
            SCARD_E_TIMEOUT != hresult and \
            SCARD_E_UNKNOWN_READER != hresult:
                raise CardRequestException(
                    'Failed to SCardGetStatusChange ' + \
                    SCardGetErrorMessage(hresult))

        # in case of timeout or reader disappearing,
        # the content of the states is useless
        # in which case we clear the changed bit
        if SCARD_E_TIMEOUT == hresult or SCARD_E_UNKNOWN_READER == hresult:
            for state in newstates:
                state[1] = state[1] & (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

        # update readerstate
        for state in newstates:
            readername, eventstate, atr = state
            readerstates[readername] = (readername, eventstate)

        # if a new card is not requested, just return the first available
        
        if not self.newcardonly:
            for state in newstates:
                readername, eventstate, atr = state
                if eventstate & SCARD_STATE_PRESENT:
                    reader = PCSCReader(readername)
                    if self.cardType.matches(atr, reader):
                        if self.cardServiceClass.supports('dummy'):
                            cardfound = True
                            return self.cardservice(reader)
        
        while not evt.isSet() and not cardfound:
            sleep(self.pollinginterval) # PCSC refresh rate
            
            # create a dictionary entry for new readers
            readernames = self.getReaderNames()
            for reader in readernames:
                if not reader in readerstates:
                    readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

            # remove dictionary entry for readers that disappeared
            for oldreader in list(readerstates.keys()):
                if oldreader not in readernames:
                    del readerstates[oldreader]

            # wait for card insertion
            if {} != readerstates:
                hresult, newstates = SCardGetStatusChange(
                    self.hcontext, 0, list(readerstates.values()))
            else:
                hresult = SCARD_E_TIMEOUT
                newstates = []

            # msr-read card intermezzo
            if msr_active:
                try:
                    if swiped:
                        return msr.process_data(data)
                    
                    data += msr.device.read(dend.bEndpointAddress, dend.wMaxPacketSize, 50) 
                    if len(data) >= 537:
                        swiped = True
                except usb.core.USBError as e:
                    if e.args == ('Operation timed out',):
                        print('Invalid swipe, discarding %s bytes of data', len(data))
                        data = []
                        continue


            # time-out
            if SCARD_E_TIMEOUT == hresult:
                if evt.isSet():
                    raise CardRequestTimeoutException()

            # reader vanished before or during the call
            elif SCARD_E_UNKNOWN_READER == hresult:
                pass

            # some error happened
            elif 0 != hresult:
                timer.cancel()
                raise CardRequestException(
                    'Failed to get status change ' + \
                    SCardGetErrorMessage(hresult))

            # something changed!
            else:
                # check if we have to return a match, i.e.
                # if no new card in inserted and there is a card found
                # or if a new card is requested, and there is a change+present
                for state in newstates:
                    readername, eventstate, atr = state
                    r, oldstate = readerstates[readername]

                    # the status can change on a card already inserted, e.g.
                    # unpowered, in use, ...
                    # if a new card is requested, clear the state changed bit
                    # if the card was already inserted and is still inserted

                    if self.newcardonly:
                        if oldstate & SCARD_STATE_PRESENT and \
                            eventstate & \
                                (SCARD_STATE_CHANGED | SCARD_STATE_PRESENT):
                            eventstate = eventstate & \
                                (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

                    if (self.newcardonly and \
                            eventstate & SCARD_STATE_PRESENT and \
                            eventstate & SCARD_STATE_CHANGED) or \
                        (not self.newcardonly and \
                         eventstate & SCARD_STATE_PRESENT):
                        reader = PCSCReader(readername)
                        if self.cardType.matches(atr, reader):
                            if self.cardServiceClass.supports('dummy'):
                                cardfound = True
                                # timer.cancel()
                                return self.cardservice(reader)

                    # update state dictionary
                    readerstates[readername] = (readername, eventstate)

            if evt.isSet():
                raise CardRequestTimeoutException()


def auto_int(x):
    """Convert a string to int with auto base detection."""
    return int(x, 0)

def main():   
    parser = ArgumentParser(prog='cardreadercli', description='%(prog)s is a command line utility for reading smartcards and magnetic stripe cards.')
    parser.add_argument('-dvid', '--device-vendor-id', type=auto_int)
    parser.add_argument('-dpid', '--device-product-id', type=auto_int)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __VERSION__)
    args = parser.parse_args()

    reader = ['ACS ACR122U 00 00'] # select reader (if reader = None -> request card from all readers)

    pcsc = PCSCCardRequest(timeout=None, readers=reader)
    msr = MsrCli(**vars(args))
    device_endpoint = msr.load_device_endpoint()
    while True:
        try:
            data = pcsc.readCard(device_endpoint, msr)
            print(json.dumps(data), flush=True)
            sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
	main()
