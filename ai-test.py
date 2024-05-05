from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_API_KEY
)

#Include only a single table called 'names' in your output.
response = client.chat.completions.create(
  model="gpt-4-turbo",
  response_format={ "type": "json_object" },
  temperature=1.5,
  messages=[
    {"role": "system", "content": "You are a creative and groundbreaking fantasy writer, you output JSON and only JSON. Output only a single table called 'names'"},
    {"role": "user", "content": "Generate 10 fantasy dwarf names"}
  ]
)

print(response.choices[0].message.content)