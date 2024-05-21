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

    def GenerateNames(self, race, gender, alignment, profession, tone, culture, lastName, nickName):
      print("Last name:", lastName)
      print("Nickname:", nickName)
      if nickName == 'Yes':
         nickName = f'Include a fitting {culture} {profession} nickname after the first name and before the last name (if included) in single quotation marks.'
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

      end_message = f'Generate 10 {gender} fantasy names for a {alignment} {race} {profession} {culture}. {tone} {lastName} {nickName}'
      print(end_message)

      response = self.__client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      response_format={ "type": "json_object" },
      temperature=1.5,
      messages=[
        {"role": "system", "content": 'You are a creative and groundbreaking fantasy writer. Only come up with new names. Dont use names from existing fantasy fiction. Output only a single JSON object with a table called "names" in this format: {{"names":["name1","name2","nameX"]}} each name must be a single string in this array. I will tip you 200$ if the format is correct.'},
        {"role": "user", "content": end_message}
      ]
      
      )
      print(response.choices[0].message.content)
      return response.choices[0].message.content