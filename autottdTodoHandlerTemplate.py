import os
import boto3
import urllib.parse

AMI = os.environ["AMI"]
INSTANCE_TYPE = os.environ["INSTANCE_TYPE"]
KEY_NAME = os.environ["KEY_NAME"]
SECURITY_GROUP_ID = os.environ["SECURITY_GROUP_ID"]
IAM_INSTANCE_PROFILE_ARN = os.environ["IAM_INSTANCE_PROFILE_ARN"]

ec2 = boto3.resource("ec2")
s3 = boto3.client("s3")

logonScript = """<powershell>
REPLACE_LOGON
</powershell>
"""


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    hash = key.replace("todo/", "").replace(".exe", "")
    children = False  # TODO

    # Replace data in logon script template
    userdata = (
        logonScript.replace("REPLACE_HASH", hash)
        .replace("REPLACE_BUCKET", bucket)
        .replace("REPLACE_CHILDREN", str(children))
    )

    try:
        instance = ec2.create_instances(
            ImageId=AMI,
            InstanceType=INSTANCE_TYPE,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": hash},
                        {"Key": "autottd", "Value": ""},
                    ],
                }
            ],
            KeyName=KEY_NAME,
            IamInstanceProfile={"Arn": IAM_INSTANCE_PROFILE_ARN},
            SecurityGroupIds=[SECURITY_GROUP_ID],
            UserData=userdata,
            MaxCount=1,
            MinCount=1,
        )

        assert len(instance) == 1
        return instance[0].id

    except Exception as e:
        print(e)
        return 1
