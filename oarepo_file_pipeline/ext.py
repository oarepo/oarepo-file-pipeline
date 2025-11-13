#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""OARepoFilePipeline flask extension."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from flask import Blueprint
from invenio_rdm_records.services.config import RDMFileRecordServiceConfig
from invenio_records_resources.config import RECORDS_RESOURCES_TRANSFERS

from oarepo_file_pipeline.pipeline_registry import PipelineRegistry
from oarepo_file_pipeline.resources.config import PipelineFileResourceConfig
from oarepo_file_pipeline.resources.resource import PipelineFileResource
from oarepo_file_pipeline.services.permissions import PipelineFilePermissionPolicy

from .services.service import PipelineFileService

if TYPE_CHECKING:
    pass

blueprint = Blueprint(
    "oarepo_file_pipeline",
    __name__,
)


class OARepoFilePipeline(object):
    """OARepoFilePipeline flask extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Register Flask app and init config."""
        self.app = app
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        app.extensions["oarepo-file-pipeline"] = self

    def init_config(self, app):
        """Define default algorithms for JWT/JWE."""
        from . import config

        app.config.setdefault(
            "PIPELINE_FILE_SERVICE_CONFIG", RDMFileRecordServiceConfig.build(app)
        )

        app.config.setdefault("PIPELINE_RESOURCE_CONFIG", PipelineFileResourceConfig)
        app.config.setdefault(
            "PIPELINE_SIGNING_ALGORITHM", config.PIPELINE_SIGNING_ALGORITHM
        )
        app.config.setdefault(
            "PIPELINE_ENCRYPTION_ALGORITHM", config.PIPELINE_ENCRYPTION_ALGORITHM
        )
        app.config.setdefault(
            "PIPELINE_ENCRYPTION_METHOD", config.PIPELINE_ENCRYPTION_METHOD
        )

        app.config.setdefault(
            "RECORDS_RESOURCES_TRANSFERS",
            [*RECORDS_RESOURCES_TRANSFERS, *config.RECORDS_RESOURCES_TRANSFERS],
        )

        app.config.setdefault(
            "RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE",
            config.RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
        )

        app.config.setdefault("RDM_PERMISSION_POLICY", PipelineFilePermissionPolicy)
        app.config.setdefault("PIPELINE_REDIRECT_URL", config.PIPELINE_REDIRECT_URL)
        app.config.setdefault("PIPELINE_REPOSITORY_JWK", config.PIPELINE_REPOSITORY_JWK)
        app.config.setdefault("PIPELINE_JWK", config.PIPELINE_JWK)

    def init_services(self, app):
        """Initialize services if needed."""
        self._pipeline_file_service = PipelineFileService(
            config=app.config["PIPELINE_FILE_SERVICE_CONFIG"]
        )

    def init_resources(self, app):
        self._pipeline_file_resource = PipelineFileResource(
            service=self._pipeline_file_service,
            config=app.config["PIPELINE_RESOURCE_CONFIG"],
        )

    @property
    def pipeline_file_resource(self):
        """Pipeline file resource getter."""
        return self._pipeline_file_resource

    @cached_property
    def pipeline_registry(self) -> PipelineRegistry:
        """Return the pipeline registry."""
        return PipelineRegistry("oarepo.file.pipelines")

    @property
    def signing_algorithm(self):
        """Signing algorithm getter."""
        return self.app.config["PIPELINE_SIGNING_ALGORITHM"]

    @property
    def pipeline_encryption_algorithm(self):
        """Encryption algorithm getter."""
        return self.app.config["PIPELINE_ENCRYPTION_ALGORITHM"]

    @property
    def pipeline_encryption_method(self):
        """Encryption method getter."""
        return self.app.config["PIPELINE_ENCRYPTION_METHOD"]

    @property
    def pipeline_redirect_url(self):
        """Redirect url server getter."""
        return self.app.config["PIPELINE_REDIRECT_URL"]

    @property
    def pipeline_repository_jwk(self):
        """Current repository RSA key pair getter."""
        return self.app.config["PIPELINE_REPOSITORY_JWK"]

    @property
    def pipeline_jwk(self):
        """Redirect server RSA public key getter"""
        return self.app.config["PIPELINE_JWK"]
