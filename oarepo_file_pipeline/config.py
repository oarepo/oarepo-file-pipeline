#
# Copyright (C) 2024 CESNET z.s.p.o.
#
# oarepo-file-pipeline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Default configuration."""

"""Private and public RSA keys for singing JWT token"""
#PIPELINE_REPOSITORY_JWK =  {
#    "private_key": "",
#    "public_key": ""
#}

"""Public RSA key of FILE_PIPELINE_SERVER to encrypt JWE token with payload"""
#PIPELINE_JWK =  {
#     "public_key": "",
#}

"""FILE_PIPELINE_SERVER redirect url"""
#PIPELINE_REDIRECT_URL = ''

"""Default algorithms"""
PIPELINE_SIGNING_ALGORITHM = "RS256"
PIPELINE_ENCRYPTION_ALGORITHM = "RSA-OAEP"
PIPELINE_ENCRYPTION_METHOD = "A256GCM"


RECORDS_RESOURCES_TRANSFERS = [
    "oarepo_file_pipeline.services.pipeline_transfer:PipelineTransfer",
]

RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE = "P"
