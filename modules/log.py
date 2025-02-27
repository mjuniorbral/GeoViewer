import logging
from logging import Formatter, StreamHandler, FileHandler, getLogger, DEBUG

# 1. Formatter
formatter = Formatter("[%(asctime)s]\n\t%(levelname)s : %(pathname)s#%(lineno)d [%(funcName)s]:\n\t\t%(message)s", datefmt="%d/%m/%Y %H:%M:%S")

# 2. Handlers
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = FileHandler("operacoes.log")
file_handler.setFormatter(formatter)

# 3. Logger
log = getLogger(__name__)
log.addHandler(stream_handler)
log.addHandler(file_handler)
log.setLevel(DEBUG)

# Remova essa linha, pois ela configura um logger raiz com um formatter padrão
# logging.basicConfig(filename=log_file)
