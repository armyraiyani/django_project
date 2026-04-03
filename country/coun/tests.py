from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Country, City, Restaurant, Food

User = get_user_model()


class APITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="123456",
            role="owner"
        )

        self.customer = User.objects.create_user(
            username="customer",
            password="123456",
            role="customer"
        )

        self.country = Country.objects.create(
            name="India",
            country_code="IN"
        )

        self.city = City.objects.create(
            name="Surat",
            country=self.country
        )

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            owner=self.owner,
            country=self.country,
            city=self.city,
            rating=4.5,
            slug="test-restaurant"   
        )

        self.food = Food.objects.create(
            name="Pizza",
            price=100,
            restaurant=self.restaurant
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # ================= AUTH =================

    def test_register(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "password": "123456",
            "email": "newuser@gmail.com",
            "role": "customer"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        url = reverse("login")
        data = {
            "username": "owner",
            "password": "123456"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)

    # ================= RESTAURANT =================

    def test_create_restaurant(self):
        self.authenticate(self.owner)

        response = self.client.post("/restaurants/create/", {
            "name": "Spice Hub",
            "country": "India",
            "city": "Ahmedabad",
            "rating": 4.2
        })

        self.assertEqual(response.status_code, 201)

    def test_customer_cannot_create_restaurant(self):
        self.authenticate(self.customer)

        response = self.client.post("/restaurants/create/", {
            "name": "Fail Restaurant",
            "country": "India",
            "city": "Delhi",
            "rating": 4.0
        })

        self.assertEqual(response.status_code, 403)

    # ================= FOOD =================

    def test_add_food(self):
        self.authenticate(self.owner)

        response = self.client.post(
            f"/restaurant/{self.restaurant.id}/add-food/",
            {"name": "Burger", "price": 150}
        )

        self.assertEqual(response.status_code, 200)

    def test_other_owner_cannot_add_food(self):
        other_owner = User.objects.create_user(
            username="owner2",
            password="123456",
            role="owner"
        )

        self.authenticate(other_owner)

        response = self.client.post(
            f"/restaurant/{self.restaurant.id}/add-food/",
            {"name": "Burger", "price": 150}
        )

        self.assertEqual(response.status_code, 403)

    def test_update_food(self):
        self.authenticate(self.owner)

        response = self.client.put(
            f"/food/{self.food.id}/update/",
            {"price": 200}
        )

        self.assertEqual(response.status_code, 200)

    def test_update_food_not_owner(self):
        other_owner = User.objects.create_user(
            username="owner3",
            password="123456",
            role="owner"
        )

        self.authenticate(other_owner)

        response = self.client.put(
            f"/food/{self.food.id}/update/",
            {"price": 300}
        )

        self.assertEqual(response.status_code, 403)

    # ================= COUNTRY =================

    def test_get_countries(self):
        self.authenticate(self.owner)

        response = self.client.get("/countries/")
        self.assertEqual(response.status_code, 200)

    def test_country_cities(self):
        self.authenticate(self.owner)

        response = self.client.get(
            f"/countries/{self.country.name}/cities/"
        )

        self.assertEqual(response.status_code, 200)

    def test_city_restaurants(self):
        self.authenticate(self.owner)

        response = self.client.get(
            f"/countries/{self.country.name}/{self.city.name}/restaurants/"
        )

        self.assertEqual(response.status_code, 200)

    # ================= MENU =================

    def test_restaurant_menu(self):
        self.authenticate(self.owner)

        response = self.client.get(
            f"/restaurant/{self.restaurant.slug}/menu/"
        )

        self.assertEqual(response.status_code, 200)

    # ================= ORDER =================

    def test_create_order(self):
        self.authenticate(self.customer)

        response = self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [
                {"food": self.food.id, "quantity": 2}
            ]
        }, format="json")

        self.assertEqual(response.status_code, 200)

    def test_owner_cannot_order(self):
        self.authenticate(self.owner)

        response = self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [
                {"food": self.food.id, "quantity": 1}
            ]
        }, format="json")

        self.assertEqual(response.status_code, 403)

    def test_order_without_items(self):
        self.authenticate(self.customer)

        response = self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id
        }, format="json")

        self.assertEqual(response.status_code, 400)

    def test_invalid_food(self):
        self.authenticate(self.customer)

        response = self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [{"food": 999, "quantity": 1}]
        }, format="json")

        self.assertEqual(response.status_code, 400)

    def test_my_orders(self):
        self.authenticate(self.customer)

        self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [{"food": self.food.id, "quantity": 1}]
        }, format="json")

        response = self.client.get("/orders/my/")
        self.assertEqual(response.status_code, 200)

    def test_owner_orders(self):
        self.authenticate(self.customer)

        self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [{"food": self.food.id, "quantity": 1}]
        }, format="json")

        self.authenticate(self.owner)

        response = self.client.get("/owner/orders/")
        self.assertEqual(response.status_code, 200)

    # ================= ANALYTICS =================

    def test_restaurant_analytics(self):
        self.authenticate(self.customer)

        self.client.post("/orders/create/", {
            "restaurant": self.restaurant.id,
            "items": [{"food": self.food.id, "quantity": 3}]
        }, format="json")

        self.authenticate(self.owner)

        response = self.client.get("/restaurant-analytics/")
        self.assertEqual(response.status_code, 200)