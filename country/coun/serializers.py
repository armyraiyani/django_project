from django.contrib.auth import authenticate
from .models import City, User
from rest_framework import serializers
from .models import Country, Food, Restaurant
from django.urls import reverse
from .models import Country, Order, OrderItem, Food, Restaurant


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        
        if not user:
            raise serializers.ValidationError("invalid credentials")
        return user
   
class CreateRestaurantSerializer(serializers.ModelSerializer):

    country = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Country.objects.all()
    )

    city = serializers.CharField()

    class Meta:
        model = Restaurant
        fields = ["name", "country", "city", "rating"]

    
    
class FoodCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ["name", "price"]
        
class CountrySerializer(serializers.ModelSerializer):
    restaurant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "country_code", "restaurant_count"]
        
class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ["id", "name", "country"] 
   
class RestaurantSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="city.name")
    country = serializers.CharField(source="country.name")
    
    class Meta:
        model = Restaurant
        fields = ["id", "name", "city", "country", "rating", "slug"]
        
class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ["id", "name", "price"]
        
class OrderItemInputSerializer(serializers.Serializer):
    food = serializers.IntegerField()
    quantity = serializers.IntegerField()
        
class OrderCreateSerializer(serializers.Serializer):
    restaurant = serializers.IntegerField()
    items = OrderItemInputSerializer(many=True)
        
class OrderItemSerializer(serializers.ModelSerializer):

    food_name = serializers.CharField(source="food.name", read_only=True)
    price = serializers.DecimalField(source="food.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "food",
            "food_name",
            "price",
            "quantity"
        ]
        
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "restaurant",
            "restaurant_name",
            "total_amount",
            "status",
            "created_at",
            "items"
        ]