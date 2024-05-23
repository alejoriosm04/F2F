import os

from django.conf import settings
from openai import OpenAI

from .models import Recipe


class OpenAIAdapter:
    from dotenv import load_dotenv

    load_dotenv(".env")
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    def generate_response_sync(self, ingredients, details, preference, portions):
        instruction = (
            f"Create a recipe using the following ingredients: {ingredients}."
            "Format the response in json with the following fields: title, steps."
            "The steps field will be a list."
            "Don't prepend numbers to each step, only add in the text."
            f"Some details to keep in mind: {details}"
            f"Cuisine: {preference}."
            f"Portions: {portions}"
            "Also, you must absolutely, positively return the recipe in json format."
        )

        response = self._generate_response(instruction)
        if response is None:
            return None
        cleaned = self.validate_recipe(response)

        return cleaned

    def _generate_response(self, instruction: str):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Please create the recipe."},
        ]

        response = OpenAIAdapter.client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.5,
            messages=messages,
            response_format={"type": "json_object"},
        )

        if response.choices[0].finish_reason != "stop":
            return None

        recipe_text = response.choices[0].message.content if response.choices else ""

        return recipe_text

    def validate_recipe(self, api_response):
        import json

        try:
            recipe = json.loads(api_response)
        except json.JSONDecodeError:
            return None

        title = recipe["title"]
        steps = recipe["steps"]

        return {"title": title, "description": steps}

    def generate_image(self, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        import ast

        recipe.description = ast.literal_eval(recipe.description)  # Deserialize safely.
        recipe_as_str = recipe.title + " " + " ".join(recipe.description)
        recipe_as_str = recipe_as_str[
            :1000
        ]  # We can't send prompts longer than 1000 characters.
        prompt = "Generate a colourful image of this recipe: " + recipe_as_str
        response = OpenAIAdapter.client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )

        url = None
        if response is not None:
            url = response.data[0].url

        return url
