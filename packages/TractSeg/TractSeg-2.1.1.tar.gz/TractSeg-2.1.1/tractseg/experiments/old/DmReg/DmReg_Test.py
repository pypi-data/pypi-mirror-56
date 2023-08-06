import os
from tractseg.experiments.base_legacy.dm_reg_legacy import Config as DmRegConfig


class Config(DmRegConfig):

    EXP_NAME = os.path.basename(__file__).split(".")[0]

    P_SAMP = 0.4
