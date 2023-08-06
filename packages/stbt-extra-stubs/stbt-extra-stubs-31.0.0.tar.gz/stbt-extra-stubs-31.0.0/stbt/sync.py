# coding: utf-8

"""API stubs for Stb-tester's premium features, to allow IDE linting &
autocompletion

The real implementations of these APIs require the Stb-tester Node hardware.

Copyright © 2018-2019 Stb-tester.com Ltd.
"""

__all__ = ["BadSyncPattern", "measure_av_sync"]

from collections import namedtuple

from stbt import UITestError

# pylint: disable=unused-argument


def _raise_premium(api_name):
    raise NotImplementedError(
        "`stbt.sync.%s` is a premium API only available to customers of "
        "Stb-tester.com Ltd. It requires *Stb-tester Node* hardware to run. "
        "See https://stb-tester.com for details on products and pricing. "
        "If you are receiving this error on the *Stb-tester Node* hardware "
        "contact support@stb-tester.com for help" % api_name)


_AVSyncResult = namedtuple(
    "_AVSyncResult",
    "offset type time duration_secs rate drift drift_p_value samples "
    "undetectable acceptable")


def measure_av_sync(duration_secs=60, start_timeout_secs=10,
                    frames=None, audiostream=None):
    import numpy
    _raise_premium("measure_av_sync")

    return _AVSyncResult(
        0.0, "", 0.0, 0.0, 0.0, 0.0, 0.0,
        numpy.array([], dtype=[
            ('video_time', 'f8'),
            ('audio_time', 'f8'),
            ('video_rate', 'f4')]),
        False, False)


class BadSyncPattern(UITestError):
    pass
