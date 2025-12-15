#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-file-pipeline (see https://github.com/oarepo/oarepo-file-pipeline).
#
# oarepo-file-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

import logging
from pathlib import Path

import pytest
from invenio_records_resources.config import RECORDS_RESOURCES_TRANSFERS
from joserfc.jwk import RSAKey

from oarepo_file_pipeline import config

pytest_plugins = [
    "pytest_oarepo.records",
    "pytest_oarepo.fixtures",
    "pytest_oarepo.users",
    "pytest_oarepo.files",
]


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


repo_private_key = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2CUaKEVGX5wPj
cAqwoQCDfS9VLxvlrNlUtP+bIQ3J77VGoGb9UXhgH+AjDAE+YBDFIv9Jsi7FwQQO
6C6qSkAGuoh/Lr8yKZ5At97jHPWyY6urg0T4GRp2WlnbgrByW5s6yAT+Gcb9ciT5
YSVVvM7d/NrvuchuJ4Zl7Pl/ru/quCdYgw9agLs/6xFQ3pHlN32MUEorx6mcomUP
a69dLpiM9KZTTlHSYm8CXzPdMos3uXq+5ED+u0sr8h+YVhSJWulB2G3vga3DNKjc
pK9QCm+BADYL1C4P6BZbZbt1+w4ukaBYX2/cQwK9FZQezt0YcjFUNPk2lm0lNFUn
mfTha6C3AgMBAAECggEAECHiTnoacQvYHF/hkqWyFfUSLMpv/nrDB+7CeE0Fm8/S
kN/GQMznjh1FD9YQhiadVds0JKPV4VCpu2h4Oj86TV5ammraJufpTnL9HcODQrvy
itCnXBVdcv+u1vVODdRwfVUcnChMqkljXXZuiJqi+qld/cDJMnnuPzoxIk+uk254
KMFV9bmcM5npxH/B1383E+rU/v/YW35ms8MZuleo32xMKY5inHasvpMCIHccvrvi
+NIOE66FSMOJPqdJVexkV9Kmi3/29py0jtjt6XqrJuD+pYUQIrOYSSeCx6F8GqDe
XR/rEVSTcCcgipz71vdSzAUK2LFUhzPaipwjkUeWgQKBgQDqrUKtLnmzwTSRZoPe
USAlcJaKfi3pOAyko9joCyEfwH8grQNG5saBMitO3ClmzlxL6qgqzMXM+xyJ8KFx
L0HXADxfOEZGOCRx/bzDaW2YbPQYAjQVOo3wcGkkcJpdwDSL/hpWfNgJGzKlJfO3
2IPEWHzO5f6mhjcESUP6R0InXQKBgQDGk49tJP57RrrY2E26T6MLGYaUObqSwhVN
Xyb9B/Ee6/d60CRseD8jLgJ/TBaqJfx9m5grGWz8z9QV6UTb5MbPx0u7lGN+hquU
KFxtjskQ1tyfg3emPkSBvdxUD8Sq9ebot2/B3mAvuhqdyx/5WeK2LiaVnDixFoKH
PT9947hLIwKBgHzueeWKLV4Fh/+z7JXI6G0mD+5wl+5lWU24sDtv2VV2+/agRHNV
Xe3fkHCuAhhp2XbM2HPYiaDDOgExKjEAMHPN+1XRto+hSb2pj/kTwjV4I0Y4vhNj
FbcfkMnGbFdmgFLalpjeY4ANi5uhpaqEyDkZxm+6vyNVpipQ+rBdiRk9AoGAQcct
cn0XoyRJznzQOpAYtRuOfdklmWma/tcvJhAUaibGArOh7SBj4bZi82Hz/Aa7Paxl
2pkAhjodyehMe/6rcLZWutsrngTkHx7DhzMOHXre+CPnZXUo4kVPD7VtcygjhiEF
bxXHjOe721smy0VgGPLuqw5lpRuMv1mlh4EAUjsCgYEAmGKkvoV2k0P/X1IxiA/d
CP9pQ3A7d8jXIq9F9tbFIg90FTPvpCSUPuPDafTnV6ODJ77Zp3GMIGQld19ausKF
JLtzz8CQoxhIp5d0UlL60DfDiA2pXr2NRx50etOVrwIkvv+5tSvbefjsoyaUQWhD
5h6tAQKsmxV7MrJLU7qnV24=
-----END PRIVATE KEY-----
"""

repo_public_key = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtglGihFRl+cD43AKsKEA
g30vVS8b5azZVLT/myENye+1RqBm/VF4YB/gIwwBPmAQxSL/SbIuxcEEDuguqkpA
BrqIfy6/MimeQLfe4xz1smOrq4NE+BkadlpZ24KwclubOsgE/hnG/XIk+WElVbzO
3fza77nIbieGZez5f67v6rgnWIMPWoC7P+sRUN6R5Td9jFBKK8epnKJlD2uvXS6Y
jPSmU05R0mJvAl8z3TKLN7l6vuRA/rtLK/IfmFYUiVrpQdht74GtwzSo3KSvUApv
gQA2C9QuD+gWW2W7dfsOLpGgWF9v3EMCvRWUHs7dGHIxVDT5NpZtJTRVJ5n04Wug
twIDAQAB
-----END PUBLIC KEY-----
"""

