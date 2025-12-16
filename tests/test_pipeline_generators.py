#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-file-pipeline (see https://github.com/oarepo/oarepo-file-pipeline).
#
# oarepo-file-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

import pytest

from oarepo_file_pipeline.pipeline_generators.crypt4gh import Crypt4GHGenerator
from oarepo_file_pipeline.pipeline_generators.image import ImageGenerator
from oarepo_file_pipeline.pipeline_generators.zip import ZipGenerator


def test_zip_generator_can_handle(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    zip_generator = ZipGenerator()

    assert zip_generator.can_handle(user.identity, draft_record_with_files.files["blah.zip"])
    assert not zip_generator.can_handle(user.identity, draft_record_with_files.files["blah.txt"])
    assert not zip_generator.can_handle(user.identity, draft_record_with_files.files["blah.jpg"])


def test_zip_generator_get_pipeline_success(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    zip_generator = ZipGenerator()

    pipeline = zip_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.zip"],
        "some_url",
        "preview_zip",
        {},
    )

    assert pipeline == [
        {
            "type": "preview_zip",
            "arguments": {
                "source_url": "some_url",
            },
        },
    ]

    pipeline = zip_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.zip"],
        "some_url",
        "extract_zip",
        {"directory_or_file_name": "some_dir"},
    )

    assert pipeline == [
        {
            "type": "extract_zip",
            "arguments": {
                "source_url": "some_url",
                "directory_or_file_name": "some_dir",
            },
        },
    ]


def test_zip_generator_get_pipeline_no_file_url(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        zip_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.zip"],
            "",
            "preview_zip",
            {},
        )


def test_zip_generator_get_pipeline_can_not_handle(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        zip_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.txt"],
            "123.com",
            "preview_zip",
            {},
        )


def test_zip_generator_get_pipeline_no_arguments(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        zip_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.zip"],
            "123.com",
            "extract_zip",
            {},
        )


def test_image_generator_can_handle(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    image_generator = ImageGenerator()

    assert not (image_generator.can_handle(user.identity, draft_record_with_files.files["blah.zip"]))
    assert not (image_generator.can_handle(user.identity, draft_record_with_files.files["blah.txt"]))
    assert image_generator.can_handle(user.identity, draft_record_with_files.files["blah.jpg"])
    assert image_generator.can_handle(user.identity, draft_record_with_files.files["blah.png"])


def test_image_generator_get_pipeline_success(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    image_generator = ImageGenerator()

    pipeline = image_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.png"],
        "some_url",
        "preview_picture",
        {},
    )

    assert pipeline == [
        {
            "type": "preview_picture",
            "arguments": {
                "source_url": "some_url",
                "max_height": 10000,
                "max_width": 10000,
            },
        },
    ]


def test_image_generator_get_pipeline_no_file_url(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    image_generator = ImageGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        image_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.jpg"],
            "",
            "preview_picture",
            {},
        )


def test_image_generator_get_pipeline_can_not_handle(
    app, client, users, draft_record_with_files, location, search_clear
):
    user = users[0]
    image_generator = ImageGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        image_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.txt"],
            "123.com",
            "preview_picture",
            {},
        )


def test_crypt4gh_generator_can_handle(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    cryp4gh_generator = Crypt4GHGenerator()

    assert not (cryp4gh_generator.can_handle(user.identity, draft_record_with_files.files["blah.zip"]))
    assert not (cryp4gh_generator.can_handle(user.identity, draft_record_with_files.files["blah.txt"]))
    assert not (cryp4gh_generator.can_handle(user.identity, draft_record_with_files.files["blah.jpg"]))
    assert cryp4gh_generator.can_handle(user.identity, draft_record_with_files.files["blah.c4gh"])


def test_crypt4gh_generator_get_pipeline_success(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    crypt4gh_generator = Crypt4GHGenerator()

    pipeline = crypt4gh_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.c4gh"],
        "some_url",
        "add_recipient_crypt4gh",
        {"recipient_pub": "secret_public_key"},
    )

    assert pipeline == [
        {
            "type": "add_recipient_crypt4gh",
            "arguments": {
                "source_url": "some_url",
                "recipient_pub": "secret_public_key",
            },
        },
    ]


def test_crypt4gh_generator_get_pipeline_no_file_url(
    app, client, users, draft_record_with_files, location, search_clear
):
    user = users[0]
    crypt4gh_generator = Crypt4GHGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        crypt4gh_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.c4gh"],
            "",
            "add_recipient_crypt4gh",
            {},
        )


def test_crypt4gh_generator_get_pipeline_can_not_handle(
    app, client, users, draft_record_with_files, location, search_clear
):
    user = users[0]
    crypt4gh_generator = Crypt4GHGenerator()
    with pytest.raises(ValueError):  # noqa: PT011
        crypt4gh_generator.get_pipeline(
            user.identity,
            draft_record_with_files.files["blah.txt"],
            "123.com",
            "add_recipient_crypt4gh",
            {},
        )


def test_crypt4gh_generator_get_pipeline_decrypt(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    crypt4gh_generator = Crypt4GHGenerator()

    pipeline = crypt4gh_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.c4gh"],
        "some_url",
        "decrypt_crypt4gh",
        {},
    )

    assert pipeline == [
        {
            "type": "decrypt_crypt4gh",
            "arguments": {
                "source_url": "some_url",
            },
        },
    ]


def test_crypt4gh_generator_get_pipeline_validate(app, client, users, draft_record_with_files, location, search_clear):
    user = users[0]
    crypt4gh_generator = Crypt4GHGenerator()

    pipeline = crypt4gh_generator.get_pipeline(
        user.identity,
        draft_record_with_files.files["blah.c4gh"],
        "some_url",
        "validate_crypt4gh",
        {},
    )

    assert pipeline == [
        {
            "type": "validate_crypt4gh",
            "arguments": {
                "source_url": "some_url",
            },
        },
    ]
