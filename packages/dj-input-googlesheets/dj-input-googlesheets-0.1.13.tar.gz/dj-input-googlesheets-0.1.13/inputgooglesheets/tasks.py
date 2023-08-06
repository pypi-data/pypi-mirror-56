from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string


logger = logging.getLogger(__name__)


LOCK_KEY = '744ed748-7685-41ca-a714-f0bfb6db0b80:{}'


def get_lock(key):
    Lock = import_string(settings.DISTRIBUTED_LOCKS_BACKEND)
    wait = getattr(settings, 'DISTRIBUTED_LOCKS_WAIT', 1)
    return Lock(settings.DISTRIBUTED_LOCKS_CONNECTION_STRING, key)


@shared_task
def start_import(spreadsheet_pk):
    from .models import Spreadsheet
    from .utils import Utils
    lock_key = LOCK_KEY.format(spreadsheet_pk)
    with get_lock(lock_key):
        try:
            spreadsheet = Spreadsheet.objects.get(pk=spreadsheet_pk)
            if not spreadsheet.enabled:
                logger.info("Could not import disabled spreadsheet: {}".format(spreadsheet_pk))
                return
            logger.info("Continue import spreadsheet: {}".format(spreadsheet_pk))
        except Spreadsheet.DoesNotExist:
            logger.warn("Import spreadsheet {} failed. It does not exist.".format(spreadsheet_pk))
        count = Utils.start_import(spreadsheet)
        logger.info("Finished importing spreadsheet {}: {} rows imported".format(spreadsheet_pk, count))


@shared_task
def continue_import(spreadsheet_pk):
    from .models import Spreadsheet
    from .utils import Utils
    lock_key = LOCK_KEY.format(spreadsheet_pk)
    with get_lock(lock_key):
        try:
            spreadsheet = Spreadsheet.objects.get(pk=spreadsheet_pk)
            if not spreadsheet.enabled:
                logger.info("Could not import disabled spreadsheet: {}".format(spreadsheet_pk))
                return
            logger.info("Continue import spreadsheet: {}".format(spreadsheet_pk))
        except Spreadsheet.DoesNotExist:
            logger.warn("Import spreadsheet {} failed. It does not exist.".format(spreadsheet_pk))
        count = Utils.continue_import(spreadsheet)
        logger.info("Finished importing spreadsheet {}: {} rows imported".format(spreadsheet_pk, count))


@shared_task
def import_all_google_spreadsheets():
    from .models import Spreadsheet
    lock_key = LOCK_KEY.format('')
    with get_lock(lock_key):
        for spreadsheet in Spreadsheet.objects.filter(enabled=True, automatically_imported=True):
            continue_import.delay(spreadsheet.pk)
