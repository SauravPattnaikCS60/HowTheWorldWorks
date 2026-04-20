from typing import TypedDict, List
from pydantic import Field
from prompts import get_world_understanding_prompt, filter_questions_to_generate_query,get_article_writing_prompt,get_article_critic_prompt
from pydantic_classes import Questions, SelectedQuestion,Article, Feedback
from langchain_core.output_parsers import JsonOutputParser
from utils import call_and_parse_from_groq
from langgraph.graph import StateGraph,END,START
from tavily_search import call_tavily
import json
import time
import os
from datetime import date

METADATA_FILE = "data/metadata.json"
ARTICLE_PATH = "data/articles/"
UI_PATH = "data/article.md"

class HTWW(TypedDict):
    selected_questions : List[str]
    selected_question : str
    existing_questions : List[str]
    context : str
    query : str
    article : str
    feedback : List[str]
    feedback_counter : int

def get_selected_questions(state : HTWW)->HTWW:
    prompt = get_world_understanding_prompt(state['existing_questions'])
    parser = JsonOutputParser(pydantic_object=Questions)
    state['selected_questions'] = call_and_parse_from_groq(prompt, parser,'questions')
    return state

def get_query(state:HTWW)->HTWW:
    prompt = filter_questions_to_generate_query(state['selected_questions'])
    parser = JsonOutputParser(pydantic_object=SelectedQuestion)
    response = call_and_parse_from_groq(prompt,parser)
    state['selected_question'] = response['selected_question']
    state['query'] = response['query']
    return state

def get_tavily_result(state:HTWW)->HTWW:
    state['context'] = call_tavily(state['query'])
    return state
    
def get_article(state:HTWW)->HTWW:
    if len(state['feedback']) > 0:
        feedback = state['feedback'][-1]
        time.sleep(5)
    else:
        feedback = ""
    prompt = get_article_writing_prompt(state['selected_question'],state['context'],feedback)
    parser = JsonOutputParser(pydantic_object=Article)
    state['article'] = call_and_parse_from_groq(prompt,parser,'article')
    return state

def get_feedback(state:HTWW)->HTWW:
    prompt = get_article_critic_prompt(state['article'],state['context'])
    parser = JsonOutputParser(pydantic_object=Feedback)
    state['feedback'].append(call_and_parse_from_groq(prompt,parser,'feedback'))
    state['feedback_counter'] -= 1
    return state

def should_continue(state: HTWW) -> str:
    last_feedback = state["feedback"][-1] if state["feedback"] else ""
    last_feedback = last_feedback.lower()
    if last_feedback == "no changes" or last_feedback == "no changes.":
        return "end"

    if state["feedback_counter"] <= 0:
        return "end"
    
    time.sleep(5)
    return "rewrite"
    
if __name__ == "__main__":
    builder = StateGraph(HTWW)
    
    builder.add_node("find_selected_topics", get_selected_questions)
    builder.add_node("filter_questions_to_get_query", get_query)
    builder.add_node("get_tavily_result", get_tavily_result)
    builder.add_node("get_article", get_article)
    builder.add_node("get_feedback", get_feedback)
    
    builder.add_edge(START,'find_selected_topics')
    builder.add_edge('find_selected_topics','filter_questions_to_get_query')
    builder.add_edge("filter_questions_to_get_query", "get_tavily_result")
    builder.add_edge("get_tavily_result", "get_article")
    builder.add_edge("get_article", "get_feedback")
    
    builder.add_conditional_edges(
        "get_feedback",
        should_continue,
        {
            "rewrite" : "get_article",
            "end" : END
        }
    )
    
    app = builder.compile()
    
    if not os.path.exists(METADATA_FILE):
        metadata_json = {}
        metadata_json["archives"] = []
    else:
        metadata_json = json.load(open(METADATA_FILE,'r'))
    
    if len(metadata_json) > 0:
        existing_questions = [row['question'] for row in metadata_json["archives"]]
    else:
        existing_questions = []
    
    initial_state = {
    "existing_questions": existing_questions,
    "selected_questions": [],
    "selected_question": "",
    "context": "",
    "query": "",
    "article": "",
    "feedback": [],
    "feedback_counter": 3,
    }
    result = app.invoke(initial_state)
    
    question = result['selected_question']
    query = result['query']
    article_content = result['article']
    article_content = f"# {question}\n\n{article_content}"
    
    metadata_json["archives"].append({"question":question,"query":query})
    json.dump(metadata_json,open(METADATA_FILE,'w'))
    
    article_file_name = query + date.today().strftime("%Y-%m-%d")
    article_file_path = os.path.join(ARTICLE_PATH,article_file_name)
    
    with open(article_file_path,'w',encoding='utf-8') as f:
        f.write(article_content)
    
    with open(UI_PATH,'w',encoding='utf-8') as f:
        f.write(article_content)
        