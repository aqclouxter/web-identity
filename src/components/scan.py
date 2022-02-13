import json
import glob
import boto3
import os
import datetime
import uuid

UUID = str(uuid.uuid4())
FOUND = False
REGION = os.environ['AWS_DEFAULT_REGION']
AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
IMAGE_REPO_NAME = os.environ['IMAGE_REPO_NAME']
IMAGE_TAG = os.environ['CODEBUILD_RESOLVED_SOURCE_VERSION']
IMAGE_ARN = "{0}.dkr.ecr.{1}.amazonaws.com/{2}:{3}".format(
    AWS_ACCOUNT_ID, REGION, IMAGE_REPO_NAME, IMAGE_TAG)

client = boto3.client('securityhub')


def get_filelist():
    try:
        files = glob.glob("anchore-reports/*vuln*")
    except Exception as e:
        print(e)
        return None
    return files


def parse_data(data):
    product_arn = "arn:aws:securityhub:{0}:{1}:product/{2}/default".format(
        REGION, AWS_ACCOUNT_ID, AWS_ACCOUNT_ID)

    curr_time = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    findings = []
    i = 0
    vulns = data.get('vulnerabilities')
    if vulns:
        for vuln in vulns:
            finding = {
                'SchemaVersion': '2018-10-08',
                'Id': "{0}-{1}-{2}".format(IMAGE_TAG, vuln['vuln'], str(i)),
                'ProductArn': product_arn,
                'ProductFields': {
                    'ProviderName': 'Anchore',
                    'ProviderVersion': 'v0.8.2',
                },
                'GeneratorId': UUID,
                'AwsAccountId': AWS_ACCOUNT_ID,
                'Types': [
                    "Software and Configuration Checks/Vulnerabilities/CVE"
                ],
                'CreatedAt': curr_time,
                'UpdatedAt': curr_time,
                'Severity': {
                    'Normalized': 89
                },
                'Title': "Vulnerability {0} found in ECR repository {1} with tag {2}'".format(vuln['vuln'], IMAGE_REPO_NAME,  IMAGE_TAG),
                'Description': "Vulnerability {0} found in {1} for {2}".format(vuln['vuln'], vuln['package'], IMAGE_TAG),
                'SourceUrl': vuln['url'],
                'Resources': [
                    {
                        'Type': 'Container',
                        'Id': IMAGE_ARN,
                        'Details': {
                                'Container': {
                                    'ImageId': IMAGE_TAG
                                }
                        }
                    }
                ],
                'Remediation': {
                    'Recommendation': {
                        'Text': "Update {0} to version {1}".format(vuln['package'], vuln['fix'])
                    }
                },
                'UserDefinedFields': {
                    'feedGroup': vuln['feed_group'],
                    'package': vuln['package'],
                    'packageType': vuln['package_type'],
                    'severity': vuln['severity'],
                }
            }
            i = i + 1
            findings.append(finding)
    return findings


files = get_filelist()

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        d = json.load(f)
        findings = parse_data(d)
        try:
            client.batch_import_findings(Findings=findings)
        except Exception as e:
            print("unable to send to sechub, ", e)
        if len(findings) > 0:
            FOUND = True
    f.close()
if FOUND:
    print("BUILD FAILED : There are issues with the image scan, please check Security Hub for details")
    exit(1)
print("No issues found with scan")
exit(0)