import json
import os
from dotenv import load_dotenv

from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

class Data(BaseModel):
    question: str

app = FastAPI()

@app.post("/answer")
async def root(data: Data):
    answer = get_answer(data.question)

    return json.dumps({ "reply": answer })

def get_answer(question):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    system_prompt = f"""
      Your purpose is to answer a question in the same languege as the question received.
      Be concise with your answer.
    """

    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": question }
        ]
    )

    return result.choices[0].message.content