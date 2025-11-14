#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""ZIP Generator."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from oarepo_file_pipeline.pipeline_registry import PipelineGenerator

if TYPE_CHECKING:
    from collections.abc import Iterator

    from flask_principal import Identity
    from invenio_records_resources.records import FileRecord


class ZipGenerator(PipelineGenerator):
    """Zip Generator."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize Zip Generator."""

    def can_handle(self, identity: Identity, file_record: FileRecord) -> bool:  # noqa: ARG002
        """Check if this is zip file."""
        return cast("bool", file_record.object_version.mimetype == "application/zip")

    def list_pipelines(self, identity: Identity, file_record: FileRecord) -> Iterator[str]:  # noqa: ARG002
        """List all available pipelines."""
        return iter(
            [
                "preview_zip",
                "extract_zip",
            ]
        )

    def get_pipeline(
        self,
        identity: Identity,
        file_record: FileRecord,
        file_url: str,
        pipeline_name: str,
        extra_arguments: dict[str, str],
    ) -> list:
        """Generate pipeline for specific file and extra arguments."""
        if not self.can_handle(identity, file_record):
            raise ValueError("ZIP Generator can not handle file")
        if not file_url:
            raise ValueError("File URL cannot be None")

        if pipeline_name == "preview_zip":
            return [
                {
                    "type": "preview_zip",
                    "arguments": {
                        "source_url": file_url,
                    },
                },
            ]
        if pipeline_name == "extract_zip":
            if not extra_arguments.get("directory_or_file_name"):
                raise ValueError("Please provide a directory or file name")

            return [
                {
                    "type": "extract_zip",
                    "arguments": {
                        "source_url": file_url,
                        "directory_or_file_name": extra_arguments["directory_or_file_name"],
                    },
                }
            ]

        return []
