#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Package initialization."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_records_resources.records.api import FileRecord

__version__ = "0.1.1"


class PipelineGetterFunction(Protocol):
    """Protocol defining the expected signature for a pipeline getter function."""

    def __call__(
        self,
        identity: Identity,
        file_record: FileRecord,
        file_url: str,
        suggested_pipeline: str | None,
        extra_arguments: dict[str, str],
    ):
        """Generate pipeline for specific file and extra arguments."""
