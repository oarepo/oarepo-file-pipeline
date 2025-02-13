#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Crypt4GH Generator."""

from typing import Iterator
from flask_principal import Identity
from invenio_records_resources.records import FileRecord

from oarepo_file_pipeline.pipeline_registry import PipelineGenerator

class Crypt4GHGenerator(PipelineGenerator):
    """Crypt4GH Generator. Generates pipeline payload for the server"""
    def __init__(self, **kwargs):
        pass

    def can_handle(self, identity: Identity, file_record: FileRecord) -> bool:
        """Check if this is crypt4gh file."""
        return file_record.key.endswith('.c4gh')

    def list_pipelines(self, identity: Identity, file_rec: FileRecord) -> Iterator[str]:
        """List all available pipelines."""
        return iter([
            'crypt4gh',
        ])

    def get_pipeline(self, identity: Identity, file_record: FileRecord, file_url: str, pipeline_name: str,
                     extra_arguments: dict[str, str]) -> list:
        """Generates pipeline for specific file and extra arguments."""
        if not self.can_handle(identity, file_record):
            raise ValueError("Crypt4GH Generator can not handle file")
        if not file_url:
            raise ValueError("File URL cannot be None")

        if pipeline_name == 'crypt4gh':
            return [
                {
                    'type': 'crypt4gh',
                    'arguments': {
                        'source_url': file_url,
                        'recipient_pub' : extra_arguments['recipient_pub'],
                    }
                 },
            ]