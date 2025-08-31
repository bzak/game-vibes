
import pygame
import random
import sys

# Inicjalizacja pygame
pygame.init()
pygame.mixer.init()  # Inicjalizacja dźwięku

# Kolory (w formacie RGB)
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
NIEBIESKI = (0, 100, 255)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
ZOLTY = (255, 255, 0)
FIOLETOWY = (128, 0, 128)
SREBRNY = (192, 192, 192)

# Ustawienia okna gry
SZEROKOSC = 800
WYSOKOSC = 600
okno = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("🚀 Statek Kosmiczny kontra Ufoludki! 🛸")

# Zegar do kontroli szybkości gry
zegar = pygame.time.Clock()

# Funkcje do tworzenia prostych dźwięków
def stworz_prosty_dzwiek(czestotliwosc, czas_ms):
    """Tworzy prosty dźwięk o danej częstotliwości"""
    try:
        import math
        sample_rate = 22050
        frames = int(czas_ms * sample_rate / 1000)
        
        # Tworzymy falę sinusoidalną
        fala = []
        for i in range(frames):
            # Obliczamy wartość fali
            czas = i / sample_rate
            amplituda = int(4096 * math.sin(2 * math.pi * czestotliwosc * czas) * (1 - czas * 4))
            # Stereo - ta sama wartość dla lewego i prawego kanału
            fala.append([amplituda, amplituda])
        
        return pygame.sndarray.make_sound(fala)
    except Exception as e:
        print(f"Nie można stworzyć dźwięku: {e}")
        return None

def stworz_dzwiek_szumu(czas_ms):
    """Tworzy dźwięk szumu (dla eksplozji)"""
    try:
        import random
        sample_rate = 22050
        frames = int(czas_ms * sample_rate / 1000)
        
        fala = []
        for i in range(frames):
            # Losowy szum z malejącą amplitudą
            amplituda = int(random.randint(-2000, 2000) * (1 - i / frames))
            fala.append([amplituda, amplituda])
        
        return pygame.sndarray.make_sound(fala)
    except Exception as e:
        print(f"Nie można stworzyć szumu: {e}")
        return None

# Tworzymy proste dźwięki
print("🔊 Tworzę dźwięki...")
dzwiek_strzal = stworz_prosty_dzwiek(800, 100)  # Wysoki ton, 100ms
dzwiek_trafienie = stworz_dzwiek_szumu(300)     # Szum, 300ms
dzwiek_kolizja = stworz_prosty_dzwiek(200, 500) # Niski ton, 500ms

if dzwiek_strzal:
    print("✅ Dźwięk strzału gotowy!")
else:
    print("❌ Problem z dźwiękiem strzału")
    
if dzwiek_trafienie:
    print("✅ Dźwięk trafienia gotowy!")
else:
    print("❌ Problem z dźwiękiem trafienia")
    
if dzwiek_kolizja:
    print("✅ Dźwięk kolizji gotowy!")
else:
    print("❌ Problem z dźwiękiem kolizji")

