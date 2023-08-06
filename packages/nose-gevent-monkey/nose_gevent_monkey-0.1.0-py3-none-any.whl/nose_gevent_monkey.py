import logging

from nose.plugins import Plugin


logger = logging.getLogger(__name__)


class GeventMonkey(Plugin):
    name = 'gevent-monkey'

    def options(self, parser, env):
        parser.add_option(
            f'--no-{self.name}',
            action='store_true',
            dest='disabled',
            help="Don't monkey patch gevent"
        )

    def configure(self, options, conf):
        super().configure(options, conf)
        if options.disabled:
            return

        try:
            from gevent.monkey import patch_all
        except ImportError:
            logger.error('Unable to import gevent.monkey module.')
            return

        patch_all()
