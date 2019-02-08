#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Biblioteka(object):
    lista_bibliotek=[]

    def __init__(self,nazwa, numer, adres):
        self.nazwa = nazwa
        self.numer = numer
        self.adres = adres

        self.lista_tytulow_biblioteki = []

        self.rezerwacje = []
        self.odbiory = []
        self.wypozyczenia = []
        self.zamowienia = []

        self.__class__.lista_bibliotek.append(self)

#BIBLIOTEKA STAN
    def dostepne_tytuly(self):
        for tytul in self.lista_tytulow_biblioteki:
            print (" - %s - %i szt" %(tytul[0], tytul[1]))
        return ('')

#BIBLIOTEKA USŁUGI
    def dodaj_wypozyczenie(self, tytul, Klient_ID):
        self.tytul = tytul
        self.Klient_ID = Klient_ID

        for tytul in self.lista_tytulow_biblioteki:
            if tytul[0] == self.tytul:
                if tytul [1] > 0:
                    for nazwa_tytulu in Tytul.lista_tytulow:
                        if nazwa_tytulu.nazwa == tytul[0]:
                            nr_egz=nazwa_tytulu.lista_egzemplarzy_tytulu.pop(0)
                            self.odbiory.append([nr_egz,self.tytul,self.Klient_ID])
                            nazwa_tytulu.ilosc_stan=nazwa_tytulu.ilosc_stan - 1
                            tytul[1]=tytul[1]-1
                            return("Książka jest dostępna zapraszamy po odbiór")
                else:
                    print("Wszystkie egzemplarze tej książki są wypożyczone czy dodać rezerwację?")
                    while True:
                        dec = input('Wpisz T lub N: ')
                        if dec == 'T':
                            self.rezerwacje.append((self.tytul, Klient_ID))
                            return ('Dodaliśmy rezerwacje z danym tytułem')
                        elif dec == 'N':
                            return ('OK!')
                        else:
                            print('Zły znak wpisz T lub N: ')

    def zwrot(self, wypozyczenie):
        self.wypozyczenie = wypozyczenie
        self.nr_egz = wypozyczenie[0][0]
        self.tytul = wypozyczenie[0][1]
        self.Klient_ID = wypozyczenie[0][2]

        for tytul in self.lista_tytulow_biblioteki:
            if tytul[0] == self.tytul:
                for nazwa_tytulu in Tytul.lista_tytulow:
                    if nazwa_tytulu.nazwa == tytul[0]:
                        nazwa_tytulu.lista_egzemplarzy_tytulu.append(self.nr_egz)
                        nazwa_tytulu.ilosc_stan=nazwa_tytulu.ilosc_stan + 1
                        tytul[1]=tytul[1]+1
                        self.wypozyczenia.remove(self.wypozyczenie)
                        for rezerwacja in self.rezerwacje:
                            if rezerwacja[0] == self.tytul:
                                print("Klient o ID: %i zostanie poinformany o dostępności zarezerwowanje książki" % rezerwacja[1])
                                self.dodaj_wypozyczenie(rezerwacja[0], rezerwacja[1])
                                self.rezerwacje.remove(rezerwacja)
                            else:
                                print("Nie ma takiej rezerwacji")
                        return("Dziękujemy za zwrot książki")

class Klient(object):
    ID_default=1
    lista_klientow=[]
    limit_wypozyczen=5

    def __init__(self, imie_klienta, nazwisko_klienta, PESEL_klienta, adres_klienta):
        self.Klient_ID = Klient.ID_default
        Klient.ID_default = Klient.ID_default + 1
        self.imie = imie_klienta
        self.nazwisko = nazwisko_klienta
        self.PESEL = PESEL_klienta
        self.adres = adres_klienta

        self.zarejestrowany = 0
        self.zalogowany = 0


        self.tytuly_wypozyczone = []
        self.__class__.lista_klientow.append(self)