server_public_key = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs8vm6OFyOpPyP6nxQwNB
pX19IKf5SMNq4FEADK/zWobLkfEOlVMhQ77/7LsA822PO/K3LHtoA42zz+CXmDir
hLu6R1j1i8/C8Z98bJ9pVigkMhD0F8B6L04FoRnN8ycj3FYfmxu3QRqjg+nF+5cN
B8Do0vVFw+IOcca9LJbqHNj59CQmJpuRO5T4l0mNmGjdTnCyG/YQdLlV1hvw85Zp
UCcUbrlVdC9b3wJ1IhgZ6RCEE4sjcuY2XMsV4bf+9uwKHa6OVwNXdX6hLVOvCbBW
GrqMHOhsJ8Sf7j1sL8LeplSjiGmqJfl1tLR7M4zr72Vt1JoYDxMWWfaZs0pwVT8o
ywIDAQAB
-----END PUBLIC KEY-----
"""

server_private_key = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzy+bo4XI6k/I/
qfFDA0GlfX0gp/lIw2rgUQAMr/NahsuR8Q6VUyFDvv/suwDzbY878rcse2gDjbPP
4JeYOKuEu7pHWPWLz8Lxn3xsn2lWKCQyEPQXwHovTgWhGc3zJyPcVh+bG7dBGqOD
6cX7lw0HwOjS9UXD4g5xxr0sluoc2Pn0JCYmm5E7lPiXSY2YaN1OcLIb9hB0uVXW
G/DzlmlQJxRuuVV0L1vfAnUiGBnpEIQTiyNy5jZcyxXht/727Aodro5XA1d1fqEt
U68JsFYauowc6GwnxJ/uPWwvwt6mVKOIaaol+XW0tHszjOvvZW3UmhgPExZZ9pmz
SnBVPyjLAgMBAAECggEAUImjLykhnmy8JFlvGXoBc2xxWunzR+1FWCLgd05vn1rn
IEIPKsN4kJyjjjq8M86dTRithY7n6kOUyqbLsSOdbREcYa5PG2ge5lXvCccki7Pi
dszSUjtlYAA+lEn3T5Z2QVIQyU2SembA3SugBFFGxHTctfapYBPILZ39Cla1muK0
TaV3QeAqNC/ikIa6dHzA+BsSKawczHeIA2D+9s5OsASuBbukn9pw6yXDG8DcI73Z
uhbsnoZEu4Ml0HegzObvozqb6EZwlwMQbVarDuVA3Jop2X6ytgyUd6aX0D0jA9MW
0rqlM3+x8TRtgkNm1uzB7w5vRwNLSIjH1ahMWm8ZYQKBgQDeM6Ua7WRHc+SY+ctN
TXbjCpRYIqdSRbKv6++m4fikZqkTf6Fb+hWh8T3jQpo8lAjQt+mLhtxiXNI3JTQu
69ksdKRBV9pvBsWTcFn4Jlu1fCQLk2Hf98En/dX5eFyV5fWWfJm3uIZye6akJSfq
rRmzyobJZbFj2BDU+vup3jP+4QKBgQDPJQf/kw70qn8nSEQrT0OsxubRZJ9jqBwp
VgosFMVMexAQvYweQ5EmS9ZiIhSvQLP0ZSTTIAsbl4DC535qsdX/Sf6eXh4OfRsV
m/NU/PCLsRr8qolDIEH0TGmQKGuoeJoDNyp8q6lRvfnFyKmrGCdYtDuryGHJSVu9
LEmlx2t5KwKBgFd5bV4UZo3aifvPGsHr5QmseInZ2pUA6z9mWooQG5pc7+LFM/jJ
kwqVtg9pgN6oSHAidsZ+6POwJvGeq9Rs9KoToTY4J73dpJpOeJzAPQpNPMNx2e4Z
0uizfTEguRIp3WzI0JsLAaLAGvIzzmsMijnFWRqf9h2gScAOrlRJLZ8BAoGBAMtS
xe8PIfb2A6lDPeZk/0BwW8/cvLbNJBdO5N0v5hmUEcjcxNRP7gFxHxVj7nm3QOv6
+5JgOYbzxueI4oVH2Y2jy9EXANmn4xXq5YXeYR480QiBPAovd42cE2H0yveqqUHO
vF1zAdfCaZDBzgiqxLRE9O1A2vsAjpO5DPE0NUHRAoGAP0siJ4Wk2XDCFcNM3fzK
FXcK3FiHdSWkTelbFU60kOpXrEpHsWShpVM0d/LtbmYPB4gtFfXCjMHf80F/PZrr
Zt4sAc6TAS+xNfT7djzy8N9tvjd1220orFLZUr1VC+m0+jfPM7dzJ9MVn3386Skm
oXMkXQNjJhyifeoAmStK3G4=
-----END PRIVATE KEY-----
"""


