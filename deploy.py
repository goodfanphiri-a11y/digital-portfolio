import os
import mimetypes
import boto3
from pathlib import Path


# ---------------------------------------------
# AWS configuration
# ---------------------------------------------

AWS_REGION = os.environ["AWS_DEFAULT_REGION"]
S3_BUCKET = os.environ["S3_BUCKET"]


# ---------------------------------------------
# Create S3 client
# ---------------------------------------------

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# ---------------------------------------------
# Website directory
# ---------------------------------------------

WEBSITE_DIR = Path(".")


# ---------------------------------------------
# Files/directories not to deploy
# ---------------------------------------------

EXCLUDED = {
    ".git",
    ".gitignore",
    "Jenkinsfile",
    "deploy.py",
    "requirements.txt",
    "venv"
}


# ---------------------------------------------
# Upload function
# ---------------------------------------------

def upload_file(file_path):

    relative_path = file_path.as_posix()

    content_type, _ = mimetypes.guess_type(relative_path)

    if content_type is None:
        content_type = "application/octet-stream"

    print(f"Uploading: {relative_path}")

    s3.upload_file(
        str(file_path),
        S3_BUCKET,
        relative_path,
        ExtraArgs={
            "ContentType": content_type
        }
    )


# ---------------------------------------------
# Find website files
# ---------------------------------------------

for file_path in WEBSITE_DIR.rglob("*"):

    if not file_path.is_file():
        continue

    if any(
        part in EXCLUDED
        for part in file_path.parts
    ):
        continue

    upload_file(file_path)


print()
print("======================================")
print("Portfolio deployment completed")
print("======================================")
print(f"AWS Region : {AWS_REGION}")
print(f"S3 Bucket  : {S3_BUCKET}")
