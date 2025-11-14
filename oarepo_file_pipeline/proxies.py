#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Proxies for accessing the current OARepo file pipeline extension without bringing dependencies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from oarepo_file_pipeline.ext import OARepoFilePipeline
    from oarepo_file_pipeline.pipeline_registry import PipelineRegistry

    current_pipeline: OARepoFilePipeline  # type: ignore[reportRedeclaration]
    current_pipeline_registry: PipelineRegistry  # type: ignore[reportRedeclaration]

# note: mypy does not understand LocalProxy[OARepoFilePipeline], so we type it as OARepoFilePipeline
# and ignore the redeclaration error
current_pipeline = LocalProxy(  # type: ignore[assignment]
    lambda: current_app.extensions["oarepo-file-pipeline"]
)

current_pipeline_registry = LocalProxy(  # type: ignore[assignment]
    lambda: current_app.extensions["oarepo-file-pipeline"].pipeline_registry
)
"""Helper proxy to get the current oarepo file pipeline extension."""
