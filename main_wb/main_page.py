from flask import Blueprint, render_template

main = Blueprint("main_page", __name__,
                 static_folder='img',
                 static_url_path='/img',
                 template_folder='templates')


@main.route('/')
def global_site():
    return render_template('index.html')