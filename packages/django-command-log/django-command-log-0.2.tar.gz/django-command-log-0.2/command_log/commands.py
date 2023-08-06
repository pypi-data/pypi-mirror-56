import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from .models import ManagementCommandLog

logger = logging.getLogger("command_log")


class DoNotCommit(Exception):
    """Exception used to indicate the --commit option is not set."""

    pass


class LoggedCommand(BaseCommand):

    """Base class for commands that automatically log their execution."""

    @property
    def app_name(self):
        return self.__module__.split(".")[-4]

    @property
    def command_name(self):
        return self.__module__.split(".")[-1]

    def do_command(self, *args, **options):
        raise NotImplementedError()

    def handle(self, *args, **options):
        """Run the do_command method and log the output."""
        log = ManagementCommandLog(
            app_name=self.app_name, command_name=self.command_name
        )
        log.start()
        try:
            output = self.do_command(*args, **options)
            log.stop(output=output, exit_code=0)
        except Exception as ex:
            logger.exception("Error running management command: %s", log)
            output = f'ERROR: see logs for full traceback ["{ex}"].'
            log.stop(output=output, exit_code=1)


class TransactionLoggedCommand(LoggedCommand):

    """Base class for commands that automatically rollback in the event of a failure."""

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--commit",
            action="store_true",
            dest="commit",
            default=False,
            help="Commit database changes",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        try:
            with transaction.atomic():
                super().handle(*args, **options)
                if not commit:
                    raise DoNotCommit()
        except DoNotCommit:
            self.print_rollback_message()

    def print_rollback_message(self):
        self.stdout.write(
            "\n"
            + self.style.NOTICE("ROLLBACK")
            + " All database changes have been rolled back (--commit option not set)"
        )