@pytest.fixture(scope="session")
def model_types():
    """Model types fixture."""
    # Define the model types used in the tests
    return {
        "Metadata": {
            "properties": {
                "title": {"type": "keyword", "required": True},
            }
        }
    }


@pytest.fixture(scope="session")
def model_a(model_types):
    from .models import modela

    return modela


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["JSONSCHEMAS_HOST"] = "localhost"
    app_config["RECORDS_REFRESOLVER_CLS"] = "invenio_records.resolver.InvenioRefResolver"
    app_config["RECORDS_REFRESOLVER_STORE"] = "invenio_jsonschemas.proxies.current_refresolver_store"

    app_config["CACHE_TYPE"] = "redis"

    app_config["PIPELINE_REPOSITORY_JWK"] = {
        "private_key": RSAKey.import_key(repo_private_key),
        "public_key": RSAKey.import_key(repo_public_key),
    }

    """Public RSA key of FILE_PIPELINE_SERVER to encrypt JWE token with payload"""
    app_config["PIPELINE_JWK"] = {
        "public_key": RSAKey.import_key(server_public_key),
    }

    """FILE_PIPELINE_SERVER redirect url"""
    app_config["PIPELINE_REDIRECT_URL"] = "http://localhost:5555/pipeline"

    app_config["PIPELINE_SIGNING_ALGORITHM"] = "RS256"
    app_config["PIPELINE_ENCRYPTION_ALGORITHM"] = "RSA-OAEP"
    app_config["PIPELINE_ENCRYPTION_METHOD"] = "A256GCM"

    # Only done for testing, should not be here in the first place
    app_config["PIPELINE_SERVER_PRIVATE"] = RSAKey.import_key(server_private_key)

    app_config["RECORDS_RESOURCES_TRANSFERS"] = [
        *RECORDS_RESOURCES_TRANSFERS,
        *config.RECORDS_RESOURCES_TRANSFERS,
    ]

    app_config["FILES_REST_STORAGE_FACTORY"] = "invenio_s3.s3fs_storage_factory"
    app_config["S3_ENDPOINT_URL"] = "http://localhost:9000"
    app_config["S3_ACCESS_KEY_ID"] = "invenio"
    app_config["S3_SECRET_ACCESS_KEY"] = "invenio8"  # noqa: S105
    app_config["S3_BUCKET"] = "default"

    return app_config


@pytest.fixture(scope="module")
def extra_entry_points(model_a):
    return {
        "invenio_base.apps": ["oarepo_file_pipeline = oarepo_file_pipeline.ext:OARepoFilePipeline"],
        "invenio_base.api_apps": ["oarepo_file_pipeline = oarepo_file_pipeline.ext:OARepoFilePipeline"],
        "oarepo.file.pipelines": [
            "zip_pipelines = oarepo_file_pipeline.pipeline_generators.zip:ZipGenerator",
            "image_pipelines = oarepo_file_pipeline.pipeline_generators.image:ImageGenerator"
            "c4gh_pipeline = oarepo_file_pipeline.pipeline_generators.crypt4gh:Crypt4GHGenerator",
        ],
        "invenio_base.blueprints": [
            "invenio_app_rdm_records = tests.models:create_app_rdm_blueprint",
            "modela_ui = tests.models:create_modela_ui_blueprint",
        ],
    }


