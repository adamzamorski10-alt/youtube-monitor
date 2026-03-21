# YouTube Monitor - Instrukcja Instalacji i Konfiguracji

## 📋 Wymagania
- Python 3.8 lub nowszy
- Konto Google (do YouTube API)
- Konto Telegram

---

## 🚀 Instalacja

### 1. Zainstaluj Python
Pobierz i zainstaluj Python z: https://www.python.org/downloads/
- **WAŻNE**: Podczas instalacji zaznacz "Add Python to PATH"

### 2. Pobierz pliki projektu
Umieść wszystkie pliki w jednym folderze, np. `C:\YouTubeMonitor\`

### 3. Zainstaluj wymagane biblioteki
Otwórz CMD (wiersz polecenia) i przejdź do folderu z projektem:
```cmd
cd C:\YouTubeMonitor
pip install -r requirements.txt
```

---

## 🔑 Konfiguracja

### KROK 1: Pobierz klucz YouTube Data API

1. Wejdź na: https://console.cloud.google.com/
2. Zaloguj się na konto Google
3. Kliknij "Select a project" → "New Project"
4. Nazwij projekt, np. "YouTube Monitor" → "Create"
5. Poczekaj chwilę, aż projekt się utworzy
6. W menu po lewej stronie wybierz: **APIs & Services** → **Library**
7. Wyszukaj: **YouTube Data API v3**
8. Kliknij na nią, potem **Enable**
9. Przejdź do: **APIs & Services** → **Credentials**
10. Kliknij **+ CREATE CREDENTIALS** → **API key**
11. **SKOPIUJ KLUCZ** - to jest Twój `youtube_api_key`
12. (Opcjonalnie) Kliknij "Edit API key" i ogranicz do YouTube Data API v3

### KROK 2: Utwórz bota Telegram

1. Otwórz Telegram i znajdź: **@BotFather**
2. Wyślij: `/newbot`
3. Podaj nazwę bota, np. `YouTube Notifier`
4. Podaj username bota, np. `twojnazwa_youtube_bot` (musi kończyć się na `_bot`)
5. **SKOPIUJ TOKEN** - to jest Twój `telegram_bot_token`
6. Rozpocznij rozmowę z Twoim botem (kliknij link od BotFather lub wyszukaj bota)
7. Wyślij dowolną wiadomość, np. `/start`

### KROK 3: Pobierz swoje Chat ID

1. Wejdź na: https://api.telegram.org/bot`TWOJ_TOKEN`/getUpdates
   - Zamień `TWOJ_TOKEN` na token z KROKU 2
   - Przykład: `https://api.telegram.org/bot123456:ABCdefGHI.../getUpdates`
2. Znajdź w JSON: `"chat":{"id":123456789...`
3. **SKOPIUJ NUMER** - to jest Twój `telegram_chat_id`

### KROK 4: Znajdź ID kanałów YouTube

**Metoda 1 - Z adresu URL kanału:**
- Jeśli kanał ma adres: `youtube.com/@nazwkanału`
- Wejdź na kanał i kliknij prawym przyciskiem → "Wyświetl źródło strony"
- Wyszukaj (Ctrl+F): `"channelId"`
- Skopiuj wartość typu: `UCxxxxxxxxxxxxxxxxxx`

**Metoda 2 - Narzędzie online:**
- Wejdź na: https://commentpicker.com/youtube-channel-id.php
- Wklej adres URL kanału
- Skopiuj Channel ID

**Metoda 3 - Z URL (jeśli kanał ma stary format):**
- Jeśli URL to: `youtube.com/channel/UCxxxxxxx` - to `UCxxxxxxx` jest Channel ID

### KROK 5: Stwórz plik config.json

1. Skopiuj plik `config.json.example` i zmień nazwę na `config.json`
2. Otwórz `config.json` w notatniku
3. Wypełnij swoimi danymi:

```json
{
  "youtube_api_key": "AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "telegram_bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
  "telegram_chat_id": "123456789",
  "channels": [
    {
      "name": "Kanał Gaming",
      "channel_id": "UCxxxxxxxxxxxxxxxxxxxxxx"
    },
    {
      "name": "Kanał Muzyczny",
      "channel_id": "UCyyyyyyyyyyyyyyyyyyyyyy"
    }
  ]
}
```

4. Zapisz plik

---

## ▶️ Uruchomienie

### Tryb Normalny (okno CMD)
Otwórz CMD w folderze projektu:
```cmd
cd C:\YouTubeMonitor
python youtube_monitor.py
```

Program będzie działał, dopóki nie zamkniesz okna CMD.

### Tryb w Tle (Windows Service) - ZALECANE

Będziesz potrzebować **NSSM** (Non-Sucking Service Manager):

1. Pobierz NSSM: https://nssm.cc/download
2. Wypakuj plik i skopiuj `nssm.exe` (64-bit) do folderu projektu
3. Otwórz CMD **jako Administrator**
4. Przejdź do folderu:
   ```cmd
   cd C:\YouTubeMonitor
   ```
5. Zainstaluj usługę:
   ```cmd
   nssm install YouTubeMonitor
   ```
