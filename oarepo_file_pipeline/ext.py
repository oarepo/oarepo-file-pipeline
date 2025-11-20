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

from invenio_records_resources.config import RECORDS_RESOURCES_TRANSFERS

from oarepo_file_pipeline.pipeline_registry import PipelineRegistry
from oarepo_file_pipeline.schemas import CustomUserProfileSchema

if TYPE_CHECKING:
    from flask import Flask
    from joserfc.jwk import RSAKey


class OARepoFilePipeline:
    """OARepoFilePipeline flask extension."""

    def __init__(self, app: Flask | None = None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Register Flask app and init config."""
        self.app = app
        self.init_config(app)
        app.extensions["oarepo-file-pipeline"] = self

    def init_config(self, app: Flask) -> None:
        """Define default algorithms for JWT/JWE."""
        from . import config

        app.config.setdefault("PIPELINE_SIGNING_ALGORITHM", config.PIPELINE_SIGNING_ALGORITHM)
        app.config.setdefault("PIPELINE_ENCRYPTION_ALGORITHM", config.PIPELINE_ENCRYPTION_ALGORITHM)
        app.config.setdefault("PIPELINE_ENCRYPTION_METHOD", config.PIPELINE_ENCRYPTION_METHOD)

        app.config.setdefault(
            "RECORDS_RESOURCES_TRANSFERS",
            [*RECORDS_RESOURCES_TRANSFERS, *config.RECORDS_RESOURCES_TRANSFERS],
        )

        app.config.setdefault("ACCOUNTS_USER_PROFILE_SCHEMA", CustomUserProfileSchema)

        app.config.setdefault("PIPELINE_REDIRECT_URL", config.PIPELINE_REDIRECT_URL)
        app.config.setdefault("PIPELINE_REPOSITORY_JWK", config.PIPELINE_REPOSITORY_JWK)
        app.config.setdefault("PIPELINE_JWK", config.PIPELINE_JWK)

    @cached_property
    def pipeline_registry(self) -> PipelineRegistry:
        """Return the pipeline registry."""
        return PipelineRegistry("oarepo.file.pipelines")

    @property
    def signing_algorithm(self) -> str:
        """Signing algorithm getter."""
        return self.app.config["PIPELINE_SIGNING_ALGORITHM"]  # type: ignore[no-any-return]

    @property
    def pipeline_encryption_algorithm(self) -> str:
        """Encryption algorithm getter."""
        return self.app.config["PIPELINE_ENCRYPTION_ALGORITHM"]  # type: ignore[no-any-return]

    @property
    def pipeline_encryption_method(self) -> str:
        """Encryption method getter."""
        return self.app.config["PIPELINE_ENCRYPTION_METHOD"]  # type: ignore[no-any-return]

    @property
    def pipeline_redirect_url(self) -> str:
        """Redirect url server getter."""
        return self.app.config["PIPELINE_REDIRECT_URL"]  # type: ignore[no-any-return]

    @property
    def pipeline_repository_jwk(self) -> dict[str, RSAKey]:
        """Current repository RSA key pair getter."""
        return self.app.config["PIPELINE_REPOSITORY_JWK"]  # type: ignore[no-any-return]

    @property
    def pipeline_jwk(self) -> dict[str, RSAKey]:
        """Redirect server RSA public key getter."""
        return self.app.config["PIPELINE_JWK"]  # type: ignore[no-any-return]
