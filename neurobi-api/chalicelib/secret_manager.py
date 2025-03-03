
import boto3

def get_openai_api_key():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="OpenAI_API_Key")
    return response["SecretString"]