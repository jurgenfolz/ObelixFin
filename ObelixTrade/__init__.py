__version__ = "0.1.0"

from .data import DataFetcher
from .indicators import SMA
from .strategies import BaseStrategy, SMACrossoverStrategy
from .backtester import Backtester
from .plotter import Plotter