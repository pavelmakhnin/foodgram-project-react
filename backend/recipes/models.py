from django.core.validators import (MinValueValidator, RegexValidator,
                                    MaxValueValidator)
from django.db import models

from users.models import User


class Tag(models.Model):
    """Model for Tags."""

    name = models.CharField(
        verbose_name='Tag Name',
        help_text='Title for Tag',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Hex-code',
        help_text='Hex-code for color, for example: #FF0000',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='The entered value is not a color in the format HEX!'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Slug id',
        help_text='Title for Slug',
        unique=True,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f'{self.name} (color: {self.color})'


class Ingredient(models.Model):
    """Model for Ingredients."""

    name = models.CharField(
        verbose_name='Ingridient Name',
        max_length=200,
        help_text='Title of the Ingredient'
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=20,
        help_text='Unit to measure the Ingredient')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Model for Recipies"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author of the recipe',
        help_text='Author of the Recipe Publishing',
    )
    name = models.CharField(
        verbose_name='Title of the recipe',
        max_length=200,
        help_text='Title for the Recipe Publishing',
    )
    text = models.TextField(
        verbose_name='Description of the recipe',
        help_text='Text to describe the Recipe',
    )
    image = models.ImageField(
        verbose_name='Image of the recipe',
        upload_to='recipes/images',
        help_text='Image to illustrate the Recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsForRecipeInAmount',
        related_name='recipes',
        verbose_name='Ingridients of the recipe',
        help_text='Ingridients needed for the Recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes',
        verbose_name='Tag of the recipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Cooking time is at least 1 minute, if you just read :).'
                ),
            MaxValueValidator(
                2880, 'Cooking time not more than 2880 minutes (2 days)).'
                )
        ],
        verbose_name='Coocking time',
        help_text='Coocking time (in minutes)',
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication day',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name}'


class IngredientsForRecipeInAmount(models.Model):
    """
    An intermediate Model for Determining.

        the Amount of Ingredients needed for Recipe
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ingredients of the Recipe',
    )

    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount of the Ingredient',
        help_text='Write the required Amount of this Ingredient',
        validators=[
            MinValueValidator(
                1, 'You must specify a volume of at least 1 unit.'
                ),
            MaxValueValidator(
                100, 'You must specify a volume not more than 100 units.'
                )
        ],
    )

    class Meta:
        verbose_name = 'IngredientRecipe'
        verbose_name_plural = 'IngredientsRecipe'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_to_recipe',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} for {self.recipe} : {self.amount}'


class RecipeTags(models.Model):
    """Model to Tags."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Tag'
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f' Tag {self.tag} for recipe {self.recipe} '


class FavoriteRecipes(models.Model):
    """Model to add Recipes to favorite List."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Recipe',
    )

    class Meta:
        verbose_name = 'FavoriteRecipes'
        verbose_name_plural = 'FavoriteRecipes'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_user_recipe',
            )
        ]

    def __str__(self):
        return f'Recipe {self.recipe} in favorite list for {self.user}'


class ShoppingList(models.Model):
    """Model to form shopping List."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='Recipe',
    )

    class Meta:
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping lists'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list_recipe',
            )
        ]

    def __str__(self):
        return f'{self.recipe} in shopping list for {self.user}'
