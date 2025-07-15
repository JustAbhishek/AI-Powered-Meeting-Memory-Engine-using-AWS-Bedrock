import json
import boto3

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        question = body.get("question")
        company = body.get("company")  # Optional

        if not question:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'question' in request"})
            }

        payload = {
            "question": question,
            "company": company
        }

        response = lambda_client.invoke(
            FunctionName='bedrock-llm',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_body = json.load(response['Payload'])

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "question": question,
                "company": company,
                "llm_response": json.loads(response_body['body'])
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