6. W oknie które się otworzy:
   - **Path**: wskaż `python.exe` (np. `C:\Python311\python.exe`)
   - **Startup directory**: wskaż folder projektu (np. `C:\YouTubeMonitor`)
   - **Arguments**: `youtube_monitor.py`
   - Zakładka **Details**: 
     - Display name: `YouTube Monitor`
     - Description: `Monitoruje kanały YouTube i wysyła powiadomienia`
   - Zakładka **I/O**:
     - Output: `C:\YouTubeMonitor\service_output.log`
     - Error: `C:\YouTubeMonitor\service_error.log`
7. Kliknij **Install service**
8. Uruchom usługę:
   ```cmd
   nssm start YouTubeMonitor
   ```

**Przydatne komendy:**
```cmd
nssm status YouTubeMonitor    # Sprawdź status
nssm stop YouTubeMonitor      # Zatrzymaj
nssm restart YouTubeMonitor   # Restart
nssm remove YouTubeMonitor    # Usuń usługę (najpierw zatrzymaj)
```

---

## 📊 Pliki generowane przez aplikację

- **youtube_monitor.log** - Logi aplikacji (wszystkie zdarzenia)
- **seen_videos.json** - Lista już zobaczonych filmów (NIE USUWAJ!)
- **service_output.log** - Output z usługi (tylko gdy działa jako usługa)
- **service_error.log** - Błędy usługi (tylko gdy działa jako usługa)

---

## 🧪 Testowanie

### Test 1: Sprawdź czy dane są poprawne
```cmd
python youtube_monitor.py
```
Jeśli wszystko działa:
- Zobaczysz logi: "YouTube Monitor uruchomiony!"
- Po chwili: "Sprawdzam kanał: ..."
- Telegram bot wyśle powiadomienia o filmach z ostatnich 24h

### Test 2: Wymuś powiadomienie
1. Usuń plik `seen_videos.json`
2. Uruchom: `python youtube_monitor.py`
3. Dostaniesz powiadomienia o najnowszych filmach (z ostatnich 24h)

---

## ⚙️ Dostosowanie

### Zmień częstotliwość sprawdzania
W pliku `youtube_monitor.py` (w funkcji `run`):
```python
time.sleep(60)  # Czekaj minutę
```
Zmień `60` na inną wartość (w sekundach), np. `300` dla 5 minut.

### Zmień zakres "nowych" filmów
W pliku `youtube_monitor.py`, linia 144:
```python
def is_video_new(self, published_at: str, hours: int = 24):
```
Zmień `hours: int = 24` na inną wartość (w godzinach).

### Dodaj więcej kanałów
Edytuj `config.json` i dodaj kolejne wpisy w sekcji `channels`:
```json
{
  "name": "Nowy Kanał",
  "channel_id": "UCzzzzzzzzzzzzzzzzzzz"
}
```

---

## ❗ Rozwiązywanie problemów

### "ImportError: No module named..."
Zainstaluj wymagane biblioteki:
```cmd
pip install -r requirements.txt
```

### "API key not valid"
Sprawdź czy klucz YouTube API jest poprawny i czy YouTube Data API v3 jest włączone w Google Cloud Console.

### Nie dostaję powiadomień Telegram
1. Sprawdź czy token bota i chat_id są poprawne
2. Upewnij się, że wysłałeś wiadomość do bota (rozpocząłeś konwersację)
3. Sprawdź logi w `youtube_monitor.log`

### "Quota exceeded"
YouTube API ma limit 10,000 jednostek dziennie. Każde zapytanie to ~100 jednostek.
- Zmniejsz częstotliwość sprawdzania
- Zmniejsz liczbę kanałów
- Lub poczekaj do następnego dnia (limit resetuje się o północy PST)

### Usługa Windows nie startuje
1. Sprawdź `service_error.log`
2. Upewnij się że ścieżki w NSSM są bezwzględne (pełne)
3. Sprawdź czy `config.json` istnieje w folderze projektu

---

## 📝 Limity i ograniczenia

- **YouTube API**: 10,000 jednostek/dzień (quota)
- **Telegram**: 30 wiadomości/sekundę (aplikacja ma opóźnienie 1s między wiadomościami)
- **Sprawdzanie co 15 min**: ~96 sprawdzeń/dzień × liczba kanałów

**Przykład:** 
- 10 kanałów × 96 sprawdzeń × ~100 jednostek = 96,000 jednostek/dzień
- To przekracza darmowy limit!
- **Rozwiązanie**: Sprawdzaj rzadziej (np. co 30 min) lub monitoruj mniej kanałów

---

## 🔒 Bezpieczeństwo

- **NIE UDOSTĘPNIAJ** pliku `config.json` - zawiera klucze API!
- Dodaj do `.gitignore` jeśli używasz Git:
  ```
  config.json
  seen_videos.json
  *.log
  ```
- Klucze API możesz ograniczyć w Google Cloud Console (tylko YouTube API, tylko Twoje IP)

---

## 📧 Kontakt i wsparcie

Jeśli masz problemy:
1. Sprawdź plik `youtube_monitor.log`
2. Sprawdź czy wszystkie kroki konfiguracji zostały wykonane
3. Upewnij się że Python i wszystkie biblioteki są zainstalowane

---

**Powodzenia! 🎉**
