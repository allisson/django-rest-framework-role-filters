from rest_framework import routers

from .views import PostViewSet

app_name = 'testapp'
router = routers.SimpleRouter()
router.register('posts', PostViewSet, 'post')
urlpatterns = router.urls
