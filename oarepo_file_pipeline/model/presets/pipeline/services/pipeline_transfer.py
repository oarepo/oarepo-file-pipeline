#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Pipeline Transfer type that expands links with possible pipeline options for file."""

from __future__ import annotations

from typing import TYPE_CHECKING

from invenio_records_resources.services.files.transfer.providers.local import (
    LocalTransfer,
)

from oarepo_file_pipeline.proxies import current_pipeline_registry

if TYPE_CHECKING:
    from flask_principal import Identity


class PipelineTransfer(LocalTransfer):
    """Pipeline Transfer type that expands links with possible pipeline options for file."""

    transfer_type = "P"

    def expand_links(self, identity: Identity, self_url: str) -> dict[str, str]:
        """Expand links with possible pipelines."""
        links: dict[str, str] = super().expand_links(identity, self_url)

        if self.status != "completed":
            return links

        for pipeline in current_pipeline_registry.list_pipelines(identity, self.file_record):
            links[pipeline] = f"{self_url}/pipeline?pipeline={pipeline}"

        return links
