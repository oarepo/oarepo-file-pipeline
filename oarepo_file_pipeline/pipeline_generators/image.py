#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Image Generator."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from oarepo_file_pipeline.pipeline_registry import PipelineGenerator

if TYPE_CHECKING:
    from collections.abc import Iterator

    from flask_principal import Identity
    from invenio_records_resources.records import FileRecord


class ImageGenerator(PipelineGenerator):
    """Image Generator."""

    def __init__(self, **kwargs: Any):
        """Initialize Image Generator."""

    def can_handle(self, identity: Identity, file_record: FileRecord) -> bool:  # noqa: ARG002
        """Check if this is image file."""
        return cast("bool", file_record.object_version.mimetype.startswith("image/"))

    def list_pipelines(self, identity: Identity, file_record: FileRecord) -> Iterator[str]:  # noqa: ARG002
        """List all available pipelines."""
        return iter(
            [
                "preview_picture",
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
            raise ValueError("Image Generator can not handle file")
        if not file_url:
            raise ValueError("File URL cannot be None")

        if pipeline_name == "preview_picture":
            return [
                {
                    "type": "preview_picture",
                    "arguments": {
                        "source_url": file_url,
                        "max_height": extra_arguments.get(
                            "max_height", 10000
                        ),  # TODO: change this to original picture size
                        "max_width": extra_arguments.get("max_width", 10000),  # dont crop it for preview
                    },
                },
            ]

        return []
