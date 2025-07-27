🚀 𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗲𝗱 𝗠𝗲𝗲𝘁𝗶𝗻𝗴 𝗜𝗻𝘀𝗶𝗴𝗵𝘁 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗦𝗲𝗿𝘃𝗲𝗿𝗹𝗲𝘀𝘀 𝗥𝗔𝗚 𝗣𝗶𝗽𝗲𝗹𝗶𝗻𝗲 𝗼𝗻 𝗔𝗪𝗦 🧠🎙️

Proud to share a recent project where I built a fully serverless AI system that turns raw meeting recordings into 𝗰𝗼𝗻𝘁𝗲𝘅𝘁-𝗮𝘄𝗮𝗿𝗲 𝗮𝗻𝘀𝘄𝗲𝗿𝘀, 𝘀𝘂𝗺𝗺𝗮𝗿𝗶𝗲𝘀, 𝗮𝗻𝗱 𝗱𝗲𝗰𝗶𝘀𝗶𝗼𝗻𝘀.

🔄 𝗘𝗻𝗱-𝘁𝗼-𝗘𝗻𝗱 𝗣𝗶𝗽𝗲𝗹𝗶𝗻𝗲 𝗕𝗿𝗲𝗮𝗸𝗱𝗼𝘄𝗻:

🎧 𝟏. 𝐀𝐮𝐝𝐢𝐨 𝐈𝐧𝐠𝐞𝐬𝐭𝐢𝐨𝐧 & 𝐓𝐫𝐚𝐧𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧

When a meeting recording is uploaded to S3, it automatically triggers transcription using 𝗔𝗺𝗮𝘇𝗼𝗻 𝗧𝗿𝗮𝗻𝘀𝗰𝗿𝗶𝗯𝗲, producing accurate raw text.

🧹 𝟐. 𝐓𝐫𝐚𝐧𝐬𝐜𝐫𝐢𝐩𝐭 𝐏𝐫𝐞𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠

The transcript is cleaned, segmented into semantic chunks, and stored back in S3 — ready for embedding.

🧬 𝟑. 𝐄𝐦𝐛𝐞𝐝𝐝𝐢𝐧𝐠 & 𝐕𝐞𝐜𝐭𝐨𝐫 𝐒𝐭𝐨𝐫𝐚𝐠𝐞

Each chunk is converted into a dense vector using 𝗔𝗺𝗮𝘇𝗼𝗻 𝗧𝗶𝘁𝗮𝗻 𝗘𝗺𝗯𝗲𝗱𝗱𝗶𝗻𝗴𝘀 (𝟭𝟱𝟯𝟲 𝗱𝗶𝗺𝗲𝗻𝘀𝗶𝗼𝗻𝘀) and stored in 𝗣𝗼𝘀𝘁𝗴𝗿𝗲𝗦𝗤𝗟 𝘄𝗶𝘁𝗵 𝗽𝗴𝘃𝗲𝗰𝘁𝗼𝗿, along with metadata like meeting_id and company. 

🧠 𝟒. 𝐑𝐀𝐆: 𝐑𝐞𝐭𝐫𝐢𝐞𝐯𝐚𝐥-𝐀𝐮𝐠𝐦𝐞𝐧𝐭𝐞𝐝 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧

When a user asks a question:
→ It’s embedded.  
→ The system retrieves 𝘁𝗼𝗽-𝗸 𝗿𝗲𝗹𝗲𝘃𝗮𝗻𝘁 chunks based on 𝘃𝗲𝗰𝘁𝗼𝗿 𝘀𝗶𝗺𝗶𝗹𝗮𝗿𝗶𝘁𝘆.  
→ The context is sent along with the question to 𝗔𝗺𝗮𝘇𝗼𝗻 𝗧𝗶𝘁𝗮𝗻 𝗧𝗲𝘅𝘁 𝗘𝘅𝗽𝗿𝗲𝘀𝘀.  
→ The model generates an accurate, 𝗰𝗼𝗻𝘁𝗲𝘅𝘁-𝗮𝘄𝗮𝗿𝗲 𝗮𝗻𝘀𝘄𝗲𝗿.  

🌐 𝟓. 𝐀𝐏𝐈 𝐋𝐚𝐲𝐞𝐫

An 𝗔𝗣𝗜 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 + 𝗟𝗮𝗺𝗯𝗱𝗮 endpoint exposes this as a simple REST API. Just pass a question (optionally filter by company), and the pipeline returns a rich answer from the meeting content.

💻 𝗦𝘁𝗿𝗲𝗮𝗺𝗹𝗶𝘁 𝗙𝗿𝗼𝗻𝘁𝗲𝗻𝗱 𝗳𝗼𝗿 𝗜𝗻𝘁𝗲𝗿𝗮𝗰𝘁𝗶𝘃𝗲 𝗘𝘅𝗽𝗹𝗼𝗿𝗮𝘁𝗶𝗼𝗻

To make the system easily usable by business users, I built a lightweight frontend using 𝗦𝘁𝗿𝗲𝗮𝗺𝗹𝗶𝘁.

Key Features:

• An Interactive Q&A interface to ask for insights from meetings.  
• Supports continuous follow-up questions, maintaining conversational context.  
• Session history tracking—users can view and export previous Q&A pairs.  
• JSON export of full chat session for downstream integration or record-keeping.  

🧠 𝗟𝗮𝘁𝗲𝘀𝘁 𝗧𝗲𝗰𝗵𝗻𝗼𝗹𝗼𝗴𝗶𝗲𝘀 & 𝗖𝗼𝗻𝗰𝗲𝗽𝘁𝘀 𝗨𝘀𝗲𝗱:

✅ Vector Databases (pgvector)  
✅ RAG architecture  
✅ LLM context awareness via semantic chunking  
✅ 𝗦𝗲𝗿𝘃𝗲𝗿𝗹𝗲𝘀𝘀 𝗔𝗪𝗦 𝗦𝘁𝗮𝗰𝗸—S3, Lambda, Transcribe, Bedrock, API Gateway  
✅ 𝗔𝗺𝗮𝘇𝗼𝗻 𝗧𝗶𝘁𝗮𝗻 for both embeddings and text generation  
✅ Metadata-aware filtering for multi-company support  
✅ 𝗦𝘁𝗿𝗲𝗮𝗺𝗹𝗶𝘁 𝗳𝗿𝗼𝗻𝘁𝗲𝗻𝗱 with session-aware follow-up and export features  

💡 𝗪𝗵𝘆 𝗜𝘁 𝗠𝗮𝘁𝘁𝗲𝗿𝘀
🔹 Automates 𝗺𝗲𝗲𝘁𝗶𝗻𝗴 𝗺𝗶𝗻𝘂𝘁𝗲𝘀 & 𝗱𝗲𝗰𝗶𝘀𝗶𝗼𝗻𝘀  
🔹 Enables 𝗿𝗲𝗮𝗹-𝘁𝗶𝗺𝗲 𝗤&𝗔 over the latest recordings  
🔹 Scales effortlessly with a 𝘀𝗲𝗿𝘃𝗲𝗿𝗹𝗲𝘀𝘀 𝗯𝗮𝗰𝗸𝗯𝗼𝗻𝗲  
🔹 Reduces 𝘁𝗶𝗺𝗲-𝘁𝗼-𝗶𝗻𝘀𝗶𝗴𝗵𝘁 across internal teams and meetings  
