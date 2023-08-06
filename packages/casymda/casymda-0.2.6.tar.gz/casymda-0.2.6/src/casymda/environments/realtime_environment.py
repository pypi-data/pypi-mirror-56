"""Realtime environment without checking of deviations, but with possibility to control the factor dynamically, e.g. from a different process"""
from simpy import RealtimeEnvironment


class RealtimeEnvironment(RealtimeEnvironment):
    """realtime environment, to be redefined"""
