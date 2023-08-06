# coding: utf-8

"""Stb-tester APIs for audio capture, analysis, and verification.

Copyright © 2018-2019 Stb-tester.com Ltd.

This file contains API stubs for local installation, to allow IDE linting &
autocompletion. The real implementation of these APIs is not open-source and it
requires the Stb-tester Node hardware.
"""

__all__ = ["AudioChunk",
           "audio_chunks",
           "get_rms_volume",
           "VolumeChangeDirection",
           "VolumeChangeTimeout",
           "wait_for_volume_change"]

from collections import namedtuple

import numpy
from enum import IntEnum

# pylint: disable=redefined-outer-name,unused-argument


def _raise_premium(api_name):
    raise NotImplementedError(
        "`stbt.audio.%s` is a premium API only available to customers of "
        "Stb-tester.com Ltd. It requires *Stb-tester Node* hardware to run. "
        "See https://stb-tester.com for details on products and pricing. "
        "If you are receiving this error on the *Stb-tester Node* hardware "
        "contact support@stb-tester.com for help" % api_name)


class AudioChunk(numpy.ndarray):
    def __new__(cls, array, dtype=None, order=None, time=None, rate=48000):
        _raise_premium("AudioChunk")

    def __array_finalize__(self, obj):
        if obj is not None:
            _raise_premium("AudioChunk")

    @property
    def time(self):
        _raise_premium("AudioChunk.time")
        return 0.

    @property
    def duration(self):
        _raise_premium("AudioChunk.duration")
        return 0.

    @property
    def rate(self):
        _raise_premium("AudioChunk.rate")
        return 0

    @property
    def end_time(self):
        _raise_premium("AudioChunk.end_time")
        return 0.


def audio_chunks(time_index=None, _dut=None):
    _raise_premium("audio_chunks")
    return iter([AudioChunk((4800,), dtype=numpy.float32)])


def get_rms_volume(duration_secs=3, stream=None):
    _raise_premium("get_rms_volume")
    return _RmsVolumeResult(0.0, 0.0, 0.0)


_RmsVolumeResult = namedtuple('RmsVolumeResult', 'time duration_secs amplitude')


class VolumeChangeDirection(IntEnum):
    LOUDER = 1
    QUIETER = -1


class VolumeChangeTimeout(AssertionError):
    pass


def wait_for_volume_change(
        direction=VolumeChangeDirection.LOUDER, stream=None,
        window_size_secs=0., threshold_db=0., noise_floor=0.0, timeout_secs=0.):
    _raise_premium("wait_for_volume_change")
    return _VolumeChangeResult(VolumeChangeDirection.LOUDER,
                               _RmsVolumeResult(0.0, 0.0, 0.0),
                               _RmsVolumeResult(0.0, 0.0, 0.0),
                               0.0, 0.0, 0.0, 0.)


_VolumeChangeResult = namedtuple(
    '_VolumeChangeResult',
    "direction rms_before rms_after difference_db difference_amplitude time "
    "window_size_secs")
