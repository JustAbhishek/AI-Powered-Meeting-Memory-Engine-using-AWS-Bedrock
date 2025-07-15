import boto3
import json
import os

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # --- Get bucket/key from S3 trigger event ---
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key'] 

    print(f"Processing file: s3://{bucket}/{key}")

    # --- Download transcript chunks from S3 ---
    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(response['Body'].read())
    chunks = data.get("chunks", [])

    if not chunks:
        raise ValueError("No chunks found in transcript file")

    embedded_results = []

    for i, chunk in enumerate(chunks):
        body = json.dumps({"inputText": chunk})

        res = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        embedding = json.loads(res['body'].read())['embedding']

        embedded_results.append({
            "chunk": chunk,
            "embedding": embedding,
            "chunk_index": i,
            "meeting_id": key.split("/")[-1].replace(".json", "")
        })

    # --- Save embeddings to a new folder in S3 ---
    base_filename = os.path.basename(key).replace(".json", ".embedded.json")
    output_key = f"embedded_transcripts/{base_filename}"

    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=json.dumps(embedded_results),
        ContentType='application/json'
    )

    print(f"Embeddings saved to: s3://{bucket}/{output_key}")

    return {
        "meeting_id": embedded_results[0]["meeting_id"],
        "s3_embedding_key": output_key,
        "chunks_embedded": len(embedded_results)
    }
