import requests
import random
import string
import json


class AutomatedBot:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        self.number_of_users = config["number_of_users"]
        self.max_posts_per_user = config["max_posts_per_user"]
        self.max_likes_per_user = config["max_likes_per_user"]
        self.base_url = "http://localhost:8000"
        self.jwt_token = None
        self.created_posts = None

    def _generate_username(self):
        username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        print("Username created: ", username)
        return username

    def _generate_password(self):
        password = "".join(random.choices(string.ascii_letters + string.digits, k=18))
        return password

    def _signup(self, username, email, password):
        print(f"Signup user: {username}")
        url = self.base_url + "/api/auth/signup/"
        headers = {
            "Content-Type": "application/json"
        }
        data = {"username": username, "email": email, "password": password}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"Failed to signup user: {response.content}")

    def _login(self, username, email, password):
        print(f"Login user: {username}")
        url = self.base_url + "/api/auth/login/"
        headers = {
            "Content-Type": "application/json"
        }
        data = {"username": username, "email": email, "password": password}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.jwt_token = response.json()["access"]
        else:
            raise ValueError(f"Failed to login user: {response.content}")

    def _create_post(self, content):
        url = self.base_url + "/api/post/create/"
        headers = {"Authorization": f"Bearer {self.jwt_token}", "Content-Type": "application/json"}
        data = {"title": content["title"], "body": content["body"]}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f'Failed to create post: {response.content}')

    def _like_post(self, post_id):
        url = self.base_url + f"/api/post/{post_id}/like/"
        headers = {"Authorization": f"Bearer {self.jwt_token}", "Content-Type": "application/json"}
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to like post: {response.content}")

    def run(self):
        for i in range(self.number_of_users):
            if self.created_posts is None:
                self.created_posts = []
            username = self._generate_username()
            password = self._generate_password()
            email = f"{username}@bot.com"
            self._signup(username, email, password)
            self._login(username, email, password)
            num_posts = random.randint(1, self.max_posts_per_user)
            print(f"Create {num_posts} posts:")
            for j in range(num_posts):
                print(f"{j + 1} post")
                content = dict(title=f"Random post title: {j}",
                               body=f"Random post data: {j}")
                self.created_posts.append(self._create_post(content))

            posts_ids = [post["id"] for post in self.created_posts]
            print(posts_ids)
            num_likes = random.randint(1, self.max_likes_per_user)
            print(f"Create {num_likes} likes:")
            for j in range(num_likes):
                print(f"{j + 1} like")
                post_id = random.choice(posts_ids)
                self._like_post(post_id)


if __name__ == "__main__":
    bot = AutomatedBot("config.json")
    bot.run()
