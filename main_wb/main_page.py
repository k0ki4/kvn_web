from flask import Blueprint, render_template

main = Blueprint("main_page", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')
methods = [
    {
        "name": "metod1",
        "image": "image.png",
        "description": "Описание метода 1"
    },
    {
        "name": "metod2",
        "image": "image.png",
        "description": "Описание метода 2"
    },
    # ...
]

@main.route('/')
def global_site():
    return render_template('index.html', methods=methods)