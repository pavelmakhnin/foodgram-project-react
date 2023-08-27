from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Customised Model for User """

    email = models.EmailField(
        verbose_name='email',
        help_text='Enter the email of the User',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        help_text='Enter the email of the User',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first_name',
        help_text='Enter the First Name of the User',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=150,
        help_text='Enter the Last Name of the User',
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    """Model to follow Recipes Authors."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Follower',
        related_name='subscribtion_user',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='subscribtion_author',
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ('user',)

        constraints = (
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_follower_author'),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='not_self_following'
                )
        )

    def __str__(self) -> str:
        return f'{self.user} is subscribed to: {self.author}'

    def clean(self):

        if self.user == self.author:

            raise ValidationError(
                'Self Following is not possible'
            )
