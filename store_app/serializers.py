from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (
    UserProfile, Category, SubCategory, Product,
    ProductImage, Review, Cart, CartItem
)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'age', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_sub']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer(read_only=True)
    photo_product = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'price', 'subcategory',
            'product_type', 'photo_product', 'average_rating', 'count_people'
        ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_product = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'subcategory_product']


class ProductDetailSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(read_only=True, many=True)
    subcategory = SubCategoryListSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'price', 'subcategory', 'description',
            'created_date', 'article', 'product_video', 'photo_product',
            'average_rating', 'count_people'
        ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']


    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['id', 'user']

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Неверный логин или пароль')
        attrs['user'] = user
        return attrs