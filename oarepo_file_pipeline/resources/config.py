from invenio_records_resources.resources.files.config import FileResourceConfig


class PipelineFileResourceConfig(FileResourceConfig):
    """Pipeline File resource config."""

    blueprint_name = "oarepo_file_pipeline"

    routes = {"read_with_pipeline": "files/<path:key>/pipeline"}
