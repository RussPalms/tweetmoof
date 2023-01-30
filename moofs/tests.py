from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Moof

# Create your tests here .
User = get_user_model()

class MoofTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Moof.objects.create(content="my first moof",
                                       user=self.user)
        Moof.objects.create(content="my first moof",
                                       user=self.user)
        Moof.objects.create(content="my first moof",
                                       user=self.userb)
        self.currentCount = Moof.objects.all().count()

    def test_moof_created(self):
        moof_obj =Moof.objects.create(content='my second moof', 
                                      user=self.user)
        self.assertEqual(moof_obj.id, 4)
        self.assertEqual(moof_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_moof_list(self):
        client = self.get_client()
        response = client.get("/api/moofs/")
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_moofs_related_name(self):
        user = self.user
        self.assertEqual(user.moofs.count(), 2)

    def test_moof_list(self):
        client = self.get_client()
        response = client.get("/api/moofs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/moofs/action/", 
                               {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        user = self.user
        my_like_instances_count = user.mooflike_set.count()
        self.assertEqual(my_like_instances_count, 1)
        my_related_likes = user.moof_user.count()
        self.assertEqual(my_like_instances_count, my_related_likes)

        #print(response.json())

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/moofs/action/", 
                               {"id": 2, "action": "like"})
        response = client.post("/api/moofs/action/", 
                               {"id": 2, "action": "unlike"})
        like_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 0)
        print(response.json())

    def test_action_remoof(self):
        client = self.get_client()
        response = client.post("/api/moofs/action/",
                               {"id": 2, "action": "remoof"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_moof_id = data.get("id")
        self.assertNotEqual(2, new_moof_id)
        self.assertEqual(self.currentCount + 1, new_moof_id)

    def test_moof_create_api_view(self):
        request_data = {"content": "This is my test moof"}
        client = self.get_client()
        response = client.post("/api/moofs/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_moof_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_moof_id)

    def test_moof_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/moofs/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_moof_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/moofs/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/moofs/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/moofs/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)


