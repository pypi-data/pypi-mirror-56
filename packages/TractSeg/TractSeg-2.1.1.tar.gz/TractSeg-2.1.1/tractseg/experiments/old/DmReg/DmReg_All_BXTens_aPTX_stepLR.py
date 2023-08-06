#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.base_legacy.dm_reg_legacy import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET_FOLDER = "HCP_preproc_all"
    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "125mm_bedpostx_peaks"
    P_SAMP = 0.4

    CLASSES = "AutoPTX_42"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])

    THRESHOLD = 0.001

    DATASET = "HCP_all"

    LEARNING_RATE = 0.002  # 0.001
    LR_SCHEDULE = True
