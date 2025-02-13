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
from invenio_base.utils import obj_or_import_string

from oarepo_file_pipeline.pipeline_registry import PipelineRegistry

if TYPE_CHECKING:
    from oarepo_file_pipeline import PipelineGetterFunction


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
        app.extensions['oarepo-file-pipeline'] = self

    def init_config(self, app):
        """Define default algorithms for JWT/JWE."""
        from . import config
        app.config.setdefault(
            "PIPELINE_SIGNING_ALGORITHM", config.PIPELINE_SIGNING_ALGORITHM
        )
        app.config.setdefault(
            "PIPELINE_ENCRYPTION_ALGORITHM", config.PIPELINE_ENCRYPTION_ALGORITHM
        )
        app.config.setdefault(
            "PIPELINE_ENCRYPTION_METHOD", config.PIPELINE_ENCRYPTION_METHOD
        )
        app.config["RECORDS_RESOURCES_TRANSFERS"] =  app.config.setdefault("RECORDS_RESOURCES_TRANSFERS", []) + config.RECORDS_RESOURCES_TRANSFERS

        if not app.config.get("RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE") or app.config.get("RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE") == "L":
            app.config["RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE"] = config.RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE

    @cached_property
    def pipeline_registry(self) -> PipelineRegistry:
        """Return the pipeline registry."""
        return PipelineRegistry('oarepo.file.pipelines')

    @property
    def signing_algorithm(self):
        """Signing algorithm getter."""
        return self.app.config['PIPELINE_SIGNING_ALGORITHM']

    @property
    def pipeline_encryption_algorithm(self):
        """Encryption algorithm getter."""
        return self.app.config['PIPELINE_ENCRYPTION_ALGORITHM']

    @property
    def pipeline_encryption_method(self):
        """Encryption method getter."""
        return self.app.config['PIPELINE_ENCRYPTION_METHOD']

    @property
    def pipeline_redirect_url(self):
        """Redirect url server getter."""
        return self.app.config['PIPELINE_REDIRECT_URL']

    @property
    def pipeline_repository_jwk(self):
        """Current repository RSA key pair getter."""
        return self.app.config['PIPELINE_REPOSITORY_JWK']

    @property
    def pipeline_jwk(self):
        """Redirect server RSA public key getter"""
        return self.app.config['PIPELINE_JWK']



