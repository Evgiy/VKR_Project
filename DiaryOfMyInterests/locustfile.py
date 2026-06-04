from locust import HttpUser, task, between
import random


class WebsiteUser(HttpUser):

    wait_time = between(1, 3)

    token = None

    # ==========================================
    # АВТОРИЗАЦИЯ
    # ==========================================

    def on_start(self):

        # логин через API
        response = self.client.post(
            "/api/users/api/login/",
            json={
                "email": "test@test.com",
                "password": "12345678"
            }
        )

        # если логин успешный
        if response.status_code == 200:

            data = response.json()

            self.token = data["token"]

            # добавляем токен ко всем запросам
            self.client.headers.update({
                "Authorization": f"Token {self.token}"
            })

    # ==========================================
    # МОИ ОТЗЫВЫ
    # ==========================================

    @task(2)
    def my_reviews(self):

        self.client.get("/api/main/api/my_reviews/")

    # ==========================================
    # РЕКОМЕНДАЦИИ
    # ==========================================

    @task(2)
    def recommendations(self):

        self.client.get("/api/main/api/my_recommendations/")

    # ==========================================
    # СОЗДАНИЕ ОТЗЫВА
    # ==========================================

    @task(1)
    def create_review(self):

        self.client.post(
            "/api/main/api/create_review/book/",
            data={
                "book_name": f"Test Book {random.randint(1, 1000000)}",
                "rating": 5,
                "review_text": "Очень хорошая книга"
            }
        )

    # ==========================================
    # СТРАНИЦА ЛОГИНА
    # ==========================================

    @task(1)
    def login_page(self):

        self.client.get("/users/login/")

    # ==========================================
    # СТРАНИЦА РЕГИСТРАЦИИ
    # ==========================================

    @task(1)
    def register_page(self):

        self.client.get("/users/")