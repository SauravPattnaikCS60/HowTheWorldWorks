import json

def get_world_understanding_prompt(existing_questions):
    prompt = f"""
    You are an expert question generator.

    Your task is to generate exactly 3 thoughtful, diverse, and intellectually meaningful questions that help a person understand how the world works.

    The goal is to generate questions that uncover:
    - how systems function
    - why things are structured the way they are
    - what incentives, constraints, and tradeoffs shape the world
    - how history, economics, politics, technology, geography, infrastructure, and human behavior interact
    - why everyday things exist in their current form
    - what hidden dependencies make modern life work

    The questions should help someone build a deep, practical, intuitive understanding of the world.

    You will be given:
    1. existing_questions: a list of questions that have already been chosen

    Your job:
    - Generate exactly 3 new questions
    - Do not repeat any question from existing_questions
    - Do not generate near-duplicates of existing_questions
    - Ensure the 3 questions are meaningfully different from one another
    - Keep the language simple and natural
    - Make the questions curiosity-driven, explanation-focused, and broad enough to reveal how the world works
    - Do not create overly long or overly complicated questions or composite questions
    - Do not create questions that are too obvious, too basic, or answerable by common everyday knowledge
    - Prefer questions whose answers reveal deeper systems, tradeoffs, incentives, historical reasons, or global dependencies
    - Each question should feel like it opens a door into understanding an important part of how society, economics, technology, infrastructure, or power actually works
    - Avoid childish or surface-level questions such as simple safety, routine, or school-level “how does this help” type questions
    - Prefer questions that make the reader think: “I use or see this all the time, but I never understood why it works this way”

    A bad question is:
    - How do traffic lights keep everyone on the road safe?

    Why it is bad:
    - It is too obvious
    - It is too simple
    - It does not reveal a deep system
    - It does not lead to rich understanding of how the world works

    Better question styles are:
    - Why are global shipping routes concentrated around a few key chokepoints?
    - How do central banks influence everyday life without most people noticing?
    - Why do some natural resources make countries richer while others create instability?
    - Why is the modern food supply chain so dependent on a few critical inputs?
    - How does insurance make large-scale economic activity possible?
    - Why do countries continue trading with rivals during geopolitical tension?

    The questions should preferably explore themes such as:
    - transportation
    - energy
    - economics
    - finance
    - trade
    - geopolitics
    - government
    - infrastructure
    - communication
    - technology
    - manufacturing
    - agriculture
    - healthcare
    - environment
    - law
    - labor
    - media
    - global systems

    Good examples of style:
    - How does a car work?
    - Why is oil so important for the world?
    - Why are there predetermined air routes?
    - Why is the dollar so strong?
    - Why are semiconductor supply chains so globally concentrated?
    - How do ports shape the economies of entire countries?
    - Why do governments borrow so much money instead of simply printing it?
    - Why is electricity difficult to store at large scale?
    - How do undersea cables quietly power the global internet?
    - Why do a few narrow sea routes matter so much to world trade?

    Return the output strictly in valid JSON using exactly this format:
    ```
    {{
    "questions": [
        "question 1",
        "question 2",
        "question 3"
    ]
    }}
    ```

    The following questions have already been chosen and must not be repeated or closely paraphrased:
    {json.dumps(existing_questions, indent=2)}

    Do not return any text outside the JSON.
    """
    return prompt

def filter_questions_to_generate_query(selected_questions):
    prompt = f"""
    You are an expert research-question selector and search-query writer.

    You will be given a list of candidate questions.
    Your task is to choose the single best question for internet research and then rewrite it as an optimized web search query.

    Input:
    - selected_questions: a list of candidate questions

    Your objectives:
    1. Select the one question that is most likely to produce rich, high-quality, explanatory search results from the internet.
    2. Prefer questions that are:
       - deep rather than superficial
       - specific enough to search well
       - broad enough to return meaningful explanatory sources
       - focused on systems, incentives, causes, tradeoffs, history, or global importance
       - likely to have good articles, explainers, reports, or educational sources available online
    3. Avoid selecting questions that are:
       - too vague
       - too obvious
       - too narrow
       - poorly phrased for research
       - likely to return weak or shallow search results

    After selecting the best question, create a search query for it.

    Rules for the query:
    - The query should be optimized for internet search engines
    - Keep the original meaning of the selected question
    - Rewrite it using important keywords likely to improve result quality
    - Remove unnecessary conversational phrasing
    - Prefer search-friendly terms such as:
      "how", "why", "causes", "importance", "history", "economics", "geopolitics", "infrastructure", "global trade", "explained"
    - The query should be concise but strong
    - Do not make it too short and keyword-poor
    - Do not make it a long sentence
    - It should be something a skilled researcher would type into a search engine

    Return the output strictly in valid JSON using exactly this format:
    ```
    {{
      "selected_question": "best question here",
      "query": "optimized internet search query here"
    }}
    ```

    Candidate questions: {selected_questions}

    Do not return any text outside the JSON.
    """
    return prompt
  

