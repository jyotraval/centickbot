# model_logic.py

import connector
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
model = os.getenv('MODEL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq()

def asktoNPL(query, model = ""):
    if not model:
        model  = "llama-3.1-8b-instant"
    context = ''
    similar = connector.gettopk(query)
    for filename in similar:
        context+= '\n'+ filename + '>\n'
        for content in similar[filename]:
            context+= '-'+content+'\n'
    if not context or not similar:
        return 'The information is not available. Please rephrase your query or provide additional context.'
    # print(context)
    system_prompt='You are an assistant for CENTRAL TICKET. Provide factual answers strictly based on the provided context. Do not add commentary or information that is not in the context.If the context does not contain the information needed to answer the user query, or if the context is irrelevant, stirckly respond by saying that the information is not available and ask the user to rephrase their query. At the end of your answer, append the file name used in brackets(if applicable).\nContext:\n' + context
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                'role' : 'system',
                'content': system_prompt 
                },
        {
            "role": "user",
            "content": query
        }
        ],
        temperature=1.25,
        max_completion_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    reply = '' 
    for chunk in completion:
        reply+=chunk.choices[0].delta.content or ""
    return reply

def generate_reply(message: str, history: list | None = None) -> str:
    """
    To be implemented by the model team.
    """
    npl_reply =asktoNPL(message,model)
    # print(npl_reply)
    response = npl_reply.split('>')
    response= response[-1]
    # print(response)
    return response.strip()

