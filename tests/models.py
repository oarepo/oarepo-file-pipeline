#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-rdm (see https://github.com/oarepo/oarepo-rdm).
#
# oarepo-rdm is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from __future__ import annotations

from typing import ClassVar

from flask import Blueprint
from invenio_records_permissions.generators import AnyUser, Generator
from oarepo_model.api import model
from oarepo_model.customizations import (
    SetPermissionPolicy,
)
from oarepo_model.presets.drafts import drafts_preset
from oarepo_model.presets.records_resources import records_resources_preset
from oarepo_runtime.services.config import EveryonePermissionPolicy

from oarepo_file_pipeline.model.presets.pipeline import pipeline_preset


class PermissionPolicyWithModelAPermission(EveryonePermissionPolicy):
    """Permission policy that adds permissions for testing."""

    can_draft_create_files: ClassVar[list[Generator]] = [
        AnyUser(),
    ]

    can_draft_set_content_files: ClassVar[list[Generator]] = [
        AnyUser(),
    ]

    can_draft_commit_files: ClassVar[list[Generator]] = [
        AnyUser(),
    ]

    can_draft_get_content_files: ClassVar[list[Generator]] = [
        AnyUser(),
    ]

    get_content_files: ClassVar[list[Generator]] = [
        AnyUser(),
    ]


modela = model(
    "modela",
    version="1.0.0",
    presets=[
        records_resources_preset,
        drafts_preset,
        pipeline_preset,
    ],
    configuration={"ui_blueprint_name": "modela_ui"},
    types=[
        {
            "Metadata": {
                "properties": {
                    "title": {"type": "fulltext+keyword"},
                    "adescription": {"type": "keyword"},
                },
            },
        }
    ],
    metadata_type="Metadata",
    customizations=[SetPermissionPolicy(PermissionPolicyWithModelAPermission)],
)
modela.register()


def create_modela_ui_blueprint(app):
    bp = Blueprint("modela_ui", __name__)

    # mock UI resource
    @bp.route("/modela_ui/preview/<pid_value>", methods=["GET"])
    def preview(pid_value: str) -> str:
        return "preview ok"

    @bp.route("/modela_ui/record_detail/<pid_value>", methods=["GET"])
    def record_detail(pid_value: str) -> str:
        return "preview ok"

    @bp.route("/modela_ui/record_latest/<pid_value>", methods=["GET"])
    def record_latest(pid_value: str) -> str:
        return "latest ok"

    @bp.route("/modela_ui/search", methods=["GET"])
    def search() -> str:
        return "search ok"

    @bp.route("/modela_ui/deposit_edit/<pid_value>", methods=["GET"])
    def deposit_edit(pid_value: str) -> str:
        return "deposit_edit ok"

    return bp
