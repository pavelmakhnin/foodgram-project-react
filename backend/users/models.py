from django.db import models

from django.contrib.auth.models import AbstractUser

# from django.db.models import F, Q


class User(AbstractUser):
    """Customised Model for User """

    email = models.EmailField(
        verbose_name='email',
        help_text='Enter the email of the User',
        max_length=254,
        unique=True,
        null=False
    )
    username = models.CharField(
        verbose_name='Username',
        help_text='Enter the email of the User',
        max_length=150,
        unique=True,
        null=False
    )
    first_name = models.CharField(
        verbose_name='first_name',
        help_text='Enter the First Name of the User',
        max_length=150,
        blank=True,
        null=False
    )
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=150,
        help_text='Enter the Last Name of the User',
        blank=True,
        null=False
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=150,
        blank=False,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
#        ordering = ('username',)

    def __str__(self):
        return self.email


class Subscribe(models.Model):
    """Model to follow Recipes Authors"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Follower',
        related_name='user_follower',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='author_to_follow',
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ('user',)

        constraints = (
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follower_author'),
            # models.CheckConstraint(
            #     check=~Q(user=F('author')),
            #     name='self_following'
            #     )
        )

    def __str__(self) -> str:
        return f'{self.user} is subscribed to: {self.author}'
