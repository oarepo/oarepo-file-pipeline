import uuid
from unittest.mock import patch, Mock

import pytest

from oarepo_file_pipeline.pipeline_generators.zip import ZipGenerator
from oarepo_file_pipeline.pipeline_generators.image import ImageGenerator
from oarepo_file_pipeline.pipeline_generators.crypt4gh import Crypt4GHGenerator



class MockResponse:
    def __init__(self):
        self.headers = {"Location": "google.com"}

def test_zip_generator_can_handle(app, client, users, record_with_files, location, search_clear):
    zip_generator = ZipGenerator()

    assert zip_generator.can_handle(users.identity, record_with_files[1].files['blah.zip']) == True
    assert zip_generator.can_handle(users.identity, record_with_files[1].files['blah.txt']) == False
    assert zip_generator.can_handle(users.identity, record_with_files[1].files['blah.jpeg']) == False

def test_zip_generator_get_pipeline_success(app, client, users, record_with_files, location, search_clear):
    zip_generator = ZipGenerator()

    pipeline = zip_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.zip'],
                                          "some_url",
                                          "preview_zip",
                                          {})

    assert pipeline == [
                {
                    'type': 'preview_zip',
                    'arguments': {
                        'source_url': 'some_url',
                    }
                 },
            ]

    pipeline = zip_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.zip'],
                                          "some_url",
                                          "extract_zip",
                                          {"directory_or_file_name": "some_dir"})

    assert pipeline == [
                {
                    'type': 'extract_zip',
                    'arguments': {
                        'source_url': 'some_url',
                        'directory_or_file_name': 'some_dir',
                    }
                 },
            ]

def test_zip_generator_get_pipeline_no_file_url(app, client, users, record_with_files, location, search_clear):
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):
        zip_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.zip'],
                                          "",
                                          "preview_zip",
                                          {})

def test_zip_generator_get_pipeline_can_not_handle(app, client, users, record_with_files, location, search_clear):
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):
        zip_generator.get_pipeline(users.identity,
                                   record_with_files[1].files['blah.txt'],
                                   "123.com",
                                   "preview_zip",
                                   {})

def test_zip_generator_get_pipeline_no_arguments(app, client, users, record_with_files, location, search_clear):
    zip_generator = ZipGenerator()
    with pytest.raises(ValueError):
        zip_generator.get_pipeline(users.identity,
                                   record_with_files[1].files['blah.zip'],
                                   "123.com",
                                   "extract_zip",
                                   {})

def test_image_generator_can_handle(app, client, users, record_with_files, location, search_clear):
    image_generator = ImageGenerator()

    assert image_generator.can_handle(users.identity, record_with_files[1].files['blah.zip']) == False
    assert image_generator.can_handle(users.identity, record_with_files[1].files['blah.txt']) == False
    assert image_generator.can_handle(users.identity, record_with_files[1].files['blah.jpeg']) == True
    assert image_generator.can_handle(users.identity, record_with_files[1].files['blah.png']) == True

def test_image_generator_get_pipeline_success(app, client, users, record_with_files, location, search_clear):
    image_generator = ImageGenerator()

    pipeline = image_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.png'],
                                          "some_url",
                                          "preview_picture",
                                          {})

    assert pipeline == [
                {
                    'type': 'preview_picture',
                    'arguments': {
                        'source_url': 'some_url',
                        'max_height': 10000,
                        'max_width': 10000
                    }
                 },
            ]

def test_image_generator_get_pipeline_no_file_url(app, client, users, record_with_files, location, search_clear):
    image_generator = ImageGenerator()
    with pytest.raises(ValueError):
        image_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.jpeg'],
                                          "",
                                          "preview_picture",
                                          {})

def test_image_generator_get_pipeline_can_not_handle(app, client, users, record_with_files, location, search_clear):
    image_generator = ImageGenerator()
    with pytest.raises(ValueError):
        image_generator.get_pipeline(users.identity,
                                   record_with_files[1].files['blah.txt'],
                                   "123.com",
                                   "preview_picture",
                                   {})

def test_image_generator_get_pipeline_no_arguments(app, client, users, record_with_files, location, search_clear):
    assert True # TODO change to real to test with real parameters

def test_crypt4gh_generator_can_handle(app, client, users, record_with_files, location, search_clear):
    cryp4gh_generator = Crypt4GHGenerator()

    assert cryp4gh_generator.can_handle(users.identity, record_with_files[1].files['blah.zip']) == False
    assert cryp4gh_generator.can_handle(users.identity, record_with_files[1].files['blah.txt']) == False
    assert cryp4gh_generator.can_handle(users.identity, record_with_files[1].files['blah.jpeg']) == False
    assert cryp4gh_generator.can_handle(users.identity, record_with_files[1].files['blah.c4gh']) == True


def test_crypt4gh_generator_get_pipeline_success(app, client, users, record_with_files, location, search_clear):
    crypt4gh_generator = Crypt4GHGenerator()

    pipeline = crypt4gh_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.c4gh'],
                                          "some_url",
                                          "crypt4gh",
                                          {'recipient_pub':"secret_public_key"})

    assert pipeline == [
                {
                    'type': 'crypt4gh',
                    'arguments': {
                        'source_url': 'some_url',
                        'recipient_pub': 'secret_public_key',
                    }
                 },
            ]


def test_crypt4gh_generator_get_pipeline_no_file_url(app, client, users, record_with_files, location, search_clear):
    crypt4gh_generator = Crypt4GHGenerator()
    with pytest.raises(ValueError):
        crypt4gh_generator.get_pipeline(users.identity,
                                          record_with_files[1].files['blah.c4gh'],
                                          "",
                                          "crypt4gh",
                                          {})

def test_crypt4gh_generator_get_pipeline_can_not_handle(app, client, users, record_with_files, location, search_clear):
    crypt4gh_generator = Crypt4GHGenerator()
    with pytest.raises(ValueError):
        crypt4gh_generator.get_pipeline(users.identity,
                                   record_with_files[1].files['blah.txt'],
                                   "123.com",
                                   "crypt4gh",
                                   {})



# file_service._get_record(id_=record_with_files['id'],identity=users.identity, action="read_files", file_key='blah.zip')
# client.get(f"/records2/{record_with_files['id']}/files

