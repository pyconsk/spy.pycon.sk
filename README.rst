Slovak Python civic association website
#######################################

.. image:: https://d322cqt584bo4o.cloudfront.net/spy-oz-website/localized.svg
    :alt: Translation status
    :target: https://crowdin.com/project/spy-oz-website

The mission of the SPy civic association is to support developers and users of the Python programming language. We support and we spread the programming language Python and other open source technologies and open source ideas in our society. Our goal is to provide help and support for beginners and people who are new to programming. Another goal is to work with schools and other educational institutions, and promote programming (independent of the programming language) in children and young people from the earliest age. We support the area of software development in socially vulnerable or otherwise disadvantaged social groups. We are dedicated to practical use of software development. We want to work on various open source projects, to create open educational content for use in schools as well as self-study and advocate for the use of open technologies in society and the public sector.


Contributing
------------

Contributions are welcome. If you found a bug please open an issue at our GitHub repo, or submit a pull request. We do welcome any kind of pull request event if it is just a typo ;)

All work done by SPy o.z. was done by volunteers. If you would like to join us and help the Python community in Slovakia to flourish get in touch with us via email: info (at) pycon.sk. We need help with many different types of work, from site administration or webdesign, throught `translations <https://crowdin.com/project/spy-oz-website>`_, to `event organization <https://www.pycon.sk/>`_... Everyone is welcome here, no matter what is your age or experience. If there is anything you would like to do, or you want to spent your time meaningfully, do not hesitate to write us.


Project structure
-----------------

**2 branches**:

- ``master`` - the `Flask <http://flask.pocoo.org/>`_ app, templates, static files, translations (make your changes here).
- ``l10n_master`` - the `Crowdin translation <https://crowdin.com/project/spy-oz-website`_ branch (do not make any changes here).


Installation
------------

- clone repository locally::

    git clone https://github.com/pyconsk/spy.python.sk.git
    cd spy.python.sk

- creates a virtual environment, activate it and installs all requirements::

    python3.6 -m venv envs3
    source envs3/bin/activate
    pip install -r requirements.txt --no-binary :all:

- start flask server, and you can view it in browser (http://127.0.0.1:5000/en/index.html)::

    python views.py


Translations
------------

For website translations we use `Crowdin translation service <https://crowdin.com/project/spy-oz-website>`_. Create a free account and you can translate directly in the browser.

Other option is to translate directly in the translation source files. Translations are made with `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_. All translations are located in ``translations`` directory, update ``messages.po`` with your translations messages.

- collect translation strings from Flask app::

    pybabel extract -F babel.cfg -o messages.pot .

- update translation ``messages.po`` files with collected translation strings::

    pybabel update -i messages.pot -d translations

- compile translated messages and generate ``messages.po`` files::

    pybabel compile -d translations


Generate static site
--------------------

`Frozen-Flask <https://pythonhosted.org/Frozen-Flask/>`_ freezes a Flask application into a set of static files. The result can be hosted without any server-side software other than a traditional web server.

- generate static files, and you can find them in ``build`` directory::

    python freezer.py

- verify the generated result in browser (http://127.0.0.1:8000/en/index.html)::

    cd build
    python -m SimpleHTTPServer 8000


Links
-----

- web: https://spy.pycon.sk https://spy.python.sk
- chat: https://riot.python.sk
- facebook: https://facebook.com/pyconsk
- twitter: https://twitter.com/pyconsk


License
-------

MIT license for code (GitHub repo), CC-BY for content, except members photos (consult with SPy member if you would like to use their avatar). For more detail read the LICENSE file.

