import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG

# 1. Formatter
formatter = Formatter("[%(asctime)s] %(levelname)s : %(pathname)s#%(lineno)d [%(funcName)s]: %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

# 2. Handler
handler = StreamHandler()
handler.setFormatter(formatter)

# 3. Logger
log = getLogger(__name__)
log.addHandler(handler)
log.setLevel(DEBUG)