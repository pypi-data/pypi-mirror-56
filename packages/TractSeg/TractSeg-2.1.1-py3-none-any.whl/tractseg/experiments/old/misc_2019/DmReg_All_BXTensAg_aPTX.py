#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.dm_reg import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET_FOLDER = "HCP_preproc_all"
    DATASET = "HCP_all"
    NUM_EPOCHS = 200    # 130 probably also fine
    P_SAMP = 0.4

    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "32g270g_BX"

    CLASSES = "AutoPTX_42"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])
    THRESHOLD = 0.001

    # Formerly called: DmReg_All_BXTensAg_aPTX_platLR20_NEW