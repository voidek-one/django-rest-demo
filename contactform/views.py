from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAdminUser
from contactform.models import FeedbackModel, FilesModel
from .serializers import FeedbackSerializer, FileUploadSerializer


class PostOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


class FileUploadView(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = FilesModel.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAdminUser | PostOnly]


class FeedbackView(ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = FeedbackModel.objects.all()
    permission_classes = [IsAdminUser | PostOnly]
