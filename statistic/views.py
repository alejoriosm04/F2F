import io
import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from matplotlib import pyplot as plt
from kitchen.models import Ingredient, RecipeHadIngredient
from recipe.models import Recipe
from django.db.models.functions import ExtractWeekDay
from django.db.models import Count
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

@login_required
def overview(request):
    user = request.user
    first_name = user.first_name or user.username

    # Most Used Ingredients
    most_used_ingredients = RecipeHadIngredient.objects.filter(recipe_id__user=user).values('ingredient_name').annotate(total=Count('ingredient_name')).order_by('-total')[:10]
    ingredients = [ingredient['ingredient_name'] for ingredient in most_used_ingredients]
    counts = [ingredient['total'] for ingredient in most_used_ingredients]
    colors = ['#812DAB', '#C39123', '#F58143', '#1E2E2B'] * 3  # Repeat colors as needed

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), facecolor='none')
    fig.subplots_adjust(hspace=0.5)

    # Bar chart
    if ingredients and counts:
        ax1.barh(ingredients, counts, color=colors)
        ax1.set_xlabel('Usage Count')
        ax1.set_title('Top 10 Most Used Ingredients', fontsize=14, weight='bold', color='#333333')
        ax1.invert_yaxis()
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Table
    table_data = [[ing, count] for ing, count in zip(ingredients, counts)]
    if table_data:
        the_table = ax2.table(
            cellText=table_data,
            colLabels=["Ingredient", "Usage Count"],
            cellLoc='center',
            loc='center',
            colColours=['#F58143', '#F58143']  # Orange color for headers
        )
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        the_table.scale(1, 2)
        ax2.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, transparent=True)
    plt.close()
    ingredients_image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Daily Recipe Generation Stats
    daily_generation_stats = Recipe.objects.filter(user=user) \
                                           .annotate(day_of_week=ExtractWeekDay('generation_date')) \
                                           .values('day_of_week') \
                                           .annotate(total=Count('id')) \
                                           .order_by('day_of_week')    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    totals = [0] * 7
    for data_point in daily_generation_stats:
        index = (data_point['day_of_week'] - 2) % 7
        totals[index] = data_point['total']

    if totals:
        plt.figure(figsize=(10, 6), facecolor='none')
        plt.bar(days, totals, color=colors[:7], edgecolor='black')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Recipe Creations')
        plt.title('Recipe Creations per Day of the Week')
        plt.grid(True, linestyle='--', linewidth=0.5, color='grey', axis='y')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, transparent=True)
        plt.close()
        daily_stats_image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

    context = {
        'ingredients_image_base64': ingredients_image_base64,
        'daily_stats_image_base64': daily_stats_image_base64,
        'first_name': first_name,
    }

    return render(request, 'overview.html', context)
