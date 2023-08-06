import sys
import logging
from cliff.app import App
from cliff.commandmanager import CommandManager
import cliff._argparse as _argparse


class MonitoringApp(App):
    """App class from cliff overriden to implement the Datadog Challenge app."""
    def __init__(self):
        self.description = 'Datadog monitoring CLI'
        self.version = '0.1'
        self.deferred_help = True
        super(MonitoringApp, self).__init__(
            description=self.description,
            version=self.version,
            command_manager=CommandManager('dd.monitoring'),
            deferred_help=self.deferred_help,
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)
 
    def build_option_parser(self, description, version,
                            argparse_kwargs=None):
        """Return an argparse option parser for this application.
        Subclasses may override this method to extend
        the parser with more global options.
        :param description: full description of the application
        :paramtype description: str
        :param version: version number for the application
        :paramtype version: str
        :param argparse_kwargs: extra keyword argument passed to the
                                ArgumentParser constructor
        :paramtype extra_kwargs: dict
        """
        argparse_kwargs = argparse_kwargs or {}
        parser = _argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        parser.add_argument(
            '--version',
            action='version',
            version='{0} {1}'.format(App.NAME, version),
        )
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        if self.deferred_help:
            parser.add_argument(
                '-h', '--help',
                dest='deferred_help',
                action='store_true',
                help="Show help message and exit.",
            )
        else:
            parser.add_argument(
                '-h', '--help',
                action=help.HelpAction,
                nargs=0,
                default=self,  # tricky
                help="Show help message and exit.",
            )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='Show tracebacks on errors.',
        )
        return parser
    def configure_logging(self):
        """Create logging handlers for any log output.
        """
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        # Set up logging to a file
        if self.options.log_file:
            file_handler = logging.FileHandler(
                filename=self.options.log_file,
            )
            formatter = logging.Formatter(self.LOG_FILE_MESSAGE_FORMAT)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Always send higher-level messages to the console via stderr
        console = logging.StreamHandler(self.stderr)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(self.CONSOLE_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)
        return


def main(argv=sys.argv[1:]):
    app = MonitoringApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
