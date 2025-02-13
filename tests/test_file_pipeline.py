import datetime
import time
import uuid
from unittest.mock import patch, Mock

from flask import Response

from oarepo_file_pipeline.services.service import PipelineFileService
from joserfc import jwt, jwe
from invenio_cache import current_cache

def test_extension_initialization(app):
    assert "oarepo-file-pipeline" in app.extensions

class MockResponse:
    def __init__(self):
        self.headers = {"Location": "google.com"}

def test_create_signed_payload_valid(app):
    service = PipelineFileService(app.config)
    signing_algorithm = app.config['PIPELINE_SIGNING_ALGORITHM']
    private_key = app.config['PIPELINE_REPOSITORY_JWK']['private_key']
    public_key = app.config['PIPELINE_REPOSITORY_JWK']['public_key']
    payload = {
        "key" : "value"
    }
    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()), leeway=5
    )
    signed_payload = service._create_signed_payload(payload, signing_algorithm, private_key)

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)
    claims_requests.validate_exp(value=decoded_jwt.claims.pop('exp'))
    claims_requests.validate_iat(value=decoded_jwt.claims.pop('iat'))
    assert {"key" : "value"} == decoded_jwt.claims

def test_create_signed_payload_expired(app, search_clear):
    service = PipelineFileService(app.config)
    signing_algorithm = app.config['PIPELINE_SIGNING_ALGORITHM']
    private_key = app.config['PIPELINE_REPOSITORY_JWK']['private_key']
    public_key = app.config['PIPELINE_REPOSITORY_JWK']['public_key']
    payload = {
        "key" : "value"
    }
    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()) + 306, leeway=5
    )
    signed_payload = service._create_signed_payload(payload, signing_algorithm, private_key)

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)
    try:
        claims_requests.validate_exp(value=decoded_jwt.claims.pop('exp'))
        claims_requests.validate_iat(value=decoded_jwt.claims.pop('iat'))
        assert False
    except Exception as e:
        print(e)
        assert True

def test_create_signed_payload_issued_in_the_future(app, search_clear):
    service = PipelineFileService(app.config)
    signing_algorithm = app.config['PIPELINE_SIGNING_ALGORITHM']
    private_key = app.config['PIPELINE_REPOSITORY_JWK']['private_key']
    public_key = app.config['PIPELINE_REPOSITORY_JWK']['public_key']
    payload = {
        "key" : "value"
    }
    claims_requests = jwt.JWTClaimsRegistry(
        now=int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())-5, leeway=5
    )
    signed_payload = service._create_signed_payload(payload, signing_algorithm, private_key)

    assert signed_payload is not None
    decoded_jwt = jwt.decode(signed_payload, public_key)

    try:
        claims_requests.validate_exp(value=decoded_jwt.claims.pop('exp'))
        claims_requests.validate_iat(value=decoded_jwt.claims.pop('iat'))
        assert False
    except Exception as e:
        print(e)
        assert True

def test_create_signed_payload_non_existing_singing_algorithm(app):
    service = PipelineFileService(app.config)
    signing_algorithm = None
    private_key = app.config['PIPELINE_REPOSITORY_JWK']['private_key']

    payload = {
        "key" : "value"
    }
    signed_payload = None
    try:
        signed_payload = service._create_signed_payload(payload, signing_algorithm, private_key)
        assert False
    except ValueError as e:
        assert True

def test_create_signed_payload_invalid_singing_algorithm(app):
    service = PipelineFileService(app.config)
    signing_algorithm = "RSA"
    private_key = app.config['PIPELINE_REPOSITORY_JWK']['private_key']

    payload = {
        "key" : "value"
    }
    signed_payload = None
    try:
        signed_payload = service._create_signed_payload(payload, signing_algorithm, private_key)
        assert False
    except ValueError as e:
        assert True

def test_pipeline(app, client, users, record_with_files, location, search_clear):
    unique_uuid = str(uuid.uuid4())

    with patch("invenio_records_resources.services.files.results.FileItem.send_file") as mock_send_file, \
         patch("uuid.uuid4", return_value=uuid.UUID(unique_uuid)) as mock_uuid4:
        mock_send_file.return_value = MockResponse()

        print(record_with_files[0])
        print(record_with_files[0]['id'])

        response = client.get(f"/records2/{record_with_files[0]['id']}/files/blah.zip/pipeline?pipeline=preview_zip")
        location = response.location
        assert response.location == f"{app.config['PIPELINE_REDIRECT_URL']}/{unique_uuid}"
        assert response.status_code == 302
        jwe_token =  current_cache.cache._read_client.get(unique_uuid).decode('utf-8')
        assert jwe_token is not None

        claims_requests = jwt.JWTClaimsRegistry(
            now=int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()), leeway=5
        )
        encrypted_jwt = jwe.decrypt_compact(jwe_token, app.config["PIPELINE_SERVER_PRIVATE"]).plaintext
        decrypted_jwt = jwt.decode(encrypted_jwt, app.config['PIPELINE_REPOSITORY_JWK']['public_key'])
        claims_requests.validate_exp(value=decrypted_jwt.claims.pop('exp'))
        claims_requests.validate_iat(value=decrypted_jwt.claims.pop('iat'))

        print(decrypted_jwt.claims)
        assert decrypted_jwt.claims == {
            "pipeline_steps" : [
            {
                'type' : "preview_zip",
                "arguments": {
                     "source_url": "google.com",
                }
            },
            ],
            "source_url": "google.com",
        }

def test_read_with_pipeline_no_source_url(app, client, record_with_files, location, search_clear,):
    try:
        client.get(f"/records2/{record_with_files[0]['id']}/files/blah.txt/pipeline")
        assert False
    except ValueError as e:
        assert True


