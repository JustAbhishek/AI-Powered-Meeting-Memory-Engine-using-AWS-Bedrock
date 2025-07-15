import boto3
import os
import time
import json
from datetime import datetime

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    print("Received event:", event)

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    if not object_key.startswith("input/"):
        print(f"Skipping file {object_key} as it's not in the input/ folder.")
        return

    base_filename = os.path.splitext(os.path.basename(object_key))[0]
    timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    job_name = f"transcribe-{base_filename}-{timestamp}"
    output_txt_key = f"transcripts/{job_name}.txt"

    media_uri = f"s3://{bucket_name}/{object_key}"

    # Start Transcribe job (no OutputBucketName specified)
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat=object_key.split('.')[-1],
            LanguageCode='en-US'
        )
        print(f"Transcription job '{job_name}' started.")
    except Exception as e:
        print("Failed to start transcription job:", str(e))
        raise e

    # Wait until the job is completed
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        print(f"Job status: {job_status}")
        if job_status in ['COMPLETED', 'FAILED']:
            break
        time.sleep(5)

    if job_status == 'FAILED':
        print("Transcription job failed.")
        return

    # Get transcript file URI (public in AWS-managed S3)
    transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

    # Fetch JSON transcript from URL
    try:
        import urllib.request
        with urllib.request.urlopen(transcript_file_uri) as response:
            transcript_json = json.loads(response.read().decode('utf-8'))
        transcript_text = transcript_json['results']['transcripts'][0]['transcript']

        # Save transcript as plain text to your S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_txt_key,
            Body=transcript_text.encode('utf-8'),
            ContentType='text/plain'
        )
        print(f"Transcript stored at: s3://{bucket_name}/{output_txt_key}")

    except Exception as e:
        print("Failed to download or store transcript:", str(e))
        raise e