#KLIENT KONTO
    def zarejestruj(self):

        if(self.zarejestrowany==0):
            print("Aby się zarejestrować ustal hasło")

            self.haslo = input("Hasło: ")
            self.zarejestrowany=1
            print ("Klient został zarejestrowany")
        else:
            print ("Jesteś już zarejestorwany!")

    def zaloguj(self):


        if(self.zalogowany==0):
            haslo_klienta = input("Wpisz hasło: ")
            if(self.haslo==haslo_klienta and self.zarejestrowany==1):
                self.zalogowany = 1
                print ("Klient został zalogowany")
            else: print ("Error")
        else: print("Jesteś już zalogowany")

    def wyloguj(self):
        if(self.zalogowany==1):
            self.zalogowany = 0
            print ("Zostałeś wylogowany")
        else: print ("Nie byłeś zalogowany!")

#KLIENT - BIBLIOTEKA
    def przegladaj(self):
        for biblioteka in Biblioteka.lista_bibliotek:
            print("Biblioteka > %s < posiada następujące książki" % biblioteka.nazwa)
            print(biblioteka.dostepne_tytuly())

    def wypozyczenie(self):

        if(self.zalogowany==1):

            if len(self.tytuly_wypozyczone)==self.limit_wypozyczen:
                print ("Nie można wypożczyć kolejnych książek, musisz zwrócić wypożyczone.")
                return

            print("Jaki tytuł chcesz wypożyczyć?")
            tytul = input()
            print("W jakiej bibliotece chcesz wypożyczyć ten tytuł? (Wpisz nr biblitoeki)")
            Biblioteka_ID = int(input())

            for biblioteka in Biblioteka.lista_bibliotek:
                if biblioteka.numer == Biblioteka_ID:
                    print("Biblioteka %s" % biblioteka.nazwa)
                    for nazwa_tytulu in biblioteka.lista_tytulow_biblioteki:
                        if nazwa_tytulu[0] == tytul:
                            return biblioteka.dodaj_wypozyczenie(tytul,self.Klient_ID)

                    print("W tej bibliotece nie ma takiej książki")
                    return
        else:
            print("Musisz się zalogować żeby wypożyczyć książke")

    def pokaz_wypozyczenia(self,bibliotekarz_access=0):
        if(self.zalogowany==1 or bibliotekarz_access==1):
            print("Lista wypożyczonych tytułów: ")

            if len(self.tytuly_wypozyczone)==0:
                return ("Brak wypożyczeń")
            i = 1
            for self.wypozczyenie in self.tytuly_wypozyczone:
                print('%i. %s' % (i, self.wypozczyenie))
                i += 1
        else:
            print("Musisz się zalogować żeby wypożyczyć książke")#pokazac wypozyczenia, nie wypozyczyc

class Bibliotekarz(object):
    ID_default = 1
    lista_bibliotekarzy = []


    def __init__(self, imie_bibliotekarza, nazwisko_bibliotekarza, nr_biblioteki):

        self.Bibliotekarz_ID = Bibliotekarz.ID_default
        Bibliotekarz.ID_default = Bibliotekarz.ID_default + 1
        self.imie = imie_bibliotekarza
        self.nazwisko = nazwisko_bibliotekarza
        self.nr_biblioteki = nr_biblioteki

        for biblioteka in Biblioteka.lista_bibliotek:
            if biblioteka.numer == self.nr_biblioteki:
                self.biblioteka = biblioteka

        self.__class__.lista_bibliotekarzy.append(self)


