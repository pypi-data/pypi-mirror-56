#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.base_legacy.tract_seg_legacy import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET_FOLDER = "HCP_preproc_bedpostX"
    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "125mm_bedpostx_tensor"

    P_SAMP = 1.
    BATCH_SIZE = 47

