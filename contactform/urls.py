'''
Url settings for endpoints
'''
from .views import FileUploadView, FeedbackView
from rest_framework.routers import DefaultRouter
app_name = "fileupload"

router = DefaultRouter()
router.register(r'feedback', FeedbackView, basename='send_mail')
router.register(r'upload', FileUploadView, basename='fileupload')
urlpatterns = router.urls
