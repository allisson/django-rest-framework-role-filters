from rest_framework import routers

from .views import PostViewSet

app_name = 'testapp'
router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, base_name='posts')
urlpatterns = router.urls
