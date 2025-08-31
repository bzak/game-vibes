import pygame
import random
import sys

# Inicjalizacja pygame
pygame.init()

# Kolory
CZARNY = (0, 0, 0)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)
POMARANCZOWY = (255, 165, 0)
ROZOWY = (255, 192, 203)
BRAZOWY = (139, 69, 19)
SREBRNY = (192, 192, 192)
CIEMNY_NIEBIESKI = (0, 0, 139)
JASNY_ROZOWY = (255, 182, 193)
ZOLTY = (255, 255, 0)
# Kolory dla tła
JASNY_ZIELONY = (144, 238, 144)
CIEMNY_ZIELONY = (34, 139, 34)
BIALY = (255, 255, 255)
JASNY_NIEBIESKI = (173, 216, 230)
FIOLETOWY = (147, 112, 219)

# Ustawienia okna
SZEROKOSC = 800
WYSOKOSC = 600
ROZMIAR_BLOKU = 20

# Inicjalizacja ekranu
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Kot Parowy - Zjadacz Tuńczyków!")

# Zegar do kontroli prędkości gry
zegar = pygame.time.Clock()

def rysuj_tlo(ekran):
    """Rysuje ładne tło dla gry"""
    # Tło gradientowe - od jasnego zielonego do ciemnego
    for y in range(WYSOKOSC):
        # Oblicz kolor dla każdej linii (gradient)
        ratio = y / WYSOKOSC
        r = int(JASNY_ZIELONY[0] * (1 - ratio) + CIEMNY_ZIELONY[0] * ratio)
        g = int(JASNY_ZIELONY[1] * (1 - ratio) + CIEMNY_ZIELONY[1] * ratio)
        b = int(JASNY_ZIELONY[2] * (1 - ratio) + CIEMNY_ZIELONY[2] * ratio)
        pygame.draw.line(ekran, (r, g, b), (0, y), (SZEROKOSC, y))
    
    # Dodaj wzór w kratkę - subtelny
    for x in range(0, SZEROKOSC, ROZMIAR_BLOKU * 2):
        for y in range(0, WYSOKOSC, ROZMIAR_BLOKU * 2):
            if (x // (ROZMIAR_BLOKU * 2) + y // (ROZMIAR_BLOKU * 2)) % 2 == 0:
                # Jasniejsze kwadraciki
                overlay_color = (*JASNY_NIEBIESKI, 30)  # Przezroczyste
                overlay = pygame.Surface((ROZMIAR_BLOKU * 2, ROZMIAR_BLOKU * 2))
                overlay.set_alpha(30)
                overlay.fill(JASNY_NIEBIESKI)
                ekran.blit(overlay, (x, y))
    
    # Dodaj dekoracyjne elementy - małe kwiatki
    # Zapisz aktualny stan random
    current_random_state = random.getstate()
    random.seed(42)  # Zawsze te same kwiatki w tych samych miejscach
    for i in range(15):  # 15 kwiatków
        x = random.randint(50, SZEROKOSC - 50)
        y = random.randint(50, WYSOKOSC - 50)
        # Mały kwiatek
        pygame.draw.circle(ekran, ZOLTY, (x, y), 3)
        # Płatki
        pygame.draw.circle(ekran, BIALY, (x - 3, y), 2)
        pygame.draw.circle(ekran, BIALY, (x + 3, y), 2)
        pygame.draw.circle(ekran, BIALY, (x, y - 3), 2)
        pygame.draw.circle(ekran, BIALY, (x, y + 3), 2)
    
    # Dodaj obramowanie
    pygame.draw.rect(ekran, BRAZOWY, (0, 0, SZEROKOSC, WYSOKOSC), 5)
    
    # Przywróć oryginalny stan random (ważne dla losowego jedzenia!)
    random.setstate(current_random_state)

class KotParowy:
    def __init__(self):
        # Pozycja startowa kota (głowa)
        self.pozycje = [(SZEROKOSC//2, WYSOKOSC//2)]
        self.kierunek = (ROZMIAR_BLOKU, 0)  # Zaczyna idąc w prawo
        self.rosnij = False
        
    def ruch(self):
        # Pobierz pozycję głowy
        glowa = self.pozycje[0]
        # Nowa pozycja głowy
        nowa_glowa = (glowa[0] + self.kierunek[0], glowa[1] + self.kierunek[1])
        
        # Sprawdź czy kot nie wyszedł poza ekran
        if (nowa_glowa[0] < 0 or nowa_glowa[0] >= SZEROKOSC or 
            nowa_glowa[1] < 0 or nowa_glowa[1] >= WYSOKOSC):
            return False  # Koniec gry
            
        # Sprawdź czy kot nie zderzył się sam ze sobą
        if nowa_glowa in self.pozycje:
            return False  # Koniec gry
            
        # Dodaj nową głowę
        self.pozycje.insert(0, nowa_glowa)
        
        # Jeśli kot nie rośnie, usuń ogon
        if not self.rosnij:
            self.pozycje.pop()
        else:
            self.rosnij = False
            
        return True
        
    def zmien_kierunek(self, nowy_kierunek):
        # Nie pozwól kotowi zawrócić w przeciwnym kierunku
        if (nowy_kierunek[0] * -1, nowy_kierunek[1] * -1) != self.kierunek:
            self.kierunek = nowy_kierunek
            
    def jedz(self):
        self.rosnij = True
        
    def rysuj_glowe_kota(self, ekran, pozycja):
        """Rysuje realistyczną głowę kota w stylu pixel art"""
        # Tło głowy - okrągłe
        pygame.draw.ellipse(ekran, POMARANCZOWY, (pozycja[0] + 1, pozycja[1] + 3, 18, 14))
        
        # DUZE KOCIE USZY - bardziej realistyczne
        # Lewe ucho
        pygame.draw.polygon(ekran, POMARANCZOWY, [(pozycja[0] + 1, pozycja[1] + 1), 
                                                 (pozycja[0] + 8, pozycja[1] + 1), 
                                                 (pozycja[0] + 6, pozycja[1] + 8)])
        # Prawe ucho
        pygame.draw.polygon(ekran, POMARANCZOWY, [(pozycja[0] + 12, pozycja[1] + 1), 
                                                 (pozycja[0] + 19, pozycja[1] + 1), 
                                                 (pozycja[0] + 14, pozycja[1] + 8)])
        
        # Wnętrze uszu - różowe
        pygame.draw.polygon(ekran, ROZOWY, [(pozycja[0] + 3, pozycja[1] + 2), 
                                           (pozycja[0] + 6, pozycja[1] + 2), 
                                           (pozycja[0] + 5, pozycja[1] + 6)])
        pygame.draw.polygon(ekran, ROZOWY, [(pozycja[0] + 14, pozycja[1] + 2), 
                                           (pozycja[0] + 17, pozycja[1] + 2), 
                                           (pozycja[0] + 15, pozycja[1] + 6)])
        
        # KOCIE OCZY - duże, zielone, migdałowate
        # Białko oczu
        pygame.draw.ellipse(ekran, (255, 255, 255), (pozycja[0] + 3, pozycja[1] + 7, 5, 4))
        pygame.draw.ellipse(ekran, (255, 255, 255), (pozycja[0] + 12, pozycja[1] + 7, 5, 4))
        # Tęczówki - zielone
        pygame.draw.ellipse(ekran, ZIELONY, (pozycja[0] + 4, pozycja[1] + 8, 3, 3))
        pygame.draw.ellipse(ekran, ZIELONY, (pozycja[0] + 13, pozycja[1] + 8, 3, 3))
        # źrenice - pionowe kreski jak u kota
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 5, pozycja[1] + 8), (pozycja[0] + 5, pozycja[1] + 10), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 14, pozycja[1] + 8), (pozycja[0] + 14, pozycja[1] + 10), 1)
        
        # KOCIE PASKI na głowie
        pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 8, pozycja[1] + 4), (pozycja[0] + 12, pozycja[1] + 4), 1)
        pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 7, pozycja[1] + 6), (pozycja[0] + 13, pozycja[1] + 6), 1)
        
        # NOSEK - trójkąt różowy
        pygame.draw.polygon(ekran, ROZOWY, [(pozycja[0] + 9, pozycja[1] + 11), 
                                           (pozycja[0] + 11, pozycja[1] + 11), 
                                           (pozycja[0] + 10, pozycja[1] + 13)])
        
        # BUZIA KOTA - linia od nosa w dół
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 10, pozycja[1] + 13), (pozycja[0] + 10, pozycja[1] + 15), 1)
        # Uśmiech kota
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 8, pozycja[1] + 15), (pozycja[0] + 10, pozycja[1] + 15), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 10, pozycja[1] + 15), (pozycja[0] + 12, pozycja[1] + 15), 1)
        
        # SUPER DŁUGIE WĄSY
        # Lewe wąsy
        pygame.draw.line(ekran, CZARNY, (pozycja[0] - 3, pozycja[1] + 10), (pozycja[0] + 5, pozycja[1] + 11), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] - 3, pozycja[1] + 12), (pozycja[0] + 5, pozycja[1] + 12), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] - 3, pozycja[1] + 14), (pozycja[0] + 5, pozycja[1] + 13), 1)
        # Prawe wąsy
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 15, pozycja[1] + 11), (pozycja[0] + 23, pozycja[1] + 10), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 15, pozycja[1] + 12), (pozycja[0] + 23, pozycja[1] + 12), 1)
        pygame.draw.line(ekran, CZARNY, (pozycja[0] + 15, pozycja[1] + 13), (pozycja[0] + 23, pozycja[1] + 14), 1)
    
    def rysuj_cialo_kota(self, ekran, pozycja, numer_segmentu):
        """Rysuje segment ciała kota w stylu pixel art"""
        # Główne ciało - bardziej owalne
        pygame.draw.ellipse(ekran, POMARANCZOWY, (pozycja[0], pozycja[1] + 2, ROZMIAR_BLOKU, ROZMIAR_BLOKU - 4))
        
        # KOCIE PASKI na ciele - jak u prawdziwego kota
        pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 3, pozycja[1] + 4), (pozycja[0] + 17, pozycja[1] + 4), 1)
        pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 2, pozycja[1] + 8), (pozycja[0] + 18, pozycja[1] + 8), 1)
        pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 3, pozycja[1] + 12), (pozycja[0] + 17, pozycja[1] + 12), 1)
        
        # KOCIE ŁAPKI - tylko przy wybranych segmentach
        if numer_segmentu % 2 == 0:  # Co drugi segment ma łapki
            # Przednie łapki
            pygame.draw.ellipse(ekran, POMARANCZOWY, (pozycja[0] + 2, pozycja[1] + 14, 4, 7))
            pygame.draw.ellipse(ekran, POMARANCZOWY, (pozycja[0] + 14, pozycja[1] + 14, 4, 7))
            # Pazurki
            pygame.draw.circle(ekran, ROZOWY, (pozycja[0] + 4, pozycja[1] + 19), 2)
            pygame.draw.circle(ekran, ROZOWY, (pozycja[0] + 16, pozycja[1] + 19), 2)
            # Małe pazurki
            pygame.draw.circle(ekran, CZARNY, (pozycja[0] + 4, pozycja[1] + 19), 1)
            pygame.draw.circle(ekran, CZARNY, (pozycja[0] + 16, pozycja[1] + 19), 1)
        
        # OGON na ostatnim segmencie
        if numer_segmentu > 3:  # Dłuższe koty mają ogon
            # Ogon kota - zakrzywiony
            pygame.draw.line(ekran, POMARANCZOWY, (pozycja[0] + 10, pozycja[1] + 16), (pozycja[0] + 8, pozycja[1] + 22), 3)
            pygame.draw.line(ekran, POMARANCZOWY, (pozycja[0] + 8, pozycja[1] + 22), (pozycja[0] + 12, pozycja[1] + 25), 3)
            # Paski na ogonie
            pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 9, pozycja[1] + 18), (pozycja[0] + 8, pozycja[1] + 20), 1)
            pygame.draw.line(ekran, BRAZOWY, (pozycja[0] + 10, pozycja[1] + 23), (pozycja[0] + 11, pozycja[1] + 24), 1)
    
    def rysuj(self, ekran):
        for i, pozycja in enumerate(self.pozycje):
            if i == 0:  # Głowa kota - teraz super realistyczna!
                self.rysuj_glowe_kota(ekran, pozycja)
            else:  # Ciało kota - też bardziej realistyczne!
                self.rysuj_cialo_kota(ekran, pozycja, i)

