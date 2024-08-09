import pytest
from services.chat_agent import ChatAgent
from model.question import Question

@pytest.fixture
def chat_agent():
    return ChatAgent()

@pytest.mark.asyncio
async def test_answer_questions(chat_agent):
    questions = ["What is the one line summary of the document?"]
    # Assume sample_document.pdf is preloaded or mocked
    answers = await chat_agent.answer_questions(questions, "resources/sample_document.pdf")
    assert len(answers) == len(questions)
    assert answers[0].answer_text != "Data Not Available"
