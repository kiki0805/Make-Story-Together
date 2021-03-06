"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from disciplines.api import DisciplineViewSet
from groups.api import GroupViewSet
from stories.api import StoryViewSet, TagViewSet, ChapterViewSet, PlotViewSet, CharacterViewSet
from writers.api import WriterViewSet
from likes.api import LikeViewSet
from feeds.api import FeedViewSet

router = routers.SimpleRouter()
router.register(r'^$', WriterViewSet, 'Writer')
router.register(r'discipline', DisciplineViewSet, 'Discipline')
router.register(r'group', GroupViewSet, 'Group')
router.register(r'story', StoryViewSet, 'Story')
router.register(r'tag', TagViewSet, 'Tag')
router.register(r'chapter', ChapterViewSet, 'Chapter')
router.register(r'plot', PlotViewSet, 'Plot')
router.register(r'character', CharacterViewSet, 'Character')
router.register(r'like', LikeViewSet, 'Like')
router.register(r'feed', FeedViewSet, 'Feed')
router.register(r'', WriterViewSet, 'Writer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('token-verify/', verify_jwt_token)
] + staticfiles_urlpatterns()

urlpatterns += router.urls
