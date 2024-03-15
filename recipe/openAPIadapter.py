# from openai import AsyncOpenAI

# class OpenAIAdapter:
#     def __init__(self, api_key):
#         self.client = AsyncOpenAI(api_key=api_key)

#     async def generate_response(self, instruction: str, prompt: str):

#         messages = [
#             {"role":"system", "content": instruction},
#             {"role":"user", "content": prompt}
#         ]

#         response = await self.client.chat.completions.create(
#             model = 'gpt-3.5-turbo',
#             max_tokens = 100,
#             temperature = 0.2,
#             messages = messages
#         )
#         recipe_text = response.choices[0].message.content if response.choices else ""

#         return recipe_text
import asyncio
from openai import AsyncOpenAI

class OpenAIAdapter:
    def __init__(self, api_key):
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

