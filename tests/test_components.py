#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-file-pipeline (see https://github.com/oarepo/oarepo-file-pipeline).
#
# oarepo-file-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

from io import BytesIO
from pathlib import Path


def test_change_transfer_type_component(app, db, users, model_a, location, search_clear):
    user = users[0]

    with Path("tests/blah.c4gh").open("rb") as f:
        c4gh = f.read()
    with Path("tests/blah.zip").open("rb") as f:
        z = f.read()
    with Path("tests/blah.jpg").open("rb") as f:
        jpg = f.read()

    records_service = model_a.proxies.current_service

    rec = records_service.create(user.identity, {"metadata": {"title": "blah"}, "files": {"enabled": True}})
    record_id = rec["id"]

    file_service = records_service._draft_files  # noqa: SLF001

    rec = file_service.init_files(
        user.identity,
        record_id,
        [
            {"key": "blah.txt"},
            {"key": "blah.zip"},
            {"key": "blah.jpg"},
            {"key": "blah.c4gh"},
        ],
    )
    assert all(v.transfer.transfer_type == "L" for v in rec._record.files._entries.values())  # noqa: SLF001

    file_service.set_file_content(user.identity, record_id, "blah.txt", BytesIO(b"blahblahblah"))
    file_service.set_file_content(user.identity, record_id, "blah.zip", BytesIO(z))
    file_service.set_file_content(user.identity, record_id, "blah.jpg", BytesIO(jpg))
    rec = file_service.set_file_content(user.identity, record_id, "blah.c4gh", BytesIO(c4gh))
    assert all(v.transfer.transfer_type == "L" for v in rec._record.files._entries.values())  # noqa: SLF001

    result = file_service.commit_file(user.identity, record_id, "blah.txt")
    assert result._record.files["blah.txt"].transfer.transfer_type == "L"  # noqa: SLF001
    result = file_service.commit_file(user.identity, record_id, "blah.zip")
    assert result._record.files["blah.zip"].transfer.transfer_type == "P"  # noqa: SLF001
    result = file_service.commit_file(user.identity, record_id, "blah.jpg")
    assert result._record.files["blah.jpg"].transfer.transfer_type == "P"  # noqa: SLF001
    result = file_service.commit_file(user.identity, record_id, "blah.c4gh")
    assert result._record.files["blah.c4gh"].transfer.transfer_type == "P"  # noqa: SLF001
