#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Crypt4GH Generator."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from oarepo_file_pipeline.pipeline_registry import PipelineGenerator

if TYPE_CHECKING:
    from collections.abc import Iterator

    from flask_principal import Identity
    from invenio_records_resources.records import FileRecord


class Crypt4GHGenerator(PipelineGenerator):
    """Crypt4GH Generator. Generates pipeline payload for the server."""

    def __init__(self, **kwargs: Any):
        """Initialize Crypt4GH Generator."""

    def can_handle(self, identity: Identity, file_record: FileRecord) -> bool:  # noqa: ARG002
        """Check if this is crypt4gh file."""
        return cast("bool", file_record.key.endswith(".c4gh"))

    def list_pipelines(self, identity: Identity, file_record: FileRecord) -> Iterator[str]:  # noqa: ARG002
        """List all available pipelines."""
        return iter(
            [
                "add_recipient_crypt4gh",
                "decrypt_crypt4gh",
                "validate_crypt4gh",
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
            raise ValueError("Crypt4GH Generator can not handle file")
        if not file_url:
            raise ValueError("File URL cannot be None")

        if pipeline_name == "add_recipient_crypt4gh":
            user_pub_key = identity.user.user_profile.get("public_key") or extra_arguments.get("recipient_pub")  # type: ignore[attr-defined]

            return [
                {
                    "type": "add_recipient_crypt4gh",
                    "arguments": {
                        "source_url": file_url,
                        "recipient_pub": user_pub_key,
                    },
                },
            ]
        if pipeline_name == "decrypt_crypt4gh":
            return [
                {
                    "type": "decrypt_crypt4gh",
                    "arguments": {
                        "source_url": file_url,
                    },
                },
            ]
        if pipeline_name == "validate_crypt4gh":
            return [
                {
                    "type": "validate_crypt4gh",
                    "arguments": {
                        "source_url": file_url,
                    },
                },
            ]

        return []
