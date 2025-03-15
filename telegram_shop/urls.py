from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),   # админка
    path('accounts/', include('django.contrib.auth.urls')),  # для работы с аутентификацией - стандартные маршруты: login, logout, password_reset и т.д.
    path('', include('shop.urls')),  # маршруты приложения "shop"
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# settings.MEDIA_URL — это URL, по которому можно получить доступ к медиа файлам.
# settings.MEDIA_ROOT — это директория на сервере, в которой хранятся медиа файлы.