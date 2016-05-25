from django.conf.urls import include, patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from student_portal.views import IndexView
from forum.views import CategoryViewSet, TopicViewSet, MessageViewSet
from users.views import LoginView, LogoutView, UserViewSet, StudentGoalsViewSet, StudentPracticeLogViewSet, StudentObjectiveViewSet, StudentWishListViewSet, StudentMaterialsViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'student-goals', StudentGoalsViewSet)
router.register(r'student-practice-logs', StudentPracticeLogViewSet)
router.register(r'student-objectives', StudentObjectiveViewSet)
router.register(r'student-wish-list', StudentWishListViewSet)
router.register(r'student-materials', StudentMaterialsViewSet)
router.register(r'forum-category', CategoryViewSet)
router.register(r'forum-topics', TopicViewSet)
router.register(r'forum-message', MessageViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),

    url(r'^$',  IndexView.as_view(), name='index'),    
    # url(r'^/$',  IndexView.as_view(), name='index'),

    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),

    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    # url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    # url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    # url(r'^reset_password_done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),  
]

# if settings.DEBUG:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if not settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
   
#     urlpatterns += staticfiles_urlpatterns()