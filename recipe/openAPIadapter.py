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

    def generate_response_sync(self, instruction: str, prompt: str):
        return asyncio.run(self._generate_response(instruction, prompt))

    async def _generate_response(self, instruction: str, prompt: str):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": prompt}
        ]

        response = await self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            max_tokens=100,
            temperature=0.2,
            messages=messages
        )
        recipe_text = response.choices[0].message.content if response.choices else ""

        return recipe_text

