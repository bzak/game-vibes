import pygame
import math
import random
import os

# Inicjalizacja pygame
pygame.init()

# Ładowanie grafik
def zaladuj_grafike(nazwa_pliku):
    try:
        sciezka = os.path.join("obrazki", nazwa_pliku)
        return pygame.image.load(sciezka)
    except:
        print(f"Nie można załadować grafiki: {nazwa_pliku}")
        return None

# Ładowanie wszystkich grafik
grafika_bohater = zaladuj_grafike("bohater-ludzik-bez-tla.png")
grafika_zombiak_slaby = zaladuj_grafike("zombiak-slaby-bez-tla.png")
grafika_zombiak_sredni = zaladuj_grafike("zombiak-sredni-bez-tla.png")
grafika_zombiak_mocny = zaladuj_grafike("zombiak-mocny-bez-tla.png")
grafika_miecz = zaladuj_grafike("miecz-bez-tla.png")
grafika_pistolet = zaladuj_grafike("pistolet-bez-tla.png")
grafika_apteczka = zaladuj_grafike("apteczka-bez-tla.png")

# Ustawienia ekranu
SZEROKOSC = 1000
WYSOKOSC = 700
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Ucieczka z Budynku Zombiaków")

# Ustawienia mapy
MAPA_SZEROKOSC = SZEROKOSC * 2  # 2x większa mapa
MAPA_WYSOKOSC = WYSOKOSC * 2
ROZMIAR_KAFELKA = 40

# Kolory
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
NIEBIESKI = (0, 0, 255)
SZARY = (128, 128, 128)
CIEMNY_SZARY = (64, 64, 64)
BRAZOWY = (139, 69, 19)
ZOLTY = (255, 255, 0)

# Ustawienia gry
FPS = 60
zegar = pygame.time.Clock()

