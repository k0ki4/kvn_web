import os
from datetime import timedelta

from flask import Flask

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'K0ki4_176',
    'UPLOAD_FOLDER': 'all_group_img',
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,  # 5MB
    'VK_DOMAIN': 'vk.com'
},
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),  # Срок жизни сессии
    SESSION_COOKIE_NAME='flask_session',  # Имя cookie
    SESSION_COOKIE_SECURE=True,  # Только HTTPS (для Glitch обязательно True)
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'  # Защита от CSRF
)

# Конфигурация VK
VK_CLIENT_ID = os.getenv('VK_CLIENT_ID')
VK_CLIENT_SECRET = os.getenv('VK_CLIENT_SECRET')
VK_REDIRECT_URI = os.getenv('VK_REDIRECT_URI')
API_VERSION = '5.131'