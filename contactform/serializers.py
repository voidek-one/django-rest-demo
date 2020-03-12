from rest_framework import serializers
from .models import FilesModel, FeedbackModel


class FileUploadSerializer(serializers.ModelSerializer):
    '''
    Serializing file uploading data
    '''
    class Meta:
        model = FilesModel
        fields = ['pk', 'uploaded_file']


class FeedbackSerializer(serializers.ModelSerializer):
    '''
    Serializing contact form data
    '''

    files_to_send = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = FeedbackModel
        fields = ['full_name', 'email', 'message', 'files_to_send', 'id']
