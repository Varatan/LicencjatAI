from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


class Generator():
    def __init__(self):
       self.__key = os.getenv('OPENAI_API_KEY')
       self.__client = OpenAI(
          api_key = self.__key
       )

    def GenerateNames(self, race, gender):
      if race == "":
        race = "dwarf"
      response = self.__client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      response_format={ "type": "json_object" },
      temperature=1.5,
      messages=[
        {"role": "system", "content": 'You are a creative and groundbreaking fantasy writer. Only come up with new names. Dont use names from existing fantasy fiction. Output only a single JSON object with a table called "names" in this format: {{"names":["name1","name2","nameX"]}}'},
        {"role": "user", "content": f'Generate 10 {gender} fantasy {race} names'}
      ]
      )
      return response.choices[0].message.content