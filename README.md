# 🍔 Django Food Ordering API

A backend REST API built using **Django** and **Django REST Framework** for managing a food ordering system. This project includes authentication, restaurant management, food items, and order processing.

---

## 🚀 Features

* 🔐 User Registration & Login (JWT Authentication)
* 🌍 Country & City-based restaurant filtering
* 🍽️ Restaurant creation & management (Owner only)
* 🍕 Add & update food items
* 🛒 Order creation with multiple items
* 📊 Food analytics (top & least selling)
* 🔒 Role-based permissions (Customer / Owner)

---

## 🛠️ Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Docker
* JWT (SimpleJWT)
* Swagger (drf-yasg)

---

## 📂 Project Structure

```
project/
│── country/          # Main app
│── manage.py
│── Dockerfile
│── docker-compose.yml
│── .env (not included in repo)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2️⃣ Create .env File

```
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=host.docker.internal
DB_PORT=5432
```

---

### 3️⃣ Run with Docker

```
docker-compose up --build
```

---

### 4️⃣ Access API

```
http://localhost:8000
```

---

## 🔑 Authentication APIs

### Register

`POST /register/`

### Login

`POST /login/`

Returns:

* Access Token
* Refresh Token

---

## 🌍 APIs Overview

### Countries List

`GET /countries/`

### Cities by Country

`GET /countries/{country_name}/cities/`

### Restaurants by City

`GET /countries/{country}/cities/{city}/restaurants/`

---

## 🍽️ Restaurant APIs

### Create Restaurant (Owner)

`POST /restaurants/`

---

## 🍕 Food APIs

### Add Food

`POST /restaurants/{id}/foods/`

### Update Food

`PUT /foods/{id}/`

### View Menu

`GET /restaurants/{slug}/menu/`

---

## 🛒 Order APIs

### Create Order

`POST /orders/`

### Owner Orders

`GET /owner/orders/`

---

## 📊 Analytics API

### Restaurant Food Analytics

`GET /analytics/`

Returns:

* Top selling food
* Least selling food
* Grouped by Country → City → Restaurant

---

## 🔐 Permissions

* **IsAuthenticated** → Logged in users
* **IsOwner** → Restaurant owners only
* **IsCustomer** → Customers only
* **Custom Permissions** for food & restaurant ownership

---

## 📌 Important Notes

* `.env` file is not included for security reasons
* Use `.env.example` as reference
* Do not expose secret keys or database credentials

---

## 👨‍💻 Author

**Army Raiyani**

* Python Developer (Fresher)
* Skills: Django, DRF, Docker, PostgreSQL

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and connect on LinkedIn!
