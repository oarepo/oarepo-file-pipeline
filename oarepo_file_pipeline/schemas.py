#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Profile schema adding public_key field."""

from __future__ import annotations

from invenio_accounts.profiles.schemas import UserProfileSchema
from marshmallow import fields


class CustomUserProfileSchema(UserProfileSchema):
    """Custom user profile schema with additional fields."""

    public_key = fields.String(required=False)
