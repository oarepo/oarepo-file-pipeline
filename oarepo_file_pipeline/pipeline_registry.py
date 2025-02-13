#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Pipeline Registry and Pipeline Generator."""
from typing import Protocol, Iterator
from flask_principal import Identity
from invenio_records_resources.records import FileRecord


class PipelineGenerator(Protocol):
    """Pipeline Generator.

    Depending on given identity and specific file can determine if
    1) if generator can handle this file
    2) list all possible pipelines
    3) generate specific pipeline for given file and extra arguments
    """
    def can_handle(self, identity: Identity, file_rec: FileRecord) -> bool:
        ...

    def list_pipelines(self, identity: Identity, file_rec: FileRecord) -> Iterator[str]:
        ...

    def get_pipeline(self,identity: Identity, file_record: FileRecord, file_url: str, pipeline_name: str, extra_arguments: dict[str,str] ) -> list:
        ...



class PipelineRegistry:
    """Pipeline Registry.

    Stores all pipeline generators (zip, image, crypt4gh etc.).

    Can list all possible pipeline for given file.
    Can generate specific pipeline for pipeline name(preview_zip, preview_picture etc.), given file and extra arguments
    """
    def __init__(self, entrypoint_name: str | None) -> None:
        self._pipeline_generators = []
        self._entrypoint_name = entrypoint_name

        import importlib_metadata
        for entrypoint in importlib_metadata.entry_points(group=self._entrypoint_name):
            self.register_pipeline(entrypoint.load()())

    @property
    def pipeline_generators(self):
        return self._pipeline_generators

    def list_pipelines(self, identity: Identity, file_rec: FileRecord) -> Iterator[str]:
        for pipeline in self.pipeline_generators:
            if pipeline.can_handle(identity, file_rec):
                yield from pipeline.list_pipelines(identity, file_rec)

    def get_pipeline(self,identity: Identity, file_record: FileRecord, file_url: str, pipeline_name: str, extra_arguments: dict[str,str]  ) -> list:
        for pipeline in self.pipeline_generators:
            if pipeline.can_handle(identity, file_record):
                if pipeline_name not in pipeline.list_pipelines(identity, file_record):
                    continue
                else:
                    return pipeline.get_pipeline(identity, file_record, file_url, pipeline_name, extra_arguments)

    def register_pipeline(self, pipeline: PipelineGenerator):
        self._pipeline_generators.append(pipeline)

