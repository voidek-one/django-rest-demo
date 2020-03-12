from django.core.mail import EmailMultiAlternatives
from contactform.models import FilesModel
from django.template.loader import render_to_string


def send_email(message, email, full_name, files_to_send):
    htmly = render_to_string('simple.html', {'full_name': full_name,
                                             'email': email,
                                             'message': message})
    email_message = EmailMultiAlternatives(subject='New message', body=message,
                                           to=["psycide@gmail.com"])
    if files_to_send:
        file_list = files_to_send
        for file_pk in file_list:
            obj = FilesModel.objects.get(pk=file_pk)
            email_message.attach_file(obj.uploaded_file.path)
    email_message.attach_alternative(htmly, "text/html")
    email_message.send()
