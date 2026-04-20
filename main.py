from prompts import get_world_understanding_prompt
from pydantic_classes import Questions
from langchain_core.output_parsers import JsonOutputParser
from groq_call import run_groq_api

def main():
    existing_questions = []
    prompt =  get_world_understanding_prompt(existing_questions)
    response = run_groq_api(prompt)
    parser = JsonOutputParser(pydantic_object=Questions)
    response_parsed = parser.parse(response)
    print(response_parsed['questions'])


if __name__ == "__main__":
    main()
