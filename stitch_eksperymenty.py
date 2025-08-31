import pygame
import random
import sys

# Inicjalizacja pygame
pygame.init()
pygame.mixer.init()

# Kolory (w formacie RGB)
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
NIEBIESKI = (0, 100, 255)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
ZOLTY = (255, 255, 0)
FIOLETOWY = (128, 0, 128)
ROZOWY = (255, 192, 203)
POMARANCZOWY = (255, 165, 0)
TURKUSOWY = (64, 224, 208)
STITCH_NIEBIESKI = (0, 150, 255)
CIEMNY_NIEBIESKI = (0, 50, 150)

# Ustawienia okna gry
SZEROKOSC = 800
WYSOKOSC = 600
okno = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("🌺 Stitch łapie eksperymenty! 🧪")

# Zegar do kontroli szybkości gry
zegar = pygame.time.Clock()

class Stitch:
    def __init__(self):
        self.x = SZEROKOSC // 2
        self.y = WYSOKOSC - 100
        self.szerokosc = 80
        self.wysokosc = 90
        self.predkosc = 8
        self.kierunek = 0  # -1 lewo, 0 środek, 1 prawo (dla animacji)
        
        # Ładujemy obrazek Stitcha
        try:
            self.obrazek = pygame.image.load("pngegg.png")
            # Skalujemy obrazek do odpowiedniego rozmiaru
            self.obrazek = pygame.transform.scale(self.obrazek, (self.szerokosc, self.wysokosc))
            print("🌺 Załadowano obrazek Stitcha!")
        except:
            print("⚠️ Nie można załadować obrazka Stitcha, używam rysowania!")
            self.obrazek = None
        
    def rysuj(self, okno):
        if self.obrazek:
            # Używamy obrazka Stitcha
            rect = self.obrazek.get_rect()
            rect.centerx = self.x
            rect.bottom = self.y + self.wysokosc // 2
            okno.blit(self.obrazek, rect)
        else:
            # Fallback - rysujemy Stitcha figurami jak wcześniej
            # Ciało Stitcha (gruszkowaty kształt)
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, 
                              (self.x - 30, self.y - 20, 60, 80))
            
            # Głowa (duży owal - główna część Stitcha!)
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, 
                              (self.x - 40, self.y - 75, 80, 65))
            
            # Brzuszek (jasnoniebieski/białawy)
            pygame.draw.ellipse(okno, (150, 220, 255), 
                              (self.x - 20, self.y - 10, 40, 50))
            
            # OGROMNE USZY - najważniejsza cecha Stitcha!
            # Lewe ucho (owalne, duże)
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, 
                              (self.x - 65, self.y - 85, 30, 50))
            # Wnętrze lewego ucha (różowe)
            pygame.draw.ellipse(okno, (255, 150, 200), 
                              (self.x - 60, self.y - 80, 20, 35))
            
            # Prawe ucho (owalne, duże)
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, 
                              (self.x + 35, self.y - 85, 30, 50))
            # Wnętrze prawego ucha (różowe)
            pygame.draw.ellipse(okno, (255, 150, 200), 
                              (self.x + 40, self.y - 80, 20, 35))
            
            # WIELKIE OCZY - charakterystyczne dla Stitcha
            # Lewe oko (duże, czarne)
            pygame.draw.circle(okno, CZARNY, (self.x - 15, self.y - 50), 12)
            # Połysk w lewym oku
            pygame.draw.circle(okno, BIALY, (self.x - 12, self.y - 53), 4)
            
            # Prawe oko (duże, czarne)
            pygame.draw.circle(okno, CZARNY, (self.x + 15, self.y - 50), 12)
            # Połysk w prawym oku
            pygame.draw.circle(okno, BIALY, (self.x + 18, self.y - 53), 4)
            
            # Nos (czarny, okrągły)
            pygame.draw.circle(okno, CZARNY, (self.x, self.y - 35), 4)
            
            # Usta (szeroki uśmiech)
            pygame.draw.arc(okno, CZARNY, (self.x - 15, self.y - 35, 30, 20), 0, 3.14, 2)
            
            # Zęby (małe białe prostokąty)
            for i in range(3):
                pygame.draw.rect(okno, BIALY, (self.x - 8 + i * 6, self.y - 28, 3, 5))
            
            # ŁAPY - 4 łapy z pazurkami
            # Górne łapy
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, (self.x - 50, self.y - 30, 15, 25))
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, (self.x + 35, self.y - 30, 15, 25))
            
            # Pazurki na górnych łapach
            for i in range(3):
                pygame.draw.line(okno, CZARNY, 
                               (self.x - 45 + i * 3, self.y - 15), 
                               (self.x - 43 + i * 3, self.y - 10), 2)
                pygame.draw.line(okno, CZARNY, 
                               (self.x + 37 + i * 3, self.y - 15), 
                               (self.x + 39 + i * 3, self.y - 10), 2)
            
            # Dolne łapy (większe)
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, (self.x - 40, self.y + 35, 20, 30))
            pygame.draw.ellipse(okno, STITCH_NIEBIESKI, (self.x + 20, self.y + 35, 20, 30))
            
            # Pazurki na dolnych łapach
            for i in range(3):
                pygame.draw.line(okno, CZARNY, 
                               (self.x - 35 + i * 4, self.y + 55), 
                               (self.x - 33 + i * 4, self.y + 60), 2)
                pygame.draw.line(okno, CZARNY, 
                               (self.x + 25 + i * 4, self.y + 55), 
                               (self.x + 27 + i * 4, self.y + 60), 2)
            
            # Ogon (mały)
            pygame.draw.circle(okno, STITCH_NIEBIESKI, (self.x, self.y + 45), 8)
    
    def ruch(self, klawisze):
        if klawisze[pygame.K_LEFT] and self.x > self.szerokosc//2:
            self.x -= self.predkosc
            self.kierunek = -1
        elif klawisze[pygame.K_RIGHT] and self.x < SZEROKOSC - self.szerokosc//2:
            self.x += self.predkosc
            self.kierunek = 1
        else:
            self.kierunek = 0

