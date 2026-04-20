from groq_call import run_groq_api

def call_and_parse_from_groq(prompt,parser,column=None):
    response = run_groq_api(prompt)
    response_parsed = parser.parse(response)
    if column:
        return response_parsed[column]
    return response_parsed