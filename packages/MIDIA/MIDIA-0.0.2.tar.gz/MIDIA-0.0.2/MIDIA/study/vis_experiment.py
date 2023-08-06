%load_ext autoreload
%autoreload 2
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 4)
pd.set_option('display.max_columns', 500)
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
from plotnine import *

from MIDIA.sql import table2df, list_tables
from MIDIA.tims_wrapper import AdvancedTims, TimsDDA, TimsDIA
from MIDIA.read import all_datasets, tdf_datasets

from timsdata import TimsData

midia_p = Path('/home/matteo/Projects/bruker/BrukerMIDIA/MIDIA_CE10_precursor/20190912_HeLa_Bruker_TEN_MIDIA_200ng_CE10_100ms_Slot1-9_1_488.d')

D = TimsDIA(midia_p)

