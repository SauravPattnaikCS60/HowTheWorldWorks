from pydantic import BaseModel
from typing import List

class Questions(BaseModel):
    questions : List[str]    
    
class SelectedQuestion(BaseModel):
    selected_question : str
    query : str

class Article(BaseModel):
    article : str

class Feedback(BaseModel):
    feedback : str