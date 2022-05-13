import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAZPSHLLK22L2U25OG'
SECRET_KEY = '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'


def upload_to_aws(videoId):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(videoId + "_short.mp4", 'bitirmebucket', videoId + ".mp4")
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
