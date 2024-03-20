import asyncio
from openai import AsyncOpenAI
import os
from django.conf import settings


class OpenAIAdapter:
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response_sync(self,ingredients_string: str, preference):
        instruction = (
            "Create a recipe title and a recipe using the following ingredients: "
            "{ingredients}. Start the response with 'Title: ', followed by the recipe title. "
            "After the title, add the recipe steps starting with 'Recipe: '."
            "As for preferences, I want the recipe to have: {preference}"
        ).format(ingredients=ingredients_string, preference=preference)

        return asyncio.run(self._generate_response(instruction))

    async def _generate_response(self, instruction: str):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Please create the recipe."}
        ]

        response = await OpenAIAdapter.client.chat.completions.create(
            model='gpt-3.5-turbo',
            max_tokens=150,
            temperature=0.5,
            messages=messages
        )
        recipe_text = response.choices[0].message.content if response.choices else ""

        return recipe_text
