# Lago Logs module - An easy way to set up your logs 
#
# To use this module, import the function logs_lake and run it.
# The function will automatically configure the logging in the right way.
# The module is extremely biased, so use by your own risk.

import logging 


def logs_lake():
    # Start the log level as debug, everything gets logged
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', 
        filename='example.log', encoding='utf-8',datefmt='%d/%m/%Y %I:%M:%S %p',
        level=logging.DEBUG)
    logger = logging.getLogger().debug("Logger started successfully")

