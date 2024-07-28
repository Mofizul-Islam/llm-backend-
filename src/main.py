from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from models import UserRequest, MCQQuestionnaire, LongAnswerQuestionnaire, ShortAnswerQuestionnaire
import os
from dotenv import load_dotenv
from prompt_template import mcq_prompt_template, long_answer_prompt_template, short_answer_prompt_template

load_dotenv()

app = FastAPI()


def read_file():
    file_name = "story.txt"
    file_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'data', file_name))

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_name}' not found at {file_path}")

    with open(file_path, "r") as file:
        story_content = file.read()

    return story_content


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/v1/post/generate-paper",
    status_code=status.HTTP_200_OK,
)
def generate_answer(custom_prompt_template: UserRequest):
    questions_count = custom_prompt_template.questions_count
    question_type = custom_prompt_template.type.lower()
    context = custom_prompt_template.context

    question = f"You MUST Generate exactly {questions_count} questions"

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(
            status_code=500, detail="OpenAI API key is missing")

    # context = read_file()

    if question_type == "mcq":
        pydantic_parser = PydanticOutputParser(
            pydantic_object=MCQQuestionnaire)
        PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=mcq_prompt_template,
            partial_variables={
                "format_instructions": pydantic_parser.get_format_instructions()
            },
        )
    elif question_type == "long_question":
        pydantic_parser = PydanticOutputParser(
            pydantic_object=LongAnswerQuestionnaire)
        PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=long_answer_prompt_template,
            partial_variables={
                "format_instructions": pydantic_parser.get_format_instructions()
            },
        )
    elif question_type == "short_question":
        pydantic_parser = PydanticOutputParser(
            pydantic_object=ShortAnswerQuestionnaire)
        PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=short_answer_prompt_template,
            partial_variables={
                "format_instructions": pydantic_parser.get_format_instructions()
            },
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid question type")

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125",
                     openai_api_key=openai_api_key, temperature=1)

    chain = PROMPT | llm | pydantic_parser

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    print("Success response")
    print(answer)

    return answer.model_dump()
