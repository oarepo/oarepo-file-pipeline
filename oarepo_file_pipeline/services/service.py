#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Service layer handles signing JWT or encrypting JWE for specific pipeline steps and file. Creates redirect link."""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Any

from flask import current_app
from invenio_access.permissions import system_identity
from invenio_cache import current_cache
from invenio_rdm_records.records.api import RDMRecord
from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_resources.services import FileService
from joserfc import jwe, jwt

from oarepo_file_pipeline.proxies import current_pipeline, current_pipeline_registry

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_records_resources.records.api import FileRecord


class PipelineFileService(FileService):
    """Service layer for files.

    Processes /pipeline route.
    """

    @property
    def record_cls(self):
        """Get the record class."""
        return RDMRecord  # TODO: hardcoded for now

    @property
    def permission_policy_cls(self):
        return RDMRecordPermissionPolicy

    def _create_signed_payload(
        self, payload: dict[str, any], signing_algorithm: str, private_key: Any
    ):
        """Create a JWS  for the given payload."""
        header = {
            "alg": signing_algorithm
        }  # because we are using RSA private key to sign it, https://jose.authlib.org/en/guide/jwt/#the-key-parameter
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        claims = {"iat": timestamp, "exp": timestamp + 300, **payload}

        signed_payload = jwt.encode(header, claims, private_key)
        return signed_payload

    def pipeline(
        self,
        identity: Identity,
        id_: FileRecord,
        file_key: str,
        suggested_pipeline: str | None,
        query_params: dict[str, str],
        current_oarepo_file_pipeline=current_pipeline,
    ) -> str:
        """Pipeline definition function.

        1) Retrieve pipeline steps
        2) Sign pipeline steps with REPOSITORY private key
        3) Encrypt payload (pipeline steps, file_url, timestamp) with public key of PIPELINE_FILE_SERVER
        4) Cache JWE under random id
        5) Generate redirect link

        """
        file_content = self.get_file_content(system_identity, id_, file_key)
        source_url = (
            file_content._file.file.uri
        )  # TODO: check if it local file, how to handle local?
        file_record = file_content._file

        if source_url is None or source_url == "":
            raise ValueError("Source URL not found")

        # Retrieve pipeline steps
        pipeline_steps = current_pipeline_registry.get_pipeline(
            identity, file_record, source_url, suggested_pipeline, query_params
        )

        # Generate the payload for the JWE
        payload = {
            "pipeline_steps": pipeline_steps,
            "source_url": source_url,
        }

        # Prepare JWS signing and JWE encryption headers
        signing_algorithm = current_oarepo_file_pipeline.signing_algorithm
        encryption_algorithm = (
            current_oarepo_file_pipeline.pipeline_encryption_algorithm
        )
        encryption_method = current_oarepo_file_pipeline.pipeline_encryption_method
        protected_header = {"alg": encryption_algorithm, "enc": encryption_method}

        # Create signed payload
        private_key = current_oarepo_file_pipeline.pipeline_repository_jwk[
            "private_key"
        ]
        signed_payload = self._create_signed_payload(
            payload, signing_algorithm, private_key
        )

        # Encrypt the signed payload into a JWE
        public_key = current_oarepo_file_pipeline.pipeline_jwk["public_key"]
        encrypted_token = jwe.encrypt_compact(
            protected_header, signed_payload, public_key
        )

        # Cache the token and generate a token ID
        token_id = str(uuid.uuid4())
        current_cache.cache._write_client.setex(
            name=token_id, value=encrypted_token, time=300
        )

        # Redirect to dedicated server
        redirect_url = f"{current_app.config['PIPELINE_REDIRECT_URL']}/{token_id}"
        return redirect_url
