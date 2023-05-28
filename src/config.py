from enum import Enum, unique, auto
from rich.logging import RichHandler
import logging


class MODE(Enum):
    EMPTY = "empty"
    BALANCED = "balanced"
    PEAK = "peak"


class LOGLEVEL(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARN = "warn"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"

    def init_logging(self):
        """
        starts up logging for this app, based on user specified log level
        """
        logging.basicConfig(
            format="%(message)s",
            level=self.value.upper(),
            handlers=[
                RichHandler(
                    markup=True,
                    show_path=False,
                    show_time=False,
                    show_level=True,
                ),
            ],
        )
        # check if it actually works :3
        logging.debug("initialized logging")
