from django.conf.urls import include, patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from student_portal.views import IndexView
from users.views import LoginView, LogoutView, UserViewSet, StudentGoalsViewSet, StudentPracticeLogViewSet, StudentObjectiveViewSet, StudentWishListViewSet, StudentMaterialsViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'student-goals', StudentGoalsViewSet)
router.register(r'student-practice-logs', StudentPracticeLogViewSet)
router.register(r'student-objectives', StudentObjectiveViewSet)
router.register(r'student-wish-list', StudentWishListViewSet)
router.register(r'student-materials', StudentMaterialsViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^$',  IndexView.as_view(), name='index'),    
    url(r'^/$',  IndexView.as_view(), name='index'),

    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
]

# if settings.DEBUG:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if not settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
   
#     urlpatterns += staticfiles_urlpatterns()