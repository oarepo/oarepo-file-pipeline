def create_pipeline_file_blueprint(app):
    blueprint = app.extensions[
        "oarepo-file-pipeline"
    ].pipeline_file_resource.as_blueprint()
    return blueprint
