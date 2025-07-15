import re
import json
import boto3
import os

s3 = boto3.client('s3')


def clean_text(text):
    """Remove extra whitespace, fix characters, and sanitize."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[.*?\]', '', text)  # remove brackets
    text = re.sub(r'\s([?.!",](?:\s|$))', r'\1', text)  # spacing around punctuation
    return text


def chunk_text(text, max_len=800):
    """Chunk long text into smaller pieces for further processing."""
    if not text:
        return []
    
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_len:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence

    if chunk:
        chunks.append(chunk.strip())

    return chunks


def lambda_handler(event, context):
    try:
        if 'Records' not in event:
            raise ValueError("No Records in event")

        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if not key.endswith('.txt'):
            print(f"Skipped non-txt file: {key}")
            return

        print(f"Processing file: s3://{bucket}/{key}")

        # Read transcript
        obj = s3.get_object(Bucket=bucket, Key=key)
        raw_text = obj['Body'].read().decode('utf-8')
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text)

        output_key = key.replace("transcripts/", "cleaned_transcripts/").replace(".txt", ".json")
        output_body = json.dumps({"chunks": chunks}, indent=2)

        # Save cleaned data
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=output_body.encode('utf-8'),
            ContentType='application/json'
        )

        print(f"Cleaned transcript saved to: s3://{bucket}/{output_key}")

    except Exception as e:
        print(f"Lambda execution failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
