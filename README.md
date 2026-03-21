# 🎬 YouTube Monitor - Monitor Kanałów YouTube

Aplikacja do automatycznego monitorowania kanałów YouTube i wysyłania powiadomień na Telegram o nowych filmach.

## ✨ Funkcje

- ✅ Monitorowanie wielu kanałów YouTube jednocześnie
- ✅ Sprawdzanie co 15 minut (konfigurowalne)
- ✅ Powiadomienia na Telegram ze szczegółami filmu
- ✅ **Pracuje 24/7 na GitHub Actions** (bez wyłączania komputera!)
- ✅ Pamięć wysłanych powiadomień (brak duplikatów)
- ✅ Szczegółowe logi do pliku
- ✅ Łatwa konfiguracja przez plik JSON

## 🚀 Szybki start (2 opcje)

### Opcja 1: GitHub Actions ⭐ REKOMENDOWANA (24/7, darmowe)

1. **Wrzuć kod na GitHub** - bez konieczności uruchamiania komputera!
2. **Skonfiguruj secrets** - token Telegram, ID czatu
3. **Gotowe!** - workflow uruchamiać się będzie automatycznie co 15 minut

📖 **Pełna instrukcja:** [WDRAZANIE_GITHUB_ACTIONS.md](WDRAZANIE_GITHUB_ACTIONS.md)

### Opcja 2: Lokalnie na Twoim komputerze

1. **Zainstaluj Python 3.8+**
   - Pobierz z https://www.python.org/downloads/
   - Zaznacz "Add Python to PATH" podczas instalacji

2. **Zainstaluj biblioteki**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Skonfiguruj aplikację**
   - Skopiuj `config.json.example` → `config.json`
   - Wypełnij swoimi danymi (Telegram bot)
   - Szczegółowa instrukcja w pliku **INSTRUKCJA.md**

4. **Uruchom aplikację**
   - **Łatwy sposób**: Kliknij dwa razy na `start_monitor.bat`
   - **Ręcznie**: `python youtube_monitor.py`

## 📚 Dokumentacja

- **[WDRAZANIE_GITHUB_ACTIONS.md](WDRAZANIE_GITHUB_ACTIONS.md)** - Deploy na GitHub Actions (24/7) ⭐
- **[INSTRUKCJA.md](INSTRUKCJA.md)** - Pełna instrukcja dla lokalnego użycia
- Wszystko co potrzebujesz do instalacji i konfiguracji

## 📋 Wymagania

### Dla GitHub Actions:
- Konto GitHub (darmowe)
- Bot Telegram (stworzony przez @BotFather)
- **Brak potrzeby Python'a - wszystko na GitHub'ie!**

### Dla lokalnego użycia:
- Python 3.8 lub nowszy
- Bot Telegram (stworzony przez @BotFather)
- System operacyjny: Windows, Linux, Mac

## 🎯 Przykładowe użycie

### Konfiguracja (config.json):
```json
{
  "telegram_bot_token": "123456:ABC...",
  "telegram_chat_id": "123456789",
  "channels": [
    {
      "name": "Kanał Tech",
      "channel_id": "UCxxxxxx..."
    }
  ]
}
```

### Powiadomienie Telegram:
```
🎬 Nowy film na YouTube!

📺 Kanał: Kanał Tech
🎥 Tytuł: Najnowsze technologie 2024

🔗 Obejrzyj teraz
```

## ⚙️ Konfiguracja

Program automatycznie:
- Sprawdza kanały co 15 minut (GitHub Actions) lub 1 minutę (lokalnie)
- Wysyła powiadomienia tylko o nowych filmach
- Zapisuje historię w `seen_videos.json`
- Loguje wszystko do `youtube_monitor.log`

## 🔐 Bezpieczeństwo

⚠️ **NIGDY NIE UDOSTĘPNIAJ:**
- YouTube API key (jeśli używasz lokalnie)
- Telegram bot token
- Plik `config.json` (jeśli używasz lokalnie)

✅ **GitHub Actions:** Tokeny przechowywane są w secrets (bezpiecznie!)

Plik `.gitignore` jest już skonfigurowany.
- Maksymalnie ~100 sprawdzeń/dzień lub ~10 kanałów × 10 sprawdzeń

**Rozwiązanie**: Zwiększ interwał sprawdzania lub zmniejsz liczbę kanałów

## 🛠️ Technologie

- **Python 3.8+**
- **google-api-python-client** - YouTube Data API
- **requests** - Telegram API
- **schedule** - Harmonogram zadań
- **NSSM** (opcjonalnie) - Windows Service Manager

## 📝 Licencja

Projekt open-source. Używaj jak chcesz! 🎉

## 🤝 Wsparcie

Problemy? Sprawdź:
1. Plik `youtube_monitor.log` - zawsze zacznij tutaj
2. INSTRUKCJA.md - sekcja "Rozwiązywanie problemów"
3. Upewnij się że config.json jest poprawny

---

**Autor**: YouTube Monitor Bot
**Wersja**: 1.0.0
**Data**: 2024

Miłego monitorowania! 🚀
