#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Pipeline Transfer type that expands links with possible pipeline options for file"""


from invenio_records_resources.services.files.transfer.providers.local import LocalTransfer
from oarepo_file_pipeline.proxies import current_pipeline_registry

class PipelineTransfer(LocalTransfer):
    transfer_type = "P"

    def expand_links(self, identity, self_url):
        links = super().expand_links(identity, self_url)

        if self.status != 'completed':
            return links

        for pipeline in current_pipeline_registry.list_pipelines(identity, self.file_record):
            print('expanding links for pipeline {}'.format(pipeline))
            links[pipeline] = f'{self_url}/pipeline?pipeline={pipeline}'

        return links