# KLIENT - BIBLIOTEKARZ
    def odbior(self):

        print("Zweryfikuj Klienta!")
        self.Klient_ID = int(input("Podaj ID Klienta: "))

        for odbior in self.biblioteka.odbiory:
            if odbior[2] == self.Klient_ID:
                for klient in Klient.lista_klientow:
                    if klient.Klient_ID == self.Klient_ID:
                        print("Klient odebrał tytuł : %s" % odbior[1])
                        self.biblioteka.odbiory.remove(odbior)
                        klient.tytuly_wypozyczone.append([odbior, self.Bibliotekarz_ID])
                        self.biblioteka.wypozyczenia.append([odbior, self.Bibliotekarz_ID])
                        return ("Dziękujemy za odbiór")

        print("Nie ma odbioru dla tego klienta")

    def anuluj_odbior(self):
        print("Lista odbiorów: ")
        i=1
        for odbior in self.biblioteka.odbiory:
            print("%i - %s" %(i,odbior))
            i+=1

        numer=int(input("Wpisz numer odbioru który chcesz anulować"))

        self.odbior=self.biblioteka.odbiory[numer-1]
        print("Mineło 5 dni - klient nie odebrał tytulu.\n Tytuł wraca na stan.")
        self.biblioteka.odbiory.remove(self.odbior)
        for tytul in self.biblioteka.lista_tytulow_biblioteki:
            if tytul[0] == self.odbior[1]:
                for nazwa_tytulu in Tytul.lista_tytulow:
                    if nazwa_tytulu.nazwa == tytul[0]:
                        nazwa_tytulu.lista_egzemplarzy_tytulu.append(self.odbior[0])
                        nazwa_tytulu.ilosc_stan = nazwa_tytulu.ilosc_stan + 1
                        tytul[1] = tytul[1] + 1
                        return "Odbiór anulowany"




        return "Nie ma takiego klienta"

    def przyjmij_zwrot(self):

        print("Zweryfikuj Klienta!")
        self.Klient_ID=int(input("Podaj ID Klienta: "))

        for klient in Klient.lista_klientow:
            if klient.Klient_ID == self.Klient_ID:
                klient.pokaz_wypozyczenia(bibliotekarz_access=1)
                print("Który z tych tytułów zwraca klient (Wpisz numer)")
                numer = int(input())

                self.biblioteka.zwrot(klient.tytuly_wypozyczone[numer-1])
                klient.tytuly_wypozyczone.remove(klient.tytuly_wypozyczone[numer - 1])
                return("Dziękujemy za zwrot")

        return ("Nie ma takiego klienta")

# BIBLIOTEKARZ - ZAMÓWIENIA

    def zamow_ksiazke(self):

        print("Wpisz tytul ksiazki jaki chcesz zamowic: ")
        tytul = input()
        ilosc= 1


        print("Czy ksiazka jest popularna?")
        while True:
            dec = input('Wpisz T lub N: ')
            if dec == 'T':
                ilosc=5
                return self.biblioteka.zamowienia.append([tytul,ilosc])
            elif dec == 'N':
                return self.biblioteka.zamowienia.append([tytul, ilosc])
            else:
                print('Zły znak wpisz T lub N: ')

    def odbierz_zamowienie(self):

        if len(self.biblioteka.zamowienia)==0:
            return ("Brak zamowien do odebrania")
        i=1
        for zamowienie in self.biblioteka.zamowienia:
            print("%i - %s" %(i,zamowienie))
            i+=1

        print("Które zamówienie chcesz odebrać?")
        numer = int(input("Wpisz numer"))

        self.tytul = self.biblioteka.zamowienia[numer-1][0]
        self.ilosc = self.biblioteka.zamowienia[numer-1][1]


        if self.tytul not in self.biblioteka.lista_tytulow_biblioteki:
            self.dodaj_nowy_tytul()
        else:
            print("Bład")

        self.dodaj_egz(tytul=self.tytul,ilosc=self.ilosc)

# BIBLIOTEKARZ - STAN(BIBLIOTEKA),

    def przegladaj(self):

        print("Biblioteka > %s < posiada następujące książki" % self.biblioteka.nazwa)
        print(self.biblioteka.dostepne_tytuly())

    def dodaj_nowy_tytul(self):

        print("Wprowadz dane dla nowego tytułu: ")
        nazwa_tytulu = input("Tytuł :")
        autor_tytulu = input("Autor :")
        wydawnictwo = input("Wydawnictwo :")
        ISBN = input("ISBN :")

        Tytul(nazwa_tytulu,autor_tytulu,wydawnictwo,ISBN)
        self.biblioteka.lista_tytulow_biblioteki.append([nazwa_tytulu, 0])

    def dodaj_egz(self,tytul='',ilosc=0):

        if (ilosc==0):
            self.tytul = input("Podaj tytuł egzemplarza ktory dodac: ")
            self.ilosc = int(input("Podaj ilosc egzemplarzy do wprowadzenia: "))
        else:
            self.tytul = tytul
            self.ilosc = ilosc

        for i in range(self.ilosc):
            Egzemplarz().dodaj_egz(self.tytul)

            for tytul in self.biblioteka.lista_tytulow_biblioteki:
                if tytul[0] == self.tytul:
                    tytul[1]+=1

    def usun_egz(self):
    # nie działą ? brak pomysłu !!!
        self.nr_egz = int(input("Podaj nr egz który chcesz usunąć: "))
        self.tytul = input("Wpisz tytul egzemplarza")

        for tytul in Tytul.lista_tytulow:
            if tytul.nazwa == self.tytul:
                if self.nr_egz in tytul.lista_egzemplarzy_tytulu:
                    tytul.lista_egzemplarzy_tytulu.remove(self.nr_egz)
                    for egz in Egzemplarz.lista_egzemplarzy:
                        if egz.nr_egz == self.nr_egz:
                            egz.__del__
                else:
                    print("Egzemplarz ktory chcesz usunać jest wypożyczony\n lub dany tytul nie ma takiego nr egzemplarza")



