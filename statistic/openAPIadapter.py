import os
import json
from openai import OpenAI
from django.conf import settings

class OpenAIAdapter:
    from dotenv import load_dotenv
    load_dotenv('.env')
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    def generate_recommendation(self, user_profile):
        ingredients = user_profile.get("favorite_ingredients")
        recipes = user_profile.get("favorite_recipes")
        instruction = (
            f"Based on the user's favorite ingredients: {ingredients} and favorite recipes: {recipes}, "
            "generate lifestyle recommendations including dietary tips, cooking practices, "
            "and cuisines to explore. Please format the output as a JSON object."
        )
        return self._generate_response(instruction)

    def _generate_response(self, instruction):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Please create the recommendation."}
        ]

        response = OpenAIAdapter.client.chat.completions.create(
            model='gpt-3.5-turbo',
            max_tokens=500,
            temperature=0.5,
            messages=messages,
            response_format={"type": "json_object"},
        )

        if response.choices[0].finish_reason != "stop":
            return None

        recommendation_text = response.choices[0].message.content if response.choices else ""

        return recommendation_text
