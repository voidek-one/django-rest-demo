import json
import io
import shutil
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from PIL import Image
from contactform.models import FeedbackModel, FilesModel
from contactform.serializers import FeedbackSerializer

client = APIClient


@override_settings(SUSPEND_SIGNALS=True)
class FeedbackListViewTest(APITestCase):
    def setUp(self):
        FeedbackModel.objects.create(
            full_name='test Name',
            email='test@test.ts',
            message='test message'
        )

        FeedbackModel.objects.create(
            full_name='test1 Name',
            email='test1@test.ts',
            message='test1 message'
        )

        FeedbackModel.objects.create(
            full_name='test2 Name',
            email='test2@test.ts',
            message='test2 message'
        )

        FeedbackModel.objects.create(
            full_name='test3 Name',
            email='test3@test.ts',
            message='test3 message'
        )
        self.u = User.objects.create_superuser('test', password='test',
                                               email='test@test.test')
        self.u.save()
        self.normal_token, created = Token.objects.get_or_create(user=self.u)

    def test_get_all_contacts(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('fileupload:send_mail-list')
        response = self.client.get(url, format='json')
        contacts = FeedbackModel.objects.all()
        serializer = FeedbackSerializer(contacts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(SUSPEND_SIGNALS=True)
class GetFeedbackViewTest(APITestCase):
    def setUp(self):
        self.test = FeedbackModel.objects.create(
            full_name='test Name',
            email='test@test.ts',
            message='test message'
        )
        self.test1 = FeedbackModel.objects.create(
            full_name='test1 Name',
            email='test1@test.ts',
            message='test1 message'
        )
        self.test2 = FeedbackModel.objects.create(
            full_name='test2 Name',
            email='test2@test.ts',
            message='test2 message',

        )
        self.test3 = FeedbackModel.objects.create(
            full_name='test3 Name',
            email='test3@test.ts',
            message='test3 message'
        )
        self.u = User.objects.create_superuser('test', password='test',
                                               email='test@test.test')
        self.u.save()
        self.normal_token, created = Token.objects.get_or_create(
            user=self.u)

    def test_get_valid_single_contact(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('fileupload:send_mail-detail',
                      kwargs={'pk': self.test2.pk})
        response = self.client.get(url, format='json')
        contact = FeedbackModel.objects.get(pk=self.test2.pk)
        serializer = FeedbackSerializer(contact)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_contact(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('fileupload:send_mail-detail', kwargs={'pk': 30})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@override_settings(SUSPEND_SIGNALS=True)
class CreateFeedbackViewTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'full_name': 'test Name',
            'email': 'test@test.ts',
            'message': 'test message'
        }
        self.invalid_payload = {
            'full_name': '',
            'email': 'test@test.ts',
            'message': 'test message'
        }

    def test_create_valid_contact(self):
        url = reverse('fileupload:send_mail-list')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_contact(self):
        url = reverse('fileupload:send_mail-list')
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(MEDIA_ROOT='./tmp/media/')
class FileUploadTest(APITestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_file(self):

        url = reverse('fileupload:fileupload-list')
        photo_file = self.generate_photo_file()
        data = {
            'uploaded_file': photo_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        try:
            shutil.rmtree('./tmp/media/')
        except OSError:
            pass


class LogInTest(APITestCase):
    def setUp(self):
        self.u = User.objects.create_user('test', password='test',
                                          email='test@test.test')
        self.u.save()

    def test_log_in(self):
        data = {
            'password': 'test',
            'username': 'test'
        }
        response = self.client.post(
            '/api/v1/auth/token/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(MEDIA_ROOT='./tmp/media/')
class GetFileTest(APITestCase):
    def setUp(self):
        self.u = User.objects.create_superuser('test', password='test',
                                               email='test@test.test')
        self.u.save()
        self.normal_token, created = Token.objects.get_or_create(
            user=self.u)

        self.file1 = FilesModel.objects.create(uploaded_file='test1.test')
        self.file2 = FilesModel.objects.create(uploaded_file='test2.test')

    def test_get_all_files_response(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('fileupload:fileupload-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_file(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('fileupload:fileupload-detail',
                      kwargs={'pk': self.file1.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "pk": self.file1.pk,
            "uploaded_file": f"http://testserver/media/{self.file1.uploaded_file}"
        })
