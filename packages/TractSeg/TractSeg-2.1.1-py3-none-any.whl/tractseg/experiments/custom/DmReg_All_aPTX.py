#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.dm_reg import Config as DmRegConfig

class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET = "HCP_all"
    DATASET_FOLDER = "HCP_preproc_all"
    FEATURES_FILENAME = "32g90g270g_CSD_BX"
    CLASSES = "AutoPTX_42"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])

    # Final DM wil be thresholded at this value
    THRESHOLD = 0.0001  # use lower value so user has more choice

    NUM_EPOCHS = 200    # 130 probably also fine
    #new: DROPOUT=True