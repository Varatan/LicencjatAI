from openai import OpenAI
import os
import json
from openai._exceptions import OpenAIError
from dotenv import load_dotenv
load_dotenv()


class Generator():
    def __init__(self):
       self.__key = os.getenv('OPENAI_API_KEY')
       self.__client = OpenAI(api_key = self.__key)

    def GenerateNames(self, race, gender, alignment, profession, tone, culture, lastName, nickName):
      if nickName == 'Yes':
         nickName = f'Using a maximum of three words include a fitting {culture} {profession} nickname after the name in single quotation marks.'
      else:
         nickName = ''
      if lastName == 'Yes':
         lastName = f'Include a {culture} last name.'
      else:
         lastName = "Don't include a last name."
      if tone != '':
         tone = f'Make the name sound {tone}.'
      if culture != '':
         culture = f'from a {culture} culture'

      endMessage = f'Generate exactly 10 {gender} fantasy names for a {alignment} {race} {profession} {culture}. {tone} {lastName} {nickName}'
      print(endMessage)

      response = None
      for i in range(3):
         print(f'trying to generate {i} time')
         try:
            response = self.__client.chat.completions.create(
               model="gpt-3.5-turbo-0125",
               response_format={"type": "json_object"},
               temperature=1.3, #Changed from 1.5, gave weird results sometimes
               messages=[
                  {"role": "system", "content": 'You are a creative and groundbreaking fantasy writer. Your task is to come up with new names. Don\'t use names from existing fantasy fiction. You must output only a single JSON object with a table called "names" in this format: {"names":["name1","name2","nameX"]}. Each name must be a single string in this array. You will be penalized for using existing names. I will tip you 200$ if the format is correct.'},
                  {"role": "user", "content": endMessage}
               ]
            )

            content = response.choices[0].message.content
            result = json.loads(content)
            print(f'{i} result',result)
            if "names" in result and isinstance(result["names"], list):
               print(result)
               return result
            else:
               print("Invalid format received:", content)
         except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing response: {e}")
         except OpenAIError as e:
            print(f"OpenAI API error: {e}")


      raise ValueError("Failed to generate valid names after several attempts")