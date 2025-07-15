import boto3
import os
import json
import psycopg2
from psycopg2.extras import execute_values

# Setup clients
s3 = boto3.client('s3')

# DB credentials (in real use, load securely from Secrets Manager or SSM)
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

def extract_company(meeting_id):
    # Extracts company from meeting_id: e.g., "transcribe-TRANSRAIL-20250713-174907"
    try:
        parts = meeting_id.split('-')
        return parts[1].upper() if len(parts) > 1 else "UNKNOWN"
    except Exception:
        return "UNKNOWN"

def lambda_handler(event, context):
    # Extract S3 bucket and key from the event
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    print(f"Triggered by file: s3://{bucket}/{key}")

    # Read and parse the embedded JSON
    response = s3.get_object(Bucket=bucket, Key=key)
    embeddings = json.loads(response['Body'].read())

    if not embeddings:
        raise ValueError("No embeddings found")

    meeting_id = embeddings[0]["meeting_id"]
    company = extract_company(meeting_id)

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    try:
        with conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO meeting_chunks (meeting_id, company, chunk, chunk_index, embedding)
                    VALUES %s
                """
                values = [
                    (row["meeting_id"], company, row["chunk"], row["chunk_index"], row["embedding"])
                    for row in embeddings
                ]
                execute_values(cur, insert_query, values)
                print(f"Inserted {len(values)} embeddings into DB")
    finally:
        conn.close()

    return {
        "status": "success",
        "inserted_rows": len(embeddings),
        "meeting_id": meeting_id,
        "company": company
    }
