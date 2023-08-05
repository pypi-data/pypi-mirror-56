"""
Library for reading tabular data from excel in a very forgiving manner.
"""

__version__ = "0.8"
import warnings
warnings.warn("EXCELerator is deprecated. Use fuzzytable instead.", DeprecationWarning)

from excelerator.main.fieldparser import FieldParser
from excelerator.main.tableparser import TableParser
from excelerator.main.worksheetparser import WorksheetParser