class Tytul(object):
    lista_tytulow=[]

    def __init__(self,nazwa_tytulu,autor_tytulu,wydawnictwo_tytulu,ISBN_tytulu):

        self.nazwa = nazwa_tytulu
        self.autor = autor_tytulu
        self.wydawnictwo = wydawnictwo_tytulu
        self.ISBN = ISBN_tytulu

        self.miejsce = 0
        self.ilosc_stan = 0
        self.__class__.lista_tytulow.append(self)

        self.lista_egzemplarzy_tytulu=[]

#Początkowe dodanie kilku tytułów do biblioteki
    def dodaj_tytul(self,Biblioteka_ID,ilosc):
        self.Biblioteka_ID = Biblioteka_ID

        for biblioteka in Biblioteka.lista_bibliotek:
            if biblioteka.numer==Biblioteka_ID:
                biblioteka.lista_tytulow_biblioteki.append([self.nazwa, ilosc])

class Kaseta(Tytul):

    def __init__(self, nazwa_tytulu, autor_tytulu, wydawnictwo_tytulu, ISBN_tytulu, nazwisko_aktora, limit_dni=30):
        Egzemplarz.__init__(self,nazwa_tytulu, autor_tytulu, wydawnictwo_tytulu, ISBN_tytulu, limit_dni)
        self.aktor = nazwisko_aktora

class Egzemplarz(object):
    nr_egz=1
    lista_egzemplarzy = []

    def __init__(self,limit_dni=30):
        self.limit = limit_dni
        self.nr_egz = Egzemplarz.nr_egz
        Egzemplarz.nr_egz = Egzemplarz.nr_egz +1

        self.__class__.lista_egzemplarzy.append(self)

    def __del__(self):
        print ("Egzemplarz usunieto")


    def dodaj_egz(self,tytul):
        self.tytul = tytul

        for tytul in Tytul.lista_tytulow:
            if tytul.nazwa == self.tytul:
                tytul.ilosc_stan = tytul.ilosc_stan + 1
                tytul.lista_egzemplarzy_tytulu.append(self.nr_egz)








#Biblioteki
B1=Biblioteka("Południowa",1,"Szybka 3")
B2=Biblioteka("Wschodnia",2,"Parkowa 5")
B3=Biblioteka("Rynek",3,"Rynek 15")

#Bibliotekarze
P1=Bibliotekarz("Bartek","Hojski",1)
P2=Bibliotekarz("Natalia","Rybska",2)


#Klienci
K1=Klient("Aneta","Królikowska",95021602145,"Kochanowskiego 2")
K2=Klient("Tomasz","Grudewski",94122225489,"Bliska 1")
K3=Klient("Nadia","Nijaka",96031125142,"Koszarowa 4")

#Tytuly
T1=Tytul("ABC","autor 1","Wyd. A",123)
T2=Tytul("XYZ","autor 2","Wyd. B",124)


#Egzemplarze
E1=Egzemplarz()
E1.dodaj_egz("ABC")
E2=Egzemplarz()
E2.dodaj_egz("ABC")
E3=Egzemplarz()
E3.dodaj_egz("XYZ")

#Dodanie tytulow do bibliotek
T1.dodaj_tytul(1,T1.ilosc_stan)
T2.dodaj_tytul(1,T2.ilosc_stan)

#Dodanie rezerwacji
B1.dodaj_wypozyczenie("ABC",1)
B1.dodaj_wypozyczenie("ABC",2)



#P1.zamow_ksiazke()

