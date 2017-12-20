#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from datetime import datetime
from flask import Flask, g, request, render_template, abort, make_response
from flask_babel import Babel, gettext

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOGO_PYCON = 'logo/pycon.svg'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
NOW = datetime.utcnow().strftime(TIME_FORMAT)


def get_mtime(filename):
    mtime = datetime.fromtimestamp(os.path.getmtime(filename))
    return mtime.strftime(TIME_FORMAT)


SITEMAP_DEFAULT = {'prio': '0.1', 'freq': 'weekly'}
SITEMAP = {
    'sitemap.xml': {'prio': '0.9', 'freq': 'daily', 'lastmod': get_mtime(__file__)},
    'index.html': {'prio': '1', 'freq': 'daily'},
}
LDJSON = {
    "@context": "http://schema.org",
    "@type": "Organization",
    "name": "PyCon SK",
    "url": "https://spy.pycon.sk",
    "logo": "https://spy.pycon.sk/static/logo/pycon.png",
    "sameAs": [
        "https://facebook.com/pyconsk",
        "https://twitter.com/pyconsk",
        "https://www.linkedin.com/company/spy-o--z-",
        "https://github.com/pyconsk",
    ]
}


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in LANGS:
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])


def _get_template_variables(**kwargs):
    variables = {
        'title': gettext('PyCon SK'),
        'logo': LOGO_PYCON,
        'ld_json': LDJSON
    }
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.route('/<lang_code>/index.html')
def index():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "url": "https://spy.pycon.sk/" + lang + "/",
        "creator": {
            "@type": "Organization",
            "name": "SPy o.z.",
            "url": "https://spy.pycon.sk/",
            "logo": "https://spy.pycon.sk/img/logo/spy-logo.png",
        }
    }
    template_variables = _get_template_variables(ld_json=LDJSON_EVENT, li_index='active')

    locations = {
        'progressbar': {
            'name': 'ProgressBar Hackerspace',
            'link': 'https://progressbar.sk/calendar/',
            'link_title': gettext('ProgressBar Calendar'),
            'address': 'Michalská 3, Bratislava'
        },
        'fiit': {
            'name': 'Fakulta informatiky a informačných technológií STU v Bratislave',
            'link': 'https://www.fiit.stuba.sk/',
            'link_title': gettext('Webstránka FIIT STU'),
            'address': 'Ilkovičova 2, Bratislava'
        },
        'fablab': {
            'name': 'FabLab',
            'link': 'https://www.fablab.sk/',
            'link_title': gettext('Webstránka FabLab'),
            'address': 'Ilkovičova 8, Bratislava'
        },
        'gjh': {
            'name': 'Gymnázium Jura Hronca',
            'link': 'https://gjh.sk/',
            'link_title': gettext('Webstránka Gymnázium Jura Hronca'),
            'address': 'Novohradská 3, Bratislava'
        },
    }
    speakers = {
        'richard_kellner': {
            'name': 'Richard Kellner',
            'link': 'https://sk.linkedin.com/in/richardkellner',
            'link_title': gettext('Profil na LinkedIn') + ': Richard Kellner',
        },
        'daniel_kontsek': {
            'name': 'Daniel Kontšek',
            'link': 'https://www.linkedin.com/in/danielkontsek/',
            'link_title': gettext('Profil na LinkedIn') + ': Daniel Kontšek',
        },
        'marek_mansell': {
            'name': 'Marek Mansell',
            'link': 'https://sk.linkedin.com/in/marekmansell',
            'link_title': gettext('Profil na LinkedIn') + ': Marek Mansell',
        },
        'tomas_pytel': {
            'name': 'Tomáš Pytel',
            'link': 'https://www.linkedin.com/in/tomas-pytel/',
            'link_title': gettext('Profil na LinkedIn') + ': Tomáš Pytel',
        },
        'pavol_kincel': {
            'name': 'Pavol Kincel',
            'link': 'https://www.linkedin.com/in/secult/',
            'link_title': gettext('Profil na LinkedIn') + ': Pavol Kincel',
        },
    }

    template_variables['events'] = {
        '2015': (
            {
                'name': '06. ' + gettext('Bratislavský Python Meetup'),
                'date': '8. december',
                'hour': '18:00',
                'speakers': ({
                                 'name': 'Juraj Bubniak',
                                 'link': 'https://www.linkedin.com/in/jurajbubniak/',
                                 'link_title': gettext('Profil na LinkedIn') + ': Juraj Bubniak',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na tomto stretnutí sa budeme pokračovať s úvodom do Pythonu. Juraj Bubniak nám príde '
                           'porozprávať o práci so základnými dátovými typmi v Pythone. Nezabudnite si priniesť '
                           'notebooky aby ste si odskúšali niečo nové...</p>'
                           '<p>Po workshope bude stretnutie dobrovoľníkov, ktorí sa podieľajú, alebo by sa chceli '
                           'pridať na organizácií PyCon SK 2016.</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201512" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201512</a></p>',
            },
            {
                'name': '05. ' + gettext('Bratislavský Python Meetup'),
                'date': '10. november',
                'hour': '18:00',
                'speakers': (speakers['richard_kellner'],),
                'location': locations['progressbar'],
                'content': '<p>Na tomto stretnutí sa budeme zameriavať na úplných začiatočníkov. Povieme si, ako '
                           'správne začať projekt v Pythone. Nezabudnite si, priniesť notebooky aby ste si odskúšali '
                           'niečo nové...</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201511"'
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201511</a></p>',
            },
            {
                'name': '04. ' + gettext('Bratislavský Python Meetup'),
                'date': '6. október',
                'hour': '18:00',
                'speakers': ({
                                 'name': 'Adam Števko',
                                 'link': 'https://www.linkedin.com/in/xenol/',
                                 'link_title': gettext('Profil na LinkedIn') + ': Adam Števko',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na tomto stretnutí si predstavíme <a href="http://www.ansible.com/" target="_blank">'
                           'Ansible</a>. V rámci workshopu bude Adam Števko rozprávať o tom, ako ansible funguje, načo '
                           'je dobrý a ako s ním začať. Nezabudnite si priniesť notebooky, aby ste si odskúšali niečo '
                           'nové...</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201510" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201510</a></p>',
            },
            {
                'name': '03. ' + gettext('Bratislavský Python Meetup'),
                'date': '8. september',
                'hour': '18:00',
                'speakers': (speakers['tomas_pytel'],),
                'location': locations['progressbar'],
                'content': '<p>Na tomto stretnutí si spravíme workshop o webscrapingu. Budeme scrapovať data z '
                           'viacerých stránok, aby sme mali praktické príklady na využitie webscrapingu. Nezabudnite si'
                           ' priniesť notebooky, aby ste si odskúšali niečo nové...</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201509" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201509</a></p>',
            },
            {
                'name': 'Začíname s Djangom',
                'date': 'august',
                'speakers': (speakers['daniel_kontsek'], speakers['richard_kellner']),
                'location': {
                    'name': 'Letné sústredenie talentovanej mládeže v elektronike',
                    'link': 'http://www.lstme.sk/',
                    'link_title': 'Webstránka LSTME.',
                    'address': 'Krahule',

                },
                'content': '<p>Úvod do programovania s webovým frameworkom Djangom pre deti na LSTME: Letné sústredenie'
                           ' talentovanej mládeže v elektronike.</p>',
            },
            {
                'name': '02. ' + gettext('Bratislavský Python Meetup'),
                'date': '4. august',
                'hour': '18:00',
                'speakers': (speakers['daniel_kontsek'], speakers['richard_kellner']),
                'location': locations['progressbar'],
                'content': '<p>Na druhom stretnutí si stručne predstavíme protokol '
                           '<a href="https://sk.wikipedia.org/wiki/Extensible_Messaging_and_Presence_Protocol" '
                           'target="_blank" title="">XMPP</a>, ktorý využíva na komunikáciu '
                           '<a href="https://github.com/erigones/Ludolph" target="_blank" title="Ludolph: Monitoring '
                           'jabber bot projekt na Githube">Ludolph</a>. Ludolph je monitorovací jabber bot, ktorý '
                           'dokáže komunikovať so Zabbixom, má však podpru pluginov a tak je možné ho rozšíriť aj iným '
                           'smerom. Na meetupe sa budeme hlavne venovať tvorbe vlastného pluginu. Na stretnutie si '
                           'doneste notebooky a budete si môcť odskúšať spraviť v Pythone plugin do existujúceho '
                           'projektu.</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201508" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201508</a></p>',
            },
            {
                'name': '01. ' + gettext('Bratislavský Python Meetup'),
                'date': '7. júl',
                'hour': '18:00',
                'speakers': (speakers['richard_kellner'], speakers['daniel_kontsek']),
                'location': locations['progressbar'],
                'content': '<p>Prvé stretnutie ľudí, ktorí majú záujem o programovanie v Pythone. Či už ste úplný '
                           'začiatočník (bez akejkoľvek skúsenosti s programovaním) alebo používate iný "zastaralý" '
                           'programovací jazyk (a radi by ste prešli na niečo "fresh"), príďte a spoznajte nové '
                           'možnosti, ktoré Python poskytuje. Ak už ste v Pythone čo-to spravili alebo ste expert, '
                           'budeme radi, keď nás prídete niečo naučiť.</p>'
                           '<p>Stretnutie je vhodné pre ľudí zo všetkých oblastí od webového programovania cez '
                           'hackovanie hardvéru až po výskum veľkých dát.</p>'
                           '<p>Vytvorenie Python komunity je dôležité, pretože veľa firiem doma aj v zahraničí začína '
                           'používať Python a spoznávať jeho výhody. Koniec koncov to bude zábava, učiť sa jeden od '
                           'druhého a pri pive si rozprávať zážitky z krotenia hadov.</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201507" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201507</a></p>',
            },),
        '2016': (
            {
                'name': '16. ' + gettext('Bratislavský Python Meetup'),
                'date': '13. december',
                'hour': '18:30',
                'speakers': ({
                                 'name': 'Jozef Sukovský',
                                 'link': '',
                                 'link_title': '',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na decembrovom meetupe nám príde Jozef Sukovský porozprávať o Paramiko (Python '
                           'implementation of the SSHv2 protocol).</p>'
                           '<p>Na meetupe preberieme:'
                           '<ul>'
                           '<li>všeobecné predstavenie paramiko</li>'
                           '<li>jednoduchý príklad pripojenia klienta so serverom</li>'
                           '<li>skúsime prácu s interaktívnou aplikáciou na druhej strane</li>'
                           '<li>povieme si, čo robiť, keď druhá strana nepošle exit a kanál zostane "visieť"</li>'
                           '<li>skúsime pretunelovanie sa cez jumphost</li></ul></p>'
                           '<p>Prednáška bude formou workshopu, tak si prineste vlastné notebooky, aby ste si mohli '
                           'odskúšať niečo nové na vlastnej klávesnici ;)</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'Hardware python pre učitelov',
                'date': '10. november',
                'speakers': (speakers['marek_mansell'],),
                'location': {
                    'name': '1. súkromné gymnázium Bajkalská',
                    'address': 'Bratislava'
                },
                'content': '<p>Klub učiteľov informatiky, v spolupráci so Startup Education Slovakia</p>'
                           '<p>Zajtra si povieme niečo o MicroPythone a zariadeniach, na ktorých sa dá bežať.Vyskúšame '
                           'si naprogramovať micro:bit od Britskej BBC a Witty Board s integrovaným WiFi modulom. '
                           'Povieme si aj o Raspberry Pi a o Arduine.Taktiež si ukážeme zopár senzorov, ako napríklad '
                           'ultrazvukový merač vzdialenosti, teplomer, senzor otvorených dvier či merač svetla.</p>'
            },
            {
                'name': '15. ' + gettext('Bratislavský Python Meetup'),
                'date': '08. november',
                'hour': '18:30',
                'speakers': (),
                'location': locations['progressbar'],
                'content': '<p>Príprava PyConSK 2017.</p>'
                           '<p>Na novembrovom meetupe sa budeme venovať primárne príprave konferencie PyConSK 2017.'
                           '<br />Ak máte záujem zapojiť sa do prípravy druhého slovenského PyCon-u, príďte! PyCon je '
                           'komunitná akcia, poďme ju preto pripraviť spolu. Tento rok bol PyCon taká pecka práve '
                           'kvôli tomu, že sme doňho dali to najlepšie. Skúsime v marci 2017 prekonať samých seba? :-)'
                           '</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>'
            },
            {
                'name': '14. ' + gettext('Bratislavský Python Meetup'),
                'date': '04. október',
                'hour': '18:00',
                'speakers': (speakers['richard_kellner'],),
                'location': locations['progressbar'],
                'content': '<p>Na oktobrovom meetupe budeme pokračovať v pair programmingu v Djangu.</p>'
                           '<p>V septembri sme začali programovať aplikáciu v Django frameworku. Na októbrovom meetupe '
                           'sa rozdelíme do dvojíc a budeme pokračovať v programovaní. Prineste si notebook aby ste '
                           'mali na čom programovať. Meetup je vhodný aj pre začiatočníkov, ktorý sa chcú naučiť '
                           'Django, ale budeme radi ak prídu aj skúsenejší, aby sme vytvorili vyvážené dvojice. '
                           'Pripravíme si aj problémy pre skúsených. Ak ste sa minulý mesiac nezúčastnili, nevadí, '
                           'budeme pokračovať a začiatočníkom pomôžeme aby vedeli pokračovať...</p>'
                           '<p>Prezentácia: <a href="https://ricco386.github.io/zaciname-s-djangom/" target="_blank">'
                           'https://ricco386.github.io/zaciname-s-djangom/</a></p>'
                           '<p>Github: <a href="https://github.com/pyconsk/django-konfera" target="_blank">'
                           'https://github.com/pyconsk/django-konfera</a></p>'
                           '<p class="text-justify">Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '13. ' + gettext('Bratislavský Python Meetup'),
                'date': '13. september',
                'hour': '18:00',
                'speakers': (speakers['richard_kellner'],),
                'location': locations['progressbar'],
                'content': '<p>Na septembrovom meetupe skúsime pair programming v Djangu.</p>'
                           '<p>Na začiatok si predstavíme Django framework a rozdelíme sa do dvojíc a budeme '
                           'programovať. Pokúsime sa spraviť opensource aplikáciu na organizáciu eventov. Prineste si '
                           'notebook aby ste mali na čom programovať. Meetup je vhodný aj pre začiatočníkov, ktorý sa '
                           'chcú naučiť Django, ale budeme radi ak prídu aj skúsenejší, aby sme vytvorili vyvážené '
                           'dvojice.</p>'
                           '<p>Prezentácia: <a href="https://ricco386.github.io/zaciname-s-djangom/" target="_blank">'
                           'https://ricco386.github.io/zaciname-s-djangom/</a></p>'
                           '<p>Github: <a href="https://github.com/pyconsk/django-konfera" target="_blank">'
                           'https://github.com/pyconsk/django-konfera</a></p>'
                           '<p class="text-justify">Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '12. ' + gettext('Bratislavský Python Meetup'),
                'date': '12. júl',
                'hour': '18:30',
                'speakers': (),
                'location': locations['progressbar'],
                'content': '<p>Na júlovom meetupe budeme mať Lightning talks show.</p>'
                           '<p>Ak máte záujem predniesť mini prednášku, o projekte na ktorom práve pracujete, alebo '
                           'inú zaujímavú tému, stači ak prídete medzi nás.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '11. ' + gettext('Bratislavský Python Meetup'),
                'date': '07. jún',
                'hour': '18:30',
                'speakers': ({
                                 'name': 'Juraj Bezručka',
                                 'link': 'https://www.linkedin.com/in/juraj-bezrucka-5651a1b/',
                                 'link_title': gettext('Profil na LinkedIn') + ': Juraj Bezručka',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na júnovom meetupe nám Juraj Bezručka predstaví "python pre neprogramatorov".</p>'
                           '<p>Juraj nám predstaví funkcie ako map, filter či reduce aj s príkladmi, ďalej tiež '
                           'list/dict comprehension, prípadne ďalšie užitočné funkcie (vysvetlí ternárny operátor a '
                           'pod.)</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '10. ' + gettext('Bratislavský Python Meetup'),
                'date': '03. máj',
                'hour': '18:30',
                'speakers': ({
                                 'name': 'Jozef Képesi',
                                 'link': '',
                                 'link_title': '',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na májový meetup nám príde porozprávať Jozef Képesi o populárnej databáze PostgreSQL.'
                           '</p><p><b>When in doubt, just use PostgreSQL.</b> Popíšeme si najlepšie praktiky z pohľadu '
                           'architektúry a vlastností databázy. Na záver Jozef prezradí aj skryté funkcie, ktoré dnes '
                           'robia z PostgreSQL viac framework na spracovanie dát, ako databázu.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '9. ' + gettext('Bratislavský Python Meetup'),
                'date': '12. apríl',
                'hour': '18:00',
                'speakers': (),
                'location': locations['progressbar'],
                'content': '<p>Na aprílovom meetupe si spravíme Coding Dojo session.</p>'
                           '<p>Netreba si nič nosiť budeme praktizovat pair programing na projektore. Stačí iba chuť '
                           'programovať. POZOR! Aby sme dokázali spraviť kvalitný workshop, zaviedli sme registráciu, '
                           'aby sme mali prehľado koľko ľudí príde. Počet miest je limitovaný, preto sa zaregistrujte '
                           'čo najskôr.</p>'
                           '<p class="center"><img src="/static/img/logo/pycon_sk_dojo.png" class="coding-dojo" /></p>'
                           '<p><a href="/static/slides/ba-09-meetup.html" target="_blank">Prezentácia</a></p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'Konferencia PyCon SK 2016',
                'date': '11. marec',
                'date_end': '13. marec',
                'speakers': (),
                'location': locations['fiit'],
                'content': '<p>PyCon SK je komunitou organizovaná konferencia pre programovací jazyk Python. '
                           '<b>Premiérový ročník konferencie PyCon SK sa uskutočnil '
                           '<a href="https://2016.pycon.sk/sk/pod-zastitou-prezidenta-slovenskej-republiky.html" '
                           'target="_blank">pod záštitou prezidenta SR Andreja Kisku</a>.</b></p>'
                           '<p>Viac o konferencii na oficialnom webe: <a href="https://2016.pycon.sk/" target="_blank" '
                           'title="Domovská stránka PyCon SK 2016">https://2016.pycon.sk/</a></p>'
                           '<p><a href="https://www.python.org/" target="_blank" title="Domovská stránka Pythonu">'
                           '<img src="https://2016.pycon.sk/static/images/logo/pycon_long.svg" alt="PyCon SK" '
                           'class="center"></a></p>',
            },
            {
                'name': '8. ' + gettext('Bratislavský Python Meetup'),
                'date': '9. február',
                'hour': '18:00',
                'speakers': ({
                                 'name': 'Miroslav Beka',
                                 'link': 'https://github.com/mirobeka',
                                 'link_title': gettext('Profil na GitHube') + ': Miro Beka',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na februárovom meetupu nám Miroslav Beka ukáže, že Python sa dá použiť na vývoj '
                           'serióznych “enterprise” alebo produktových aplikácií. Bude hovoriť o pojmoch ako '
                           'škálovateľnosť, zero down time deployments, continuous integration, continuous deployment '
                           'a oboznámi nás s osvedčenými postupmi v oblasti nasadenia Pythonových aplikácii na '
                           'produkčné servery.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201602" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201602</a></p>'
                           '<p>V marci všetko naše úsilie zameriame na PyCon, takže marcový meetup vynecháme a '
                           '<strong>ďalšie stretnutie bude v apríli</strong>.</p>',
            },
            {
                'name': '7. ' + gettext('Bratislavský Python Meetup'),
                'date': '12. január',
                'hour': '18:00',
                'speakers': ({
                                 'name': 'Andrej Mošať',
                                 'link': 'https://sk.linkedin.com/in/mosat',
                                 'link_title': gettext('Profil na LinkedIn') + ': Andrej Mošať',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Prvý meetup v novom roku začneme minimalisticky. Andrej Mošať nám príde predstaviť '
                           '<a href="https://micropython.org/" title="Python pre mikrocontroleri" target="_blank">'
                           'MicroPython</a>, povieme si prečo je vlastne micro a na čo je dobré mať MicroPython keď '
                           'máme štandardný Python.</p>'
                           '<p>Andrej so sebou prinesie <a href="http://wipy.io/" target="_blank">WiPy</a> a '
                           '<a href="https://micropython.org/store/#/store" target="_blank">PyBoard</a>, porozpráva '
                           'o vývoji hardwaru v micropythone. Ukáže workflow vývoja zariadení, základné schémy, a na '
                           'záver zostrojí budík. Ak sa zaujímate o Internet of Things, ale neviete kde začať, alebo '
                           'sa chcete dozvedieť ako si začať vyrábať doma jednoúčelové zariadenia, tento meetup Vás '
                           'určite zaujme.</p>'
                           '<p>Jeden štastlivec, ktorý bude dávať pozor, bude mať šancu vyhrať vývojový kit s '
                           'micropythonom na prototypovanie.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>'
                           '<p>Github: <a href="https://github.com/pyconsk/meetup/tree/master/Bratislava/201601" '
                           'target="_blank">https://github.com/pyconsk/meetup/tree/master/Bratislava/201601</a></p>'
                           '<p class="center"><iframe width="640" height="360" '
                           'src="https://www.youtube.com/embed/dQYnJVSsd8Q" frameborder="0" allowfullscreen></iframe>'
                           '</p>',
            },),
        '2017': (
            {
                'name': 'MicroPython & elektronika: BBC microbit',
                'date': '13. december',
                'speakers': (speakers['marek_mansell'],),
                'location': {
                    'name': '',
                    'address': 'Bratislava'
                },
                'content': '<p>TBD</p>',
            },
            {
                'name': '27. ' + gettext('Bratislavský Python Meetup'),
                'date': '05. december',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['progressbar'],
                'content': '<p><b>Špeciálna vianočná edícia</b></p>'
                           '<p>Máte chuť na príjemný geekovský večer? Rozblikáme s (micro)Pythonom vianočné svetlá a '
                           'urobíme si správnu decembrovú náladu! Nezabudnite si priniesť notebook... :-)</p>'
                           '<p>Konkrétne si naprogramujeme animácie na Neopixel LED pásoch cez mikrokontrolér NodeMCU.'
                           ' A to všetko v Pythone :-)</p>'
                           '<p>Na workshop nie sú potrebné predchádzajúce znalosti programovania či elektroniky, '
                           'všetko potrebné si vysvetlíme. Či už chodíte pravidelne na meetupy alebo ste u nás nikdy '
                           'neboli, radi Vás uvidíme!</p>'
                           '<p>Budeme mať aj súťaž o jednu licenciu PyCharm Professional.</p>',
            },
            {
                'name': 'MicroPython & elektronika: WiFi, IoT a domáca automatizácia',
                'date': '15. november',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['fablab'],
                'content': '<p>Na workshope môžete získať prehľad o využívaní WiFi komunikácie v elektronike pre účely '
                           'IoT a domácej automatizácie. Naprogramujeme si jednoduchý web server, vďaka ktorému budeme '
                           'vedieť čítať hodnoty zo senzorov (napr. teplomer) na mobile či počítači. Zároveň budeme '
                           'cez WiFi ovládať LED svetlá.</p>'
                           '<p>Na workshop nie sú potrebné predchádzajúce znalosti programovania či elektroniky, všetko'
                           ' potrebné si vysvetlíme. Stačí si len doniesť vlastný počítač (s nabíjačkou a s ľubovoľným '
                           'operačným systémom).</p>',
            },
            {
                'name': '26. ' + gettext('Bratislavský Python Meetup'),
                'date': '14. november',
                'speakers': (speakers['pavol_kincel'],),
                'location': locations['progressbar'],
                'content': '<p><b>Higher-order functions</b></p>'
                           '<p>Počas meetupu sa skúsime dostať do zóny komfortu s higher-order functions. Prejdeme '
                           'si ich zmysel, nakódime si príklady, vyskúšame si MapReduce a iné buzzwordy. Odporúčame si '
                           'zobrať vlastný laptop.</p>'
                           '<p>Budeme mať aj súťaž o jednu licenciu PyCharm Professional.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'Lessons learned from organizing community conference, a.k.a PyCon SK story.',
                'date': '25. október',
                'speakers': (speakers['richard_kellner'],),
                'location': {
                    'name': 'Open Source Summit + Embedded Linux Conference Europe',
                    'link': 'https://events17.linuxfoundation.org/events/open-source-summit-europe',
                    'link_title': 'Webstránka Open Source Summit v Prahe.',
                    'address': 'Hilton Prague, ' + gettext('Prague, Czech Republic'),

                },
                'content': '<p>V rámci <a href="https://osseu17.sched.com/event/ByIi" target="_blank">Open Source '
                           'Summit</a> v Prahe sa v stredu uskutoční prednáška o PyCon SK. Richard Kellner bude '
                           'rozprávať ako to celé začalo, aké boli problémy a čo všetko sa dá naučiť organizovaním '
                           'konferencie.</p>'
                           '<p>Prezentácia: <a href="https://ricco386.github.io/pyconsk-story/#/" target="_blank">'
                           'https://ricco386.github.io/pyconsk-story/#/</a></p>',
            },
            {
                'name': 'MicroPython & elektronika: úvod',
                'date': '11. október',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['fablab'],
                'content': '<p>Na tomto seminári môžete získať prehľad základných možností v elektronike a inšpirovať '
                           'sa pre "zhmotňovanie" svojich nápadov. Ak už máte nejaký vyhliadnutý projekt a chceli by '
                           'ste sa poradiť ako začať, radi Vám pomôžeme.</p>'
                           '<p>Vážnejší záujemcovia sa môžu v nasledovných pravidelných stretnutiach naučiť '
                           'programovať, tlačiť na 3D tlačiarni, vytvárať a realizovať svoje nápady a projekty.</p>'
                           '<p>Na workshop nie sú potrebné predchádzajúce znalosti programovania či elektroniky, všetko'
                           ' potrebné si vysvetlíme. Stačí si len doniesť vlastný počítač (s nabíjačkou a s ľubovoľným '
                           'operačným systémom).</p>',
            },
            {
                'name': '25. ' + gettext('Bratislavský Python Meetup'),
                'date': '03. október',
                'speakers': (speakers['daniel_kontsek'],),
                'location': locations['progressbar'],
                'content': '<p>Daniel Kontšek je dlhoročný administrátor a Python programátor. Dano nám príde '
                           'porozprávať o tom ako je využitý Python pri správe datacentier. Ak sa zaujímate o '
                           'administráciu, správu, programovanie alebo automatizáciu cloudových datacentier, prídte si '
                           'vypočut prednášku o <a href="https://danubecloud.org" target="_blank">Danube Cloud</a>.</p>'
                           '<p>Budeme mať aj súťaž o jednu licenciu PyCharm Professional.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '24. ' + gettext('Bratislavský Python Meetup'),
                'date': '05. september',
                'speakers': (speakers['richard_kellner'],),
                'location': locations['progressbar'],
                'content': '<p>Report z PyConPL, pokračovanie príprav PyCon SK 2018, no a pravdaže diskusia o '
                           'Pythone.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '23. ' + gettext('Bratislavský Python Meetup'),
                'date': '01. august',
                'speakers': (speakers['tomas_pytel'],),
                'location': locations['progressbar'],
                'content': '<p>Na augustovom meetupe budeme mať PyCon SK 2018 Sprint.</p>'
                           '<p>Tešiť sa môžete na Flask, Twitter-Botov a iné veci.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'MicroPython pre deti',
                'date': '20. júl',
                'speakers': (speakers['marek_mansell'],),
                'location': {},
                'content': '<p>MicroPython pre deti na letnom tábore MATFYZU.</p>',
            },
            {
                'name': '22. ' + gettext('Bratislavský Python Meetup'),
                'date': '04. júl',
                'speakers': (),
                'location': locations['progressbar'],
                'content': '<p>V júli si vychutnáme prázdninovú pohodu. Urobíme si movie night a pozrieme si talky z '
                           'PyCon-ov po svete. No a ku tomu hamburgery, radler alebo nejaké iné dobroty.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'MicroPython seminár pre učiteľov',
                'date': '27. jún',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['gjh'],
                'content': '',
            },
            {
                'name': 'Micropython a hardvér (OSS Víkend) workshop',
                'date': '18. jún',
                'speakers': (speakers['marek_mansell'],),
                'location': {
                    'name': 'OSS Víkend 2016',
                    'link': 'http://ossvikend.sk/archive/bratislava17.html',
                    'link_title': 'Prednášky na OSS víkende.',
                    'address': 'FMFI UK, Bratislava'

                },
                'content': '<p>V rámci <a href="http://ossvikend.sk/archive/abs_bratislava17.html#python" '
                           'target="_blank">OSS víkendu</a> sa v nedeľu uskutoční prednáška a workshop na tému '
                           'microPython a hadvér.</p>',
            },
            {
                'name': '21. ' + gettext('Bratislavský Python Meetup'),
                'date': '06. jún',
                'speakers': (speakers['pavol_kincel'],),
                'location': locations['progressbar'],
                'content': '<p>Téma júnového meetupu: PyCharm IDE (integrovaný git klient, debugger, remote '
                           'interpreter a práca na vzdialenom serveri v rámci vývoja,...).</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '20. ' + gettext('Bratislavský Python Meetup'),
                'date': '09. máj',
                'speakers': (),
                'location': locations['progressbar'],
                'content': '<p>Na májovom meetupe budeme mať Lightning talky.</p>'
                           '<p>Ak máte záujem predniesť mini prednášku (rozsahovo od 1 minúty do 10 minút) o projekte '
                           'na ktorom práve pracujete, o nejakej knižnici v Pythone ktorú používate alebo o inej '
                           'zaujímavej téme, stačí, ak prídete medzi nás.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'MicroPython na NodeMCU workshop',
                'date': '12. apríl',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['fablab'],
                'content': '<p>Pomocou MicroPythonu dokážeme vyvíjať hardvér rýchlo, bezbolestne a lacno. Na '
                           'zariadeniach NodeMCU si vyskúšame rozsvietiť LEDku, prehrať 1D animáciu na LED pásiku, '
                           'odmerať teplotu či množstvo svetla. Samozrejme toto všetko môžeme ovládať aj z mobilu '
                           'alebo počítača cez internet, nakoľko NodeMCU obsahuje WiFi modul. Workshop zvládnete aj '
                           'bez predchádzajúcich znalostí elektroniky či programovania v Pythone.</p>',
            },
            {
                'name': '19. ' + gettext('Bratislavský Python Meetup'),
                'date': '11. apríl',
                'speakers': (speakers['richard_kellner'],),
                'location': locations['progressbar'],
                'content': '<p>Na Aprílovom meetupe prediskutujeme čo s doménou python.sk, čo a ako by sme s ňou mali '
                           'robiť, takisto sú vítané návrhy na projekty na tejto doméne.</p>'
                           '<p>Pre začiatok budeme používať Flask a preto si urobíme intro do tohoto jednoduchého '
                           'Frameworku.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': 'Konferencia PyCon SK 2017',
                'date': '10. marec',
                'date_end': '13. marec',
                'speakers': (),
                'location': locations['fiit'],
                'content': '<p>PyCon SK je komunitou organizovaná konferencia pre programovací jazyk Python. '
                           '<b>Druhý ročník konferencie PyCon SK sa uskutočnil pod záštitou prezidenta SR Andreja '
                           'Kisku.</b></p>'
                           '<p>Viac o konferencii na oficialnom webe: <a href="https://2017.pycon.sk/" target="_blank" '
                           'title="Domovská stránka PyCon SK 2017">https://2017.pycon.sk/</a></p>'
                           '<p><a href="https://www.python.org/" target="_blank" title="Domovská stránka Pythonu">'
                           '<img src="https://2017.pycon.sk/static/images/logo/pycon_date_2017.svg" alt="PyCon SK" '
                           'class="center"></a></p>',
            },
            {
                'name': '18. ' + gettext('Bratislavský Python Meetup'),
                'date': '07. február',
                'speakers': ({
                                 'name': 'Mišo Prusak',
                                 'link': '',
                                 'link_title': '',
                             },),
                'location': locations['progressbar'],
                'content': '<p>Na februárovom meetupe nám Mišo Prusak ukáže ako na Iteratívnu analýzu dát v pythone.'
                           '</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>'
                           '<p>V marci všetko naše úsilie zameriame na PyCon, takže marcový meetup vynecháme a '
                           '<strong>ďalšie stretnutie bude v apríli</strong>.</p>',
            },
            {
                'name': '17. ' + gettext('Bratislavský Python Meetup'),
                'date': '10. január',
                'speakers': (speakers['marek_mansell'],),
                'location': locations['progressbar'],
                'content': '<p>Na januárovom meetupe nám Marek Mansell urobí workshop o <a '
                           'href="https://micropython.org/" target="_blank">MicroPythone</a>. Máme k dispozícii 20 '
                           'kusov <a href="http://www.nodemcu.com/index_en.html" target="_blank">NodeMCU</a>, spravíme '
                           'si stručný úvod do práce s hardvérom, aby si každý mohol vytvoriť vlastný IoT device.</p>'
                           '<p>Pomocou MicroPythonu budeme merať teplotu, rozsvecovať LEDky a kopec ďalších vecí... Ak '
                           'budete mať záujem, na workshope si môžete kúpiť celý hardware kit. Orientačná cena je 15 '
                           'EUR.</p>'
                           '<p>Na prácu budete potrebovať vlastný notebook. Radi vás uvidíme aj vtedy, keď sa budete '
                           'chcieť na prácu s harvdérom len pozrieť. Pokiaľ už máte vlastný hardvér, budeme radi, ak '
                           'si ho prinesiete so sebou.</p>'
                           '<p>Workshop zvládnete aj bez predchádzajúcich znalostí elektroniky či programovania v '
                           'Pythone.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },),
        '2018': (
            {
                'name': 'Konferencia PyCon SK 2018',
                'date': '09. marec',
                'date_end': '11. marec',
                'speakers': (),
                'location': locations['fiit'],
                'content': '<p>PyCon SK je komunitou organizovaná konferencia pre programovací jazyk Python. '
                           '<p>Viac o konferencii na oficialnom webe: <a href="https://2018.pycon.sk/" target="_blank" '
                           'title="Domovská stránka PyCon SK 2018">https://2018.pycon.sk/</a></p>'
                           '<p><a href="https://www.python.org/" target="_blank" title="Domovská stránka Pythonu">'
                           '<img src="https://2018.pycon.sk/static/img/logo/pycon_long_2018.svg" alt="PyCon SK" '
                           'class="center"></a></p>',
            },
            {
                'name': '29. ' + gettext('Bratislavský Python Meetup'),
                'date': '13. február',
                'speakers': ({
                                 'name': 'Ján Gondoľ',
                                 'link': 'https://www.linkedin.com/in/jangondol',
                                 'link_title': gettext('Profil na LinkedIn') + ': Ján Gondoľ',
                             },),
                'location': locations['progressbar'],

                'content': '<p>TBD</p>'
                           '<p>Budeme mať aj súťaž o jednu licenciu PyCharm Professional.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },
            {
                'name': '28. ' + gettext('Bratislavský Python Meetup'),
                'date': '09. január',
                'speakers': ({
                                 'name': 'Michal Nalevanko',
                                 'link': 'https://sk.linkedin.com/in/mnalevanko',
                                 'link_title': gettext('Profil na LinkedIn') + ': Michal Nalevanko',
                             },),
                'location': locations['progressbar'],

                'content': '<p>TBD</p>'
                           '<p>Budeme mať aj súťaž o jednu licenciu PyCharm Professional.</p>'
                           '<p>Tešíme sa na Vás na stretnutí.</p>',
            },),
    }

    return render_template('index.html', **template_variables)


def get_lastmod(route, sitemap_entry):
    """Used by sitemap() below"""
    if 'lastmod' in sitemap_entry:
        return sitemap_entry['lastmod']

    template = route.rule.split('/')[-1]
    template_file = os.path.join(SRC_DIR, 'templates', template)

    if os.path.exists(template_file):
        return get_mtime(template_file)

    return NOW


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    domain = 'https://spy.pycon.sk'
    pages = []

    # static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            if len(rule.arguments) == 0:
                indx = rule.rule.replace('/', '')
                sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                pages.append({
                    'loc': domain + rule.rule,
                    'lastmod': get_lastmod(rule, sitemap_data),
                    'freq': sitemap_data['freq'],
                    'prio': sitemap_data['prio'],
                })

            elif 'lang_code' in rule.arguments:
                indx = rule.rule.replace('/<lang_code>/', '')

                for lang in LANGS:
                    alternate = []

                    for alt_lang in LANGS:
                        if alt_lang != lang:
                            alternate.append({
                                'lang': alt_lang,
                                'url': domain + rule.rule.replace('<lang_code>', alt_lang)
                            })

                    sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                    pages.append({
                        'loc': domain + rule.rule.replace('<lang_code>', lang),
                        'alternate': alternate,
                        'lastmod': get_lastmod(rule, sitemap_data),
                        'freq': sitemap_data['freq'],
                        'prio': sitemap_data['prio'],
                    })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True, host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=int(os.environ.get('FLASK_PORT', 5000)))
