import os
import json
import boto3
import psycopg2

# AWS clients
bedrock = boto3.client('bedrock-runtime', region_name="us-east-1")

# PostgreSQL connection using environment variables
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

def embed_query(text):
    body = json.dumps({"inputText": text})
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        contentType="application/json",
        accept="application/json",
        body=body
    )
    embedding = json.loads(response['body'].read())['embedding']
    return embedding

def fetch_relevant_chunks(embedding, company=None, top_k=5):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    # Convert list to PostgreSQL pgvector format — use square brackets
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'

    if company:
        cur.execute(
            """
            SELECT chunk
            FROM meeting_chunks
            WHERE company = %s
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
            """,
            (company.upper(), embedding_str, top_k)
        )
    else:
        cur.execute(
            """
            SELECT chunk
            FROM meeting_chunks
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
            """,
            (embedding_str, top_k)
        )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

def query_llm_titan(context, question):
    prompt = f"""You are a helpful assistant. Use the context below to answer the user's question.

Context:
{context}

Question:
{question}

Answer:"""

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 800,
            "temperature": 0.7,
            "topP": 0.9,
            "stopSequences": []
        }
    })

    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1",
        contentType="application/json",
        accept="application/json",
        body=body
    )

    return json.loads(response['body'].read())['results'][0]['outputText'].strip()

def lambda_handler(event, context):
    try:
        question = event.get("question")
        company = event.get("company")  # optional

        if not question:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'question' in request"})
            }

        embedding = embed_query(question)
        chunks = fetch_relevant_chunks(embedding, company=company)
        if not chunks:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "No relevant context found"})
            }

        context_text = "\n\n".join(chunks)
        answer = query_llm_titan(context_text, question)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "question": question,
                "company": company,
                "answer": answer
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