class Jedzenie:
    def __init__(self, pozycje_kota=None):
        self.pozycja = self.nowa_pozycja(pozycje_kota)
        self.typ = random.choice(['tunczyk', 'karma'])
        
    def nowa_pozycja(self, pozycje_kota=None):
        """Generuje nową pozycję jedzenia, unikając kolizji z kotem"""
        while True:
            x = random.randint(0, (SZEROKOSC - ROZMIAR_BLOKU) // ROZMIAR_BLOKU) * ROZMIAR_BLOKU
            y = random.randint(0, (WYSOKOSC - ROZMIAR_BLOKU) // ROZMIAR_BLOKU) * ROZMIAR_BLOKU
            nowa_pozycja = (x, y)
            
            # Sprawdź czy nowa pozycja nie koliduje z kotem
            if pozycje_kota is None or nowa_pozycja not in pozycje_kota:
                return nowa_pozycja
        
    def rysuj(self, ekran):
        if self.typ == 'tunczyk':
            # Rysuj rybę - tuńczyka
            # Ciało ryby
            pygame.draw.ellipse(ekran, SREBRNY, (self.pozycja[0] + 2, self.pozycja[1] + 5, 16, 10))
            # Ogon ryby
            pygame.draw.polygon(ekran, CIEMNY_NIEBIESKI, [(self.pozycja[0], self.pozycja[1] + 8), 
                                                         (self.pozycja[0], self.pozycja[1] + 12), 
                                                         (self.pozycja[0] + 5, self.pozycja[1] + 10)])
            # Oko ryby
            pygame.draw.circle(ekran, CZARNY, (self.pozycja[0] + 15, self.pozycja[1] + 8), 2)
            pygame.draw.circle(ekran, ZOLTY, (self.pozycja[0] + 15, self.pozycja[1] + 8), 1)
            # Płetwy
            pygame.draw.line(ekran, CIEMNY_NIEBIESKI, (self.pozycja[0] + 10, self.pozycja[1] + 15), (self.pozycja[0] + 12, self.pozycja[1] + 18), 2)
            pygame.draw.line(ekran, CIEMNY_NIEBIESKI, (self.pozycja[0] + 10, self.pozycja[1] + 5), (self.pozycja[0] + 12, self.pozycja[1] + 2), 2)
        else:  # karma dla kota
            # Rysuj karmę - jedna większa brązowa kulka
            środek_x = self.pozycja[0] + ROZMIAR_BLOKU // 2
            środek_y = self.pozycja[1] + ROZMIAR_BLOKU // 2
            
            # Główna kulka karmy - większa
            pygame.draw.circle(ekran, BRAZOWY, (środek_x, środek_y), 8)
            # Błysk na karmie - żółty środek
            pygame.draw.circle(ekran, ZOLTY, (środek_x - 2, środek_y - 2), 3)
            # Mały biały błysk dla realizmu
            pygame.draw.circle(ekran, BIALY, (środek_x - 1, środek_y - 1), 1)

def rysuj_guzik(ekran, tekst, x, y, szerokosc, wysokosc, kolor_tla, kolor_tekstu):
    """Rysuje guzik z tekstem"""
    pygame.draw.rect(ekran, kolor_tla, (x, y, szerokosc, wysokosc))
    pygame.draw.rect(ekran, CZARNY, (x, y, szerokosc, wysokosc), 3)
    
    font = pygame.font.Font(None, 36)
    tekst_surface = font.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_surface.get_rect(center=(x + szerokosc//2, y + wysokosc//2))
    ekran.blit(tekst_surface, tekst_rect)
    
    return pygame.Rect(x, y, szerokosc, wysokosc)

def ekran_konca_gry(ekran, punkty):
    """Pokazuje ekran końca gry z guzikiem restart"""
    font_duzy = pygame.font.Font(None, 72)
    font_sredni = pygame.font.Font(None, 48)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    mouse_pos = pygame.mouse.get_pos()
                    # Sprawdź czy kliknięto w guzik
                    guzik_rect = pygame.Rect(SZEROKOSC//2 - 100, WYSOKOSC//2 + 50, 200, 60)
                    if guzik_rect.collidepoint(mouse_pos):
                        return True  # Zagraj ponownie
        
        # Rysuj tło
        ekran.fill(CZARNY)
        
        # Tytuł "KONIEC GRY!"
        tekst_koniec = font_duzy.render("KONIEC GRY!", True, CZERWONY)
        tekst_rect = tekst_koniec.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 100))
        ekran.blit(tekst_koniec, tekst_rect)
        
        # Wynik
        tekst_wynik = font_sredni.render(f"Twój wynik: {punkty} punktów!", True, ZIELONY)
        wynik_rect = tekst_wynik.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 40))
        ekran.blit(tekst_wynik, wynik_rect)
        
        # Guzik "Zagraj ponownie"
        rysuj_guzik(ekran, "Zagraj ponownie", SZEROKOSC//2 - 100, WYSOKOSC//2 + 50, 200, 60, ZIELONY, CZARNY)
        
        # Instrukcja
        tekst_instrukcja = font_sredni.render("Kliknij guzik, żeby zagrać ponownie!", True, ZOLTY)
        instr_rect = tekst_instrukcja.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 150))
        ekran.blit(tekst_instrukcja, instr_rect)
        
        pygame.display.flip()
        zegar.tick(60)

