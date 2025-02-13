#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Resource layer delegates pipeline processing logic to service layer by calling service.pipeline()."""

from __future__ import annotations
from typing import TYPE_CHECKING

from invenio_records_resources.resources import FileResource
from invenio_records_resources.resources.files.resource import request_view_args

from flask_resources import route, resource_requestctx
from flask import redirect, request, g


if TYPE_CHECKING:
    from flask import Response

class PipelineFileResource(FileResource):
    """Resource layer for files.

    Delegates pipeline processing logic to service layer by calling service.pipeline().
    """
    def create_url_rules(self) -> list:
        """Add /pipeline route"""
        routes = self.config.routes

        rules = super().create_url_rules()
        rules.append(
            route("GET", routes["item"] + "/pipeline", self.read_with_pipeline),
        )

        return rules


    @request_view_args
    def read_with_pipeline(self) -> Response:
        """Process pipeline request with service layer

        Service layer returns a redirect link for current pipeline steps
        """
        query_params = request.args.to_dict()
        redirect_url = self.service.pipeline(identity=g.identity,
                                             id_=resource_requestctx.view_args["pid_value"],
                                             file_key=resource_requestctx.view_args["key"],
                                             suggested_pipeline=query_params.get("pipeline"),
                                             query_params=query_params
                                             )
        print(redirect_url)
        return redirect(redirect_url, code=302)

