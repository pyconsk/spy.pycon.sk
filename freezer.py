from flask_frozen import Freezer
from views import app

LANGUAGES = (
    {'lang_code': 'sk'},
    {'lang_code': 'en'}
)

app.config['FREEZER_DESTINATION'] = 'docs'  # GitHub pages directory for static site

freezer = Freezer(app)


@freezer.register_generator
def index():
    for lang in LANGUAGES:
        yield lang


if __name__ == '__main__':
    freezer.freeze()
