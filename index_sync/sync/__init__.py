# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Index Sync is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Index Sync."""

from invenio_index_migrator.api import SyncJob

from .. import config


class RecordSyncJob(SyncJob):
    def rollover(self):
        """Rollover."""
        print('RecordSyncJob::rollover()')
