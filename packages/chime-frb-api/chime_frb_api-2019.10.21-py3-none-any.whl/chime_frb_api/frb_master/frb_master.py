#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chime_frb_api.core import API
from chime_frb_api.frb_master.swarm import Swarm
from chime_frb_api.frb_master.events import Events
from chime_frb_api.frb_master.parameters import Parameters
from chime_frb_api.frb_master.calibration import Calibration
from chime_frb_api.frb_master.metrics import Metrics
from chime_frb_api.frb_master.mimic import Mimic


class FRBMaster(API):
    """
    CHIME/FRB Master and Control API
    """

    def __init__(self, base_url: str = "http://frb-vsop.chime:8001"):
        API.__init__(self, base_url=base_url)
        self.swarm = Swarm(base_url)
        self.events = Events(base_url)
        self.parameters = Parameters(base_url)
        self.calibration = Calibration(base_url)
        self.metrics = Metrics(base_url)
        self.mimic = Mimic(base_url)
