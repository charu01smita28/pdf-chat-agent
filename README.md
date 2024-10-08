# AI Agent for PDF-Based Question Answering

## Overview

This project is an AI agent that leverages the capabilities of large language models to extract answers from large PDF documents and post the results on Slack. It is built using OpenAI's language models and other technologies such as FastAPI, LangChain, and ChromaDB for efficient processing and retrieval.

## Features

- **PDF Text Extraction**: Uses Langchain PyPDFLoader to extract and chunk text from PDF documents.
- **Question Answering**: Utilizes OpenAI's LLM to answer questions based on the extracted text.
- **Parallel Processing**: Employs concurrent futures for efficient, parallel processing of multiple LLM queries for faster response times.
- **Custom Chain Logic**: Implements custom logic for handling multi-step query processing and retrieval with tools and agent framework.
- **Microservice Architecture**: This promotes modularity and maintainability by allowing individual components to be developed, tested, and deployed independently.
- **Dependency Injection**: This facilitates the decoupling of services, making the system more flexible and easier to scale, as components can be swapped or updated without extensive reconfiguration.
- **Slack Integration**: Json answers are generated which will be later posted as answers directly to a specified Slack channel. (Future work)

## Table of Contents

- [AI Agent for PDF-Based Question Answering](#ai-agent-for-pdf-based-question-answering)
  - [Overview](#overview)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Architecture](#architecture)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Endpoints](#endpoints)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Testing](#testing)
  - [CONCLUSION](#conclusion)

## Architecture
![Architecture Diagram](/AiAgent%20(1).jpg)

## Setup

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.8+](https://www.python.org/)

### Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/charu01smita28/pdf-chat-agent.git
   cd pdf-chat-agent

2. **Create and Activate Virtual Environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
4. **Set Up Environment Variables**:
    Update the .env file in the root directory as per your installation or use the one in project.

5. **Build and Run Docker Containers**:
    ```sh
    docker-compose up -d


6. **Running the Application**:
    You can run the FastAPI Application:
    ```sh
    uvicorn app:app --reload

7. **Access the Application**:
    Open your browser and go to http://localhost:8000.

8. **Swagger Endpoints**:
    To try the endpoints, go to http://localhost:8000/docs
    

## Endpoints
- **POST /process-and-query/**: This endpoint takes in a list of questions and the PDF document on which you need to chat with. 

## Project Structure

    ├── app.py                 # Main application entry point
    ├── dependencies.py        # Dependency Injection
    ├── agents/
    │   ├── model/
    │   │   ├── question.py    # Question model (for the input list of questions)
    │   │   ├── answer.py      # Answer model (for the answer to be returned)
    │   ├── api/
    │   │   └── endpoints.py   # FastAPI endpoints for the app
    │   ├── services/
    │   │   ├── agent_service.py   # AI Agent Logic
    │   │   ├── slack_service.py   # Slack integration
    │   │   ├── pdf_loader.py      # PDF loading and text extraction
    │   │   ├── embedding_service.py # Model and vector embeddings usage
    │   │   └── chromadb_service.py # Vector database interactions
    |   ├── utils.py              # API Cost calculation function and more
    |   ├── frontend/          # Folder for adding front end components
    ├── tests/                 # Unit and integration tests
    │   └── test_chat_service.py # Test cases for PDF Chat service
    ├── Dockerfile             # Dockerfile for the application
    ├── docker-compose.yml     # Docker Compose configuration
    ├── logger.py              # Custom Logger for logging 
    ├── .env                   # Environment variables
    ├── .gitignore             # Git ignore file
    ├── README.md              # Project readme file
    └── requirements.txt       # Python dependencies

## Usage
1. Upload a PDF file and submit your questions via the provided API endpoint.
2. The application processes the PDF, answers the questions using the AI model, and posts the results as json at the moment but future improvement to Slack.

## Testing
    Run unit and integration tests to verify functionality:
    ```sh
    pytest tests/

## CONCLUSION
- This project demonstrates the integration of advanced AI capabilities with real-world applications by leveraging OpenAI's language models to process and extract information from PDF documents.
- With features such as **parallel processing and usage of LangChain agents**, this solution provides an efficient and scalable way to automate question-answering tasks which can be further enhanced and easily appended with more tools (like Google Search or Wikipedia Search).
- The project also follows a **microservice architecture** with **dependency injection**, which **promotes modularity** and maintainability by allowing **individual components to be developed, tested, and deployed independently**. This approach enables seamless integration of various services, ensuring that each service can evolve without impacting others. Dependency injection facilitates the decoupling of services, making the system more flexible and easier to scale, as components can be swapped or updated without extensive reconfiguration.

## FUTURE WORK OR IMPROVEMENT(s)

- **How to make solution more accurate ?**
  1. Fine-Tuning the Language Model:
     - Using domain-specific datasets to fine-tune the language model to better understand and answer questions related to the PDF.

  2. Better Prompt Engineering:
     - Crafting precise and contextually rich prompts to elicit more accurate responses from the language model.
     - Experiment with different prompt formats and templates to see which yields the best results.

  3. Larger Context Window:
     - Utilizing language models with larger context windows to process and understand more extensive sections of the PDF at once,
     thereby providing more coherent and contextually informed responses.

 - **Enhancing Modularity, Scalability, and Production Readiness**

    1. Already used a **microservice architecture** for handling tasks like PDF processing, question answering, and Slack integration. This allows for independent scaling and deployment of each component.
    2. Already used **dependency injection** frameworks to manage and configure dependencies more cleanly, allowing for easier testing and flexibility in changing implementations.
    3. Already used **parallel processing** by using thread pools or asynchronous frameworks to handle multiple requests concurrently without blocking. This can be made better.
    4. We can utilize **serverless computing** (e.g., AWS Lambda) for functions that can benefit from event-driven scalability.
    5. We need to Implement a **full suite of unit, integration, and performance tests** to ensure reliability and to catch issues early in the development process.
    6. **Robust Logging and Monitoring** There is also an important need of Incorporate logging for critical operations and errors to aid in debugging and understanding system behavior.
       We can use MLFLow and DagsHub for monitoring and logging and also checking the trace of Large Language Models. 

## DEMO

[Project Demo](https://drive.google.com/file/d/1Ay60ZFgG_3iQMFbp1r1ArEatlSgrtEKT/view?usp=drive_link)

