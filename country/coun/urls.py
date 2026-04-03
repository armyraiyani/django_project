from django.urls import path
from .views import CityRestaurantsView, CountryCitiesView, CountryListView, CreateOrderView, CreateRestaurantView,  OwnerOrdersView,   RegisterView, LoginView,  RestaurantFoodAnalytics, RestaurantMenuView, UpdateFoodView, AddFoodView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('login/', LoginView.as_view(), name='login'),
    
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("countries/", CountryListView.as_view(), name="countries"),
        
    path("restaurants/create/", CreateRestaurantView.as_view()),
    
    path("restaurant/<int:restaurant_id>/add-food/", AddFoodView.as_view()),       
    path("food/<int:food_id>/update/",UpdateFoodView.as_view()),
        
    path("countries/<str:country_name>/cities/",CountryCitiesView.as_view()),
     
    path("countries/<str:country_name>/<str:city>/restaurants/",CityRestaurantsView.as_view()),

    path("restaurant/<slug:slug>/menu/",RestaurantMenuView.as_view()),
    
    path("orders/create/", CreateOrderView.as_view()),
     
    
    path("owner/orders/", OwnerOrdersView.as_view()),
    
    path("restaurant-analytics/", RestaurantFoodAnalytics.as_view()),

]