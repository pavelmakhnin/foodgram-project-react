from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, IngredientsForRecipeInAmount


def add_ingridient(ingredients, recipe):
    for ingredient in ingredients:
        amount = ingredient['amount']
        ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

        IngredientsForRecipeInAmount.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )


def get_shopping_cart(request):
    ingredients = (
        IngredientsForRecipeInAmount.objects.filter(
            recipe__in_shopping_list__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by())
    buy_list_text = [
        '{} - {} {}.'.format(*ingredient) for ingredient in ingredients]
    response = HttpResponse(
        'Список покупок с сайта Foodgram:\n'
        + '\n'.join(buy_list_text),
        content_type='text/plain'
    )
    response['Content-Disposition'] = (
        'attachment; filename=shopping-list.txt'
    )
    return response
