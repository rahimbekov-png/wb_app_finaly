from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(null=True, blank=True)

    STATUS_CHOICES = (
        ("gold", "gold"),
        ("silver", "silver"),
        ("bronze", "bronze"),
        ("simple", "simple"),
    )

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="simple"
    )
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}" if self.first_name else self.username


class Category(models.Model):
    category_image = models.ImageField(upload_to="photo_category")
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=32, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub')

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_name = models.CharField(max_length=64)
    price = models.PositiveIntegerField()
    article = models.PositiveSmallIntegerField(unique=True)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory_product')
    product_video = models.FileField(upload_to='product_video/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    product_type = models.BooleanField(default=None, null=True, blank=True)

    def get_average_rating(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings if i.rating) / ratings.count(), 1)
        return 0.0

    def get_count_people(self):
        return self.product_review.count()

    def __str__(self):
        return f'{self.product_name}, {self.subcategory}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photo_product')
    image = models.ImageField(upload_to='product_image/')


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True
    )
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'Корзина {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} x {self.quantity}'