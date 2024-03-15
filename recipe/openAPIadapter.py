import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

class OpenAIAdapter:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("No se encontró la clave API de OpenAI. Asegúrate de que está definida en .env.")
        self.client = AsyncOpenAI(api_key=api_key)

    def generate_response_sync(self,ingredients_string: str):
        instruction = (
            "Create a recipe title and a recipe using the following ingredients: "
            "{ingredients}. Start the response with 'Title: ', followed by the recipe title. "
            "After the title, add the recipe steps starting with 'Recipe: '."
        ).format(ingredients=ingredients_string)

        return asyncio.run(self._generate_response(instruction))

    async def _generate_response(self, instruction: str):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Please create the recipe."}
        ]

        response = await self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            max_tokens=150,
            temperature=0.5,
            messages=messages
        )
        recipe_text = response.choices[0].message.content if response.choices else ""

        return recipe_text