class Eksperyment:
    def __init__(self):
        self.x = random.randint(30, SZEROKOSC - 30)
        self.y = -50
        self.szerokosc = 40
        self.wysokosc = 40
        self.predkosc = random.randint(2, 6)
        self.punkty = random.randint(5, 20)
        self.obroty = 0  # Dla animacji obrotu
        
        # Ładujemy losowy obrazek eksperymentu
        self.typ_obrazka = random.choice(["e1.png", "e2.png", "e3.png", "e4.png"])
        try:
            self.obrazek = pygame.image.load(self.typ_obrazka)
            self.obrazek = pygame.transform.scale(self.obrazek, (self.szerokosc, self.wysokosc))
            print(f"🧪 Załadowano eksperyment: {self.typ_obrazka}")
        except:
            print(f"⚠️ Nie można załadować {self.typ_obrazka}, używam rysowania!")
            self.obrazek = None
            self.kolor = random.choice([ZOLTY, FIOLETOWY, ROZOWY, POMARANCZOWY, TURKUSOWY, ZIELONY])
        
    def ruch(self):
        self.y += self.predkosc
        self.obroty += 5  # Obracamy eksperyment
        
    def rysuj(self, okno):
        if self.obrazek:
            # Używamy prawdziwego obrazka eksperymentu!
            rect = self.obrazek.get_rect()
            rect.centerx = self.x
            rect.centery = self.y
            
            # Obracamy eksperyment podczas spadania
            obrocony_obrazek = pygame.transform.rotate(self.obrazek, self.obroty)
            nowy_rect = obrocony_obrazek.get_rect(center=rect.center)
            okno.blit(obrocony_obrazek, nowy_rect)
        else:
            # Fallback - rysujemy kolorowe kółko jeśli obrazek się nie załadował
            pygame.draw.circle(okno, self.kolor, (int(self.x), int(self.y)), self.szerokosc//2)
            pygame.draw.circle(okno, BIALY, (int(self.x - 5), int(self.y - 5)), 5)

def rysuj_tlo(okno):
    """Rysuje tropikalne tło - plaża i palmy"""
    # Niebo (gradient)
    for y in range(WYSOKOSC//2):
        r = min(255, 135 + y//3)
        g = min(255, 206 + y//4)
        b = 235
        kolor_nieba = (r, g, b)
        pygame.draw.line(okno, kolor_nieba, (0, y), (SZEROKOSC, y))
    
    # Morze
    for y in range(WYSOKOSC//2, WYSOKOSC):
        r = 0
        g = min(255, 100 + (y - WYSOKOSC//2)//4)
        b = 200
        kolor_morza = (r, g, b)
        pygame.draw.line(okno, kolor_morza, (0, y), (SZEROKOSC, y))
    
    # Plaża (piasek)
    pygame.draw.ellipse(okno, (238, 203, 173), (0, WYSOKOSC - 150, SZEROKOSC, 200))
    
    # Palmy (proste)
    for i in range(3):
        x_palma = 100 + i * 300
        # Pień
        pygame.draw.rect(okno, (139, 69, 19), (x_palma - 10, WYSOKOSC - 200, 20, 100))
        # Liście
        for j in range(6):
            angle = j * 60
            end_x = x_palma + 40 * (1 if j % 2 == 0 else -1)
            end_y = WYSOKOSC - 200 - 20
            pygame.draw.line(okno, ZIELONY, (x_palma, WYSOKOSC - 200), (end_x, end_y), 5)
    
    # Chmurki
    for i in range(4):
        x_chmura = 150 + i * 200
        y_chmura = 50 + i * 30
        pygame.draw.circle(okno, BIALY, (x_chmura, y_chmura), 30)
        pygame.draw.circle(okno, BIALY, (x_chmura + 25, y_chmura), 25)
        pygame.draw.circle(okno, BIALY, (x_chmura - 25, y_chmura), 20)

# Sklep z gadżetami
class Sklep:
    def __init__(self):
        self.gadżety = {
            "worek": {"cena": 50, "opis": "Zwiększa obszar łapania!", "kupiony": False},
            "szczypce": {"cena": 100, "opis": "Łapie z daleka!", "kupiony": False},
            "magnes": {"cena": 150, "opis": "Przyciąga eksperymenty!", "kupiony": False}
        }
    
    def rysuj_sklep(self, okno, punkty):
        # Tło sklepu
        pygame.draw.rect(okno, (50, 50, 100), (100, 100, 600, 400))
        pygame.draw.rect(okno, BIALY, (100, 100, 600, 400), 5)
        
        # Tytuł sklepu
        czcionka_duza = pygame.font.Font(None, 48)
        tytul = czcionka_duza.render("🛒 SKLEP STITCHA 🧪", True, BIALY)
        okno.blit(tytul, (200, 120))
        
        # Punkty gracza
        czcionka = pygame.font.Font(None, 36)
        tekst_punkty = czcionka.render(f"Twoje punkty: {punkty}", True, ZOLTY)
        okno.blit(tekst_punkty, (150, 170))
        
        # Lista gadżetów
        y_pozycja = 220
        for i, (nazwa, info) in enumerate(self.gadżety.items()):
            kolor = ZIELONY if info["kupiony"] else BIALY
            if info["kupiony"]:
                tekst = f"{i+1}. ✅ {nazwa.upper()} - {info['opis']} (KUPIONY!)"
            else:
                tekst = f"{i+1}. {nazwa.upper()} - {info['opis']} - {info['cena']} pkt"
            
            gadżet_tekst = czcionka.render(tekst, True, kolor)
            okno.blit(gadżet_tekst, (150, y_pozycja))
            y_pozycja += 40
        
        # Instrukcje
        instrukcje = [
            "Naciśnij 1, 2 lub 3 aby kupić gadżet",
            "ESC - powrót do gry"
        ]
        y_pozycja += 20
        czcionka_mala = pygame.font.Font(None, 24)
        for instrukcja in instrukcje:
            tekst = czcionka_mala.render(instrukcja, True, BIALY)
            okno.blit(tekst, (150, y_pozycja))
            y_pozycja += 25

# Główna funkcja gry
def main():
    # Tworzenie obiektów gry
    stitch = Stitch()
    eksperymenty = []
    sklep = Sklep()
    punkty = 0
    zegar_eksperymentow = 0
    w_sklepie = False  # Czy jesteśmy w sklepie
    
    # Czcionka do wyświetlania punktów
    czcionka = pygame.font.Font(None, 48)
    czcionka_mala = pygame.font.Font(None, 32)
    
    # Główna pętla gry
    dziala = True
    while dziala:
        # Obsługa wydarzeń
        for wydarzenie in pygame.event.get():
            if wydarzenie.type == pygame.QUIT:
                dziala = False
            elif wydarzenie.type == pygame.KEYDOWN:
                if wydarzenie.key == pygame.K_s:  # S - Sklep
                    w_sklepie = not w_sklepie
                elif wydarzenie.key == pygame.K_ESCAPE:  # ESC - Wyjście ze sklepu
                    w_sklepie = False
                elif w_sklepie:  # Kupowanie w sklepie
                    if wydarzenie.key == pygame.K_1:  # Worek
                        nazwa = "worek"
                        if not sklep.gadżety[nazwa]["kupiony"] and punkty >= sklep.gadżety[nazwa]["cena"]:
                            punkty -= sklep.gadżety[nazwa]["cena"]
                            sklep.gadżety[nazwa]["kupiony"] = True
                            print(f"🛒 Kupiono {nazwa}! Pozostało punktów: {punkty}")
                    elif wydarzenie.key == pygame.K_2:  # Szczypce
                        nazwa = "szczypce"
                        if not sklep.gadżety[nazwa]["kupiony"] and punkty >= sklep.gadżety[nazwa]["cena"]:
                            punkty -= sklep.gadżety[nazwa]["cena"]
                            sklep.gadżety[nazwa]["kupiony"] = True
                            print(f"🛒 Kupiono {nazwa}! Pozostało punktów: {punkty}")
                    elif wydarzenie.key == pygame.K_3:  # Magnes
                        nazwa = "magnes"
                        if not sklep.gadżety[nazwa]["kupiony"] and punkty >= sklep.gadżety[nazwa]["cena"]:
                            punkty -= sklep.gadżety[nazwa]["cena"]
                            sklep.gadżety[nazwa]["kupiony"] = True
                            print(f"🛒 Kupiono {nazwa}! Pozostało punktów: {punkty}")
        
        if not w_sklepie:
            # Pobieramy stan klawiszy
            klawisze = pygame.key.get_pressed()
            
            # Ruch Stitcha
            stitch.ruch(klawisze)
        
        # Dodawanie nowych eksperymentów
        if random.randint(1, 40) == 1:  # Co jakiś czas pojawia się nowy eksperyment
            nowy_eksperyment = Eksperyment()
            eksperymenty.append(nowy_eksperyment)
        
        # Ruch eksperymentów
        for eksperyment in eksperymenty[:]:
            eksperyment.ruch()
            if eksperyment.y > WYSOKOSC:  # Eksperyment spadł poza ekran
                eksperymenty.remove(eksperyment)
        
        if not w_sklepie:
            # Sprawdzanie kolizji Stitch-eksperyment z gadżetami
            for eksperyment in eksperymenty[:]:
                # Sprawdzamy odległość z uwzględnieniem gadżetów
                odleglosc_x = abs(stitch.x - eksperyment.x)
                odleglosc_y = abs(stitch.y - eksperyment.y)
                
                # Worek zwiększa obszar łapania
                obszar_x = 60 if sklep.gadżety["worek"]["kupiony"] else 40
                obszar_y = 65 if sklep.gadżety["worek"]["kupiony"] else 45
                
                # Szczypce łapią z daleka
                if sklep.gadżety["szczypce"]["kupiony"]:
                    obszar_x += 30
                    obszar_y += 30
                
                # Magnes przyciąga eksperymenty
                if sklep.gadżety["magnes"]["kupiony"] and odleglosc_x < 100 and odleglosc_y < 100:
                    # Przyciąganie eksperymentu do Stitcha
                    if eksperyment.x < stitch.x:
                        eksperyment.x += 2
                    elif eksperyment.x > stitch.x:
                        eksperyment.x -= 2
                
                if odleglosc_x < obszar_x and odleglosc_y < obszar_y:
                    # Złapanie! Usuwamy eksperyment
                    eksperymenty.remove(eksperyment)
                    punkty += eksperyment.punkty
                    print(f"🧪 Stitch złapał eksperyment {eksperyment.typ_obrazka}! +{eksperyment.punkty} punktów! Razem: {punkty}")
        
        # Rysowanie wszystkiego
        okno.fill((135, 206, 235))  # Jasne niebo jako tło
        
        # Rysujemy tropikalne tło
        rysuj_tlo(okno)
        
        # Rysujemy Stitcha
        stitch.rysuj(okno)
        
        # Rysujemy eksperymenty
        for eksperyment in eksperymenty:
            eksperyment.rysuj(okno)
        
        # Wyświetlamy punkty
        tekst_punkty = czcionka.render(f"🧪 Eksperymenty: {punkty}", True, BIALY)
        okno.blit(tekst_punkty, (10, 10))
        
        if w_sklepie:
            # Rysujemy sklep
            sklep.rysuj_sklep(okno, punkty)
        else:
            # Instrukcje sterowania
            instrukcje = [
                "🌺 Stitch łapie eksperymenty! 🧪",
                "⬅️ ➡️ Strzałki - ruch Stitcha",
                "🛒 S - Sklep z gadżetami",
                "🎯 Łap spadające eksperymenty!"
            ]
            for i, instrukcja in enumerate(instrukcje):
                tekst = czcionka_mala.render(instrukcja, True, BIALY)
                okno.blit(tekst, (10, WYSOKOSC - 120 + i * 25))
        
        # Odświeżamy ekran
        pygame.display.flip()
        zegar.tick(60)  # 60 klatek na sekundę
    
    # Kończymy grę
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("🌺 Witaj w grze Stitch łapie eksperymenty! 🧪")
    print("Użyj strzałek do poruszania Stitchem!")
    print("Łap spadające eksperymenty i zdobywaj punkty!")
    main()
