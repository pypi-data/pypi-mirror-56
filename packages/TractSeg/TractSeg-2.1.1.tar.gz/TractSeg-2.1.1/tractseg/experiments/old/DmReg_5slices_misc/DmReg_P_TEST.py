#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.base_legacy.dm_reg_legacy import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET_FOLDER = "HCP_preproc"
    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "270g_125mm_bedpostx_peaks_scaled"
    P_SAMP = 0.4

    CLASSES = "AutoPTX"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])

    THRESHOLD = 0.001
    LR_SCHEDULE = True


    # BATCH_SIZE = 47
    BATCH_SIZE = 92
    DATA_AUGMENTATION = False
