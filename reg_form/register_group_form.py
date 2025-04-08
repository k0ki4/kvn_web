import os
import re

import requests
from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename


from data.register import CreateTeamForm
from __init import app, VK_CLIENT_ID, VK_REDIRECT_URI, VK_CLIENT_SECRET

register_form = Blueprint("reg", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')


@register_form.route('/vk-auth')
def vk_auth():
    # Формируем URL для авторизации
    auth_url = (
        f"https://oauth.vk.com/authorize?"
        f"client_id={VK_CLIENT_ID}&"
        f"display=page&"
        f"redirect_uri={VK_REDIRECT_URI}&"
        f"scope=email,groups&"  # Запрашиваем доступ к email и группам
        f"response_type=code&"
        f"v=5.131"
    )
    return redirect(auth_url)


@register_form.route('/auth/callback')
def vk_callback():
    # Получаем код от VK
    code = request.args.get('code')
    if not code:
        return "Ошибка авторизации", 400

    # Получаем access token
    token_url = (
        f"https://oauth.vk.com/access_token?"
        f"client_id={VK_CLIENT_ID}&"
        f"client_secret={VK_CLIENT_SECRET}&"
        f"redirect_uri={VK_REDIRECT_URI}&"
        f"code={code}"
    )

    response = requests.get(token_url)
    data = response.json()

    if 'error' in data:
        return f"Ошибка: {data['error_description']}", 400

    # Сохраняем данные пользователя в сессии
    session['vk_user_id'] = data.get('user_id')
    session['vk_access_token'] = data.get('access_token')
    session['vk_email'] = data.get('email', '')

    # Получаем дополнительную информацию о пользователе
    user_info = get_vk_user_info(data['access_token'], data['user_id'])
    if user_info:
        session['vk_user_name'] = f"{user_info['first_name']} {user_info['last_name']}"
        session['vk_user_photo'] = user_info.get('photo_50', '')

    return redirect(url_for('home'))


def get_vk_user_info(access_token, user_id):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'access_token': access_token,
        'user_ids': user_id,
        'fields': 'photo_50',
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('response', [{}])[0] if 'response' in data else None


@register_form.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('global_site'))


def normalize_vk_link(link):
    """Приводит ссылку ВК к единому формату"""
    link = link.strip()
    if not link.startswith(('http://', 'https://')):
        link = 'https://' + link
    return link.lower()


@register_form.route('/form', methods=['GET', 'POST'])
def get_form():
    if 'vk_user_id' not in session:
        print("Redirecting to auth...")
        return redirect(url_for('reg.start_auth'))

    form = CreateTeamForm()

    if form.validate_on_submit():
        try:
            # Нормализация ссылок ВК
            captain_link = normalize_vk_link(form.captain_link.data)
            group_link = normalize_vk_link(form.group_link.data)

            # Проверка валидности API ключа (базовая)
            if not re.match(r'^vk1\.[a-zA-Z0-9\.\-_]+$', form.api_group.data):
                flash('Неверный формат API ключа', 'error')
                return render_template('form.html', form=form)

            # Обработка фото
            photo_path = None
            if form.team_photo.data:
                filename = secure_filename(form.team_photo.data.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                form.team_photo.data.save(save_path)
                photo_path = f"all_group_img/{filename}"

            # Здесь сохраняем данные в БД
            # team = VKTeam(
            #     captain_link=captain_link,
            #     group_link=group_link,
            #     api_key=form.api_group.data,
            #     photo=photo_path,
            #     description=form.description.data
            # )
            # db.session.add(team)
            # db.session.commit()

            flash('Команда успешно создана!', 'success')
            return redirect(url_for('team_page'))

        except Exception as e:
            flash(f'Ошибка при создании команды: {str(e)}', 'error')

    return render_template('form.html', form=form)


@register_form.route('/start')
def start_auth():
    return render_template("no_reqister.html")