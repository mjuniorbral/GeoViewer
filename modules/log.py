import logging
from logging import Formatter, StreamHandler, getLogger, DEBUG

# 1. Formatter
formatter = Formatter("[%(asctime)s] %(levelname)s : %(filename)s.%(funcName)s: [line %(lineno)d]: %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

# 2. Handler
handler = StreamHandler()
handler.setFormatter(formatter)

# 3. Logger
log = getLogger(__name__)
log.addHandler(handler)
log.setLevel(DEBUG)