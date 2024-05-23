import base64
import io
import json

# Use a non-interactive Matplotlib backend to prevent a runtime error from
# starting a Matplotlib GUI outside of main thread.
# See also: https://stackoverflow.com/q/69924881
import matplotlib
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.shortcuts import redirect, render
from django.utils.timezone import now, timedelta
from matplotlib import pyplot as plt

from kitchen.models import Ingredient, RecipeHadIngredient
from recipe.models import Recipe

from .models import Report
from .openAPIadapter import OpenAIAdapter

matplotlib.use("agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


@login_required
def overview(request):
    user = request.user
    first_name = user.first_name or user.username

    # Fetch the last recommendation report, if it exists
    last_report = Report.objects.filter(user=user).order_by("-report_date").first()
    can_request_recommendation = False
    days_until_next_recommendation = 0

    if last_report:
        days_since_last = (now().date() - last_report.report_date).days
        days_until_next_recommendation = 15 - days_since_last
        can_request_recommendation = days_since_last >= 15
    else:
        can_request_recommendation = True

    # Most Used Ingredients
    most_used_ingredients = (
        RecipeHadIngredient.objects.filter(recipe_id__user=user)
        .values("ingredient_name")
        .annotate(total=Count("ingredient_name"))
        .order_by("-total")[:10]
    )
    ingredients = [
        ingredient["ingredient_name"] for ingredient in most_used_ingredients
    ]
    counts = [int(ingredient["total"]) for ingredient in most_used_ingredients]
    colors = ["#812DAB", "#C39123", "#F58143", "#1E2E2B"] * 3

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), facecolor="none")
    fig.subplots_adjust(hspace=0.5)

    # Bar chart
    if ingredients and counts:
        ax1.barh(ingredients, counts, color=colors)
        ax1.set_xlabel("Usage Count", fontsize=20, color="#f58243")
        ax1.set_title(
            "Top 10 Most Used Ingredients", fontsize=20, weight="bold", color="#f58243"
        )
        ax1.invert_yaxis()
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax1.tick_params(axis="x", labelsize=15, colors="#f58243")
        ax1.tick_params(axis="y", labelsize=15, colors="#f58243")

    # Table
    table_data = [[ing, count] for ing, count in zip(ingredients, counts)]
    if table_data:
        the_table = ax2.table(
            cellText=table_data,
            colLabels=["Ingredient", "Usage Count"],
            cellLoc="center",
            loc="center",
            colColours=["#f58243", "#f58243"],
        )
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(20)
        the_table.scale(1, 2)
        ax2.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300, transparent=True)
    plt.close()
    ingredients_image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    # Daily Recipe Generation Stats
    daily_generation_stats = (
        Recipe.objects.filter(user=user)
        .annotate(day_of_week=ExtractWeekDay("generation_date"))
        .values("day_of_week")
        .annotate(total=Count("id"))
        .order_by("day_of_week")
    )
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    totals = [0] * 7
    for data_point in daily_generation_stats:
        index = (data_point["day_of_week"] - 2) % 7
        totals[index] = data_point["total"]

    if totals:
        plt.figure(figsize=(10, 6), facecolor="none")
        plt.bar(days, totals, color=colors[:7], edgecolor="black")
        plt.xlabel("Day of the Week", fontsize=15, color="#f58243")
        plt.ylabel("Number of Recipe Creations", fontsize=15, color="#f58243")
        plt.title(
            "Recipe Creations per Day of the Week",
            fontsize=20,
            weight="bold",
            color="#f58243",
        )
        plt.grid(True, linestyle="--", linewidth=0.5, color="grey", axis="y")
        plt.tick_params(axis="x", labelsize=15, colors="#f58243")
        plt.tick_params(axis="y", labelsize=15, colors="#f58243")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300, transparent=True)
        plt.close()
        daily_stats_image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()

    context = {
        "ingredients_image_base64": ingredients_image_base64,
        "daily_stats_image_base64": daily_stats_image_base64,
        "first_name": first_name,
        "can_request_recommendation": can_request_recommendation,
        "days_until_next_recommendation": days_until_next_recommendation,
    }

    return render(request, "overview.html", context)


@login_required
def generate_recommendation(request):
    user = request.user

    # Check if the user is eligible for a new recommendation
    last_report = Report.objects.filter(user=user).order_by("-report_date").first()
    if last_report and (now().date() - last_report.report_date).days < 15:
        # Not enough days have passed
        return redirect(
            "statistics_overview"
        )  # Redirect to overview or an error message page

    # Gather user data for the recommendation
    user_ingredients = Ingredient.objects.filter(user=user).values_list(
        "name", flat=True
    )
    favorite_recipes = Recipe.objects.filter(
        user=user, favourite_state=True
    ).values_list("title", flat=True)

    user_profile = {
        "favorite_ingredients": ", ".join(user_ingredients),
        "favorite_recipes": ", ".join(favorite_recipes),
    }

    # Generate recommendation using OpenAIAdapter
    adapter = OpenAIAdapter()
    recommendation_json = adapter.generate_recommendation(user_profile)

    # Ensure recommendation_json is a dict, not a string
    if isinstance(recommendation_json, str):
        recommendation_info = json.loads(
            recommendation_json
        )  # Parse JSON string into Python dictionary
    else:
        recommendation_info = recommendation_json  # Assuming it's already a dict

    if not recommendation_info:
        # Handle case where no recommendation was returned
        return render(
            request,
            "overview.html",
            {
                "error_message": "Failed to generate a recommendation. Please try again later."
            },
        )

    # Save the new recommendation (assuming it's already a string or serializing as needed)
    new_report = Report(
        user=user, report_date=now(), report_info=json.dumps(recommendation_info)
    )
    new_report.save()

    # Redirect or render the page where the recommendation is displayed
    return render(
        request, "view_recommendation.html", {"recommendation": recommendation_info}
    )
