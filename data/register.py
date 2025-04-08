from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Regexp


class CreateTeamForm(FlaskForm):
    captain_link = StringField('Ссылка на капитана (ВК)',
                               validators=[
                                   DataRequired(message="Укажите ссылку на капитана"),
                                   Regexp(r'^(https?:\/\/)?(www\.)?vk\.com\/[a-zA-Z0-9_\.]+$',
                                          message="Укажите корректную ссылку ВКонтакте")
                               ],
                               render_kw={
                                   "placeholder": "https://vk.com/id123 или https://vk.com/nickname",
                                   "pattern": "(https?:\/\/)?(www\.)?vk\.com\/[a-zA-Z0-9_\.]+"
                               })

    group_link = StringField('Ссылка на группу (ВК)',
                             validators=[
                                 DataRequired(message="Укажите ссылку на группу"),
                                 Regexp(r'^(https?:\/\/)?(www\.)?vk\.com\/[a-zA-Z0-9_\.]+$',
                                        message="Укажите корректную ссылку ВКонтакте")
                             ],
                             render_kw={
                                 "placeholder": "https://vk.com/club123 или https://vk.com/groupname",
                                 "pattern": "(https?:\/\/)?(www\.)?vk\.com\/[a-zA-Z0-9_\.]+"
                             })

    api_group = StringField('API ключ группы ВК',
                            validators=[DataRequired(message="Укажите API ключ")],
                            render_kw={
                                "placeholder": "vk1.a.1234567890...",
                                "autocomplete": "off"
                            })

    team_photo = FileField('Фото команды',
                           validators=[
                               FileAllowed(['jpg', 'jpeg', 'png'], 'Только JPG/PNG изображения')
                           ],
                           render_kw={"accept": "image/jpeg, image/png"})

    description = TextAreaField('Краткое описание команды',
                                validators=[DataRequired(message="Добавьте описание команды")],
                                render_kw={
                                    "placeholder": "Основная информация о команде...",
                                    "rows": 4,
                                    "maxlength": "500"
                                })

    submit = SubmitField('Создать команду',
                         render_kw={"class": "btn vk-btn"})