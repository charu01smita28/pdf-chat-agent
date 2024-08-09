from langchain_community.callbacks import get_openai_callback
from logger import logging

def log_llm_api_cost(cb: get_openai_callback):
    """Logs the open ai api call cost depending on the callback."""

    logging.info(print(f"Total Tokens: {cb.total_tokens}"))
    logging.info(f"Prompt Tokens: {cb.prompt_tokens}")
    logging.info(f"Completion Tokens: {cb.completion_tokens}")
    logging.info(f"Total Cost (USD): ${cb.total_cost}")
