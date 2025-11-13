from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_records_resources.services.files.generators import IfTransferType

from oarepo_file_pipeline.config import RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE


class PipelineFilePermissionPolicy(RDMRecordPermissionPolicy):
    can_draft_create_files = [
        *RDMRecordPermissionPolicy.can_draft_create_files,
        IfTransferType(
            RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
            RDMRecordPermissionPolicy.can_review,
        ),
    ]

    can_draft_set_content_files = [
        *RDMRecordPermissionPolicy.can_draft_set_content_files,
        IfTransferType(
            RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
            RDMRecordPermissionPolicy.can_review,
        ),
    ]

    can_draft_commit_files = [
        *RDMRecordPermissionPolicy.can_draft_commit_files,
        IfTransferType(
            RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
            RDMRecordPermissionPolicy.can_review,
        ),
    ]

    can_draft_get_content_files = [
        *RDMRecordPermissionPolicy.can_draft_get_content_files,
        IfTransferType(
            RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
            RDMRecordPermissionPolicy.can_draft_read_files,
        ),
    ]

    can_get_content_files = [
        *RDMRecordPermissionPolicy.can_get_content_files,
        IfTransferType(
            RECORDS_RESOURCES_DEFAULT_TRANSFER_TYPE,
            RDMRecordPermissionPolicy.can_read_files,
        ),
    ]
