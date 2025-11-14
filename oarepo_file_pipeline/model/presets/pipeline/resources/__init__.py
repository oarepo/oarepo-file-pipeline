#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Resource package initialization."""

from __future__ import annotations

from .config import PipelineResourceConfigPreset
from .resource import PipelineResourcePreset

__all__ = ["PipelineResourceConfigPreset", "PipelineResourcePreset"]
