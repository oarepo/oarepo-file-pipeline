#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-rdm (see https://github.com/oarepo/oarepo-rdm).
#
# oarepo-rdm is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""RDM model presets for oarepo-model package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from oarepo_file_pipeline.model.presets.pipeline.resources.config import (
    PipelineResourceConfigPreset,
)
from oarepo_file_pipeline.model.presets.pipeline.resources.resource import (
    PipelineResourcePreset,
)
from oarepo_file_pipeline.model.presets.pipeline.services.permissions import (
    PipelinePermissionPolicyPreset,
)
from oarepo_file_pipeline.model.presets.pipeline.services.service import (
    PipelineServicePreset,
)

if TYPE_CHECKING:
    from oarepo_model.api import FunctionalPreset
    from oarepo_model.presets import Preset


pipeline_preset: list[type[Preset | FunctionalPreset]] = [
    PipelineResourceConfigPreset,
    PipelinePermissionPolicyPreset,
    PipelineServicePreset,
    PipelineResourcePreset,
]


__all__ = ("pipeline_preset",)
