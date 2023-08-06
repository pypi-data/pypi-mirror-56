import argparse
from .wide import WideHelpFormatter


class ThreeQuarterWidthHelpFormatter(WideHelpFormatter):
    percentage_of_line_length = 0.75


class ThreeQuarterWidthDefaultsHelpFormatter(ThreeQuarterWidthHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


__all__ = (
    WideHelpFormatter, 
    ThreeQuarterWidthHelpFormatter, 
    ThreeQuarterWidthDefaultsHelpFormatter
)