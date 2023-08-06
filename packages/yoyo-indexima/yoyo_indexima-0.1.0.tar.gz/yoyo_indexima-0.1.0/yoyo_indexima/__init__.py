"""yoyo-indexima definition."""
from pkg_resources import DistributionNotFound, get_distribution
from yoyo import read_migrations  # noqa

from .connections import get_backend  # noqa


try:
    __version__ = get_distribution('yoyo_indexima').version
except DistributionNotFound:
    __version__ = '(local)'
