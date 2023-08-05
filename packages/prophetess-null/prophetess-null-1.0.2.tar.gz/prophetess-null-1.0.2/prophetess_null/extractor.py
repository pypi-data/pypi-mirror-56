
import logging

from prophetess.plugin import Extractor

log = logging.getLogger('prophetess.plugins.null.extractor')


class NullExtractor(Extractor):

    async def run(self):
        pass
