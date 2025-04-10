import json
import os
from re import U
import sys
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
from http import HTTPStatus
from dotenv import load_dotenv

from requests.exceptions import HTTPError

load_dotenv()

role_arn = os.getenv('ROLE_ARN')
region   = os.getenv('AWS_REGION')
api_id   = os.getenv('API_ID')
host     = f'{api_id}.execute-api.us-east-1.amazonaws.com'
 
sts = boto3.client('sts')

def assume_role_and_get_session(role_arn):
    assume_role_response = sts.assume_role(RoleArn=role_arn,RoleSessionName="aurelia-test")
    credentials = assume_role_response.get('Credentials')
    access_key = credentials.get('AccessKeyId')
    secret_key = credentials.get('SecretAccessKey')
    session_token = credentials.get('SessionToken')

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region
    )
    return session

session = assume_role_and_get_session(role_arn)
session_credentials = session.get_credentials()
if not session_credentials:
    raise Exception('No credentials in session')

def send_signed_request(method, path, payload=None):
    service = 'execute-api'
    url=f'https://{host}/v1{path}'
    if payload != None:
        data = json.dumps(payload)
    else:
        data = None

    request = AWSRequest(
        method,
        url,
        headers={'Host': host},
        data=data
    )

    SigV4Auth(session_credentials, service, region).add_auth(request) # type: ignore
    request.headers['Content-Type'] = 'application/json' 

    try:
        response = requests.request(method, url, headers=dict(request.headers), data=data, timeout=5)
        response.raise_for_status()
    except:
        print(f'!!! {method} {url} FAILED !!!')
        for (header, value) in response.headers.items():
            print(f'{header}: {value}')
        print(response.text)
        raise
    return json.loads(response.content.decode("utf-8"))


item = send_signed_request('GET', '/item/test1')
print(f'GET response: {json.dumps(item)}')

response = send_signed_request('POST', '/item', { "id": "test2", "name": "Test Item 2", "description": "Another Test Item"} )
print(f'POST response: {json.dumps(response)}')
