
import logging

from prophetess.plugin import Transformer

log = logging.getLogger('prophetess.plugins.null.transformer')


class NullTransformer(Transformer):

    async def run(self, data):
        log.info(data)
        yield data
