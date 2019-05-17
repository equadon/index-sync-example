# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Index Sync is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Index Sync."""

from invenio_search.sync import SyncJob

from .. import config


class RecordSyncJob(SyncJob):
    def __init__(self, rollover_threshold, source_indexes, dest_indexes,
                 **kwargs):
        """Records sync job."""
        super(RecordSyncJob, self).__init__(
            rollover_threshold=rollover_threshold,
            source_indexes=source_indexes,
            dest_indexes=dest_indexes
        )