def ekran_pauzy(ekran, punkty, kot, jedzenie):
    """Pokazuje ekran pauzy z widoczną planszą w tle"""
    font_duzy = pygame.font.Font(None, 72)
    font_sredni = pygame.font.Font(None, 48)
    font_maly = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Wciśnij P żeby wrócić do gry
                    return  # Wróć do gry
                elif event.key == pygame.K_ESCAPE:  # ESC też może wrócić do gry
                    return
        
        # NAJPIERW rysuj całą planszę jak normalnie
        rysuj_tlo(ekran)  # Ładne tło także podczas pauzy!
        
        # Rysuj kota i jedzenie (jak w normalnej grze)
        kot.rysuj(ekran)
        jedzenie.rysuj(ekran)
        
        # Wyświetl punkty (jak w normalnej grze)
        tekst_punkty = font_maly.render(f"Punkty: {punkty}", True, ZIELONY)
        ekran.blit(tekst_punkty, (10, 10))
        
        # TERAZ nałóż półprzezroczyste tło dla menu pauzy
        overlay = pygame.Surface((SZEROKOSC, WYSOKOSC))
        overlay.set_alpha(150)  # Trochę bardziej przezroczyste żeby lepiej widzieć kota
        overlay.fill(CZARNY)
        ekran.blit(overlay, (0, 0))
        
        # Ramka dla menu pauzy
        pygame.draw.rect(ekran, POMARANCZOWY, (SZEROKOSC//2 - 200, WYSOKOSC//2 - 120, 400, 240), 3)
        pygame.draw.rect(ekran, CZARNY, (SZEROKOSC//2 - 197, WYSOKOSC//2 - 117, 394, 234))
        
        # Tytuł "PAUZA" z tłem
        tekst_pauza = font_duzy.render("PAUZA", True, ZOLTY)
        tekst_rect = tekst_pauza.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 80))
        # Tło dla tekstu
        pygame.draw.rect(ekran, CZARNY, (tekst_rect.x - 10, tekst_rect.y - 5, tekst_rect.width + 20, tekst_rect.height + 10))
        ekran.blit(tekst_pauza, tekst_rect)
        
        # Aktualny wynik
        tekst_wynik = font_sredni.render(f"Aktualny wynik: {punkty} punktów", True, ZIELONY)
        wynik_rect = tekst_wynik.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 20))
        ekran.blit(tekst_wynik, wynik_rect)
        
        # Instrukcje
        tekst_instrukcja1 = font_sredni.render("Wciśnij P lub ESC, żeby wrócić do gry", True, ROZOWY)
        instr1_rect = tekst_instrukcja1.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 30))
        ekran.blit(tekst_instrukcja1, instr1_rect)
        
        tekst_instrukcja2 = font_sredni.render("🐱 Kot cierpliwie czeka! 🐱", True, POMARANCZOWY)
        instr2_rect = tekst_instrukcja2.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 70))
        ekran.blit(tekst_instrukcja2, instr2_rect)
        
        pygame.display.flip()
        zegar.tick(60)

