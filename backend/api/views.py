from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminPermission
from recipes.models import (Recipe, ShoppingList, Ingredient, Tag,
                            FavoriteRecipes)
from users.models import (User, Subscribe)
from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer, IngredientSerializer,
                          TagSerializer, SubscriptionSerializer)
from .utils import get_shopping_cart


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeSerializer

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if FavoriteRecipes.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Recipe is added.')

        FavoriteRecipes.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if not FavoriteRecipes.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Recipe is not in Favorite Recipes or it is deleted.'
            )

        favorite = get_object_or_404(FavoriteRecipes, user=user, recipe=recipe)
        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Recipe is addedto Shopping List.'
            )

        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not ShoppingList.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Recipe is not in Shopping List or it is deleted..'
            )

        shopping_cart = get_object_or_404(
            ShoppingList,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        try:
            return get_shopping_cart(request)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['GET'],
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(user_follower__user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if user == author:
            raise exceptions.ValidationError(
                'Subscription to yourself is not possible.'
            )
        if Subscribe.objects.filter(
            user=user,
            author=author
        ).exists():
            raise exceptions.ValidationError('Subscribtion exists.')

        Subscribe.objects.create(user=user, author=author)
        serializer = self.get_serializer(author)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)

        if not Subscribe.objects.filter(
            user=user,
            author=author
        ).exists():
            raise exceptions.ValidationError(
                'Subscription not registered or is already been deleted.'
            )
        Subscribe.objects.get(user=user, author=author).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
