from django.conf import settings
from django.db import models


class Recipe(models.Model):
    """
    related_name='recipes': Este argumento en
    el campo ForeignKey significa que puedes acceder a
    todas las recetas de un usuario usando user.recipes.all()
    si user es una instancia del modelo User.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    parameters = models.TextField()
    generation_date = models.DateField(
        auto_now_add=True
    )  # Esto automáticamente establecerá la fecha cuando la receta se cree
    image = models.URLField(blank=True, null=True)
    cuisine = models.TextField()
    number_of_portions = models.TextField()
    favourite_state = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("recipe:show", kwargs={"pk": self.pk})

    @property
    def short_description(self):
        preview_length = 150
        import ast

        description = " ".join(ast.literal_eval(self.description))
        try:
            description = description[:preview_length]
        except IndexError:
            pass
        return description
