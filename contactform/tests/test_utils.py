import shutil
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from contactform.utils import send_email
from contactform.models import FilesModel
from django.core import mail


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    MEDIA_ROOT='./tmp/media/')
class TestSendEmail(TestCase):
    def setUp(self):
        self.test_file = SimpleUploadedFile('test.txt', b'test')
        self.f = FilesModel.objects.create(uploaded_file=self.test_file)

    def test_send_email(self):
        send_email(
            message='test message',
            email='psycide@gmail',
            full_name='test name',
            files_to_send=[self.f.pk]
            )
        self.assertEqual(len(mail.outbox), 1)

    def tearDown(self):
        try:
            shutil.rmtree('./tmp/media/')
        except OSError:
            pass