@pytest.fixture
def draft_record_with_files(app, db, users, model_a):
    user = users[0]

    with Path("tests/blah.c4gh").open("rb") as f:
        c4gh = f.read()
    with Path("tests/blah.zip").open("rb") as f:
        z = f.read()
    with Path("tests/blah.jpg").open("rb") as f:
        jpg = f.read()
    with Path("tests/blah.png").open("rb") as f:
        png = f.read()

    records_service = model_a.proxies.current_service

    rec = records_service.create(user.identity, {"metadata": {"title": "blah"}, "files": {"enabled": True}})

    file_service = records_service._draft_files  # noqa: SLF001

    file_service.init_files(
        user.identity,
        rec["id"],
        [
            {"key": "blah.txt"},
            {"key": "blah.zip"},
            {"key": "blah.jpg"},
            {"key": "blah.png"},
            {"key": "blah.c4gh"},
        ],
    )

    from io import BytesIO

    file_service.set_file_content(user.identity, rec["id"], "blah.txt", BytesIO(b"blahblahblah"))
    file_service.set_file_content(user.identity, rec["id"], "blah.zip", BytesIO(z))
    file_service.set_file_content(user.identity, rec["id"], "blah.jpg", BytesIO(jpg))
    file_service.set_file_content(user.identity, rec["id"], "blah.png", BytesIO(png))
    file_service.set_file_content(user.identity, rec["id"], "blah.c4gh", BytesIO(c4gh))

    result = file_service.commit_file(user.identity, rec["id"], "blah.txt")
    result = file_service.commit_file(user.identity, rec["id"], "blah.zip")
    result = file_service.commit_file(user.identity, rec["id"], "blah.jpg")
    result = file_service.commit_file(user.identity, rec["id"], "blah.png")
    result = file_service.commit_file(user.identity, rec["id"], "blah.c4gh")

    model_a.Draft.index.refresh()
    return result._record  # noqa: SLF001


@pytest.fixture
def published_record_with_files(app, db, users, model_a):
    user = users[0]

    with Path("tests/blah.c4gh").open("rb") as f:
        c4gh = f.read()
    with Path("tests/blah.zip").open("rb") as f:
        z = f.read()
    with Path("tests/blah.jpg").open("rb") as f:
        jpg = f.read()
    with Path("tests/blah.png").open("rb") as f:
        png = f.read()

    records_service = model_a.proxies.current_service

    rec = records_service.create(user.identity, {"metadata": {"title": "blah"}, "files": {"enabled": True}})

    file_service = records_service._draft_files  # noqa: SLF001

    file_service.init_files(
        user.identity,
        rec["id"],
        [
            {"key": "blah.txt"},
            {"key": "blah.zip"},
            {"key": "blah.jpg"},
            {"key": "blah.png"},
            {"key": "blah.c4gh"},
        ],
    )

    from io import BytesIO

    file_service.set_file_content(user.identity, rec["id"], "blah.txt", BytesIO(b"blahblahblah"))
    file_service.set_file_content(user.identity, rec["id"], "blah.zip", BytesIO(z))
    file_service.set_file_content(user.identity, rec["id"], "blah.jpg", BytesIO(jpg))
    file_service.set_file_content(user.identity, rec["id"], "blah.png", BytesIO(png))
    file_service.set_file_content(user.identity, rec["id"], "blah.c4gh", BytesIO(c4gh))

    result = file_service.commit_file(user.identity, rec["id"], "blah.txt")
    result = file_service.commit_file(user.identity, rec["id"], "blah.zip")
    result = file_service.commit_file(user.identity, rec["id"], "blah.jpg")
    result = file_service.commit_file(user.identity, rec["id"], "blah.png")
    result = file_service.commit_file(user.identity, rec["id"], "blah.c4gh")

    records_service.publish(
        user.identity,
        rec["id"],
    )

    model_a.Record.index.refresh()
    return result._record  # noqa: SLF001


@pytest.fixture(scope="module")
def location(database):
    """Create a simple default s3 location for a test."""
    from invenio_files_rest.models import Location

    location_obj = Location(name="pytest-location", uri="s3://default", default=True)

    database.session.add(location_obj)
    database.session.commit()

    return location_obj


@pytest.fixture
def user_with_public_key_in_profile(app, UserFixture, db):  # noqa: N803
    user1 = UserFixture(
        email="very_unique_not_causing_intergrity_sql_error_email@example.org",
        password="superpassword",  # noqa: S106
        active=True,
        confirmed=True,
        user_profile={
            "affiliations": "CERN",
            "public_key": "super_duper_non_secret_public_key_value",
        },
        preferences={"locale": "en", "visibility": "public"},
    )
    user1.create(app, db)
    return user1
