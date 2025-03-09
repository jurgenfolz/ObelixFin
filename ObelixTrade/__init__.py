__version__ = "0.1.0"

from .data import DataFetcher
from .indicators import SMA
from .Strategies.BaseStrategy import BaseStrategy
from .Strategies.SMA import SMACrossoverStrategy
from .Strategies.KNN import KNNStrategy
from .backtester import Backtester
from .plotter import Plotter