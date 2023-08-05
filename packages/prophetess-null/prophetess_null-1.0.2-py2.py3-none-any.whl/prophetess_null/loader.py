
import logging

from prophetess.plugin import Loader

log = logging.getLogger('prophetess.plugins.null.loader')


class NullLoader(Loader):

    async def run(self, record):
        log.info(record)
