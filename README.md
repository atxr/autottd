# autottd ⚙️
Automate and sandbox TTD recording with AWS

## Setup
### autottd AMI
#### Create new role and policy
The EC2 instances must have some S3 permissions:

autottdBucketPolicy 
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectTagging",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::autottd-bucket",
                "arn:aws:s3:::autottd-bucket/*"
            ]
        }
    ]
}
```

Create a new role autottdEC2Role with this policy.

#### Create a new AMI
Launch a classic Windows AMI, and execute this:
```ps1
#Install aws
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

#Install TTD
Invoke-WebRequest https://aka.ms/ttd/download -OutFile ttd.appinstaller
Add-AppxPackage -AppInstallerFile ttd.appinstaller
```

Then, create a new AMI based on this image. Don't forget to change/save the password of the instance if you want to debug the AMI created later.

### Lambda functions
#### Policy and Role

Create a new policy for lambda functions.
Lambda must be able to:
- Run and manage EC2 all instances (maybe be more granular)
- Read and manage autottd S3 bucket
- Log (lambda constraint)
- Pass the role *autottdEC2Role* to the created instances

autottdHandlerPolicy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2Managment",
            "Effect": "Allow",
            "Action": [
                "ec2:TerminateInstances",
                "ec2:CreateTags",
                "ec2:RunInstances",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Sid": "S3",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::autottd-bucket",
                "arn:aws:s3:::autottd-bucket/*"
            ]
        },
        {
            "Sid": "Logs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Ressource": [
                "arn:aws:logs:*:*:*"
            ]
        }
        {
            "Sid": "IAMForEC2Instance",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::<account>:role/autottdEC2Role"
            ]
        }
    ]
}
```

Create associated role autottdHandlerRole.

#### Todo Handler
Generate the lambda function with:
```ps1
python .\generateTodoHandler.py
```

Create a new lambda autottdTodoHandler with this function and the role *autottdHandlerRole*.
Use a simple S3 trigger that matches `todo/*.exe`:
```
Service principal: s3.amazonaws.com
Bucket arn: arn:aws:s3:::autottd-bucket
Event types: s3:ObjectCreated:*
Prefix: todo/
Suffix: .exe
```

#### Done Handler

Create a new lambda autottdDoneHandler with the function in `autottdDoneHandler` and the role *autottdHandlerRole*.
Use a simple S3 trigger that matches `done/*.zip`:
```
Service principal: s3.amazonaws.com
Bucket arn: arn:aws:s3:::autottd-bucket
Event types: s3:ObjectCreated:*
Prefix: done/
Suffix: .zip
```

## Usage

Coming soon...