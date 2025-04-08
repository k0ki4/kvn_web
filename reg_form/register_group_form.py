import datetime as dt
import json
from datetime import datetime
import os
import re
import secrets
from functools import wraps

import requests
from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename


from data.register import CreateTeamForm
from __init import app, VK_CLIENT_ID, VK_REDIRECT_URI, VK_CLIENT_SECRET

register_form = Blueprint("reg", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')


def normalize_vk_link(link):
    """Приводит ссылку ВК к единому формату"""
    link = link.strip()
    if not link.startswith(('http://', 'https://')):
        link = 'https://' + link
    return link.lower()


@register_form.route('/form', methods=['GET', 'POST'])
def get_form():

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
            return redirect(url_for('global_site'))

        except Exception as e:
            flash(f'Ошибка при создании команды: {str(e)}', 'error')

    return render_template('form.html', form=form)