class Gracz:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerokosc = 40
        self.wysokosc = 40
        self.predkosc = 5
        self.zycia = 3
        self.max_zycia = 3
        self.bron = "pistolet"  # "pistolet" lub "miecz"
        self.ostatni_strzal = 0
        self.czas_miedzy_strzalami = 300  # milisekundy
        self.kierunek_x = 0
        self.kierunek_y = 0
        
    def ruch(self, klawisze):
        self.kierunek_x = 0
        self.kierunek_y = 0
        
        if klawisze[pygame.K_LEFT] or klawisze[pygame.K_a]:
            self.kierunek_x = -1
        if klawisze[pygame.K_RIGHT] or klawisze[pygame.K_d]:
            self.kierunek_x = 1
        if klawisze[pygame.K_UP] or klawisze[pygame.K_w]:
            self.kierunek_y = -1
        if klawisze[pygame.K_DOWN] or klawisze[pygame.K_s]:
            self.kierunek_y = 1
            
        # Normalizacja ruchu po przekątnej
        if self.kierunek_x != 0 and self.kierunek_y != 0:
            self.kierunek_x *= 0.7
            self.kierunek_y *= 0.7
            
        self.x += self.kierunek_x * self.predkosc
        self.y += self.kierunek_y * self.predkosc
        
        # Sprawdź kolizje ze ścianami
        nowa_pozycja = pygame.Rect(self.x, self.y, self.szerokosc, self.wysokosc)
        
        # Kolizje ze ścianami będą sprawdzane w klasie Gra
        
        # Ograniczenia mapy (nie ekranu!)
        self.x = max(0, min(MAPA_SZEROKOSC - self.szerokosc, self.x))
        self.y = max(0, min(MAPA_WYSOKOSC - self.wysokosc, self.y))
    
    def strzal(self, cel_x, cel_y):
        czas = pygame.time.get_ticks()
        if czas - self.ostatni_strzal > self.czas_miedzy_strzalami:
            self.ostatni_strzal = czas
            
            # Oblicz kierunek strzału
            dx = cel_x - (self.x + self.szerokosc // 2)
            dy = cel_y - (self.y + self.wysokosc // 2)
            odleglosc = math.sqrt(dx**2 + dy**2)
            
            if odleglosc > 0:
                dx /= odleglosc
                dy /= odleglosc
                return Pocisk(self.x + self.szerokosc // 2, self.y + self.wysokosc // 2, dx, dy)
        return None
    
    def atak_mieczem(self, zombiaki):
        # Atak mieczem - zasięg bliski
        for zombiak in zombiaki[:]:
            dx = zombiak.x - self.x
            dy = zombiak.y - self.y
            odleglosc = math.sqrt(dx**2 + dy**2)
            
            if odleglosc < 60:  # Zasięg miecza
                zombiak.otrzymaj_obrazenia(1)
                if zombiak.zycia <= 0:
                    zombiaki.remove(zombiak)
    
    def rysuj(self, ekran):
        # Rysuj gracza z grafiką lub prostokątem jako fallback
        if grafika_bohater:
            grafika_skalowana = pygame.transform.scale(grafika_bohater, (self.szerokosc, self.wysokosc))
            ekran.blit(grafika_skalowana, (self.x, self.y))
        else:
            pygame.draw.rect(ekran, NIEBIESKI, (self.x, self.y, self.szerokosc, self.wysokosc))
        
        # Rysuj broń w ręku
        srodek_x = self.x + self.szerokosc // 2
        srodek_y = self.y + self.wysokosc // 2
        
        if self.bron == "miecz" and grafika_miecz:
            bron_grafika = pygame.transform.scale(grafika_miecz, (20, 20))
            ekran.blit(bron_grafika, (srodek_x + 15, srodek_y - 10))
        elif self.bron == "pistolet" and grafika_pistolet:
            bron_grafika = pygame.transform.scale(grafika_pistolet, (20, 20))
            ekran.blit(bron_grafika, (srodek_x + 15, srodek_y - 10))
        
        # Rysuj kierunek patrzenia
        if self.kierunek_x != 0 or self.kierunek_y != 0:
            koniec_x = srodek_x + self.kierunek_x * 30
            koniec_y = srodek_y + self.kierunek_y * 30
            pygame.draw.line(ekran, BIALY, (srodek_x, srodek_y), (koniec_x, koniec_y), 2)

class Zombiak:
    def __init__(self, x, y, typ=1):
        self.x = x
        self.y = y
        self.szerokosc = 35
        self.wysokosc = 35
        self.typ = typ  # 1, 2, lub 3 życia
        self.zycia = typ
        self.max_zycia = typ
        self.predkosc = max(1, 3 - typ * 0.5)  # Słabsze zombiaki są szybsze
        self.punkty = typ * 10
        
    def ruch_do_gracza(self, gracz, sciany):
        dx = gracz.x - self.x
        dy = gracz.y - self.y
        odleglosc = math.sqrt(dx**2 + dy**2)
        
        if odleglosc > 0:
            dx /= odleglosc
            dy /= odleglosc
            
            # Zapisz starą pozycję
            stary_x = self.x
            stary_y = self.y
            
            # Spróbuj się ruszyć
            nowy_x = self.x + dx * self.predkosc
            nowy_y = self.y + dy * self.predkosc
            
            # Sprawdź kolizje ze ścianami
            nowa_pozycja = pygame.Rect(nowy_x, nowy_y, self.szerokosc, self.wysokosc)
            kolizja = False
            
            for sciana in sciany:
                if nowa_pozycja.colliderect(sciana.rect):
                    kolizja = True
                    break
            
            # Jeśli nie ma kolizji, rusz się normalnie
            if not kolizja:
                self.x = nowy_x
                self.y = nowy_y
            else:
                # Spróbuj ruch tylko w osi X
                nowa_pozycja_x = pygame.Rect(nowy_x, self.y, self.szerokosc, self.wysokosc)
                kolizja_x = False
                for sciana in sciany:
                    if nowa_pozycja_x.colliderect(sciana.rect):
                        kolizja_x = True
                        break
                
                if not kolizja_x:
                    self.x = nowy_x
                else:
                    # Spróbuj ruch tylko w osi Y
                    nowa_pozycja_y = pygame.Rect(self.x, nowy_y, self.szerokosc, self.wysokosc)
                    kolizja_y = False
                    for sciana in sciany:
                        if nowa_pozycja_y.colliderect(sciana.rect):
                            kolizja_y = True
                            break
                    
                    if not kolizja_y:
                        self.y = nowy_y
    
    def otrzymaj_obrazenia(self, obrazenia):
        self.zycia -= obrazenia
    
    def rysuj(self, ekran):
        # Rysuj zombiaka z odpowiednią grafiką
        grafika_zombiak = None
        if self.typ == 1 and grafika_zombiak_slaby:
            grafika_zombiak = grafika_zombiak_slaby
        elif self.typ == 2 and grafika_zombiak_sredni:
            grafika_zombiak = grafika_zombiak_sredni
        elif self.typ == 3 and grafika_zombiak_mocny:
            grafika_zombiak = grafika_zombiak_mocny
        
        if grafika_zombiak:
            grafika_skalowana = pygame.transform.scale(grafika_zombiak, (self.szerokosc, self.wysokosc))
            ekran.blit(grafika_skalowana, (self.x, self.y))
        else:
            # Fallback - kolorowe prostokąty
            if self.typ == 1:
                kolor = (100, 200, 100)  # Jasny zielony
            elif self.typ == 2:
                kolor = (150, 150, 50)   # Żółto-zielony
            else:
                kolor = (200, 100, 100)  # Czerwono-zielony
            pygame.draw.rect(ekran, kolor, (self.x, self.y, self.szerokosc, self.wysokosc))
        
        # Pasek życia
        szerokosc_paska = self.szerokosc
        wysokosc_paska = 5
        pygame.draw.rect(ekran, CZERWONY, (self.x, self.y - 10, szerokosc_paska, wysokosc_paska))
        
        procent_zycia = self.zycia / self.max_zycia
        pygame.draw.rect(ekran, ZIELONY, (self.x, self.y - 10, szerokosc_paska * procent_zycia, wysokosc_paska))

class Pocisk:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.predkosc = 10
        self.promien = 3
        
    def ruch(self):
        self.x += self.dx * self.predkosc
        self.y += self.dy * self.predkosc
        
    def czy_poza_ekranem(self):
        return (self.x < 0 or self.x > SZEROKOSC or 
                self.y < 0 or self.y > WYSOKOSC)
    
    def rysuj(self, ekran):
        pygame.draw.circle(ekran, ZOLTY, (int(self.x), int(self.y)), self.promien)

class Apteczka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerokosc = 25
        self.wysokosc = 25
        self.zebrana = False
        
    def sprawdz_kolizje(self, gracz):
        if not self.zebrana:
            if (gracz.x < self.x + self.szerokosc and
                gracz.x + gracz.szerokosc > self.x and
                gracz.y < self.y + self.wysokosc and
                gracz.y + gracz.wysokosc > self.y):
                self.zebrana = True
                gracz.zycia = min(gracz.max_zycia, gracz.zycia + 1)
                return True
        return False
    
    def rysuj(self, ekran, gracz):
        if not self.zebrana:
            if grafika_apteczka:
                grafika_skalowana = pygame.transform.scale(grafika_apteczka, (self.szerokosc, self.wysokosc))
                ekran.blit(grafika_skalowana, (self.x, self.y))
            else:
                # Fallback - rysuj prostokąt z krzyżem
                pygame.draw.rect(ekran, BIALY, (self.x, self.y, self.szerokosc, self.wysokosc))
                pygame.draw.rect(ekran, CZERWONY, (self.x + 8, self.y + 5, 9, 15))
                pygame.draw.rect(ekran, CZERWONY, (self.x + 5, self.y + 8, 15, 9))

class Sciana:
    def __init__(self, x, y, szerokosc, wysokosc):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
    
    def rysuj(self, ekran):
        pygame.draw.rect(ekran, BRAZOWY, self.rect)
        pygame.draw.rect(ekran, CZARNY, self.rect, 2)

class Drzwi:
    def __init__(self, x, y, szerokosc, wysokosc, cel_pietro=None):
        self.x = x
        self.y = y
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.cel_pietro = cel_pietro  # None dla drzwi między pokojami, numer dla schodów
    
    def rysuj(self, ekran):
        if self.cel_pietro:  # Schody
            pygame.draw.rect(ekran, (100, 100, 100), self.rect)
            pygame.draw.rect(ekran, BIALY, self.rect, 2)
        else:  # Zwykłe drzwi
            pygame.draw.rect(ekran, (139, 69, 19), self.rect)
            pygame.draw.rect(ekran, CZARNY, self.rect, 2)

class Kamera:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def aktualizuj(self, gracz):
        # Kamera podąża za graczem
        self.x = gracz.x - SZEROKOSC // 2
        self.y = gracz.y - WYSOKOSC // 2
        
        # Ograniczenia kamery do granic mapy
        self.x = max(0, min(MAPA_SZEROKOSC - SZEROKOSC, self.x))
        self.y = max(0, min(MAPA_WYSOKOSC - WYSOKOSC, self.y))

class Gra:
    def __init__(self):
        self.gracz = Gracz(200, 200)  # Start w większej mapie
        self.zombiaki = []
        self.pociski = []
        self.apteczki = []
        self.sciany = []
        self.drzwi = []
        self.kamera = Kamera()
        self.odkryte_obszary = set()  # Zbiór odkrytych kafelków (x, y)
        self.pietro = 5  # Zaczynamy od najwyższego piętra
        self.pokoj = 1
        self.punkty = 0
        self.font = pygame.font.Font(None, 36)
        self.maly_font = pygame.font.Font(None, 24)
        self.generuj_poziom()
        
    def generuj_poziom(self):
        self.zombiaki.clear()
        self.apteczki.clear()
        self.sciany.clear()
        self.drzwi.clear()
        
        # Ustaw gracza w bezpiecznej pozycji na początku każdego poziomu
        self.gracz.x = 100
        self.gracz.y = 100
        
        # Generuj ściany budynku (zewnętrzne granice większej mapy)
        self.sciany.append(Sciana(0, 0, MAPA_SZEROKOSC, 20))  # Góra
        self.sciany.append(Sciana(0, MAPA_WYSOKOSC-20, MAPA_SZEROKOSC, 20))  # Dół
        self.sciany.append(Sciana(0, 0, 20, MAPA_WYSOKOSC))  # Lewa
        self.sciany.append(Sciana(MAPA_SZEROKOSC-20, 0, 20, MAPA_WYSOKOSC))  # Prawa
        
        # Uproszczony labirynt z bardzo szerokimi przejściami
        # Tylko kilka głównych ścian z dużymi przerwami
        self.sciany.append(Sciana(100, 200, 150, 20))  # Górny korytarz - lewa część
        self.sciany.append(Sciana(350, 200, 100, 20))  # Górny korytarz - środek
        self.sciany.append(Sciana(550, 200, 150, 20))  # Górny korytarz - prawa część
        
        self.sciany.append(Sciana(100, 400, 80, 20))   # Środkowy korytarz - lewa część
        self.sciany.append(Sciana(280, 400, 80, 20))   # Środkowy korytarz - środek
        self.sciany.append(Sciana(460, 400, 100, 20))  # Środkowy korytarz - prawa część
        
        self.sciany.append(Sciana(200, 600, 150, 20))  # Dolny korytarz - lewa część
        self.sciany.append(Sciana(450, 600, 100, 20))  # Dolny korytarz - prawa część
        
        # Pionowe ściany z bardzo szerokimi przejściami (100+ pikseli)
        self.sciany.append(Sciana(200, 100, 20, 80))   # Lewy pionowy - góra
        self.sciany.append(Sciana(200, 320, 20, 60))   # Lewy pionowy - dół
        
        self.sciany.append(Sciana(400, 50, 20, 60))    # Środkowy pionowy - góra
        self.sciany.append(Sciana(400, 280, 20, 60))   # Środkowy pionowy - środek
        self.sciany.append(Sciana(400, 480, 20, 40))   # Środkowy pionowy - dół
        
        self.sciany.append(Sciana(600, 100, 20, 80))   # Prawy pionowy - góra
        self.sciany.append(Sciana(600, 320, 20, 60))   # Prawy pionowy - dół
        
        # Minimalne pokoje - tylko podstawowe ściany z ogromnymi wyjściami
        # Lewy górny pokój
        self.sciany.append(Sciana(50, 50, 80, 20))     # Górna ściana - skrócona
        self.sciany.append(Sciana(50, 50, 20, 60))     # Lewa ściana - skrócona
        
        # Prawy górny pokój  
        self.sciany.append(Sciana(500, 50, 80, 20))    # Górna ściana - skrócona
        self.sciany.append(Sciana(650, 50, 20, 60))    # Prawa ściana - skrócona
        
        # Środkowy pokój
        self.sciany.append(Sciana(280, 280, 60, 20))   # Mała ściana
        self.sciany.append(Sciana(280, 280, 20, 60))   # Mała ściana
        
        # Dolny pokój
        self.sciany.append(Sciana(150, 520, 80, 20))   # Dolna ściana - skrócona
        self.sciany.append(Sciana(150, 480, 20, 40))   # Lewa ściana - skrócona
        
        # Schody (w różnych miejscach na różnych piętrach)
        if self.pietro > 1:
            self.drzwi.append(Drzwi(MAPA_SZEROKOSC-80, MAPA_WYSOKOSC-80, 40, 40, self.pietro-1))
        
        # Liczba zombiaków zależy od piętra (im niżej, tym więcej)
        liczba_zombiakow = (6 - self.pietro) * 2 + random.randint(1, 3)
        
        for _ in range(liczba_zombiakow):
            # Spawni zombiaki w różnych obszarach (nie blisko gracza)
            pokoj_nr = random.randint(2, 6)  # Więcej obszarów do wyboru
            x, y = self.get_pozycja_w_pokoju(pokoj_nr)
            
            # Upewnij się, że zombiak nie spawni za blisko gracza (dodatkowa ochrona)
            while math.sqrt((x - 100)**2 + (y - 100)**2) < 150:
                pokoj_nr = random.randint(2, 6)
                x, y = self.get_pozycja_w_pokoju(pokoj_nr)
            
            # Typ zombiaka zależy od piętra
            if self.pietro >= 4:
                typ = random.choice([1, 1, 2])  # Głównie słabe
            elif self.pietro >= 2:
                typ = random.choice([1, 2, 2, 3])  # Mix
            else:
                typ = random.choice([2, 3, 3])  # Głównie mocne
            
            self.zombiaki.append(Zombiak(x, y, typ))
        
        # Generuj apteczki (1-2 na poziom)
        for _ in range(random.randint(1, 2)):
            pokoj_nr = random.randint(1, 6)
            x, y = self.get_pozycja_w_pokoju(pokoj_nr)
            self.apteczki.append(Apteczka(x, y))
        
        # Schody (w różnych miejscach na różnych piętrach)
        if self.pietro > 1:
            if self.pietro == 5:
                self.drzwi.append(Drzwi(MAPA_SZEROKOSC - 100, MAPA_WYSOKOSC - 100, 60, 60, self.pietro - 1))
            elif self.pietro == 4:
                self.drzwi.append(Drzwi(100, MAPA_WYSOKOSC - 100, 60, 60, self.pietro - 1))
            elif self.pietro == 3:
                self.drzwi.append(Drzwi(MAPA_SZEROKOSC//2, 50, 60, 60, self.pietro - 1))
            else:
                self.drzwi.append(Drzwi(MAPA_SZEROKOSC - 150, 200, 60, 60, self.pietro - 1))
    
    def get_pozycja_w_pokoju(self, pokoj_nr):
        # Zwraca losową pozycję w różnych obszarach większej mapy
        obszary = [
            (100, 300, 100, 180),    # Lewy górny obszar
            (500, 700, 100, 180),    # Prawy górny obszar  
            (300, 500, 300, 380),    # Środkowy obszar
            (150, 350, 450, 580),    # Lewy dolny obszar
            (450, 650, 450, 580),    # Prawy dolny obszar
            (750, 850, 350, 450),    # Mały pokój prawy
        ]
        
        if pokoj_nr <= len(obszary):
            x_min, x_max, y_min, y_max = obszary[pokoj_nr - 1]
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
        else:
            # Fallback - losowa pozycja na mapie
            x = random.randint(50, MAPA_SZEROKOSC - 50)
            y = random.randint(50, MAPA_WYSOKOSC - 50)
        
        return x, y
    
    def odkryj_obszar(self, gracz_x, gracz_y):
        # Odkryj obszar wokół gracza
        promien_odkrycia = 80
        for dx in range(-promien_odkrycia, promien_odkrycia + 1, ROZMIAR_KAFELKA):
            for dy in range(-promien_odkrycia, promien_odkrycia + 1, ROZMIAR_KAFELKA):
                x = gracz_x + dx
                y = gracz_y + dy
                if 0 <= x < MAPA_SZEROKOSC and 0 <= y < MAPA_WYSOKOSC:
                    kafelek_x = x // ROZMIAR_KAFELKA
                    kafelek_y = y // ROZMIAR_KAFELKA
                    self.odkryte_obszary.add((kafelek_x, kafelek_y))
    
    def sprawdz_kolizje_pociski(self):
        for pocisk in self.pociski[:]:
            for zombiak in self.zombiaki[:]:
                dx = pocisk.x - (zombiak.x + zombiak.szerokosc // 2)
                dy = pocisk.y - (zombiak.y + zombiak.wysokosc // 2)
                odleglosc = math.sqrt(dx**2 + dy**2)
                
                if odleglosc < zombiak.szerokosc // 2 + pocisk.promien:
                    zombiak.otrzymaj_obrazenia(1)
                    self.pociski.remove(pocisk)
                    
                    if zombiak.zycia <= 0:
                        self.punkty += zombiak.punkty
                        self.zombiaki.remove(zombiak)
                    break
    
    def sprawdz_kolizje_gracz_zombiaki(self):
        czas = pygame.time.get_ticks()
        for zombiak in self.zombiaki:
            if (self.gracz.x < zombiak.x + zombiak.szerokosc and
                self.gracz.x + self.gracz.szerokosc > zombiak.x and
                self.gracz.y < zombiak.y + zombiak.wysokosc and
                self.gracz.y + self.gracz.wysokosc > zombiak.y):
                
                # Gracz otrzymuje obrażenia tylko co sekundę
                if not hasattr(self.gracz, 'ostatni_atak') or czas - self.gracz.ostatni_atak > 1000:
                    self.gracz.zycia -= 1
                    self.gracz.ostatni_atak = czas
                    
                    # Odepchnij gracza
                    dx = self.gracz.x - zombiak.x
                    dy = self.gracz.y - zombiak.y
                    if dx != 0 or dy != 0:
                        odleglosc = math.sqrt(dx**2 + dy**2)
                        dx /= odleglosc
                        dy /= odleglosc
                        self.gracz.x += dx * 30
                        self.gracz.y += dy * 30
                break
    
    def sprawdz_kolizje_sciany(self, obiekt, nowy_x, nowy_y):
        nowa_pozycja = pygame.Rect(nowy_x, nowy_y, obiekt.szerokosc, obiekt.wysokosc)
        for sciana in self.sciany:
            if nowa_pozycja.colliderect(sciana.rect):
                return True
        return False
    
    def sprawdz_kolizje_z_zombiakami(self, nowy_x, nowy_y):
        # Sprawdź czy gracz koliduje z zombiakami na nowej pozycji
        gracz_rect = pygame.Rect(nowy_x, nowy_y, self.gracz.szerokosc, self.gracz.wysokosc)
        for zombiak in self.zombiaki:
            zombiak_rect = pygame.Rect(zombiak.x, zombiak.y, zombiak.szerokosc, zombiak.wysokosc)
            if gracz_rect.colliderect(zombiak_rect):
                return True
        return False
    
    def sprawdz_drzwi(self):
        gracz_rect = pygame.Rect(self.gracz.x, self.gracz.y, self.gracz.szerokosc, self.gracz.wysokosc)
        for drzwi in self.drzwi:
            if gracz_rect.colliderect(drzwi.rect):
                if drzwi.cel_pietro:  # Schody
                    if len(self.zombiaki) == 0:  # Można zejść tylko gdy nie ma zombiaków
                        self.pietro = drzwi.cel_pietro
                        self.generuj_poziom()
                        self.gracz.x = 100
                        self.gracz.y = 100
                        return True
                return False
        return False

    def aktualizuj(self):
        klawisze = pygame.key.get_pressed()
        
        # Ruch gracza - najpierw sprawdź czy są naciśnięte klawisze
        stary_x, stary_y = self.gracz.x, self.gracz.y
        
        # Bezpośredni ruch gracza
        ruch_x = 0
        ruch_y = 0
        
        if klawisze[pygame.K_LEFT] or klawisze[pygame.K_a]:
            ruch_x = -self.gracz.predkosc
            self.gracz.kierunek_x = -1
        elif klawisze[pygame.K_RIGHT] or klawisze[pygame.K_d]:
            ruch_x = self.gracz.predkosc
            self.gracz.kierunek_x = 1
        else:
            self.gracz.kierunek_x = 0
            
        if klawisze[pygame.K_UP] or klawisze[pygame.K_w]:
            ruch_y = -self.gracz.predkosc
            self.gracz.kierunek_y = -1
        elif klawisze[pygame.K_DOWN] or klawisze[pygame.K_s]:
            ruch_y = self.gracz.predkosc
            self.gracz.kierunek_y = 1
        else:
            self.gracz.kierunek_y = 0
        
        # Zastosuj ruch
        nowa_x = self.gracz.x + ruch_x
        nowa_y = self.gracz.y + ruch_y
        
        # Ograniczenia mapy
        nowa_x = max(20, min(MAPA_SZEROKOSC - self.gracz.szerokosc - 20, nowa_x))
        nowa_y = max(20, min(MAPA_WYSOKOSC - self.gracz.wysokosc - 20, nowa_y))
        
        # Sprawdź kolizje ze ścianami i zombiakami - jeśli kolizja, nie ruszaj się
        if not self.sprawdz_kolizje_sciany(self.gracz, nowa_x, nowa_y) and not self.sprawdz_kolizje_z_zombiakami(nowa_x, nowa_y):
            self.gracz.x = nowa_x
            self.gracz.y = nowa_y
        
        # Aktualizuj kamerę
        self.kamera.aktualizuj(self.gracz)
        
        # Odkryj obszar wokół gracza
        self.odkryj_obszar(self.gracz.x, self.gracz.y)
        
        # Sprawdź drzwi
        self.sprawdz_drzwi()
        
        # Zmiana broni
        if klawisze[pygame.K_1]:
            self.gracz.bron = "pistolet"
        elif klawisze[pygame.K_2]:
            self.gracz.bron = "miecz"
        
        # Ruch zombiaków
        for zombiak in self.zombiaki:
            zombiak.ruch_do_gracza(self.gracz, self.sciany)
        
        # Ruch pocisków
        for pocisk in self.pociski[:]:
            pocisk.ruch()
            if pocisk.czy_poza_ekranem():
                self.pociski.remove(pocisk)
        
        # Sprawdź kolizje
        self.sprawdz_kolizje_pociski()
        self.sprawdz_kolizje_gracz_zombiaki()
        
        # Sprawdź apteczki
        for apteczka in self.apteczki:
            apteczka.sprawdz_kolizje(self.gracz)
        
        # Sprawdź czy wszystkie zombiaki zostały pokonane
        if len(self.zombiaki) == 0:
            if self.pietro > 1:
                self.pietro -= 1
                self.generuj_poziom()
                self.gracz.x = SZEROKOSC // 2
                self.gracz.y = WYSOKOSC // 2
            else:
                return "wygrana"
        
        # Sprawdź czy gracz żyje
        if self.gracz.zycia <= 0:
            return "przegrana"
            
        return "gra"
    
    def rysuj(self, ekran):
        ekran.fill(CZARNY)
        
        # Rysuj fog of war (ciemne kafelki dla nieodkrytych obszarów)
        for kafelek_x in range(int(self.kamera.x // ROZMIAR_KAFELKA), int((self.kamera.x + SZEROKOSC) // ROZMIAR_KAFELKA) + 1):
            for kafelek_y in range(int(self.kamera.y // ROZMIAR_KAFELKA), int((self.kamera.y + WYSOKOSC) // ROZMIAR_KAFELKA) + 1):
                ekran_x = kafelek_x * ROZMIAR_KAFELKA - self.kamera.x
                ekran_y = kafelek_y * ROZMIAR_KAFELKA - self.kamera.y
                
                if (kafelek_x, kafelek_y) in self.odkryte_obszary:
                    # Odkryty obszar - rysuj podłogę
                    pygame.draw.rect(ekran, CIEMNY_SZARY, (ekran_x, ekran_y, ROZMIAR_KAFELKA, ROZMIAR_KAFELKA))
                else:
                    # Nieodkryty obszar - zostaw czarny
                    pass
        
        # Rysuj ściany i drzwi (tylko te widoczne)
        for sciana in self.sciany:
            ekran_x = sciana.x - self.kamera.x
            ekran_y = sciana.y - self.kamera.y
            
            # Sprawdź czy ściana jest w widocznym obszarze
            if (-sciana.szerokosc <= ekran_x <= SZEROKOSC and -sciana.wysokosc <= ekran_y <= WYSOKOSC):
                # Sprawdź czy obszar wokół ściany jest odkryty
                kafelek_x = sciana.x // ROZMIAR_KAFELKA
                kafelek_y = sciana.y // ROZMIAR_KAFELKA
                if (kafelek_x, kafelek_y) in self.odkryte_obszary:
                    pygame.draw.rect(ekran, BRAZOWY, (ekran_x, ekran_y, sciana.szerokosc, sciana.wysokosc))
                    pygame.draw.rect(ekran, CZARNY, (ekran_x, ekran_y, sciana.szerokosc, sciana.wysokosc), 2)
            
        for drzwi in self.drzwi:
            ekran_x = drzwi.x - self.kamera.x
            ekran_y = drzwi.y - self.kamera.y
            
            if (-drzwi.szerokosc <= ekran_x <= SZEROKOSC and -drzwi.wysokosc <= ekran_y <= WYSOKOSC):
                kafelek_x = drzwi.x // ROZMIAR_KAFELKA
                kafelek_y = drzwi.y // ROZMIAR_KAFELKA
                if (kafelek_x, kafelek_y) in self.odkryte_obszary:
                    if drzwi.cel_pietro:  # Schody
                        pygame.draw.rect(ekran, (100, 100, 100), (ekran_x, ekran_y, drzwi.szerokosc, drzwi.wysokosc))
                        pygame.draw.rect(ekran, BIALY, (ekran_x, ekran_y, drzwi.szerokosc, drzwi.wysokosc), 2)
                    else:  # Zwykłe drzwi
                        pygame.draw.rect(ekran, (139, 69, 19), (ekran_x, ekran_y, drzwi.szerokosc, drzwi.wysokosc))
                        pygame.draw.rect(ekran, CZARNY, (ekran_x, ekran_y, drzwi.szerokosc, drzwi.wysokosc), 2)
        
        # Rysuj gracza (zawsze widoczny)
        ekran_x = self.gracz.x - self.kamera.x
        ekran_y = self.gracz.y - self.kamera.y
        
        # Debug - wyświetl pozycję gracza i kamery
        debug_text = self.maly_font.render(f"Gracz: {int(self.gracz.x)}, {int(self.gracz.y)} | Kamera: {int(self.kamera.x)}, {int(self.kamera.y)}", True, BIALY)
        ekran.blit(debug_text, (10, 100))
        
        # Debug - pozycja myszy
        mysz_x, mysz_y = pygame.mouse.get_pos()
        swiatowa_x = mysz_x + self.kamera.x
        swiatowa_y = mysz_y + self.kamera.y
        debug_text2 = self.maly_font.render(f"Mysz: {mysz_x}, {mysz_y} | Świat: {int(swiatowa_x)}, {int(swiatowa_y)}", True, BIALY)
        ekran.blit(debug_text2, (10, 120))
        
        if grafika_bohater:
            grafika_skalowana = pygame.transform.scale(grafika_bohater, (self.gracz.szerokosc, self.gracz.wysokosc))
            ekran.blit(grafika_skalowana, (ekran_x, ekran_y))
        else:
            pygame.draw.rect(ekran, NIEBIESKI, (ekran_x, ekran_y, self.gracz.szerokosc, self.gracz.wysokosc))
        
        # Rysuj broń w ręku
        srodek_x = ekran_x + self.gracz.szerokosc // 2
        srodek_y = ekran_y + self.gracz.wysokosc // 2
        
        if self.gracz.bron == "miecz" and grafika_miecz:
            bron_grafika = pygame.transform.scale(grafika_miecz, (20, 20))
            ekran.blit(bron_grafika, (srodek_x + 15, srodek_y - 10))
        elif self.gracz.bron == "pistolet" and grafika_pistolet:
            bron_grafika = pygame.transform.scale(grafika_pistolet, (20, 20))
            ekran.blit(bron_grafika, (srodek_x + 15, srodek_y - 10))
        
        # Rysuj kierunek patrzenia
        if self.gracz.kierunek_x != 0 or self.gracz.kierunek_y != 0:
            koniec_x = srodek_x + self.gracz.kierunek_x * 30
            koniec_y = srodek_y + self.gracz.kierunek_y * 30
            pygame.draw.line(ekran, BIALY, (srodek_x, srodek_y), (koniec_x, koniec_y), 2)
        
        # Rysuj zombiaki (tylko te widoczne i w odkrytych obszarach)
        for zombiak in self.zombiaki:
            ekran_x = zombiak.x - self.kamera.x
            ekran_y = zombiak.y - self.kamera.y
            
            if (-zombiak.szerokosc <= ekran_x <= SZEROKOSC and -zombiak.wysokosc <= ekran_y <= WYSOKOSC):
                kafelek_x = zombiak.x // ROZMIAR_KAFELKA
                kafelek_y = zombiak.y // ROZMIAR_KAFELKA
                if (kafelek_x, kafelek_y) in self.odkryte_obszary:
                    # Rysuj zombiaka z odpowiednią grafiką
                    grafika_zombiak = None
                    if zombiak.typ == 1 and grafika_zombiak_slaby:
                        grafika_zombiak = grafika_zombiak_slaby
                    elif zombiak.typ == 2 and grafika_zombiak_sredni:
                        grafika_zombiak = grafika_zombiak_sredni
                    elif zombiak.typ == 3 and grafika_zombiak_mocny:
                        grafika_zombiak = grafika_zombiak_mocny
                    
                    if grafika_zombiak:
                        grafika_skalowana = pygame.transform.scale(grafika_zombiak, (zombiak.szerokosc, zombiak.wysokosc))
                        ekran.blit(grafika_skalowana, (ekran_x, ekran_y))
                    else:
                        # Fallback - kolorowe prostokąty
                        if zombiak.typ == 1:
                            kolor = (100, 200, 100)  # Jasny zielony
                        elif zombiak.typ == 2:
                            kolor = (150, 150, 50)   # Żółto-zielony
                        else:
                            kolor = (200, 100, 100)  # Czerwono-zielony
                        pygame.draw.rect(ekran, kolor, (ekran_x, ekran_y, zombiak.szerokosc, zombiak.wysokosc))
                    
                    # Pasek życia
                    szerokosc_paska = zombiak.szerokosc
                    wysokosc_paska = 5
                    pygame.draw.rect(ekran, CZERWONY, (ekran_x, ekran_y - 10, szerokosc_paska, wysokosc_paska))
                    
                    procent_zycia = zombiak.zycia / zombiak.max_zycia
                    pygame.draw.rect(ekran, ZIELONY, (ekran_x, ekran_y - 10, szerokosc_paska * procent_zycia, wysokosc_paska))
            
        # Rysuj pociski (zawsze widoczne gdy są na ekranie)
        for pocisk in self.pociski:
            ekran_x = pocisk.x - self.kamera.x
            ekran_y = pocisk.y - self.kamera.y
            
            if (0 <= ekran_x <= SZEROKOSC and 0 <= ekran_y <= WYSOKOSC):
                pygame.draw.circle(ekran, ZOLTY, (int(ekran_x), int(ekran_y)), pocisk.promien)
            
        # Rysuj apteczki (tylko w odkrytych obszarach)
        for apteczka in self.apteczki:
            ekran_x = apteczka.x - self.kamera.x
            ekran_y = apteczka.y - self.kamera.y
            
            if not apteczka.zebrana and (-apteczka.szerokosc <= ekran_x <= SZEROKOSC and -apteczka.wysokosc <= ekran_y <= WYSOKOSC):
                kafelek_x = apteczka.x // ROZMIAR_KAFELKA
                kafelek_y = apteczka.y // ROZMIAR_KAFELKA
                if (kafelek_x, kafelek_y) in self.odkryte_obszary:
                    if grafika_apteczka:
                        grafika_skalowana = pygame.transform.scale(grafika_apteczka, (apteczka.szerokosc, apteczka.wysokosc))
                        ekran.blit(grafika_skalowana, (ekran_x, ekran_y))
                    else:
                        # Fallback - rysuj prostokąt z krzyżem
                        pygame.draw.rect(ekran, BIALY, (ekran_x, ekran_y, apteczka.szerokosc, apteczka.wysokosc))
                        pygame.draw.rect(ekran, CZERWONY, (ekran_x + 8, ekran_y + 5, 9, 15))
                        pygame.draw.rect(ekran, CZERWONY, (ekran_x + 5, ekran_y + 8, 15, 9))
        
        # Interfejs użytkownika
        # Życia
        for i in range(self.gracz.zycia):
            pygame.draw.circle(ekran, CZERWONY, (30 + i * 40, 30), 15)
            pygame.draw.circle(ekran, BIALY, (30 + i * 40, 30), 15, 2)
        
        # Informacje o grze
        tekst_pietro = self.font.render(f"Piętro: {self.pietro}", True, BIALY)
        ekran.blit(tekst_pietro, (SZEROKOSC - 200, 20))
        
        tekst_punkty = self.font.render(f"Punkty: {self.punkty}", True, BIALY)
        ekran.blit(tekst_punkty, (SZEROKOSC - 200, 60))
        
        tekst_zombiaki = self.font.render(f"Zombiaki: {len(self.zombiaki)}", True, BIALY)
        ekran.blit(tekst_zombiaki, (SZEROKOSC - 200, 100))
        
        tekst_bron = self.font.render(f"Broń: {self.gracz.bron}", True, BIALY)
        ekran.blit(tekst_bron, (20, WYSOKOSC - 60))
        
        # Instrukcje
        instrukcje = [
            "WASD/Strzałki - ruch",
            "Mysz - celowanie i strzał",
            "Spacja - atak mieczem",
            "1 - pistolet, 2 - miecz",
            "Pokonaj wszystkie zombiaki!",
            "Znajdź schody (szare) na dół",
            "R - restart"
        ]
        
        for i, instrukcja in enumerate(instrukcje):
            tekst = self.maly_font.render(instrukcja, True, BIALY)
            ekran.blit(tekst, (20, WYSOKOSC - 150 + i * 25))
        
        # Rysuj celownik myszy (tylko gdy gracz ma pistolet)
        if self.gracz.bron == "pistolet":
            mysz_x, mysz_y = pygame.mouse.get_pos()
            # Sprawdź czy mysz jest w granicach ekranu
            if 0 <= mysz_x < SZEROKOSC and 0 <= mysz_y < WYSOKOSC:
                pygame.draw.circle(ekran, CZERWONY, (mysz_x, mysz_y), 5, 2)
                pygame.draw.line(ekran, CZERWONY, (mysz_x - 10, mysz_y), (mysz_x + 10, mysz_y), 2)
                pygame.draw.line(ekran, CZERWONY, (mysz_x, mysz_y - 10), (mysz_x, mysz_y + 10), 2)

def main():
    gra = Gra()
    dziala = True
    stan = "gra"
    
    while dziala:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dziala = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gra = Gra()
                    stan = "gra"
                elif event.key == pygame.K_ESCAPE:
                    dziala = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and gra.gracz.bron == "pistolet" and stan == "gra":  # Lewy przycisk myszy
                    mysz_x, mysz_y = pygame.mouse.get_pos()
                    # Dodaj pozycję kamery do pozycji myszy
                    swiatowa_x = mysz_x + gra.kamera.x
                    swiatowa_y = mysz_y + gra.kamera.y
                    pocisk = gra.gracz.strzal(swiatowa_x, swiatowa_y)
                    if pocisk:
                        gra.pociski.append(pocisk)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and gra.gracz.bron == "miecz" and stan == "gra":
                    gra.gracz.atak_mieczem(gra.zombiaki)
        
        if stan == "gra":
            stan = gra.aktualizuj()
            gra.rysuj(ekran)
        elif stan == "wygrana":
            ekran.fill(CZARNY)
            tekst = gra.font.render("GRATULACJE! UDAŁO CI SIĘ UCIEC!", True, ZIELONY)
            rect = tekst.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 50))
            ekran.blit(tekst, rect)
            
            tekst_punkty = gra.font.render(f"Twoje punkty: {gra.punkty}", True, BIALY)
            rect_punkty = tekst_punkty.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2))
            ekran.blit(tekst_punkty, rect_punkty)
            
            tekst_restart = gra.maly_font.render("Naciśnij R aby zagrać ponownie", True, BIALY)
            rect_restart = tekst_restart.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 50))
            ekran.blit(tekst_restart, rect_restart)
        elif stan == "przegrana":
            ekran.fill(CZARNY)
            tekst = gra.font.render("PRZEGRAŁEŚ! ZOMBIAKI CIĘ DOPADŁY!", True, CZERWONY)
            rect = tekst.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 50))
            ekran.blit(tekst, rect)
            
            tekst_punkty = gra.font.render(f"Twoje punkty: {gra.punkty}", True, BIALY)
            rect_punkty = tekst_punkty.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2))
            ekran.blit(tekst_punkty, rect_punkty)
            
            tekst_restart = gra.maly_font.render("Naciśnij R aby zagrać ponownie", True, BIALY)
            rect_restart = tekst_restart.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 50))
            ekran.blit(tekst_restart, rect_restart)
        
        pygame.display.flip()
        zegar.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
