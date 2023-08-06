#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.data import dataset_specific_utils
from tractseg.experiments.dm_reg import Config as DmRegConfig

class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET = "biobank_20k"
    DATASET_FOLDER = "biobank_preproc"
    FEATURES_FILENAME = "105g_2mm_bedpostx_peaks_scaled"
    CLASSES = "AutoPTX_27"
    NR_OF_CLASSES = len(dataset_specific_utils.get_bundle_names(CLASSES)[1:])
    RESOLUTION = "2mm"

    LABELS_FILENAME = "bundle_masks_autoPTX_dm"

    # Final DM wil be thresholded at this value
    THRESHOLD = 0.0001  # use lower value so user has more choice

    NUM_EPOCHS = 250
    EPOCH_MULTIPLIER = 0.05

    DATA_AUGMENTATION = False

    PAD_TO_SQUARE = False