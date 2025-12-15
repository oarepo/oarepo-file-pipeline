#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-model (see http://github.com/oarepo/oarepo-model).
#
# oarepo-model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Module to generate permission policy class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, override

from flask import current_app
from invenio_records_resources.services.files.components.base import FileServiceComponent
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.uow import RecordCommitOp
from oarepo_model.customizations import Customization, PrependMixin
from oarepo_model.presets import Preset

from oarepo_file_pipeline.proxies import current_pipeline_registry

from .pipeline_transfer import PipelineTransfer

if TYPE_CHECKING:
    from collections.abc import Generator

    from flask_principal import Identity
    from invenio_records_resources.records.api import Record
    from oarepo_model.builder import InvenioModelBuilder
    from oarepo_model.model import InvenioModel


class PipelineFileComponent(FileServiceComponent):
    """File service component for correctly setting transfer type on supported files."""

    def commit_file(self, identity: Identity, id_: str, file_key: str, record: Record) -> None:  # noqa: ARG002
        """Change transfer type to PipelineTransfer if pipeline can handle the file."""
        if (
            "oarepo_file_pipeline.model.presets.pipeline.services.pipeline_transfer:PipelineTransfer"
            not in current_app.config["RECORDS_RESOURCES_TRANSFERS"]
        ):
            return

        f_obj = record.files.get(file_key)  # type: ignore[attr-defined]
        pipeline_can_handle = len(list(current_pipeline_registry.list_pipelines(identity, f_obj))) > 0

        if pipeline_can_handle and f_obj.transfer.transfer_type != PipelineTransfer.transfer_type:
            f_obj.transfer.transfer_type = PipelineTransfer.transfer_type
            self.uow.register(RecordCommitOp(f_obj))


class PipelineFileServiceConfigMixin:
    """Mixin to add PipelineFileComponent to file service config."""

    components: ClassVar[list[type[FileServiceComponent]]] = [
        *FileServiceConfig.components,  # type: ignore[reportAttributeAccessIssue]
        PipelineFileComponent,
    ]  # add component at the end to ensure that it runs last


class PipelineFileServiceConfigPreset(Preset):
    """Preset for permission policy class."""

    modifies = ("FileServiceConfig",)

    @override
    def apply(
        self,
        builder: InvenioModelBuilder,
        model: InvenioModel,
        dependencies: dict[str, Any],
    ) -> Generator[Customization]:
        yield PrependMixin("FileServiceConfig", PipelineFileServiceConfigMixin)


class PipelineDraftFileServiceConfigPreset(Preset):
    """Preset for permission policy class."""

    modifies = ("DraftFileServiceConfig",)

    @override
    def apply(
        self,
        builder: InvenioModelBuilder,
        model: InvenioModel,
        dependencies: dict[str, Any],
    ) -> Generator[Customization]:
        yield PrependMixin("DraftFileServiceConfig", PipelineFileServiceConfigMixin)
