#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.experiments.tract_seg import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]


    # 150ep would be enough -> but use 200ep because in some cases LR-reduction might come later because of noise
    # Formerly called: TractSeg_HR_CSDBX_platLR_NEW

