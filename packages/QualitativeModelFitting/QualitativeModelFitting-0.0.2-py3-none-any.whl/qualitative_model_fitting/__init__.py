"""
todo implement a cache system for performance improvements
todo build in full profile type analysis
 Do I manually code this, and if so, how?
 Or I could create lots of data and use ML to predict which class
todo implement the 'between' operator
todo implement the 'almost' operator
todo implement the 'start' and 'end' operators for time intervals
todo allow for assigning variables to collections so we can
 list species that have the same rules
todo write docs
todo build the steady state block
todo build a doseresponse block
todo build the plot block
todo build in loops so we can do bulk validations
todo build in variable assignment

#todo build interface into global profile type statement with the following syntax
# obs = 'Obs12: hyperbolic up Akt[InsulinOnly]'
# obs = 'Obs13: oscillation Akt[InsulinOnly]'
# obs = 'Obs14: sigmoidal down Akt[InsulinOnly]'

"""
import logging

from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter
from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._runner import Runner

MAJOR = 2
MINOR = 1
MICRO = 1
VERSION = f'{MAJOR}.{MINOR}.{MICRO}'


OPTIONS = dict(
    logging=dict(
        level=dict(
            fh=logging.DEBUG,
            ch=logging.INFO,
        ),
        use_file_logger=False,
        use_console_logger=True,
        filename='qmf_file_logger.log',
    )
)


def logging_config():
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(lineno)d:%(levelname)s: %(message)s')
    if OPTIONS['logging']['use_file_logger']:
        fh = logging.FileHandler(OPTIONS['logging']['filename'])
        fh.setLevel(OPTIONS['logging']['level']['fh'])
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    if OPTIONS['logging']['use_console_logger']:
        ch = logging.StreamHandler()
        ch.setLevel(OPTIONS['logging']['level']['ch'])
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    # create formatter and add it to the handlers
    # add the handlers to the logger
    return logger


LOG = logging_config()

# silence matplotlib logger
mpl_logger = logging.getLogger('matplotlib.pyplot').setLevel(logging.CRITICAL)


def change_logging_level(handler='ch', level=logging.INFO):
    pass

