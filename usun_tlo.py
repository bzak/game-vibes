#!/usr/bin/env python3
"""
Skrypt do automatycznego usuwania tła z obrazków.
Zamienia kolor pierwszego piksela (lewy górny róg) na przezroczysty.
"""

import os
from PIL import Image
def usun_tlo_z_obrazka(sciezka_wejsciowa, sciezka_wyjsciowa=None):
    """
    Usuwa
d tło z obrazka na podstawie koloru pierwszego piksela.
    
    Args:
        sciezka_wejsciowa: Ścieżka do obrazka wejściowego
        sciezka_wyjsciowa: Ścieżka do obrazka wyjściowego (opcjonalne)
    """
    try:
        # Otwieramy obrazek
        obrazek = Image.open(sciezka_wejsciowa)
        
        # Konwertujemy do RGBA (z obsługą przezroczystości)
        obrazek = obrazek.convert("RGBA")
        
        # Pobieramy dane pikseli
        dane = obrazek.getdata()
        
        # Pobieramy kolor tła (pierwszy piksel)
        kolor_tla = dane[0][:3]  # Tylko RGB, bez alpha
        print(f"Kolor tła: {kolor_tla}")
        
        # Tworzymy nową listę pikseli
        nowe_dane = []
        pikseli_zmienionych = 0
        
        for piksel in dane:
            # Jeśli piksel ma taki sam kolor jak tło, robimy go przezroczystym
            if piksel[:3] == kolor_tla:
                nowe_dane.append((0, 0, 0, 0))  # Przezroczysty
                pikseli_zmienionych += 1
            else:
                nowe_dane.append(piksel)  # Zachowujemy oryginalny kolor
        
        # Ustawiamy nowe dane
        obrazek.putdata(nowe_dane)
        
        # Zapisujemy obrazek
        if sciezka_wyjsciowa is None:
            sciezka_wyjsciowa = sciezka_wejsciowa
        
        obrazek.save(sciezka_wyjsciowa, "PNG")
        print(f"✅ Przetworzono: {sciezka_wejsciowa}")
        print(f"   Zmieniono {pikseli_zmienionych} pikseli na przezroczyste")
        
    except Exception as e:
        print(f"❌ Błąd przy przetwarzaniu {sciezka_wejsciowa}: {e}")

def przetworz_folder(folder):
    """
    Przetwarza wszystkie pliki PNG w folderze.
    """
    if not os.path.exists(folder):
        print(f"❌ Folder {folder} nie istnieje!")
        return
    
    pliki_png = [f for f in os.listdir(folder) if f.lower().endswith('.png')]
    
    if not pliki_png:
        print(f"❌ Brak plików PNG w folderze {folder}")
        return
    
    print(f"🔄 Przetwarzam {len(pliki_png)} plików PNG w folderze {folder}")
    
    for plik in pliki_png:
        sciezka_pelna = os.path.join(folder, plik)
        usun_tlo_z_obrazka(sciezka_pelna)
    
    print("🎉 Przetwarzanie zakończone!")

if __name__ == "__main__":
    # Przetwarzamy folder obrazki
    folder_obrazki = "obrazki"
    przetworz_folder(folder_obrazki)
