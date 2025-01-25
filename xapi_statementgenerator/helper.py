from datetime import datetime, timedelta
import json
import jwt
import requests
import os

SECRET_KEY='django-insecure-_vpe_zb%6i09*rd6+7mq4y%ug=*!hhauf3w8=@_u)z8yknj!#y'

# Get token from lrs.http which is printed in the console with Name Encoded Token:
def send_data_to_lrs(json_file_path, lrs_url, auth_token):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        statements = json.load(file)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_token}',
        'X-Experience-API-Version': '1.0.3'
    }
    
    for statement in statements:
        response = requests.post(lrs_url, headers=headers, json=statement)
        if response.status_code == 200 or response.status_code == 204:
            print(f"Successfully sent statement {statement['id']}")
        else:
            print(f"Failed to send statement {statement['id']}: {response.status_code} - {response.text}")
            
def generate_token_for_testing(user_id, roles, email):
    """
    Generates an access token and a refresh token for the user.
    """
    access_payload = {
        "sub": user_id,
        "roles": roles,
        "exp": datetime.utcnow() + timedelta(days=30*6),  # Access token expires in 6 months
        "email": email
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm='HS256')
    return access_token
# # Example usage
# json_file_path = './generated_data/xapi_statements_12userdataset.json'
# lrs_url = 'http://localhost:8080/xapi/statements'
# auth_token = 'OGQxZGNjNWJkMWZmMTUxZDU3ZTlmYmM2MDU3NjIxMDIyNTRmYzdkMWQ5MzM2ZjdmMmYzNzU2MGJlMDRjODQ5MzoxNzcxOTk5ZWNhZGFhZDMwZTBjMTg3YTUxNGUyMDMwZDUwMGY4NWEwMjRkYjBkMjBlODFlODMzODg5MzYxNmY3'

# send_data_to_lrs(json_file_path, lrs_url, auth_token)


token=generate_token_for_testing('12345', ['http://purl.imsglobal.org/vocab/lis/v2/membership#Learner'], 'user_test_consistent_12w_725bac5c@example.com')
print("LearnerToken",token)

token=generate_token_for_testing('12345', ['http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'], 'instructor3@example.com')
print("InstructorToken",token)

token=generate_token_for_testing('12345', ['http://purl.imsglobal.org/vocab/lis/v2/membership#Administrator'], 'admin@example.com')
print("AdminToken",token)