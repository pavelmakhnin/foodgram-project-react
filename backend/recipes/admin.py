from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe,
    IngredientsForRecipeInAmount,
    FavoriteRecipes, ShoppingList
)

EMPTY_VALUE = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tags Administration Model"""
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredients Administration Model"""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientsForRecipeInAmountInLine(admin.TabularInline):
    """Presentation of Ingredients, Amounts"""
    model = IngredientsForRecipeInAmount
    extra = 1
    min_num = 1


@admin.register(IngredientsForRecipeInAmount)
class IngredientsForRecipeInAmountAdmin(admin.ModelAdmin):
    """Presentation of Ingredients,
      Amounts for Recipes in administration Bar"""
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipes Administration Model"""
    list_display = (
        'name',
        'author',
        'added_to_favorites'
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    inlines = (IngredientsForRecipeInAmountInLine,)
    empty_value_display = EMPTY_VALUE

    def added_to_favorites(self, obj):
        return obj.to_favorites_recipe.count()


@admin.register(FavoriteRecipes)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = EMPTY_VALUE
