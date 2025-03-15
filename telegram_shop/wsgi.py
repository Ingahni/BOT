import os
from django.core.wsgi import get_wsgi_application
# функция Django, которая создает WSGI-приложение, необходимое для развертывания проекта.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_shop.settings')
application = get_wsgi_application()

# os.environ.setdefault(...) — устанавливает переменную окружения 
# DJANGO_SETTINGS_MODULE, которая указывает Django, где искать настройки (settings.py).
# 'telegram_shop.settings' — путь к файлу settings.py вашего проекта Django.