def ekran_startowy(ekran):
    """Pokazuje ekran startowy z tytułem i guzikiem PLAY"""
    font_tytul = pygame.font.Font(None, 96)
    font_duzy = pygame.font.Font(None, 72)
    font_sredni = pygame.font.Font(None, 48)
    font_maly = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    mouse_pos = pygame.mouse.get_pos()
                    # Sprawdź czy kliknięto w guzik PLAY
                    guzik_rect = pygame.Rect(SZEROKOSC//2 - 100, WYSOKOSC//2 + 50, 200, 80)
                    if guzik_rect.collidepoint(mouse_pos):
                        return  # Rozpocznij grę!
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return  # Można też zacząć spacją lub enterem
        
        # Rysuj ładne tło
        rysuj_tlo(ekran)
        
        # Półprzezroczyste tło dla menu
        overlay = pygame.Surface((SZEROKOSC, WYSOKOSC))
        overlay.set_alpha(180)
        overlay.fill(CZARNY)
        ekran.blit(overlay, (0, 0))
        
        # Tytuł gry - kolorowy i duży!
        tekst_tytul1 = font_tytul.render("KOT", True, POMARANCZOWY)
        tytul1_rect = tekst_tytul1.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 120))
        ekran.blit(tekst_tytul1, tytul1_rect)
        
        tekst_tytul2 = font_duzy.render("PARÓWKA", True, ROZOWY)
        tytul2_rect = tekst_tytul2.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 70))
        ekran.blit(tekst_tytul2, tytul2_rect)
        
        # Podtytuł
        tekst_podtytul = font_sredni.render("🐱 Zjadacz Tuńczyków! 🐟", True, ZIELONY)
        podtytul_rect = tekst_podtytul.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 - 20))
        ekran.blit(tekst_podtytul, podtytul_rect)
        
        # Guzik PLAY - duży i kolorowy!
        rysuj_guzik(ekran, "PLAY", SZEROKOSC//2 - 100, WYSOKOSC//2 + 50, 200, 80, ZIELONY, CZARNY)
        
        # Instrukcje
        tekst_instrukcja1 = font_maly.render("Kliknij PLAY lub wciśnij SPACJĘ", True, ZOLTY)
        instr1_rect = tekst_instrukcja1.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 160))
        ekran.blit(tekst_instrukcja1, instr1_rect)
        
        tekst_instrukcja2 = font_maly.render("Sterowanie: strzałki, P = pauza", True, JASNY_ROZOWY)
        instr2_rect = tekst_instrukcja2.get_rect(center=(SZEROKOSC//2, WYSOKOSC//2 + 190))
        ekran.blit(tekst_instrukcja2, instr2_rect)
        
        # Mały kot w rogu dla dekoracji
        pygame.draw.ellipse(ekran, POMARANCZOWY, (50, 50, 30, 25))
        # Uszka
        pygame.draw.polygon(ekran, POMARANCZOWY, [(50, 50), (60, 50), (55, 40)])
        pygame.draw.polygon(ekran, POMARANCZOWY, [(65, 50), (75, 50), (70, 40)])
        # Oczy
        pygame.draw.circle(ekran, ZIELONY, (58, 58), 2)
        pygame.draw.circle(ekran, ZIELONY, (67, 58), 2)
        # Wąsy
        pygame.draw.line(ekran, CZARNY, (45, 62), (52, 63), 1)
        pygame.draw.line(ekran, CZARNY, (73, 63), (80, 62), 1)
        
        pygame.display.flip()
        zegar.tick(60)

def main():
    # Najpierw pokaż ekran startowy
    ekran_startowy(ekran)
    
    while True:  # Główna pętla gry - pozwala na restart
        # Zresetuj grę
        kot = KotParowy()
        jedzenie = Jedzenie()
        punkty = 0
        font = pygame.font.Font(None, 36)
        gra_trwa = True
        
        while gra_trwa:
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        kot.zmien_kierunek((0, -ROZMIAR_BLOKU))
                    elif event.key == pygame.K_DOWN:
                        kot.zmien_kierunek((0, ROZMIAR_BLOKU))
                    elif event.key == pygame.K_LEFT:
                        kot.zmien_kierunek((-ROZMIAR_BLOKU, 0))
                    elif event.key == pygame.K_RIGHT:
                        kot.zmien_kierunek((ROZMIAR_BLOKU, 0))
                    elif event.key == pygame.K_p:  # PAUZA!
                        ekran_pauzy(ekran, punkty, kot, jedzenie)
            
            # Ruch kota
            if not kot.ruch():
                gra_trwa = False  # Koniec tej rundy
                
            # Sprawdź czy kot zjadł jedzenie
            if gra_trwa and kot.pozycje[0] == jedzenie.pozycja:
                kot.jedz()
                if jedzenie.typ == 'tunczyk':
                    punkty += 10
                else:  # karma
                    punkty += 5
                jedzenie = Jedzenie(kot.pozycje)  # Nowe jedzenie - unikaj pozycji kota!
                
            if gra_trwa:
                # Rysowanie tylko gdy gra trwa
                rysuj_tlo(ekran)  # Najpierw ładne tło!
                kot.rysuj(ekran)
                jedzenie.rysuj(ekran)
                
                # Wyświetl punkty
                tekst_punkty = font.render(f"Punkty: {punkty}", True, ZIELONY)
                ekran.blit(tekst_punkty, (10, 10))
                
                # Wyświetl instrukcje
                instrukcje = font.render("Strzałki = ruch, P = pauza, Zjadaj tuńczyki i karmę!", True, ZIELONY)
                ekran.blit(instrukcje, (10, WYSOKOSC - 40))
                
                pygame.display.flip()
                zegar.tick(10)  # 10 klatek na sekundę
        
        # Pokaż ekran końca gry i czekaj na restart
        if not ekran_konca_gry(ekran, punkty):
            # Jeśli gracz nie chce grać ponownie, wróć do ekranu startowego
            ekran_startowy(ekran)

if __name__ == "__main__":
    main()
