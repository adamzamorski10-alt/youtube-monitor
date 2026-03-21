# 🚀 Wdrażanie YouTube Monitora na GitHub Actions

## Co to jest?
GitHub Actions to darmowa usługa GitHub'a, która automatycznie uruchamia Twój kod:
- ✅ **24/7** - nonstop, bez wyłączania komputera
- ✅ **Darmowe** - 2000 minut na miesiąc (wystarczy!)
- ✅ **Automatyczne** - uruchamia się co 15 minut
- ✅ **Powiadomienia Telegram** - wysyła o nowych filmach

---

## 📋 Kroki wdrażania

### 1. **Przygotuj GitHub**

Jeśli nie masz konta GitHub:
1. Wejdź na https://github.com/signup
2. Zarejestruj się (to darmowe)

### 2. **Utwórz nowe repozytorium**

1. Wejdź na https://github.com/new
2. Nazwa: `youtube-monitor` (lub inna)
3. Wybierz: **Public** lub **Private** (jak chcesz)
4. **WAŻNE:** NIE dodawaj README, .gitignore ani LICENSE - zaznacz "Add .gitignore: Python"
5. Kliknij "Create repository"

### 3. **Wrzuć kod na GitHub**

W PowerShell, w folderze `Dashboard`:

```powershell
# Inicjalizuj git
git init

# Dodaj zdalne repozytorium (zamień USERNAME i REPO!)
git remote add origin https://github.com/USERNAME/REPO.git

# Dodaj wszystkie pliki
git add .

# Zatwierdź zmiany
git commit -m "YouTube Monitor - GitHub Actions setup"

# Wyślij na GitHub
git branch -M main
git push -u origin main
```

**Jeśli GitHub prosi o autentykację:**
- Użyj Personal Access Token: https://github.com/settings/tokens
- Lub zainstaluj GitHub CLI: https://cli.github.com/

### 4. **Utwórz secrets (zmienne tajne)** ⚠️ WAŻNE!

GitHub musi znać Twoje tokeny Telegram, ale **nie mogą być widoczne publicznie**.

1. Idź na: `https://github.com/USERNAME/REPO/settings/secrets/actions`
2. Kliknij "New repository secret" (zielony przycisk)
3. Utwórz 3 secrets:

#### Secret 1: `TELEGRAM_BOT_TOKEN`
- **Name:** `TELEGRAM_BOT_TOKEN`
- **Value:** Token od @BotFather (np. `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
- Kliknij "Add secret"

#### Secret 2: `TELEGRAM_CHAT_ID`
- **Name:** `TELEGRAM_CHAT_ID`
- **Value:** Twój ID czatu (np. `123456789`)
- Kliknij "Add secret"

#### Secret 3: `YOUTUBE_CHANNELS`
- **Name:** `YOUTUBE_CHANNELS`
- **Value:** JSON z kanałami (całość w jednej linii!)

Przykład:
```json
[{"name":"Kanał 1","channel_id":"UCxxxxxxxxxxxxxx"},{"name":"Kanał 2","channel_id":"UCyyyyyyyyyyyyy"}]
```

⚠️ **PAMIĘTAJ:** To JSON w jednej linii, bez spacji!

---

## 🧪 Testowanie

### Testuj lokalnie najpierw (opcjonalnie):

```powershell
# Uruchom monitor raz (bez pętli)
python youtube_monitor.py --once
```

### Uruchom workflow ręcznie:

1. Wejdź do: `https://github.com/USERNAME/REPO/actions`
2. Kliknij "YouTube Monitor" (po lewej)
3. Kliknij "Run workflow" → "Run workflow" (zielony przycisk)
4. Czekaj ~30 sekund na wykonanie

Powinieneś zobaczyć:
- ✅ Setup Python
- ✅ Install dependencies
- ✅ Run YouTube Monitor
- ✅ Commit and push

Jeśli się powiedzie - **Gratulacje!** 🎉

---

## 📊 Monitoring

### Sprawdzaj uruchomienia:

1. Idź na: `https://github.com/USERNAME/REPO/actions`
2. Widzisz historię wszystkich uruchomień
3. Zielona checkmark ✅ = sukces
4. Czerwony X ❌ = błąd (klinkij aby zobaczyć szczegóły)

### Autorski log: 

Jeśli coś pójdzie nie tak, sprawdź logi w workflow:
- Kliknij najnowsze uruchomienie
- Rozwiń "Run YouTube Monitor"
- Przejrzyj output

---

## 💡 Wskazówki

- **Workflow uruchamia się co 15 minut** - to wystarczy, nie musisz zmieniać
- Jeśli zmienisz kanały - edytuj secret `YOUTUBE_CHANNELS` na GitHub
- **Dane persystują** - `seen_videos.json` jest commitowany do gita (brak pokazywania tych samych filmów)

---

## 🔍 Rozwiązywanie problemów

### "Authentication failed"
**Rozwiązanie:** Sprawdź czy secrets są prawidłowo ustawione:
1. Settings → Secrets → Actions
2. Upewnij się że obydwie wartości są tam
3. Spróbuj ręcznie uruchomić workflow

### "No such file or directory: config.json"
**Rozwiązanie:** To OK! Workflow używa secrets, nie config.json.

### "Telegram API error: 401 Unauthorized"
**Rozwiązanie:** Token Telegram jest zły. Sprawdź w secret `TELEGRAM_BOT_TOKEN`

### "404 Unauthorized"
**Rozwiązanie:** Chat ID jest zły. Sprawdź w secret `TELEGRAM_CHAT_ID`

### Workflow nie uruchamia się automatycznie
**Rozwiązanie:** GitHub może mieć opóźnienie. Czekaj ~30 minut od push'u kodu.

---

## ✨ Co się dzieje za kulisami?

```
GitHub Actions (co 15 minut):
1. ✓ Pobiera najnowszy kod z gita
2. ✓ Instaluje Python i biblioteki
3. ✓ Uruchamia: python youtube_monitor.py --once
4. ✓ Sprawdza kanały YouTube (RSS Feed)
5. ✓ Porównuje z seen_videos.json
6. ✓ Wysyła powiadomienia Telegram o nowych filmach
7. ✓ Aktualizuje seen_videos.json i commituje do gita
8. ✓ Historia dostępna w GitHub Actions → Logs
```

---

**Gotowe! Twój YouTube Monitor teraz pracuje 24/7!** 🚀

