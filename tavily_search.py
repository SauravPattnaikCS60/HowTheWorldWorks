from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json

# load_dotenv()

def parse_results(response):
    context = ""
    for result in response['results']:
        context += result['content']
    
    return context        

def call_tavily(query):
    tavily_client = TavilyClient(api_key=os.getenv('TAVILY'))
    response = tavily_client.search(query, search_depth='advanced',max_results=3,chunks_per_source=3)
    response_string = parse_results(response)
    return response_string