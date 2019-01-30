# -*- coding: utf-8 -*-
import os


LIB_DIR = os.path.dirname(os.path.abspath(__file__))
CHANNELS_DIR = os.path.join(LIB_DIR, "channels")

TMP_DIR=""

channels = dict()
ordered_channels = []
hidden_channels = []
hidden_channelsName = []