def get_article_writing_prompt(selected_question, context, feedback):
    prompt = f"""
    You are an expert explanatory writer.

    Your task is to write a beginner-friendly article answering the question below using the supplied internet context.

    Selected Question:
    {selected_question}

    Context:
    {context}

    Reviewer Feedback:
    {feedback}

    Your job:
    - Write a clear, well-structured article that answers the question
    - Use the context as the primary source of support
    - Synthesize the information instead of copying it
    - Stay faithful to the context
    - Do not invent unsupported facts
    - If the context suggests uncertainty or multiple viewpoints, reflect that honestly
    - Explain the topic in lucid, simple language suitable for beginners

    Feedback handling rules:
    - If reviewer feedback is present and is not "No changes", incorporate it while writing the article
    - Use the feedback to improve clarity, completeness, structure, depth, grounding in context, and readability wherever applicable
    - If the feedback points out missing context, unsupported claims, weak structure, shallow explanation, or unclear writing, correct those issues in the article
    - If the feedback is "No changes" or empty, write the article normally using the question and context
    - Do not mention the reviewer feedback explicitly in the article
    - Do not output a list of changes or discuss the editing process

    The article must be:
    - easy to read
    - logically structured
    - informative but not overly technical
    - rich in explanation, not just summary
    - focused on helping the reader understand how and why something works

    Structure the article with these exact sections:

    ## 1. Introduction / Necessary Background Information
    Provide the minimum important background needed to understand the topic well.

    ## 2. Answer to the Question
    Give the main answer clearly and explain it in a step-by-step, understandable way.

    ## 3. Why This Is an Important Topic and Why We Should Be Aware of It
    Explain why the topic matters in the real world and why it deserves attention.

    ## 4. Additional Information / Related Topics / Consequences
    Add useful related ideas, spillover effects, implications, or connected topics if relevant.

    Additional writing guidance:
    - Prefer plain English over jargon
    - Explain unfamiliar terms simply
    - Use examples and analogies where useful
    - Keep paragraphs readable
    - Avoid fluff
    - Avoid repetition
    - Avoid overly simplistic treatment
    - Avoid sounding academic or robotic

    Output requirements:
    - Return the output in the below JSON format
    ```
    {{
      "article": "full article here"
    }}
    ```
    - The value of "article" must be a single markdown string containing the full article
    - Do not output any text outside the JSON
    - Ensure the JSON is valid
    """
    return prompt
  

def get_article_critic_prompt(article, context):
    prompt = f"""
    You are an expert editor and critic for beginner-friendly explanatory writing.

    Your task is to review the article given below using the supporting context and decide whether the article needs any improvement.

    Article:
    {article}

    Supporting Context:
    {context}

    Your job:
    - Carefully evaluate the article as a beginner-friendly explanatory article
    - Check whether the article is consistent with the supporting context
    - Check whether the article uses the context properly and does not ignore important information from it
    - Check whether the article contains claims that are unsupported, exaggerated, or not grounded in the context
    - Check whether the article clearly answers the main question
    - Check whether the writing is lucid, simple, and easy to follow
    - Check whether the structure is logical and complete
    - Check whether the article is sufficiently informative and not superficial
    - Check whether the sections are well balanced
    - Check whether the article avoids unnecessary jargon
    - Check whether technical terms, if any, are explained properly
    - Check whether the article avoids repetition, fluff, vague claims, and confusing sentences
    - Check whether the article explains why the topic matters
    - Check whether the article includes useful background and relevant consequences or related ideas where needed
    - Check whether the tone is natural and readable rather than robotic or overly academic

    Evaluation criteria:
    1. Grounding in Context
       - Is the article faithful to the supporting context?
       - Does it avoid unsupported claims?
       - Does it miss any important point from the context that should reasonably be included?

    2. Clarity
       - Is the article easy for a beginner to understand?
       - Are the explanations clear and well phrased?

    3. Completeness
       - Does the article provide enough background?
       - Does it answer the question properly?
       - Does it explain why the topic is important?

    4. Depth
       - Is the article meaningful and insightful rather than shallow?
       - Does it help the reader understand how or why something works?

    5. Structure
       - Are the sections logically organized?
       - Does the flow feel natural?

    6. Style
       - Is the language lucid and accessible?
       - Are there any awkward, overly complex, or repetitive parts?

    Response rules:
    - If the article looks good and no meaningful improvements are needed, return:
      {{
        "feedback": "No changes"
      }}

    - Otherwise, return feedback that clearly explains what should be improved.
    - The feedback should be specific and actionable.
    - Mention whether the issue is related to:
      - missing or misused context
      - clarity
      - completeness
      - structure
      - depth
      - style
    - Focus only on meaningful improvements.
    - Do not rewrite the whole article.
    - Do not praise the article unnecessarily.
    - Do not return anything outside the JSON.

    Output format:
    Return strictly valid JSON with exactly one key:
    {{
      "feedback": "your feedback here"
    }}
    """
    return prompt