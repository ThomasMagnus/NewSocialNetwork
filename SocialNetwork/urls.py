from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('authorization.urls')),
                  path('reg/', include('registration.urls')),
                  path('users/', include('users.urls')),
                  path('createPost/', include('createPosts.urls')),
                  path('friends/', include('friends.urls')),
                  path('friendPage/', include('friends_page.urls')),
                  path('friendsRequests/', include('friends_requests.urls'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
