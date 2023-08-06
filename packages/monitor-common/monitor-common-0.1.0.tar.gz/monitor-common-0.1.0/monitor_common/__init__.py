"""Package provides common code used by the internet monitor found at {URI}."""
from pkg_resources import get_distribution, DistributionNotFound

# Try and expose __version__, as per PEP396.
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
