# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-model (see http://github.com/oarepo/oarepo-model).
#
# oarepo-model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Preset for creating file resource config.

This module provides a preset that modifies file resource config.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, override

# TODO: from oarepo_runtime.resources.config import BaseRecordResourceConfig as RDMBaseRecordResourceConfig
from oarepo_model.customizations import Customization, PrependMixin
from oarepo_model.presets import Preset

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping

    from invenio_records_resources.resources.files.config import FileResourceConfig
    from oarepo_model.builder import InvenioModelBuilder
    from oarepo_model.model import InvenioModel
else:
    FileResourceConfig = object


class PipelineFileResourceConfig(FileResourceConfig):
    """Pipeline File resource config."""

    @property
    def routes(self) -> Mapping[str, str]:  # pyright: ignore[reportIncompatibleVariableOverride]
        """Add read_with_pipeline route."""
        return {**super().routes, "read_with_pipeline": "files/<path:key>/pipeline"}


class PipelineResourceConfigPreset(Preset):
    """Preset for file resource config class."""

    modifies = ("FileResourceConfig",)

    @override
    def apply(
        self,
        builder: InvenioModelBuilder,
        model: InvenioModel,
        dependencies: dict[str, Any],
    ) -> Generator[Customization]:
        yield PrependMixin(
            "FileResourceConfig",
            PipelineFileResourceConfig,
        )
