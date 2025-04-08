from flask import Blueprint, render_template

group = Blueprint("group", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')

methods = [
    {
        "name": "metod1",
        "image": "image1.png",
        "description": "Описание метода 1"
    },
    {
        "name": "metod2",
        "image": "image2.png",
        "description": "Описание метода 2"
    },
    # ...
]

@group.route("/<name>")
def set_web(name):
    method = methods

    if not method:
        return "Метод не найден", 404  # Обработка 404

    return render_template('method.html', method=method)