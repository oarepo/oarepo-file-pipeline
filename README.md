# OARepoFilePipeline

Flask extension for OARepoFilePipeline. 

### Setup

In app configuration define:

1) This repository RSA key pair (public_key, private_key)
2) PIPELINE_FILE_SERVER RSA public key
3) PIPELINE_FILE_SERVER URL

Optionally you can change:
1) Signing algorithm for the JWT
2) Encryption algorithm and method for the JWE
```
"""Private and public RSA keys for singing JWT token"""
PIPELINE_REPOSITORY_JWK =  {
    "private_key": "",
    "public_key": ""
}

"""Public RSA key of FILE_PIPELINE_SERVER to encrypt JWE token with payload"""
PIPELINE_JWK =  {
     "public_key": "",
}

"""FILE_PIPELINE_SERVER redirect url"""
PIPELINE_REDIRECT_URL = ''

"""Default algorithms"""
PIPELINE_SIGNING_ALGORITHM = "RS256"
PIPELINE_ENCRYPTION_ALGORITHM = "RSA-OAEP"
PIPELINE_ENCRYPTION_METHOD = "A256GCM"
```

### Usage

Endpoint initiating pipeline is `.../<id_>/<file_key>/pipeline`. It accepts optional query parameters, such as pipeline, 
for suggested processing steps (preview_zip, preview_picture etc.). Then it redirect the client to a dedicated server 