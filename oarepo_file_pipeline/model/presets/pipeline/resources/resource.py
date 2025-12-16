#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Resource layer delegates pipeline processing logic to service layer by calling service.pipeline()."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from flask import g, redirect, request
from flask_resources import resource_requestctx, route
from invenio_records_resources.resources import FileResource
from invenio_records_resources.resources.files.resource import request_view_args
from oarepo_model.customizations import Customization, PrependMixin
from oarepo_model.presets import Preset

if TYPE_CHECKING:
    from collections.abc import Generator

    from oarepo_model.builder import InvenioModelBuilder
    from oarepo_model.model import InvenioModel
    from werkzeug.wrappers import Response as WerkzeugResponse


class PipelineFileResource(FileResource):
    """Resource layer for files.

    Delegates pipeline processing logic to service layer by calling service.pipeline().
    """

    def create_url_rules(self) -> list:
        """Add /pipeline route."""
        routes = self.config.routes

        return [
            *super().create_url_rules(),
            route("GET", routes["read_with_pipeline"], self.read_with_pipeline),
        ]

    @request_view_args
    def read_with_pipeline(self) -> WerkzeugResponse:
        """Process pipeline request with service layer.

        Service layer returns a redirect link for current pipeline steps
        """
        query_params = request.args.to_dict()
        redirect_url = self.service.pipeline(
            identity=g.identity,
            id_=resource_requestctx.view_args["pid_value"],
            file_key=resource_requestctx.view_args["key"],
            suggested_pipeline=query_params.pop("pipeline", None),
            query_params=query_params,
        )
        return redirect(redirect_url, code=302)


class PipelineResourcePreset(Preset):
    """Preset for file resource class."""

    modifies = ("FileResource",)

    @override
    def apply(
        self,
        builder: InvenioModelBuilder,
        model: InvenioModel,
        dependencies: dict[str, Any],
    ) -> Generator[Customization]:
        yield PrependMixin("FileResource", PipelineFileResource)
