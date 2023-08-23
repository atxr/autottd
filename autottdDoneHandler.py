import os
import urllib.parse
import boto3

ec2 = boto3.resource("ec2")
client = boto3.client("ec2")
s3 = boto3.client("s3")


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    instanceName = key.replace("done/", "").replace(".zip", "")

    try:
        response = ec2.instances.filter(
            Filters=[{"Name": "tag:Name", "Values": [instanceName]}]
        ).terminate()
        assert(len(response) > 0)

        print(f"Instance {instanceName} terminated")
        return True

    except Exception as e:
        print(f"Unable to terminate instance {instanceName}")
        print(e)
        return False
