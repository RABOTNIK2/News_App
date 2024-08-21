from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, name, age, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
   
        user = self.model(email=email, name=name, age=age, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, name=None , age=18, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, name, age, **extra_fields)

    def create_superuser(self, email, password, name, age, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, name, age, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Электронная почта",
        unique=True,
        max_length=255,
        blank=False
    )
    name = models.CharField("Имя", max_length=60, blank=False)
    age = models.PositiveIntegerField("Возраст" ,validators=[MinValueValidator(18), MaxValueValidator(120)], default=18, null=False)
    image = models.ImageField("Фото профиля", upload_to="images/", default="default.jpg", blank=True)

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "age"]

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
class Category(models.Model):
    name = models.CharField("Название категории", max_length=60)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class News(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    news_text = models.TextField("Содержание")
    news_image = models.ImageField("Фото статьи", upload_to='news', blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    news_posted_at = models.DateTimeField("Дата публикации", default=timezone.now)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Новости"
        ordering = ["-news_posted_at"]

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    comment_text = models.TextField("Содержание")
    comment_to_news = models.ForeignKey(News, verbose_name="К посту", on_delete=models.CASCADE)
    comment_posted_at = models.DateTimeField("Опубликован", default=timezone.now)

    def __str__(self) -> str:
        return self.comment_text
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-comment_posted_at"]


# Create your models here.
