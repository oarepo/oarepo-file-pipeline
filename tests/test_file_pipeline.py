#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-file-pipeline (see https://github.com/oarepo/oarepo-file-pipeline).
#
# oarepo-file-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

import datetime
import uuid
from unittest.mock import patch

from invenio_cache import current_cache
from joserfc import jwe, jwt


def test_extension_initialization(app):
    assert "oarepo-file-pipeline" in app.extensions


def test_create_signed_payload_valid(app, model_a, search_clear):
    model_a_file_service = model_a.proxies.current_service.files

    signing_algorithm = app.config["PIPELINE_SIGNING_ALGORITHM"]
    private_key = app.config["PIPELINE_REPOSITORY_JWK"]["private_key"]
    public_key = app.config["PIPELINE_REPOSITORY_JWK"]["public_key"]
    payload = {"key": "value"}
    claims_requests = jwt.JWTClaimsRegistry(now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()), leeway=5)

    signed_payload = model_a_file_service._create_signed_payload(payload, signing_algorithm, private_key)  # noqa: SLF001

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)
    claims_requests.validate_exp(value=decoded_jwt.claims.pop("exp"))
    claims_requests.validate_iat(value=decoded_jwt.claims.pop("iat"))
    assert decoded_jwt.claims == {"key": "value"}


def test_create_signed_payload_expired(app, model_a, search_clear):
    model_a_file_service = model_a.proxies.current_service.files

    signing_algorithm = app.config["PIPELINE_SIGNING_ALGORITHM"]
    private_key = app.config["PIPELINE_REPOSITORY_JWK"]["private_key"]
    public_key = app.config["PIPELINE_REPOSITORY_JWK"]["public_key"]
    payload = {"key": "value"}
    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()) + 306,
        leeway=5,
    )
    signed_payload = model_a_file_service._create_signed_payload(payload, signing_algorithm, private_key)  # noqa: SLF001

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)
    try:
        claims_requests.validate_exp(value=decoded_jwt.claims.pop("exp"))
        claims_requests.validate_iat(value=decoded_jwt.claims.pop("iat"))
        raise AssertionError
    except Exception:  # noqa: BLE001
        assert True


def test_create_signed_payload_issued_in_the_future(app, model_a, search_clear):
    model_a_file_service = model_a.proxies.current_service.files

    signing_algorithm = app.config["PIPELINE_SIGNING_ALGORITHM"]
    private_key = app.config["PIPELINE_REPOSITORY_JWK"]["private_key"]
    public_key = app.config["PIPELINE_REPOSITORY_JWK"]["public_key"]
    payload = {"key": "value"}
    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()) - 5,
        leeway=5,
    )

    signed_payload = model_a_file_service._create_signed_payload(payload, signing_algorithm, private_key)  # noqa: SLF001

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)

    try:
        claims_requests.validate_exp(value=decoded_jwt.claims.pop("exp"))
        claims_requests.validate_iat(value=decoded_jwt.claims.pop("iat"))
        raise AssertionError
    except Exception:  # noqa: BLE001
        assert True


def test_create_signed_payload_non_existing_singing_algorithm(app, model_a, search_clear):
    model_a_file_service = model_a.proxies.current_service.files
    signing_algorithm = None
    private_key = app.config["PIPELINE_REPOSITORY_JWK"]["private_key"]

    payload = {"key": "value"}
    try:
        _ = model_a_file_service._create_signed_payload(payload, signing_algorithm, private_key)  # noqa: SLF001
        raise AssertionError
    except Exception:  # noqa: BLE001
        assert True


def test_create_signed_payload_invalid_singing_algorithm(app, model_a, search_clear):
    model_a_file_service = model_a.proxies.current_service.files
    signing_algorithm = "RSA"
    private_key = app.config["PIPELINE_REPOSITORY_JWK"]["private_key"]

    payload = {"key": "value"}
    try:
        _ = model_a_file_service._create_signed_payload(payload, signing_algorithm, private_key)  # noqa: SLF001
        raise AssertionError
    except Exception:  # noqa: BLE001
        assert True


def test_pipeline(app, client, users, published_record_with_files, location, search_clear):
    unique_uuid = str(uuid.uuid4())

    with (
        patch("uuid.uuid4", return_value=uuid.UUID(unique_uuid)) as _,
    ):
        response = client.get(
            f"/modela/{published_record_with_files['id']}/files/blah.zip/pipeline?pipeline=preview_zip"
        )

        assert response.status_code == 302
        assert response.location == f"{app.config['PIPELINE_REDIRECT_URL']}/{unique_uuid}"

        jwe_token = current_cache.cache._read_client.get(unique_uuid).decode("utf-8")  # noqa: SLF001
        assert jwe_token is not None

        claims_requests = jwt.JWTClaimsRegistry(
            now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()),
            leeway=5,
        )
        encrypted_jwt = jwe.decrypt_compact(jwe_token, app.config["PIPELINE_SERVER_PRIVATE"]).plaintext
        decrypted_jwt = jwt.decode(encrypted_jwt, app.config["PIPELINE_REPOSITORY_JWK"]["public_key"])
        claims_requests.validate_exp(value=decrypted_jwt.claims.pop("exp"))
        claims_requests.validate_iat(value=decrypted_jwt.claims.pop("iat"))

        claims = decrypted_jwt.claims

        assert claims["pipeline_steps"][0]["type"] == "preview_zip"
        assert claims["pipeline_steps"][0]["arguments"]["source_url"]
        assert claims["source_url"]