while True:
    print("Kim jesteś?")
    print("1.Bibliotekarz")
    print("2.Klient")

    numer=int(input("Wpisz numer: "))

    if(numer==1):
        while True:
            print("\nWitaj bibliotekarzu!")
            i=1
            for bibliotekarz in Bibliotekarz.lista_bibliotekarzy:
                print("%i - %s" %(i, bibliotekarz.nazwisko))
                i+=1

            print("Wpisz nr bibliotekarza którym jesteś LUB wpisz 0 jeśli chcesz stworzyć nowego")
            numer_2=int(input("Wpisz numer"))
            if (numer_2==0):
                imie=input("Wpisz imie: ")
                nazwisko=input("Wpisz nazwisko: ")
                nr_biblioteki=int(input("Wpisz nr biblioteki: "))

                Bibliotekarz(imie,nazwisko,nr_biblioteki)
            else:
                bibliotekarz = Bibliotekarz.lista_bibliotekarzy[numer_2-1]
                print("\nWitaj %s" % bibliotekarz.nazwisko)

                print(">Co chcesz zrobić?")
                print(" 1. Wykonaj odbiór książki")
                print(" 2. Anuluj odbiór książki")
                print(" 3. Przyjmij zwrot książki")
                print(" 4. Zamów książkę")
                print(" 5. Odbierz zamówienie")
                print(" 6. Przeglądaj książki")
                print(" 7. Dodaj nowy tytuł")
                print(" 8. Dodaj egzemplarz")
                print(" 9. Usuń egzemplarz")
                print(" 10. Zakończ prace z systemem")

                numer_3=int(input("Wpisz numer"))

                if(numer_3 == 1):
                    bibliotekarz.odbior()
                elif(numer_3 == 2):
                    bibliotekarz.anuluj_odbior()
                elif(numer_3 == 3):
                    bibliotekarz.przyjmij_zwrot()
                elif(numer_3 == 4):
                    bibliotekarz.zamow_ksiazke()
                elif (numer_3 == 5):
                    bibliotekarz.odbierz_zamowienie()
                elif (numer_3 == 6):
                    bibliotekarz.przegladaj()
                elif (numer_3 == 7):
                    bibliotekarz.dodaj_nowy_tytul()
                elif (numer_3 == 8):
                    bibliotekarz.dodaj_egz()
                elif (numer_3 == 9):
                    bibliotekarz.usun_egz()
                elif (numer_3 == 10):
                    print("Żegnaj!\n")
                    break
                else:
                    print("Zły numer ")


    elif(numer==2):
        while True:
            print("\nWitaj kliencie!")
            i=1
            for klient in Klient.lista_klientow:
                print("%i - %s" %(i, klient.nazwisko))
                i+=1

            print("Wpisz nr klienta którym jesteś LUB wpisz 0 jeśli chcesz stworzyć nowego")
            numer_2=int(input("Wpisz numer"))
            if (numer_2 == 0):
                imie = input("Wpisz imie: ")
                nazwisko = input("Wpisz nazwisko: ")
                PESEL = input("Wpisz nr biblioteki: ")
                adres = input("Wpisz adres: ")

                Klient(imie, nazwisko, PESEL, adres)
            else:
                while True:
                    klient = Klient.lista_klientow[numer_2 - 1]
                    print("\nWitaj %s" % klient.nazwisko)

                    print(">Co chcesz zrobić?")
                    print(" 1. Przeglądaj")
                    print(" 2. Zarejestruj")
                    print(" 3. Zaloguj")
                    print(" 4. Wypożycz")
                    print(" 5. Pokaż wypożyczenia")
                    print(" 6. Wyloguj")

                    numer_3 = int(input("Wpisz numer"))

                    if (numer_3 == 1):
                        klient.przegladaj()
                    elif (numer_3 == 2):
                        klient.zarejestruj()
                    elif (numer_3 == 3):
                        klient.zaloguj()
                    elif (numer_3 == 4):
                        klient.wypozyczenie()
                    elif (numer_3 == 5):
                        klient.pokaz_wypozyczenia()
                    elif (numer_3 == 6):
                        klient.wyloguj()
                    else:
                        print("Zły numer ")


    else:
        print("Zły numer")