class Statek:
    def __init__(self, typ="podstawowy"):
        self.x = SZEROKOSC // 2
        self.y = WYSOKOSC - 80
        self.typ = typ
        
        # Różne typy statków
        if typ == "podstawowy":
            self.szerokosc = 60
            self.wysokosc = 40
            self.predkosc = 7
            self.kolor_glowny = SREBRNY
            self.kolor_silniki = NIEBIESKI
            self.podwojne_strzaly = False
        elif typ == "szybki":
            self.szerokosc = 50
            self.wysokosc = 35
            self.predkosc = 10
            self.kolor_glowny = (255, 215, 0)  # Złoty
            self.kolor_silniki = (255, 100, 0)  # Pomarańczowy
            self.podwojne_strzaly = False
        elif typ == "podwojny":
            self.szerokosc = 70
            self.wysokosc = 45
            self.predkosc = 6
            self.kolor_glowny = (128, 0, 128)  # Fioletowy
            self.kolor_silniki = (255, 0, 255)  # Magenta
            self.podwojne_strzaly = True
        elif typ == "pancerny":
            self.szerokosc = 80
            self.wysokosc = 50
            self.predkosc = 5
            self.kolor_glowny = (64, 64, 64)  # Ciemny szary
            self.kolor_silniki = CZERWONY
            self.podwojne_strzaly = False
        elif typ == "stealth":
            self.szerokosc = 45
            self.wysokosc = 30
            self.predkosc = 9
            self.kolor_glowny = (25, 25, 25)  # Prawie czarny
            self.kolor_silniki = (0, 255, 255)  # Cyjan
            self.podwojne_strzaly = False
        elif typ == "rakietowy":
            self.szerokosc = 65
            self.wysokosc = 40
            self.predkosc = 7
            self.kolor_glowny = (255, 69, 0)  # Czerwono-pomarańczowy
            self.kolor_silniki = ZOLTY
            self.podwojne_strzaly = True  # Rakiety!
        elif typ == "plazma":
            self.szerokosc = 55
            self.wysokosc = 35
            self.predkosc = 8
            self.kolor_glowny = (0, 255, 127)  # Zielono-niebieski
            self.kolor_silniki = (255, 20, 147)  # Różowy
            self.podwojne_strzaly = False
        elif typ == "quantum":
            self.szerokosc = 75
            self.wysokosc = 45
            self.predkosc = 6
            self.kolor_glowny = (138, 43, 226)  # Fioletowy
            self.kolor_silniki = (255, 215, 0)  # Złoty
            self.podwojne_strzaly = True
        elif typ == "alien":
            self.szerokosc = 90
            self.wysokosc = 55
            self.predkosc = 4
            self.kolor_glowny = (50, 205, 50)  # Zielony
            self.kolor_silniki = (255, 0, 255)  # Magenta
            self.podwojne_strzaly = True
        elif typ == "crystal":
            self.szerokosc = 40
            self.wysokosc = 25
            self.predkosc = 12
            self.kolor_glowny = (173, 216, 230)  # Jasnoniebieski
            self.kolor_silniki = BIALY
            self.podwojne_strzaly = False
        
    def rysuj(self, okno):
        # Korpus statku (trójkąt w kolorze statku)
        punkty = [
            (self.x, self.y),  # czubek
            (self.x - self.szerokosc//2, self.y + self.wysokosc),  # lewy dolny
            (self.x + self.szerokosc//2, self.y + self.wysokosc)   # prawy dolny
        ]
        pygame.draw.polygon(okno, self.kolor_glowny, punkty)
        
        # Silniki (w kolorze statku)
        odleglosc_silnikow = 15 if self.typ != "podwojny" else 20
        pygame.draw.circle(okno, self.kolor_silniki, (self.x - odleglosc_silnikow, self.y + self.wysokosc + 5), 8)
        pygame.draw.circle(okno, self.kolor_silniki, (self.x + odleglosc_silnikow, self.y + self.wysokosc + 5), 8)
        
        # Dodatkowe silniki dla statku podwójnego
        if self.typ == "podwojny":
            pygame.draw.circle(okno, self.kolor_silniki, (self.x - 35, self.y + self.wysokosc + 3), 6)
            pygame.draw.circle(okno, self.kolor_silniki, (self.x + 35, self.y + self.wysokosc + 3), 6)
        
        # Kokpit (żółte okienko)
        pygame.draw.circle(okno, ZOLTY, (self.x, self.y + 15), 8)
        
        # Specjalne oznaczenia dla różnych typów
        if self.typ == "szybki":
            # Paski szybkości
            for i in range(3):
                pygame.draw.line(okno, BIALY, 
                               (self.x - 10 + i * 10, self.y + 25), 
                               (self.x - 10 + i * 10, self.y + 30), 2)
        elif self.typ == "pancerny":
            # Pancerz
            pygame.draw.rect(okno, BIALY, (self.x - 15, self.y + 20, 30, 5))
        elif self.typ == "stealth":
            # Niewidzialne linie stealth
            for i in range(2):
                pygame.draw.line(okno, (100, 100, 100), 
                               (self.x - 20 + i * 40, self.y + 10), 
                               (self.x - 10 + i * 20, self.y + 35), 1)
        elif self.typ == "rakietowy":
            # Rakiety po bokach
            pygame.draw.rect(okno, CZERWONY, (self.x - 25, self.y + 15, 8, 20))
            pygame.draw.rect(okno, CZERWONY, (self.x + 17, self.y + 15, 8, 20))
        elif self.typ == "plazma":
            # Plazma w środku
            pygame.draw.circle(okno, (0, 255, 255), (self.x, self.y + 20), 6)
            pygame.draw.circle(okno, BIALY, (self.x, self.y + 20), 3)
        elif self.typ == "quantum":
            # Quantum efekt - migające kropki
            import random
            for i in range(4):
                if random.randint(1, 3) == 1:  # Losowe miganie
                    x_pos = self.x - 15 + i * 10
                    pygame.draw.circle(okno, (255, 255, 255), (x_pos, self.y + 25), 2)
        elif self.typ == "alien":
            # Alien wzory
            pygame.draw.polygon(okno, (255, 255, 0), 
                              [(self.x, self.y + 10), (self.x - 8, self.y + 25), (self.x + 8, self.y + 25)])
        elif self.typ == "crystal":
            # Kryształowe wzory
            pygame.draw.polygon(okno, BIALY, 
                              [(self.x, self.y + 15), (self.x - 6, self.y + 22), 
                               (self.x, self.y + 29), (self.x + 6, self.y + 22)])
    
    def ruch(self, klawisze):
        # Sterowanie strzałkami
        if klawisze[pygame.K_LEFT] and self.x > self.szerokosc//2:
            self.x -= self.predkosc
        if klawisze[pygame.K_RIGHT] and self.x < SZEROKOSC - self.szerokosc//2:
            self.x += self.predkosc
        if klawisze[pygame.K_UP] and self.y > 50:
            self.y -= self.predkosc
        if klawisze[pygame.K_DOWN] and self.y < WYSOKOSC - self.wysokosc - 20:
            self.y += self.predkosc
            
        # Sterowanie klawiszami A i D
        if klawisze[pygame.K_a] and self.x > self.szerokosc//2:
            self.x -= self.predkosc
        if klawisze[pygame.K_d] and self.x < SZEROKOSC - self.szerokosc//2:
            self.x += self.predkosc

class Pocisk:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.predkosc = 10
        self.rozmiar = 5
        
    def ruch(self):
        self.y -= self.predkosc
        
    def rysuj(self, okno):
        pygame.draw.circle(okno, ZOLTY, (self.x, self.y), self.rozmiar)
        # Dodajemy błysk
        pygame.draw.circle(okno, BIALY, (self.x, self.y), 2)

class Eksplozja:
    def __init__(self, x, y, rozmiar=1):
        self.x = x
        self.y = y
        self.czas_zycia = 30  # Ile klatek będzie trwać eksplozja
        self.max_czas = 30
        self.rozmiar = rozmiar
        self.czasteczki = []
        
        # Tworzymy czasteczki eksplozji
        import random
        for i in range(int(15 * rozmiar)):
            czasteczka = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'vx': random.randint(-8, 8),  # prędkość x
                'vy': random.randint(-8, 8),  # prędkość y
                'kolor': random.choice([CZERWONY, ZOLTY, (255, 165, 0), BIALY])  # Pomarańczowy też
            }
            self.czasteczki.append(czasteczka)
    
    def aktualizuj(self):
        """Aktualizuje eksplozję - zwraca False gdy się kończy"""
        self.czas_zycia -= 1
        
        # Aktualizujemy pozycje cząsteczek
        for czasteczka in self.czasteczki:
            czasteczka['x'] += czasteczka['vx']
            czasteczka['y'] += czasteczka['vy']
            # Spowalniamy cząsteczki
            czasteczka['vx'] *= 0.95
            czasteczka['vy'] *= 0.95
        
        return self.czas_zycia > 0
    
    def rysuj(self, okno):
        """Rysuje eksplozję"""
        # Obliczamy jak bardzo eksplozja jest zaawansowana (0-1)
        postep = 1 - (self.czas_zycia / self.max_czas)
        
        # Rysujemy cząsteczki
        for czasteczka in self.czasteczki:
            # Rozmiar cząsteczki maleje z czasem
            rozmiar_czasteczki = max(1, int(8 * (1 - postep)))
            
            # Przezroczystość - cząsteczki znikają
            if rozmiar_czasteczki > 0:
                pygame.draw.circle(okno, czasteczka['kolor'], 
                                 (int(czasteczka['x']), int(czasteczka['y'])), 
                                 rozmiar_czasteczki)
        
        # Dodajemy błysk w centrum na początku
        if self.czas_zycia > 20:
            rozmiar_blysk = int(30 * self.rozmiar * (self.czas_zycia - 20) / 10)
            pygame.draw.circle(okno, BIALY, (int(self.x), int(self.y)), rozmiar_blysk)
            pygame.draw.circle(okno, ZOLTY, (int(self.x), int(self.y)), rozmiar_blysk // 2)

class Ufoludek:
    def __init__(self, typ="maly"):
        self.x = random.randint(30, SZEROKOSC - 30)
        self.y = random.randint(-100, -50)
        self.typ = typ
        
        # Różne typy ufoludków
        if typ == "maly":
            self.szerokosc = 40
            self.wysokosc = 25
            self.predkosc = random.randint(2, 4)
            self.kolor = random.choice([ZIELONY, FIOLETOWY])
            self.punkty = 10
            self.zycia = 1
        elif typ == "sredni":
            self.szerokosc = 60
            self.wysokosc = 35
            self.predkosc = random.randint(1, 3)
            self.kolor = CZERWONY
            self.punkty = 25
            self.zycia = 2
        elif typ == "duzy":
            self.szerokosc = 80
            self.wysokosc = 50
            self.predkosc = 1
            self.kolor = (255, 100, 0)  # Pomarańczowy
            self.punkty = 50
            self.zycia = 3
        elif typ == "szybki":
            self.szerokosc = 35
            self.wysokosc = 20
            self.predkosc = random.randint(6, 8)
            self.kolor = (255, 0, 255)  # Magenta
            self.punkty = 20
            self.zycia = 1
            
    def ruch(self):
        self.y += self.predkosc
        # Szybkie ufoludki mogą się trochę kołysać
        if self.typ == "szybki":
            self.x += random.randint(-2, 2)
            # Nie wychodzimy poza ekran
            if self.x < 30:
                self.x = 30
            elif self.x > SZEROKOSC - 30:
                self.x = SZEROKOSC - 30
        
    def trafiony(self):
        """Zmniejsza życia ufoludka, zwraca True jeśli zniszczony"""
        self.zycia -= 1
        return self.zycia <= 0
        
    def rysuj(self, okno):
        # Główna część UFO (owalna)
        pygame.draw.ellipse(okno, self.kolor, 
                          (self.x - self.szerokosc//2, self.y - self.wysokosc//2, 
                           self.szerokosc, self.wysokosc))
        
        # Kopuła (mniejsza elipsa na górze)
        rozmiar_kopuly = min(30, self.szerokosc//2)
        pygame.draw.ellipse(okno, SREBRNY, 
                          (self.x - rozmiar_kopuly//2, self.y - self.wysokosc//2 - 8, 
                           rozmiar_kopuly, 16))
        
        # Światełka (więcej dla większych UFO)
        liczba_swiatel = max(3, self.szerokosc // 15)
        for i in range(liczba_swiatel):
            kolor_swiatla = random.choice([ZOLTY, BIALY, NIEBIESKI])
            pos_x = self.x - (liczba_swiatel * 7) // 2 + i * 14
            pygame.draw.circle(okno, kolor_swiatla, (pos_x, self.y), 3)
            
        # Pokazujemy życia dla trudniejszych przeciwników
        if self.zycia > 1:
            for i in range(self.zycia):
                pygame.draw.circle(okno, CZERWONY, 
                                 (self.x - 10 + i * 10, self.y - self.wysokosc//2 - 15), 3)

def rysuj_gwiazdy(okno, gwiazdy):
    """Rysuje twinkling gwiazdy w tle"""
    for gwiazda in gwiazdy:
        jasnosc = random.randint(100, 255)
        kolor = (jasnosc, jasnosc, jasnosc)
        pygame.draw.circle(okno, kolor, gwiazda, 1)

# System sklepu i statków
STATKI_SKLEP = {
    "podstawowy": {"nazwa": "Podstawowy", "cena": 0, "opis": "Darmowy statek startowy"},
    "szybki": {"nazwa": "Szybki", "cena": 100, "opis": "Szybszy ruch, złoty kolor"},
    "podwojny": {"nazwa": "Podwójny", "cena": 250, "opis": "Strzela dwoma pociskami!"},
    "pancerny": {"nazwa": "Pancerny", "cena": 500, "opis": "Wolniejszy ale mocniejszy"},
    "stealth": {"nazwa": "Stealth", "cena": 350, "opis": "Niewidzialny, bardzo szybki"},
    "rakietowy": {"nazwa": "Rakietowy", "cena": 600, "opis": "Podwójne rakiety, średni"},
    "plazma": {"nazwa": "Plazma", "cena": 450, "opis": "Energetyczny, szybki"},
    "quantum": {"nazwa": "Quantum", "cena": 800, "opis": "Zaawansowany, podwójne strzały"},
    "alien": {"nazwa": "Alien", "cena": 1000, "opis": "Obcy tech, duży i mocny"},
    "crystal": {"nazwa": "Crystal", "cena": 750, "opis": "Najszybszy ze wszystkich!"}
}


def wczytaj_dane_gracza():
    """Wczytuje dane gracza z pliku"""
    try:
        with open("gracz_dane.txt", "r") as f:
            linie = f.readlines()
            calkowite_punkty = int(linie[0].strip())
            posiadane_statki = linie[1].strip().split(",") if len(linie) > 1 else ["podstawowy"]
            return calkowite_punkty, posiadane_statki
    except:
        return 0, ["podstawowy"]  # Domyślne wartości

def zapisz_dane_gracza(calkowite_punkty, posiadane_statki):
    """Zapisuje dane gracza do pliku"""
    try:
        with open("gracz_dane.txt", "w") as f:
            f.write(f"{calkowite_punkty}\n")
            f.write(",".join(posiadane_statki))
    except:
        pass

def resetuj_gre(typ_statku="podstawowy"):
    """Resetuje grę do stanu początkowego z wybranym statkiem"""
    statek = Statek(typ_statku)
    pociski = []
    ufoludki = []
    eksplozje = []
    punkty = 0
    zycia_statku = 3
    game_over = False
    return statek, pociski, ufoludki, eksplozje, punkty, zycia_statku, game_over

def ekran_startowy():
    """Wyświetla ekran startowy ze sklepem"""
    # Wczytujemy dane gracza
    calkowite_punkty, posiadane_statki = wczytaj_dane_gracza()
    wybrany_statek = "podstawowy"
    
    # Tworzymy gwiazdy w tle
    gwiazdy = [(random.randint(0, SZEROKOSC), random.randint(0, WYSOKOSC)) for _ in range(100)]
    
    # Czcionki
    czcionka_duza = pygame.font.Font(None, 72)
    czcionka_srednia = pygame.font.Font(None, 48)
    czcionka_mala = pygame.font.Font(None, 32)
    czcionka_bardzo_mala = pygame.font.Font(None, 24)
    
    w_sklepie = False
    
    while True:
        for wydarzenie in pygame.event.get():
            if wydarzenie.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif wydarzenie.type == pygame.MOUSEBUTTONDOWN:
                # Obsługa klików myszy
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if w_sklepie:
                    # Sprawdzamy czy kliknięto przycisk resetowania konta
                    if (SZEROKOSC//2 - 100 <= mouse_x <= SZEROKOSC//2 + 100 and 
                        WYSOKOSC - 100 <= mouse_y <= WYSOKOSC - 60):
                        # Resetujemy konto
                        calkowite_punkty = 0
                        posiadane_statki = ["podstawowy"]
                        zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                        print("🗑️ KONTO ZRESETOWANE! Wszystkie statki i punkty usunięte.")
                
            elif wydarzenie.type == pygame.KEYDOWN:
                if not w_sklepie:
                    if wydarzenie.key == pygame.K_s:
                        return wybrany_statek  # Start gry
                    elif wydarzenie.key == pygame.K_k:
                        w_sklepie = True  # Wejdź do sklepu
                    elif wydarzenie.key == pygame.K_1:
                        wybrany_statek = "podstawowy"
                    elif wydarzenie.key == pygame.K_2 and "szybki" in posiadane_statki:
                        wybrany_statek = "szybki"
                    elif wydarzenie.key == pygame.K_3 and "podwojny" in posiadane_statki:
                        wybrany_statek = "podwojny"
                    elif wydarzenie.key == pygame.K_4 and "pancerny" in posiadane_statki:
                        wybrany_statek = "pancerny"
                    elif wydarzenie.key == pygame.K_5 and "stealth" in posiadane_statki:
                        wybrany_statek = "stealth"
                    elif wydarzenie.key == pygame.K_6 and "rakietowy" in posiadane_statki:
                        wybrany_statek = "rakietowy"
                    elif wydarzenie.key == pygame.K_7 and "plazma" in posiadane_statki:
                        wybrany_statek = "plazma"
                    elif wydarzenie.key == pygame.K_8 and "quantum" in posiadane_statki:
                        wybrany_statek = "quantum"
                    elif wydarzenie.key == pygame.K_9 and "alien" in posiadane_statki:
                        wybrany_statek = "alien"
                    elif wydarzenie.key == pygame.K_0 and "crystal" in posiadane_statki:
                        wybrany_statek = "crystal"
                else:
                    # W sklepie
                    if wydarzenie.key == pygame.K_ESCAPE:
                        w_sklepie = False  # Wyjście ze sklepu
                    elif wydarzenie.key == pygame.K_1:
                        # Kup szybki statek
                        if "szybki" not in posiadane_statki and calkowite_punkty >= 100:
                            posiadane_statki.append("szybki")
                            calkowite_punkty -= 100
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś szybki statek!")
                    elif wydarzenie.key == pygame.K_2:
                        # Kup podwójny statek
                        if "podwojny" not in posiadane_statki and calkowite_punkty >= 250:
                            posiadane_statki.append("podwojny")
                            calkowite_punkty -= 250
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś podwójny statek!")
                    elif wydarzenie.key == pygame.K_3:
                        # Kup pancerny statek
                        if "pancerny" not in posiadane_statki and calkowite_punkty >= 500:
                            posiadane_statki.append("pancerny")
                            calkowite_punkty -= 500
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś pancerny statek!")
                    elif wydarzenie.key == pygame.K_4:
                        # Kup stealth statek
                        if "stealth" not in posiadane_statki and calkowite_punkty >= 350:
                            posiadane_statki.append("stealth")
                            calkowite_punkty -= 350
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś stealth statek!")
                    elif wydarzenie.key == pygame.K_5:
                        # Kup rakietowy statek
                        if "rakietowy" not in posiadane_statki and calkowite_punkty >= 600:
                            posiadane_statki.append("rakietowy")
                            calkowite_punkty -= 600
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś rakietowy statek!")
                    elif wydarzenie.key == pygame.K_6:
                        # Kup plazma statek
                        if "plazma" not in posiadane_statki and calkowite_punkty >= 450:
                            posiadane_statki.append("plazma")
                            calkowite_punkty -= 450
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś plazma statek!")
                    elif wydarzenie.key == pygame.K_7:
                        # Kup quantum statek
                        if "quantum" not in posiadane_statki and calkowite_punkty >= 800:
                            posiadane_statki.append("quantum")
                            calkowite_punkty -= 800
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś quantum statek!")
                    elif wydarzenie.key == pygame.K_8:
                        # Kup alien statek
                        if "alien" not in posiadane_statki and calkowite_punkty >= 1000:
                            posiadane_statki.append("alien")
                            calkowite_punkty -= 1000
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś alien statek!")
                    elif wydarzenie.key == pygame.K_9:
                        # Kup crystal statek
                        if "crystal" not in posiadane_statki and calkowite_punkty >= 750:
                            posiadane_statki.append("crystal")
                            calkowite_punkty -= 750
                            zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                            print("🎉 Kupiłeś crystal statek!")
        
        # Rysowanie
        okno.fill(CZARNY)
        
        # Rysujemy gwiazdy
        rysuj_gwiazdy(okno, gwiazdy)
        
        if not w_sklepie:
            # Ekran główny
            tytul = czcionka_duza.render("🚀 STATEK KOSMICZNY 🛸", True, ZOLTY)
            rect_tytul = tytul.get_rect(center=(SZEROKOSC//2, 100))
            okno.blit(tytul, rect_tytul)
            
            # Punkty gracza
            tekst_punkty = czcionka_srednia.render(f"💰 Twoje punkty: {calkowite_punkty}", True, ZIELONY)
            rect_punkty = tekst_punkty.get_rect(center=(SZEROKOSC//2, 160))
            okno.blit(tekst_punkty, rect_punkty)
            
            # Wybór statku
            tekst_wybor = czcionka_mala.render(f"🚀 Wybrany statek: {STATKI_SKLEP[wybrany_statek]['nazwa']}", True, BIALY)
            rect_wybor = tekst_wybor.get_rect(center=(SZEROKOSC//2, 220))
            okno.blit(tekst_wybor, rect_wybor)
            
            # Podgląd wybranego statku
            statek_podglad = Statek(wybrany_statek)
            statek_podglad.x = SZEROKOSC // 2
            statek_podglad.y = 280
            statek_podglad.rysuj(okno)
            
            # Menu
            y_start = 350
            opcje = [
                "🎮 S - START GRY!",
                "🛍 K - SKLEP STATKÓW",
                "",
                "Wybierz statek:"
            ]
            
            for i, opcja in enumerate(opcje):
                kolor = ZIELONY if "START" in opcja else ZOLTY if "SKLEP" in opcja else BIALY
                tekst = czcionka_mala.render(opcja, True, kolor)
                rect = tekst.get_rect(center=(SZEROKOSC//2, y_start + i * 35))
                okno.blit(tekst, rect)
            
            # Lista statków - w dwóch kolumnach
            y_statki = y_start + 140
            statki_lista = list(STATKI_SKLEP.items())
            
            for i, (typ, info) in enumerate(statki_lista):
                # Numeracja dla wyboru
                if i == 0: numer_klawisz = "1"
                elif i == 1: numer_klawisz = "2" 
                elif i == 2: numer_klawisz = "3"
                elif i == 3: numer_klawisz = "4"
                elif i == 4: numer_klawisz = "5"
                elif i == 5: numer_klawisz = "6"
                elif i == 6: numer_klawisz = "7"
                elif i == 7: numer_klawisz = "8"
                elif i == 8: numer_klawisz = "9"
                elif i == 9: numer_klawisz = "0"
                else: numer_klawisz = str(i)
                
                # Pozycja w dwóch kolumnach
                kolumna = i % 2
                rzad = i // 2
                x_pos = 50 + kolumna * 350
                y_pos = y_statki + rzad * 25
                
                if typ in posiadane_statki:
                    kolor = ZIELONY if typ == wybrany_statek else BIALY
                    symbol = "✓" if typ == wybrany_statek else "○"
                    tekst = f"{symbol} {numer_klawisz}. {info['nazwa']}"
                else:
                    kolor = CZERWONY
                    tekst = f"X {numer_klawisz}. {info['nazwa']} - {info['cena']}p"
                
                tekst_statek = czcionka_bardzo_mala.render(tekst, True, kolor)
                okno.blit(tekst_statek, (x_pos, y_pos))
        
        else:
            # Ekran sklepu
            tytul_sklep = czcionka_duza.render("🛑 SKLEP STATKÓW 🚀", True, ZOLTY)
            rect_tytul_sklep = tytul_sklep.get_rect(center=(SZEROKOSC//2, 80))
            okno.blit(tytul_sklep, rect_tytul_sklep)
            
            # Punkty
            tekst_punkty_sklep = czcionka_mala.render(f"💰 Twoje punkty: {calkowite_punkty}", True, ZIELONY)
            rect_punkty_sklep = tekst_punkty_sklep.get_rect(center=(SZEROKOSC//2, 130))
            okno.blit(tekst_punkty_sklep, rect_punkty_sklep)
            
            # Oferta sklepu - wszystkie statki oprócz podstawowego
            y_oferta = 150
            statki_do_kupienia = [
                ("szybki", 1), ("podwojny", 2), ("pancerny", 3), ("stealth", 4), 
                ("rakietowy", 5), ("plazma", 6), ("quantum", 7), ("alien", 8), ("crystal", 9)
            ]
            
            # Rysujemy w dwóch kolumnach
            for i, (typ, numer) in enumerate(statki_do_kupienia):
                info = STATKI_SKLEP[typ]
                
                # Pozycja - dwie kolumny
                kolumna = i % 2
                rzad = i // 2
                x_pos = 50 + kolumna * 350
                y_pos = y_oferta + rzad * 70
                
                # Ramka
                if typ in posiadane_statki:
                    kolor_ramki = ZIELONY
                    status = "POSIADASZ"
                elif calkowite_punkty >= info['cena']:
                    kolor_ramki = ZOLTY
                    status = f"Naciśnij {numer} - KUP!"
                else:
                    kolor_ramki = CZERWONY
                    status = "Za mało punktów"
                
                pygame.draw.rect(okno, kolor_ramki, (x_pos, y_pos - 5, 330, 60), 2)
                
                # Podgląd statku (mniejszy)
                statek_sklep = Statek(typ)
                statek_sklep.x = x_pos + 40
                statek_sklep.y = y_pos + 20
                # Zmniejszamy statek dla podglądu
                original_w, original_h = statek_sklep.szerokosc, statek_sklep.wysokosc
                statek_sklep.szerokosc = int(original_w * 0.6)
                statek_sklep.wysokosc = int(original_h * 0.6)
                statek_sklep.rysuj(okno)
                
                # Informacje
                tekst_nazwa = czcionka_bardzo_mala.render(f"{numer}. {info['nazwa']} - {info['cena']}p", True, BIALY)
                okno.blit(tekst_nazwa, (x_pos + 80, y_pos + 5))
                
                tekst_opis = pygame.font.Font(None, 18).render(info['opis'], True, BIALY)
                okno.blit(tekst_opis, (x_pos + 80, y_pos + 25))
                
                tekst_status = pygame.font.Font(None, 18).render(status, True, kolor_ramki)
                okno.blit(tekst_status, (x_pos + 80, y_pos + 40))
            
            # Przycisk resetowania konta
            pygame.draw.rect(okno, CZERWONY, (SZEROKOSC//2 - 100, WYSOKOSC - 100, 200, 40), 2)
            tekst_reset = czcionka_mala.render("🗑️ RESETUJ KONTO", True, CZERWONY)
            rect_reset = tekst_reset.get_rect(center=(SZEROKOSC//2, WYSOKOSC - 80))
            okno.blit(tekst_reset, rect_reset)
            
            tekst_reset_info = czcionka_bardzo_mala.render("Kliknij aby usunąć wszystkie statki i punkty", True, BIALY)
            rect_reset_info = tekst_reset_info.get_rect(center=(SZEROKOSC//2, WYSOKOSC - 55))
            okno.blit(tekst_reset_info, rect_reset_info)
            
            # Instrukcje
            tekst_wyjscie = czcionka_mala.render("🚪 ESC - Powrót do menu", True, CZERWONY)
            rect_wyjscie = tekst_wyjscie.get_rect(center=(SZEROKOSC//2, WYSOKOSC - 25))
            okno.blit(tekst_wyjscie, rect_wyjscie)
        
        pygame.display.flip()
        zegar.tick(60)

def main():
    # Pokazujemy ekran startowy i dostajemy wybrany statek
    wybrany_statek = ekran_startowy()
    
    # Tworzenie obiektów gry z wybranym statkiem
    statek, pociski, ufoludki, eksplozje, punkty, zycia_statku, game_over = resetuj_gre(wybrany_statek)
    
    # Tworzymy gwiazdy w tle
    gwiazdy = [(random.randint(0, SZEROKOSC), random.randint(0, WYSOKOSC)) for _ in range(100)]
    
    # Czcionka do wyświetlania punktów
    czcionka = pygame.font.Font(None, 36)
    
    # Główna pętla gry
    dziala = True
    while dziala:
        # Obsługa wydarzeń
        for wydarzenie in pygame.event.get():
            if wydarzenie.type == pygame.QUIT:
                dziala = False
            elif wydarzenie.type == pygame.KEYDOWN:
                if wydarzenie.key == pygame.K_SPACE and not game_over:
                    # Strzelamy pociskiem (lub pociskami)!
                    if statek.podwojne_strzaly:
                        # Podwójne strzaly
                        pocisk1 = Pocisk(statek.x - 15, statek.y)
                        pocisk2 = Pocisk(statek.x + 15, statek.y)
                        pociski.append(pocisk1)
                        pociski.append(pocisk2)
                    else:
                        # Pojedynczy pocisk
                        nowy_pocisk = Pocisk(statek.x, statek.y)
                        pociski.append(nowy_pocisk)
                    
                    # Odtwarzamy dźwięk strzału
                    if dzwiek_strzal:
                        try:
                            dzwiek_strzal.play()
                            if statek.podwojne_strzaly:
                                print("🔫🔫 Podwójny pew pew!")
                            else:
                                print("🔫 Pew pew!")
                        except:
                            print("🔫 Pew pew! (bez dźwięku)")
                    else:
                        print("🔫 Pew pew! (brak dźwięku)")
                elif wydarzenie.key == pygame.K_ESCAPE and game_over:
                    # Powrót do menu głównego
                    main()  # Uruchamiamy ponownie całą grę z menu
                    return
                elif wydarzenie.key == pygame.K_r and game_over:
                    # Restart gry z tym samym statkiem!
                    statek, pociski, ufoludki, eksplozje, punkty, zycia_statku, game_over = resetuj_gre(statek.typ)
                    print(f"🎆 Nowa gra rozpoczęta ze statkiem {statek.typ}! Powodzenia!")
        
        # Pobieramy stan klawiszy
        klawisze = pygame.key.get_pressed()
        
        # Ruch statku (tylko jeśli gra się nie skończyła)
        if not game_over:
            statek.ruch(klawisze)
        
        # Ruch pocisków
        for pocisk in pociski[:]:  # Kopiujemy listę żeby bezpiecznie usuwać
            pocisk.ruch()
            if pocisk.y < 0:  # Pocisk wyleciał poza ekran
                pociski.remove(pocisk)
        
        # Dodawanie nowych ufoludków (różne typy)
        if random.randint(1, 40) == 1:  # Co jakiś czas pojawia się nowy ufoludek
            # Losujemy typ ufoludka
            szansa = random.randint(1, 100)
            if szansa <= 50:  # 50% - mały
                typ = "maly"
            elif szansa <= 75:  # 25% - szybki
                typ = "szybki"
            elif szansa <= 90:  # 15% - średni
                typ = "sredni"
            else:  # 10% - duży
                typ = "duzy"
                
            nowy_ufoludek = Ufoludek(typ)
            ufoludki.append(nowy_ufoludek)
        
        # Ruch ufoludków
        for ufoludek in ufoludki[:]:
            ufoludek.ruch()
            if ufoludek.y > WYSOKOSC:  # Ufoludek wyleciał poza ekran
                ufoludki.remove(ufoludek)
        
        # Aktualizujemy eksplozje
        for eksplozja in eksplozje[:]:
            if not eksplozja.aktualizuj():  # Jeśli eksplozja się skończyła
                eksplozje.remove(eksplozja)
        
        # Sprawdzanie kolizji pocisk-ufoludek
        for pocisk in pociski[:]:
            for ufoludek in ufoludki[:]:
                # Prosta kolizja - sprawdzamy odległość
                odleglosc_x = abs(pocisk.x - ufoludek.x)
                odleglosc_y = abs(pocisk.y - ufoludek.y)
                
                if odleglosc_x < ufoludek.szerokosc//2 + 10 and odleglosc_y < ufoludek.wysokosc//2 + 10:
                    # Trafienie! Usuwamy pocisk
                    pociski.remove(pocisk)
                    
                    # Sprawdzamy czy ufoludek został zniszczony
                    if ufoludek.trafiony():
                        # Tworzymy eksplozję w miejscu ufoludka!
                        rozmiar_eksplozji = 1
                        if ufoludek.typ == "duzy":
                            rozmiar_eksplozji = 2
                        elif ufoludek.typ == "sredni":
                            rozmiar_eksplozji = 2  # Zmieniam na int
                        
                        nowa_eksplozja = Eksplozja(ufoludek.x, ufoludek.y, rozmiar_eksplozji)
                        eksplozje.append(nowa_eksplozja)
                        
                        ufoludki.remove(ufoludek)
                        punkty += ufoludek.punkty
                        # Odtwarzamy dźwięk eksplozji
                        if dzwiek_trafienie:
                            try:
                                dzwiek_trafienie.play()
                                print(f"🎯 BOOM! 💥 (z eksplozją!) Zniszczono {ufoludek.typ} UFO! +{ufoludek.punkty} punktów! Razem: {punkty}")
                            except:
                                print(f"🎯 BOOM! 💥 (eksplozja bez dźwięku) Zniszczono {ufoludek.typ} UFO! +{ufoludek.punkty} punktów! Razem: {punkty}")
                        else:
                            print(f"🎯 BOOM! 💥 (eksplozja bez dźwięku) Zniszczono {ufoludek.typ} UFO! +{ufoludek.punkty} punktów! Razem: {punkty}")
                    else:
                        # Dźwięk trafienia (cichszy)
                        if dzwiek_trafienie:
                            try:
                                dzwiek_trafienie.set_volume(0.3)
                                dzwiek_trafienie.play()
                                print(f"💥 Trafienie! (z dźwiękiem) {ufoludek.typ} UFO ma {ufoludek.zycia} żyć!")
                            except:
                                print(f"💥 Trafienie! (bez dźwięku) {ufoludek.typ} UFO ma {ufoludek.zycia} żyć!")
                        else:
                            print(f"💥 Trafienie! (brak dźwięku) {ufoludek.typ} UFO ma {ufoludek.zycia} żyć!")
                    break
                    
        # Sprawdzanie kolizji ufoludek-statek
        for ufoludek in ufoludki[:]:
            odleglosc_x = abs(statek.x - ufoludek.x)
            odleglosc_y = abs(statek.y - ufoludek.y)
            
            if odleglosc_x < ufoludek.szerokosc//2 + 25 and odleglosc_y < ufoludek.wysokosc//2 + 20:
                # Kolizja ze statkiem! Tworzymy eksplozję!
                nowa_eksplozja = Eksplozja(ufoludek.x, ufoludek.y, 2)  # Duża eksplozja przy kolizji
                eksplozje.append(nowa_eksplozja)
                
                ufoludki.remove(ufoludek)
                zycia_statku -= 1
                # Odtwarzamy dźwięk kolizji
                if dzwiek_kolizja:
                    try:
                        dzwiek_kolizja.play()
                        print(f"💥 CRASH! 🔥 (z eksplozją!) Kolizja! Zostało Ci {zycia_statku} żyć!")
                    except:
                        print(f"💥 CRASH! 🔥 (eksplozja bez dźwięku) Kolizja! Zostało Ci {zycia_statku} żyć!")
                else:
                    print(f"💥 CRASH! 🔥 (eksplozja bez dźwięku) Kolizja! Zostało Ci {zycia_statku} żyć!")
                
                if zycia_statku <= 0:
                    # Zapisujemy punkty do całkowitych punktów gracza
                    calkowite_punkty, posiadane_statki = wczytaj_dane_gracza()
                    calkowite_punkty += punkty
                    zapisz_dane_gracza(calkowite_punkty, posiadane_statki)
                    
                    # Głośniejszy dźwięk końca gry
                    if dzwiek_kolizja:
                        try:
                            dzwiek_kolizja.set_volume(1.0)
                            dzwiek_kolizja.play()
                            print(f"🚀💥 KONIEC GRY! Zdobyłeś {punkty} punktów! Razem masz: {calkowite_punkty}")
                        except:
                            print(f"🚀💥 KONIEC GRY! Zdobyłeś {punkty} punktów!")
                    else:
                        print(f"🚀💥 KONIEC GRY! Zdobyłeś {punkty} punktów!")
                    
                    # Krótka pauza i powrót do menu głównego
                    pygame.time.wait(2000)  # Czekamy 2 sekundy
                    main()  # Wracamy do menu głównego
                    return
                break
        
        # Rysowanie wszystkiego
        okno.fill(CZARNY)  # Czarne tło kosmosu
        
        # Rysujemy gwiazdy
        rysuj_gwiazdy(okno, gwiazdy)
        
        # Rysujemy statek
        statek.rysuj(okno)
        
        # Rysujemy pociski
        for pocisk in pociski:
            pocisk.rysuj(okno)
        
        # Rysujemy ufoludki
        for ufoludek in ufoludki:
            ufoludek.rysuj(okno)
        
        # Rysujemy eksplozje (na wierzchu!)
        for eksplozja in eksplozje:
            eksplozja.rysuj(okno)
        
        # Wyświetlamy punkty i życia
        tekst_punkty = czcionka.render(f"Punkty: {punkty}", True, BIALY)
        okno.blit(tekst_punkty, (10, 10))
        
        # Wyświetlamy życia jako serduszka
        tekst_zycia = czcionka.render(f"Życia: ", True, BIALY)
        okno.blit(tekst_zycia, (10, 50))
        for i in range(zycia_statku):
            pygame.draw.circle(okno, CZERWONY, (100 + i * 30, 65), 8)
            pygame.draw.circle(okno, CZERWONY, (110 + i * 30, 65), 8)
            pygame.draw.polygon(okno, CZERWONY, [(105 + i * 30, 75), (95 + i * 30, 60), (115 + i * 30, 60)])
        
        # Instrukcje sterowania i informacje o UFO
        czcionka_mala = pygame.font.Font(None, 24)
        instrukcje = [
            "🚀 Strzałki lub A/D - ruch statku",
            "🔫 SPACJA - strzelaj! (Pew pew!)",
            "🛸 UFO: Mały(10p), Szybki(20p), Średni(25p), Duży(50p)",
            "💥 Eksplozje! Większe UFO = większe wybuchy!"
        ]
        for i, instrukcja in enumerate(instrukcje):
            tekst = czcionka_mala.render(instrukcja, True, BIALY)
            okno.blit(tekst, (10, WYSOKOSC - 80 + i * 25))
            
        # Ekran końcowy
        if game_over:
            # Półprzezroczyste tło
            overlay = pygame.Surface((SZEROKOSC, WYSOKOSC))
            overlay.set_alpha(128)
            overlay.fill(CZARNY)
            okno.blit(overlay, (0, 0))
            
            # Tekst końcowy
            czcionka_duza = pygame.font.Font(None, 72)
            tekst_koniec = czcionka_duza.render("KONIEC GRY!", True, CZERWONY)
            rect_koniec = tekst_koniec.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 50))
            okno.blit(tekst_koniec, rect_koniec)
            
            tekst_wynik = czcionka.render(f"Twój wynik: {punkty} punktów!", True, BIALY)
            rect_wynik = tekst_wynik.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2))
            okno.blit(tekst_wynik, rect_wynik)
            
            # Informacja o zdobytych punktach
            calkowite_punkty, _ = wczytaj_dane_gracza()
            tekst_calkowite = czcionka_mala.render(f"💰 Całkowite punkty: {calkowite_punkty}", True, ZOLTY)
            rect_calkowite = tekst_calkowite.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 30))
            okno.blit(tekst_calkowite, rect_calkowite)
            
            # Przyciski restart i wyjście
            tekst_restart = czcionka_mala.render("🎆 Naciśnij R - Zagraj ponownie!", True, ZIELONY)
            rect_restart = tekst_restart.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 60))
            okno.blit(tekst_restart, rect_restart)
            
            tekst_exit = czcionka_mala.render("🚪 Naciśnij ESC - Powrót do menu", True, CZERWONY)
            rect_exit = tekst_exit.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 90))
            okno.blit(tekst_exit, rect_exit)
        
        # Odświeżamy ekran
        pygame.display.flip()
        zegar.tick(60)  # 60 klatek na sekundę
    
    # Kończymy grę
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("🚀 Witaj w grze Statek Kosmiczny! 🛸")
    print("Użyj strzałek do poruszania się i SPACJI do strzelania!")
    print("Zestrzel jak najwięcej ufoludków!")
    main()