def test_pipeline_crypt4gh_key_taken_from_user_profile(
    app, logged_client, user_with_public_key_in_profile, published_record_with_files, location, search_clear
):
    # since in tests permissions are not enforced we can use any user
    client = logged_client(user_with_public_key_in_profile)

    response = client.get(
        f"/modela/{published_record_with_files['id']}/files/blah.c4gh/pipeline?pipeline=add_recipient_crypt4gh"
    )

    assert response.status_code == 302

    jwe_token = current_cache.cache._read_client.get(response.location.rsplit("/", 1)[-1]).decode("utf-8")  # noqa: SLF001
    assert jwe_token is not None

    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()),
        leeway=5,
    )
    encrypted_jwt = jwe.decrypt_compact(jwe_token, app.config["PIPELINE_SERVER_PRIVATE"]).plaintext
    decrypted_jwt = jwt.decode(encrypted_jwt, app.config["PIPELINE_REPOSITORY_JWK"]["public_key"])
    claims_requests.validate_exp(value=decrypted_jwt.claims.pop("exp"))
    claims_requests.validate_iat(value=decrypted_jwt.claims.pop("iat"))

    claims = decrypted_jwt.claims

    assert claims["pipeline_steps"][0]["type"] == "add_recipient_crypt4gh"
    assert claims["pipeline_steps"][0]["arguments"]["source_url"]
    assert (
        claims["pipeline_steps"][0]["arguments"]["recipient_pub"] == "super_duper_non_secret_public_key_value"
    )  # defined in fixture
    assert claims["source_url"]


def test_pipeline_validate_crypt4gh_step(
    app, logged_client, user_with_public_key_in_profile, published_record_with_files, location, search_clear
):
    # since in tests permissions are not enforced we can use any user
    client = logged_client(user_with_public_key_in_profile)

    response = client.get(
        f"/modela/{published_record_with_files['id']}/files/blah.c4gh/pipeline?pipeline=validate_crypt4gh"
    )

    assert response.status_code == 302

    jwe_token = current_cache.cache._read_client.get(response.location.rsplit("/", 1)[-1]).decode("utf-8")  # noqa: SLF001
    assert jwe_token is not None

    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()),
        leeway=5,
    )
    encrypted_jwt = jwe.decrypt_compact(jwe_token, app.config["PIPELINE_SERVER_PRIVATE"]).plaintext
    decrypted_jwt = jwt.decode(encrypted_jwt, app.config["PIPELINE_REPOSITORY_JWK"]["public_key"])
    claims_requests.validate_exp(value=decrypted_jwt.claims.pop("exp"))
    claims_requests.validate_iat(value=decrypted_jwt.claims.pop("iat"))

    claims = decrypted_jwt.claims

    assert claims["pipeline_steps"][0]["type"] == "validate_crypt4gh"
    assert claims["pipeline_steps"][0]["arguments"]["source_url"]
    assert claims["source_url"]


def test_pipeline_decrypt_crypt4gh_step(
    app, logged_client, user_with_public_key_in_profile, published_record_with_files, location, search_clear
):
    # since in tests permissions are not enforced we can use any user
    client = logged_client(user_with_public_key_in_profile)

    response = client.get(
        f"/modela/{published_record_with_files['id']}/files/blah.c4gh/pipeline?pipeline=decrypt_crypt4gh"
    )

    assert response.status_code == 302

    jwe_token = current_cache.cache._read_client.get(response.location.rsplit("/", 1)[-1]).decode("utf-8")  # noqa: SLF001
    assert jwe_token is not None

    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.UTC).timestamp()),
        leeway=5,
    )
    encrypted_jwt = jwe.decrypt_compact(jwe_token, app.config["PIPELINE_SERVER_PRIVATE"]).plaintext
    decrypted_jwt = jwt.decode(encrypted_jwt, app.config["PIPELINE_REPOSITORY_JWK"]["public_key"])
    claims_requests.validate_exp(value=decrypted_jwt.claims.pop("exp"))
    claims_requests.validate_iat(value=decrypted_jwt.claims.pop("iat"))

    claims = decrypted_jwt.claims

    assert claims["pipeline_steps"][0]["type"] == "decrypt_crypt4gh"
    assert claims["pipeline_steps"][0]["arguments"]["source_url"]
    assert claims["source_url"]
