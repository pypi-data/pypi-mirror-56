#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.base_legacy.dm_reg_legacy import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "125mm_bedpostx_peaks_scaled"
    P_SAMP = 0.4

    CLASSES = "AutoPTX"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])

    THRESHOLD = 0.001
    NUM_EPOCHS = 1000

    BATCH_NORM = True
