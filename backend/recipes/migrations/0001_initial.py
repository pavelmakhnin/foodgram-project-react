# Generated by Django 2.2.28 on 2023-08-22 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title of the Ingredient', max_length=200, verbose_name='Ingridient')),
                ('measurement_unit', models.CharField(help_text='Unit to measure the Ingredient', max_length=200, verbose_name='Measurement unit')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='IngredientsForRecipeInAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Write the required Amount of this Ingredient', verbose_name='Amount of the Ingredient')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.Ingredient', verbose_name='Ingredients of the Recipe')),
            ],
            options={
                'verbose_name': 'Ingredient for the recipe',
                'verbose_name_plural': 'Ingredients for the recipe',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title for the Recipe Publishing', max_length=200, verbose_name='Title of the recipe')),
                ('text', models.TextField(help_text='Text to describe the Recipe', verbose_name='Description of the recipe')),
                ('image', models.ImageField(help_text='Image to illustrate the Recipe', upload_to='recipes/images', verbose_name='Image of the recipe')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='Coocking time')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication day')),
                ('author', models.ForeignKey(help_text='Author of the Recipe Publishing', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Author of the recipe')),
                ('ingredients', models.ManyToManyField(help_text='Ingridients needed for the Recipe', through='recipes.IngredientsForRecipeInAmount', to='recipes.Ingredient', verbose_name='Ingridients of the recipe')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Title for Tag', max_length=200, unique=True, verbose_name='Tag')),
                ('color', models.CharField(help_text='Hex-code for color, for example: #FF0000', max_length=7, unique=True, verbose_name='Hex-code')),
                ('slug', models.SlugField(help_text='Title for Slug', max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_to_shopping', to='recipes.Recipe', verbose_name='Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_shopping', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Shopping list',
                'verbose_name_plural': 'Shopping lists',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='Tag of the recipe'),
        ),
        migrations.AddField(
            model_name='ingredientsforrecipeinamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.Recipe', verbose_name='Recipe'),
        ),
        migrations.CreateModel(
            name='FavoriteRecipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_favorites_recipe', to='recipes.Recipe', verbose_name='Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_favorites_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Ingredient for the recipe',
                'verbose_name_plural': 'Ingredients for the recipe',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_user_recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredientsforrecipeinamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_to_recipe'),
        ),
        migrations.AddConstraint(
            model_name='favoriterecipes',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_user_recipe'),
        ),
    ]
