from __future__ import print_function
import argparse

import itertools
import mechanicalsoup
from getpass import getpass
import re
import datetime


class LibrusOceny():

    def __init__(self):

        self.browser = mechanicalsoup.StatefulBrowser()

        self.base_link = "https://synergia.librus.pl"
        self.oceny = []
        self.oceny2 = []
        self.oceny_skon = []
        self.numerek = 0
        self.numerek_dzien = ''
        self.klasa = ''
        self.full_links = []
        self.full_spr = []
        self.prace = []

    def connectToLibrus(self, username, password):

        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.open("https://synergia.librus.pl/loguj")

        # Fill-in the search form
        self.browser.select_form('.login-form')
        self.browser["login"] = username
        self.browser['passwd'] = password
        self.browser.submit_selected()

        self.getOceny()

    def ocenySprawdzian(self):
        pageOceny = self.browser.open(
            "https://synergia.librus.pl/przegladaj_oceny/uczen")
        p = self.browser.get_current_page()
        oceny = p.findAll("span", style="background-color:#FF0000; ")

        a_atr = []
        for a in oceny:
            te = a.find('a')
            a_atr.append(te)

        linki = [link['href'] for link in a_atr]

        ocenyInfoSpr = []
        for table in linki:
            page = self.browser.open(self.base_link + table)
            p = self.browser.get_current_page()
            table = p.find(
                'table', class_='decorated medium center').find('tbody')
            ocena = table.find('tr', class_='line1').find('td')
            clean = [i.strip() for i in table.text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]

            d = dict(itertools.zip_longest(*[iter(clean)] * 2, fillvalue=""))

            # d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}
            if 'Dodał' in d:
                del d['Dodał']
            if 'Widoczność' in d:
                del d['Widoczność']

            if d['Kategoria'] == 'klasówka':
                d['Kategoria'] = 'sprawdzian'

            if 'Komentarz' in d:
                pass
            else:
                d.update({'Komentarz': 'Brak'})
            ocenyInfoSpr.append(d)

        return ocenyInfoSpr

    def getOceny(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/przegladaj_oceny/uczen")
        p = self.browser.get_current_page()
        x = p.findAll('span', class_='grade-box')

        self.oceny = [t.text for t in x]

        self.replaceGrades()
        self.konfiguracjaOcen(self.oceny2)
        self.sredniaArytmetyczna(self.oceny2)
        self.ocenkiDoWyswietlenia()
        self.getLuckyNumber()
        self.sprawdziany()
        self.prace_klasowe()

    def getUserName(self):
        info_page = self.browser.open('https://synergia.librus.pl/informacja')
        response = self.browser.get_current_page()
        table = response.find(
            'table', class_='decorated big center form').find('tbody')
        line_imie = table.find('tr', class_='line1').find('td')

        return line_imie.text

    def numerUcznia(self):
        info_page = self.browser.open('https://synergia.librus.pl/informacja')
        response = self.browser.get_current_page()
        table = response.find(
            'table', class_='decorated big center form').find('tbody')

        all_lines1 = table.findAll('tr', class_='line1')
        numrek_line = all_lines1[1].find('td')
        numerek = ''.join(numrek_line.text.split())

        return numerek

    def klasaUcznia(self):
        page4 = self.browser.open(
            "https://synergia.librus.pl/informacja")
        p = self.browser.get_current_page()
        klasa = p.find('tr', class_='line0').find('td').text
        klasa = ' '.join((klasa.split()))

        return klasa

    def ocenkiDoWyswietlenia(self):
        for ocena in self.oceny:
            ocena = ocena.replace('\n', '')
            self.oceny_skon.append(ocena)
        del self.oceny_skon[0]
        self.oceny_skon.remove('')
        self.oceny_skon = list(
            filter(lambda a: a != 'np' and a != 'T', self.oceny_skon))

    def replaceGrades(self):
        for ocena in self.oceny:
            ocena = ocena.replace('\n', '')
            ocena = ocena.replace('6-', '5.75')
            ocena = ocena.replace('5-', '4.75')
            ocena = ocena.replace('5+', '5.5')
            ocena = ocena.replace('4-', '3.75')
            ocena = ocena.replace('4+', '4.5')
            ocena = ocena.replace('3-', '2.75')
            ocena = ocena.replace('3+', '3.5')
            ocena = ocena.replace('2-', '1.75')
            ocena = ocena.replace('2+', '2.5')
            ocena = ocena.replace('1-', '0.75')
            ocena = ocena.replace('1+', '1.5')
            self.oceny2.append(ocena)

    def getLuckyNumber(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/uczen_index")
        p = self.browser.get_current_page()
        self.numerek_dzien = p.find('h2', class_='center').text
        self.numerek_dzien = [e for e in self.numerek_dzien.replace(
            '\n', ' ').split(' ') if e != '']
        self.numerek_dzien = ' '.join(self.numerek_dzien)

        self.numerek = p.find(
            "div", class_="szczesliwy-numerek").find("span").text

        try:
            self.numerek = int(self.numerek)
        except:
            pass

    def getGradesLink(self):
        pageOceny = self.browser.open(
            'https://synergia.librus.pl/przegladaj_oceny/uczen')

        p = self.browser.get_current_page()
        oceny_list = p.findAll('a', class_='ocena')

        # oceny_link = [ocena.text for ocena in oceny_list]

        oceny_link = [ocena['href'] for ocena in oceny_list if ocena.text not in (
            'np', '0', 'bz', '-', '+', 'T')]
        del oceny_link[0]

        return oceny_link

    def getGradesWithTypes(self, gradesLink):

        grades = []
        types = []
        for grade_link in gradesLink:
            grade_page = self.browser.open(self.base_link + grade_link)
            p = self.browser.get_current_page()
            table = p.find('table', class_='decorated medium center')
            grade = table.find('tr', class_='line1').find('td').text
            grade_type = table.find('tr', class_='line0').find('td').text
            grades.append(grade)
            types.append(grade_type)

        x = dict(zip(grades, types))
        print(x)

    def prace_klasowe(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/terminarz")
        p = self.browser.get_current_page()
        kalendarz = p.find('table', class_='kalendarz').findAll(
            'td', class_='center')

        x = []
        for prac_kl in kalendarz:
            prace_klasowa = prac_kl.findAll(
                'td', style='background-color: #FFD700; cursor: pointer;')

            for y in prace_klasowa:
                x.append(y['onclick'])

        linki2 = []
        base = 'https://synergia.librus.pl'
        full_links = []
        for cut in x:
            cut = cut.split("location.href='", 1)[1]
            cut = cut[:-1]
            linki2.append(cut)
            pelen_link = base + cut
            full_links.append(pelen_link)

        opisy = []
        te = []
        for link in self.full_links[:2]:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            # Clean the input data by splitting by row and removing blanks
            clean = [i.strip() for i in tab_text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]
            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}

        for link in full_links:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            clean = [i.strip() for i in tab_text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]
            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}
            if 'Przedmiot' in d:
                pass

            else:
                d.update({'Przedmiot': 'Język polski'})
            self.prace.append(d)

    def sprawdziany(self):
        now = datetime.datetime.now()

        page3 = self.browser.open(
            "https://synergia.librus.pl/terminarz")
        p = self.browser.get_current_page()
        kalendarz = p.find('table', class_='kalendarz').findAll(
            'td', class_='center')

        x = []
        for spr in kalendarz:

            # lista sprawdzianów
            sprawdzian = spr.findAll(
                'td', style='background-color: #7B68EE; cursor: pointer;')

            # jeden sprawdzian

            for y in sprawdzian:
                x.append(y['onclick'])

        linki2 = []
        base = 'https://synergia.librus.pl'

        for cut in x:
            cut = cut.split("location.href='", 1)[1]
            cut = cut[:-1]
            linki2.append(cut)
            pelen_link = base + cut
            self.full_links.append(pelen_link)

        for link in self.full_links:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            clean = [i.strip() for i in tab_text.split("\n") if i]

            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}

            if d['Nauczyciel'] == 'Szczygieł Agnieszka':
                d.update({'Przedmiot': 'Geografia'})
            if d['Nauczyciel'] == 'Hajduk Aleksandra':
                d.update({'Przedmiot': 'Język polski'})
            # jeśli nie ma podanego przedmiotu
            if d.get("Przedmiot", None) == None:
                d.update({"Przedmiot": "Nie został podany"})

            self.full_spr.append(d)

    def wiadomosci(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/wiadomosci")
        p = self.browser.get_current_page()
        tabela = p.find('table', style='margin: 5px 0px;').find(
            'tbody').findAll('td')

        linki_do_wiado = []
        for td in tabela:
            x = td.findAll('a')
            for y in x:
                linki_do_wiado.append(y['href'])

        linki_do_wiado = list(filter(
            lambda a: a != 'javascript:void(0); return false;', linki_do_wiado))

        wiadomosci_linki_pelne = []
        for link in linki_do_wiado:
            pelen = self.base_link + link
            wiadomosci_linki_pelne.append(pelen)

        messages = []
        for message_link in wiadomosci_linki_pelne:
            message_page = self.browser.open(message_link)
            p = self.browser.get_current_page()
            tabela_main = p.find('div', class_='container-background') \
                .find('table', class_='stretch container-message')

            tabela_info = tabela_main.findAll('table', class_='stretch')[
                2].findAll('td', class_='left')

            info = [i.text for i in tabela_info]

            dict_info = dict(itertools.zip_longest(
                *[iter(info)] * 2, fillvalue=""))

            message_body = tabela_main.find(
                'div', class_='container-message-content')
            message = message_body.text
            dict_info.update({'Widaomośc': message})

            messages.append(dict_info)

        return messages

    def konfiguracjaOcen(self, oceny):
        try:
            del oceny[0]
        except IndexError:
            raise Exception("BŁĄD")
        try:
            oceny.remove('0')
            oceny.remove('')
            oceny.remove('-')
            oceny.remove('+')
            oceny.remove('bz')
        except:
            pass
        self.oceny2 = list(
            filter(lambda a: a != 'np' and a != '0' and a != 'T' and a != 'bz' and a != '+' and a != '-', oceny))
        self.oceny2 = list(map(float, self.oceny2))

    def sredniaArytmetyczna(self, oceny):
        liczba_ocen = len(oceny)
        wartos_ocen = sum(oceny)

        srednia = wartos_ocen / liczba_ocen

        return srednia
