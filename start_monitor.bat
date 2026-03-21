@echo off
chcp 65001 >nul
echo ========================================
echo   YouTube Monitor - Monitor kanałów
echo ========================================
echo.

:: Sprawdź czy config.json istnieje
if not exist "config.json" (
    echo [BŁĄD] Nie znaleziono pliku config.json
    echo.
    echo Skopiuj plik config.json.example i zmień nazwę na config.json
    echo Następnie wypełnij go swoimi danymi.
    echo.
    pause
    exit /b 1
)

:: Sprawdź czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo [BŁĄD] Python nie jest zainstalowany lub nie jest w PATH
    echo.
    echo Pobierz Python z: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python zainstalowany
echo.

:: Sprawdź czy biblioteki są zainstalowane
python -c "import googleapiclient" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instaluję wymagane biblioteki...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [BŁĄD] Nie udało się zainstalować bibliotek
        pause
        exit /b 1
    )
    echo.
    echo [OK] Biblioteki zainstalowane
    echo.
)

echo Uruchamiam YouTube Monitor...
echo.
echo Aby zatrzymać program, naciśnij Ctrl+C
echo ========================================
echo.

python youtube_monitor.py

pause
