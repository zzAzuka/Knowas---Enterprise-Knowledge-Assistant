from fastapi import APIRouter, Depends
from core.auth import require_role
from core.models import embeddings_ollama, model_ollama
from core.auth import get_current_user
from pinecone import Pinecone
from schemas.querySchema import queryInput, queryOutput
from core.prompt import chatPrompt
import os
import mlflow
from dotenv import load_dotenv
from datetime import datetime
from fastapi.concurrency import run_in_threadpool 
import logging

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()
pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))
index = pc.Index("knowledge-assistant-vector-lake")

@router.post("/", response_model=queryOutput)
async def answerQuery(input: queryInput, current_user=Depends(get_current_user)):
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("Query_Route_Experiment")

    with mlflow.start_run(run_name=f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        try:
            userQuery = input.query
            mlflow.log_param("user_query", userQuery)

            embeddedQuery = await run_in_threadpool(embeddings_ollama.embed_query, userQuery)
            vectorSearch = index.query(
                vector=embeddedQuery,
                top_k=3,
                include_metadata=True
            )

            top_texts = [
                match["metadata"].get("text", "")
                for match in vectorSearch["matches"]
                if "metadata" in match and "text" in match["metadata"]
            ]

            combined_text = "\n\n".join(top_texts)
            mlflow.log_param("context_length", len(combined_text))

            systemPrompt = chatPrompt(combined_text)
            messages = [("system", systemPrompt), ("user", userQuery),]

            response = await run_in_threadpool(model_ollama.invoke, messages)
            mlflow.log_metric("response_length", len(response.content))
            mlflow.set_tag("query_status", "completed")

            sources = [m["metadata"].get("source", "") for m in vectorSearch["matches"]]
            return {"response": response.content, "sources": sources}
        
        except Exception as e:
            logger.exception("Error while processing query")
            mlflow.set_tag("query_status", "failed")
            mlflow.log_param("error_message", str(e))
            return {"response": "An error occurred while processing your query."}     
