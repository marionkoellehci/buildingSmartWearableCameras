import smbus
import time
from collections.abc import Iterable

_ch_map = [[0x06 + i * 4, 0x08 + i * 4] for i in range(0, 16)]
_ch_active = []

_bus = smbus.SMBus(1)
_addr = 0x40
_bus.write_byte_data(_addr, 0, 0x20)     # enable the chip
_bus.write_byte_data(_addr, 0xfe, 0x1e) # configure the chip for multi-byte write


def _validChannel(channel):
    return channel >= 0 and channel < len(_ch_map)

def _activeChannel(channels):
    if isinstance(channels, Iterable):
        for ch in channels:
            if not ch in _ch_active:
                return False
        return True
    else:
        return channels in _ch_active

def initChannel(channels):
    if isinstance(channels, Iterable):
        for ch in channels:
            if not _validChannel(ch):
                print("Invalid channel!")
                exit(23)
            _bus.write_word_data(_addr, _ch_map[ch][0], 0)
            _ch_active.append(ch)
    else:
        if not _validChannel(channels):
            print("Invalid channel!")
            exit(23)
        _bus.write_word_data(_addr, _ch_map[channels][0], 0)
        _ch_active.append(channels)
    time.sleep(1)
    close(channels)
    open(channels)

def _move(channels, value, delay):
    if not _activeChannel(channels):
        print("Did not initialize channels, abbort!")
        exit(23)
    if isinstance(channels, Iterable):
        for ch in channels:
            _bus.write_word_data(_addr, _ch_map[ch][1], value)
    else:
        _bus.write_word_data(_addr, _ch_map[channels][1], value)
    time.sleep(delay)

# open seems to work now
def open(channels = _ch_active):
    """ Open the eye """
    _move(channels, 1500, 0.3)
    _move(channels, 1600, 0.3)
    _move(channels, 1644, 0.03)
    _move(channels, 0, 0.0)

#
def close(channels = _ch_active):
    """ close the eye """
    _move(channels, 1250, 0.6)
    _move(channels, 1200, 0.2)
    _move(channels, 1100, 0.03)
    _move(channels, 0, 0.0)

def test_servohat_200Hz_tuned(channels):
    #_move(channels, 1250, 2)
    #_move(channels, 900, 2)
    open()
    print("open")
    time.sleep(3)
    close()
    print("close")
    time.sleep(3)
    open()
    print("open")
