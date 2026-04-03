from .serializers import  CountrySerializer, CreateRestaurantSerializer, FoodCreateSerializer, OrderCreateSerializer, RegisterSerializer, LoginSerializer, FoodSerializer, OrderSerializer, RestaurantSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import City, Country, Food, Restaurant, Order
from rest_framework.generics import ListAPIView
from django.db.models import Count, Sum
from coun.models import OrderItem
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsCustomer, IsOwner, IsRestaurantOwner, IsFoodOwner



# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=RegisterSerializer
    )
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
          
            serializer.save()
            return Response({"message": "user register  successfully"}, status=201)
        return Response(serializer.errors, status=400)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer 
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            
            refresh = RefreshToken.for_user(user)

            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=200)

        return Response(serializer.errors, status=400)
    
class CountryListView(ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Country.objects.all().annotate(restaurant_count=Count("restaurants"))

        
class CreateRestaurantView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(request_body=CreateRestaurantSerializer)
    def post(self, request):

        serializer = CreateRestaurantSerializer(data=request.data)

        if serializer.is_valid():

            validated_data = serializer.validated_data

            country = validated_data.get("country")
            city_name = validated_data.get("city")

            city, _ = City.objects.get_or_create(
                name=city_name,
                country=country
            )

            validated_data.pop("city")

            restaurant = Restaurant.objects.create(
                owner=request.user,
                country=country,
                city=city,
                **validated_data
            )

            print("Restaurant created:", restaurant)

            return Response(
                RestaurantSerializer(restaurant).data,
                status=201
            )

        else:
            print("Errors:", serializer.errors)
            return Response(serializer.errors, status=400)
        
class AddFoodView(APIView):
    permission_classes = [IsAuthenticated, IsOwner, IsRestaurantOwner]
    @swagger_auto_schema(request_body=FoodCreateSerializer)

    def post(self, request, restaurant_id):
     
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        self.check_object_permissions(request, restaurant)

        serializer = FoodCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data)

        return Response(serializer.errors)
    
class UpdateFoodView(APIView):
    permission_classes = [IsAuthenticated, IsOwner, IsFoodOwner]
    @swagger_auto_schema(request_body=FoodSerializer)

    def put(self, request, food_id):

        food = get_object_or_404(Food, id=food_id)
        
        self.check_object_permissions(request, food)

        serializer = FoodSerializer(food, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
   
      

class CountryCitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, country_name):

        cities = (
            Restaurant.objects
            .filter(country__name__iexact=country_name)
            .values_list("city__name", flat=True)
            .distinct()
        )

        return Response({
            "country": country_name,
            "cities": list(cities)
        })
        
class CityRestaurantsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, country_name, city):

        restaurants = Restaurant.objects.filter(
            country__name__iexact=country_name,
            city__name__iexact=city
        )

        data = [
            {
                "name": r.name,
                "slug": r.slug
            }
            for r in restaurants
        ]

        return Response({
            "country": country_name,
            "city": city,
            "restaurants": data
        })
    
    
class RestaurantMenuView(ListAPIView):

    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        restaurant_slug = self.kwargs["slug"]

        return Food.objects.filter(
            restaurant__slug=restaurant_slug
        )


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @swagger_auto_schema(request_body=OrderCreateSerializer)
    def post(self, request):

        serializer = OrderCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data

        restaurant_id = validated_data.get("restaurant")
        items = validated_data.get("items")

        if not items:
            return Response({"error": "Items are required"}, status=400)

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant
        )

        total = 0
        order_items = []

        for item in items:
            food = get_object_or_404(Food, id=item["food"])

            if food.restaurant != restaurant:
                return Response({
                    "error": f"{food.name} does not belong to this restaurant"
                }, status=400)

            quantity = item.get("quantity", 1)

            order_items.append(
                OrderItem(
                    order=order,
                    food=food,
                    quantity=quantity
                )
            )

            total += food.price * quantity

        OrderItem.objects.bulk_create(order_items)

        order.total_amount = total
        order.save()

        order = Order.objects.select_related(
            "customer", "restaurant"
        ).prefetch_related(
            "items"  
        ).get(id=order.id)

        return Response({
            "message": "Order placed successfully",
            "order": OrderSerializer(order).data
        }, status=201)
    
    
class OwnerOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.filter(
            restaurant__owner=self.request.user
        )
        
        
class RestaurantFoodAnalytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = (OrderItem.objects.values("food__restaurant__country__name","food__restaurant__city__name","food__restaurant__name","food__name")                                                                          
            .annotate(total_sold=Sum("quantity"))
        )

        result = {}

        # Group data manually
        for item in data:
            country = item["food__restaurant__country__name"]
            city = item["food__restaurant__city__name"]
            restaurant = item["food__restaurant__name"]
            food = item["food__name"]
            total = item["total_sold"]
            result.setdefault(country, {})
            result[country].setdefault(city, {})
            result[country][city].setdefault(restaurant, [])
            result[country][city][restaurant].append(
                {"food": food, "total_sold": total}
                
            )

        # Now calculate top & least
        final_result = {}

        for country, cities in result.items():
            final_result[country] = {}

            for city, restaurants in cities.items():
                final_result[country][city] = {}

                for restaurant, foods in restaurants.items():
                    foods_sorted = sorted(
                        foods, key=lambda x: x["total_sold"]
                    )

                    least = foods_sorted[0]
                    top = foods_sorted[-1]

                    final_result[country][city][restaurant] = {
                        "top_selling": top,
                        "least_selling": least
                    }
    
        return Response(final_result)
    