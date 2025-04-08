import os

from flask import Flask

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'K0ki4_176',
    'UPLOAD_FOLDER': 'all_group_img',
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,  # 5MB
    'VK_DOMAIN': 'vk.com'
})

# Конфигурация VK
VK_CLIENT_ID = os.getenv('VK_CLIENT_ID')
VK_CLIENT_SECRET = os.getenv('VK_CLIENT_SECRET')
VK_REDIRECT_URI = os.getenv('VK_REDIRECT_URI')
API_VERSION = '5.131'