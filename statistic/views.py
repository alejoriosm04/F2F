import io
import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from matplotlib import pyplot as plt
from kitchen.models import Ingredient
from django.db.models.functions import TruncDay
from django.db.models import Count


# Use a non-interactive Matplotlib backend to prevent a runtime error from
# starting a Matplotlib GUI outside of main thread.
# See also: https://stackoverflow.com/q/69924881
import matplotlib
matplotlib.use('agg')

@login_required
def overview(request):
    ingredients_per_day = Ingredient.objects.annotate(day=TruncDay('created_at')).values('day').annotate(total=Count('id')).order_by('day')
    days = [ingredient['day'] for ingredient in ingredients_per_day]
    totals = [ingredient['total'] for ingredient in ingredients_per_day]

    cumulative_totals = []
    current_total = 0
    for total in totals:
        current_total += total
        cumulative_totals.append(current_total)

    plt.figure(figsize=(10, 6))
    plt.plot(days, cumulative_totals, marker='o', linestyle='-', color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Number of Ingredients')
    plt.title('Cumulative Ingredients Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close()
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    context = {'image_base64': image_base64}
    return render(request, 'overview.html', context)
