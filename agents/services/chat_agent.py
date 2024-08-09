from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from agents.services.embedding_service import EmbeddingService
from agents.services.chromadb_service import ChromaDBService
from agents.services.pdf_loader import PDFLoaderService
from agents.model.question import Question
from langchain_core.tools import create_retriever_tool
from fastapi import HTTPException
from logger import logging
from typing import List
from agents.utils import log_llm_api_cost
import asyncio
import json

json_format = """
            {
                "question_id": {
                    "question": "question text",
                    "answer": "correct answer"
                    "confidence" : "similarity score"
                    },

               "question_id": {
                    "question": "question text",
                    "answer": "correct answer"
                    "confidence" : "similarity score"
                    },
                "question_id": {
                    "question": "question text",
                    "answer": "correct answer"
                    "confidence" : "similarity score"
                    }
                }


            }"""

class ChatAgent:
    def __init__(self, pdf_loader_service: PDFLoaderService, embeddings_service: EmbeddingService, vector_db_service: ChromaDBService):
        self._pdf_loader_service = pdf_loader_service
        self._embeddings_service = embeddings_service
        self._vector_db_service = vector_db_service
        
    async def handle_queries(self, file, questions: list[Question]):
        try:
            logging.info("Inside handle_queries")
            # Read the file content asynchronously
            contents = await file.read()
            with open("temp.pdf", "wb") as f:
                f.write(contents)

            # Extract text chunks from the uploaded PDF
            text_chunks = self._pdf_loader_service.extract_text("temp.pdf")

            retriever = self._vector_db_service.generate_retriever(text_chunks, self._embeddings_service._embeddings)
            
            # Get the custom prompt template
            prompt = self.get_custom_prompt()
            
            # Create retriever tool
            tool = create_retriever_tool(
                retriever,
                "pdf_content_retriever",
                "Searches and returns excerpts from the Chroma vector database.",
            )
            tools = [tool]

            executor: AgentExecutor = self.create_agent(tools, prompt)

            response = await self.process_questions_parallel(questions, executor)
            # Process each question asynchronously
            # with get_openai_callback() as cb:
            #      tasks = [executor.invoke({"question_id": question.id, "question": question.text, "chat_history": [], "agent_scratchpad": "", "response_json": json_format}) for question in questions]
            #      response = 
            # log_llm_api_cost(cb)
            
            if response:
                logging.info(f"Agent response: {response}")
                formatted_response = self._format_results(response)
                logging.info(f"Formatted response: {formatted_response}")
                return formatted_response
            else:
                return "No relevant context found."

        except Exception as e:
            logging.error(f"Error processing PDF and handling query: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    

    async def process_questions_parallel(self, questions: List[Question], agent):
        # Create tasks for each question
        tasks = [self.process_single_question(question, agent) for question in questions]

        # Use asyncio.gather to execute tasks in parallel
        results = await asyncio.gather(*tasks)
        return results

    async def process_single_question(self, question: Question, agent):
        # Analyze the query using the agent
        return await agent.ainvoke({"question_id": question.id, "question": question.text, "chat_history": [], "agent_scratchpad": "", "response_json": json_format})

    def get_custom_prompt(self):
        """Returns the custom prompt template for the ReAct agent."""

        template = """
            You have the ability to work on multiple questions at once. Each question will have its own separate answer. Answer the following questions as best you can. 
            You have access to the following tools:

            {tools}

            Use the following format for each question:

            Question: {question}
            Thought: Let's first check the PDF document to see if it contains the information.
            Action: Choose the tool from {tool_names}.
            Action Input: {question}
            Observation: Based on the retriever retrieve the closest match to the {question} and store the similarity score as a variable called confidence. If the answer is a descriptive question, 
            provide a comprehensive answer with 90 characters with all significant details.
                Use the agent_scratchpad to process any intermediate steps:
                {agent_scratchpad}

            Answer so on for other questions. 
            
            Final Answer: Provide the answer to each question separately. It should be like this {question} along with the question id {question_id} and answer and confidence score
            stored as json like {response_json}.

            Begin!
            
            Thought: I have now gathered all the necessary information.
            Action: Done
            Action Input: None
            Final Answer: {agent_scratchpad}
        """
        return PromptTemplate(
            input_variables=["question_id","questions", "tool_names", "tools", "agent_scratchpad", "response_json"],
            template=template,
        )
    
    def create_agent(self, tools, prompt):
        """Creates a ReAct agent using the provided model, tools, and prompt."""
        logging.info("Creating ReAct agent with provided model, tools, and prompt.")
        # Create OpenAI agent with the updated tools
        agent = create_react_agent(llm=self._embeddings_service._model, tools=tools, prompt=prompt)
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations =5,
            early_stopping_method = "force"
        )
        logging.info("ReAct agent created successfully.")
        return agent_executor

    def _format_results(self, detailed_response):
        # Create a dictionary for questions with confidence score less than 0.30
        logging.info("Inside formatting response")
        question_answer_dict = {}
        parsed_response = json.loads(detailed_response[0]['output'])
        logging.info(f"Parsed respones = {parsed_response}")
        for _, details in parsed_response.items():
            question = details['question']
            answer = details['answer']
            confidence = float(details['confidence'])

            # Check if the confidence score is less than 0.30 or low confidence
            if confidence > 0.30:
                question_answer_dict[question] = answer
            else:
                question_answer_dict[question] = "Data Not Available"

        return question_answer_dict