from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from agents.services.chat_agent import ChatAgent
from agents.model.question import Question
from dependencies import get_chat_agent
from logger import logging
from random import randint

router = APIRouter()

@router.post("/process-and-query/")
async def process_and_query(
    file: UploadFile = File(...),
    questions: list[str] = [],
    chat_agent: ChatAgent = Depends(get_chat_agent)
):
    try:
        # Handle the queries using the ChatAgent
        questions_formatted = [
            Question(id=randint(1000, 9999), text=ques)
            for ques in questions
        ]        
        logging.info(f"{questions_formatted}")

        response = await chat_agent.handle_queries(file, questions_formatted)
        return {"responses": response}

    except Exception as e:
        logging.error(f"Error processing PDF and handling queries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))