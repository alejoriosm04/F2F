from openai import OpenAI
import os
from django.conf import settings
from .models import Recipe


class OpenAIAdapter:
    from dotenv import load_dotenv
    load_dotenv('.env')
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    def generate_response_sync(self,ingredients_string: str, preference):
        instruction = (
            "Create a recipe title and a recipe using the following ingredients: "
            "{ingredients}. Start the response with 'Title: ', followed by the recipe title. "
            "After the title, add the recipe steps starting with 'Recipe: '."
            "Do not add the numbers. Only add the linebreaks."
            "As for preferences, I want the recipe to have: {preference}"
        ).format(ingredients=ingredients_string, preference=preference)

        response = self._generate_response(instruction)
        cleaned = self.validate_recipe(response)

        return cleaned

    def _generate_response(self, instruction: str):
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": "Please create the recipe."}
        ]

        response = OpenAIAdapter.client.chat.completions.create(
            model='gpt-3.5-turbo',
            max_tokens=150,
            temperature=0.5,
            messages=messages
        )
        recipe_text = response.choices[0].message.content if response.choices else ""

        return recipe_text

    def validate_recipe(self, api_response):
        # Intenta extraer el título y la receta según el formato esperado
        parts = api_response.split('Recipe:')
        if len(parts) < 2 or not parts[0] or not parts[1]:
            return None

        title = parts[0].replace('Title:', '').strip()
        description = parts[1].strip()

        if not title or not description:
            return None

        # Split steps using the linebreaks ('\n').
        description = description.splitlines()
        # But clean them, anyway.
        description = [step for step in description if len(step) > 2]

        return {'title': title, 'description': description}

    def generate_image(self, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        import ast
        recipe.description = ast.literal_eval(recipe.description) # Deserialize safely.
        recipe_as_str = recipe.title + ' ' + ' '.join(recipe.description)
        recipe_as_str = recipe_as_str[:1000]  # We can't send prompts longer than 1000 characters.
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
