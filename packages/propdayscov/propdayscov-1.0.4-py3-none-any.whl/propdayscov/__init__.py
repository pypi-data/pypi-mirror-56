import datetime as dt
import sys
import multiprocessing
from functools import partial
import numpy as np
import pandas as pd

from propdayscov import _covdays
from propdayscov import calc_pdc