

# 🎮 Gry do Nauki Programowania dla Dzieci

To repozytorium zawiera kolekcję gier stworzonych w celu nauki programowania dla dzieci w wieku 7-10 lat (i trochę starszych). 

W repozytorium znajduje się plik `.windsurfrules`, który zawiera specjalne instrukcje dla AI asystenta pomagającego w nauce programowania. Dzięki temu AI dostosowuje swoje odpowiedzi do poziomu młodego programisty. Wszystkie gry zostały stworzone przez dzieci 7-10 lat (z niewielką pomocą rodziców), poprzez mówienie do edytora Windsurf, na razie bez rozumienia kodu. O dziwo Windsurf bardzo dobrze rozpoznaje mowę po polsku nawet dyktowaną przez dzieci, a AI Claude Sonnet całkiem dobrze radzi sobie z pisaniem prostych gier w pygame. Warto też dodać do edytora AI [MCP stability-ai](https://github.com/tadasant/mcp-server-stability-ai) do generowania grafik do gier. 

## 🛠️ Instalacja

**Wymagania:**
- Python 3.6 lub nowszy
- pip (menedżer pakietów Python)

Przed uruchomieniem gier, zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

To zainstaluje bibliotekę pygame w wersji 2.5.2, która jest potrzebna do uruchomienia wszystkich gier.

## 🎯 Dostępne gry

### 1. Statek Kosmiczny kontra Ufoludki 🚀

**Plik:** `statek_kosmiczny.py`

Epicka gra kosmiczna z systemem sklepu i różnymi statkami do odblokowania!

**Jak grać:**
- Steruj statkiem strzałkami lewo/prawo
- Strzelaj spacją do ufoludków
- Zbieraj punkty i kupuj nowe statki w sklepie
- 4 rodzaje statków: podstawowy, szybki, podwójny, pancerny
- System zapisu postępów

**Uruchomienie:**
```
python statek_kosmiczny.py
```

### 2. Kot Parowa - Gra Snake z Kotem! 🐱

**Plik:** `kot_parowy.py`

Klasyczna gra Snake, ale zamiast węża mamy uroczego kota parówkę!

**Jak grać:**
- Używaj **strzałek** na klawiaturze, żeby sterować kotem
- Zbieraj tuńczyki (10 punktów) i karmę dla kota (5 punktów)
- Kot rośnie po zjedzeniu jedzenia!
- Uważaj, żeby nie uderzyć w ścianę lub w siebie!

**Uruchomienie:**
```
python kot_parowy.py
```

### 🎮 Inne gry w repozytorium:
- **Diablo Zombiaki** (`diablo_zombiaki.py`) - gra akcji w stylu Diablo
- **Stitch łapie eksperymenty** (`stitch_eksperymenty.py`) - łap spadające eksperymenty

## 🛠️ Instalacja

1. Zainstaluj wymagane biblioteki:
```
pip install -r requirements.txt
```

2. Wybierz grę i uruchom ją komendą python!

## 🎨 Grafiki

W folderze `obrazki/` znajdują się grafiki pixel art do gier, wygenerowane i przetworzone specjalnie dla młodych graczy.

## 👨‍🎓 Cel edukacyjny

Projekt ma na celu:
- Pokazanie dzieciom, że programowanie może być świetną zabawą
- Nauka podstaw programowania w Python
- Rozwijanie logicznego myślenia przez tworzenie gier
- Szybkie efekty i satysfakcja z własnych projektów

Miłej zabawy i powodzenia w nauce programowania! 🎮✨

