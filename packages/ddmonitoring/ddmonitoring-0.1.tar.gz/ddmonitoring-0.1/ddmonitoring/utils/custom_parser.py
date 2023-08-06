import cliff._argparse as _argparse
from cliff.app import App

class CustomParser:
    def __init__(self, description, version, deferred_help):
        """Return an argparse option parser for this application.
        Subclasses may override this method to extend
        the parser with more global options.
        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        """
        argparse_kwargs = {}
        self.parser = _argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        self.parser.add_argument(
            '--version',
            action='version',
            version='{0} {1}'.format(App.NAME, version),
        )
        self.parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        if deferred_help:
            self.parser.add_argument(
                '-h', '--help',
                dest='deferred_help',
                action='store_true',
                help="Show help message and exit.",
            )
        else:
            self.parser.add_argument(
                '-h', '--help',
                action=help.HelpAction,
                nargs=0,
                default=self,  # tricky
                help="Show help message and exit.",
            )
        self.parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='Show tracebacks on errors.',
        )