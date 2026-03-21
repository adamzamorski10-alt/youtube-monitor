import os
import json
import time
import logging
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Set
import feedparser
import requests

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youtube_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class YouTubeMonitor:
    def __init__(self, config_file: str = 'config.json', ignore_cache: bool = False):
        """Inicjalizacja monitora YouTube (RSS Feed)"""
        self.config_file = config_file
        self.config = self.load_config()
        self.seen_videos_file = 'seen_videos.json'
        self.seen_videos = self.load_seen_videos()
        
        # Jeśli flaga ignore_cache, zignoruj cache (wyczyść z pamięci)
        if ignore_cache:
            self.seen_videos = set()
            logger.info("Cache ignorowany - start ze świeżego stanu!")
        
        logger.info("YouTube Monitor (RSS Feed) zainicjalizowany")
    
    def load_config(self) -> Dict:
        """Wczytuje konfigurację z pliku JSON lub zmiennych środowiskowych"""
        try:
            # Najpierw spróbuj zmiennych środowiskowych (GitHub Actions)
            if os.getenv('TELEGRAM_BOT_TOKEN'):
                channels = []
                youtube_channels = os.getenv('YOUTUBE_CHANNELS', '[]')
                try:
                    channels = json.loads(youtube_channels)
                except json.JSONDecodeError:
                    logger.warning(f"Nie można sparsować YOUTUBE_CHANNELS: {youtube_channels}")
                    channels = []
                
                config = {
                    'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
                    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
                    'channels': channels
                }
                logger.info("✓ Konfiguracja załadowana ze zmiennych środowiskowych (GitHub Actions)")
                return config
            
            # W przeciwnym razie załaduj z pliku (lokalny komputer)
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Walidacja konfiguracji
            required_fields = ['telegram_bot_token', 'telegram_chat_id', 'channels']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Brak wymaganego pola w konfiguracji: {field}")
            
            logger.info("✓ Konfiguracja załadowana z pliku")
            return config
        except FileNotFoundError:
            logger.error(f"Nie znaleziono pliku konfiguracji: {self.config_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Błąd parsowania JSON w pliku konfiguracji: {e}")
            raise
    
    def load_seen_videos(self) -> Set[str]:
        """Wczytuje listę już zobaczonych filmów"""
        try:
            if os.path.exists(self.seen_videos_file):
                with open(self.seen_videos_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('video_ids', []))
            return set()
        except Exception as e:
            logger.warning(f"Błąd wczytywania seen_videos.json: {e}")
            return set()
    
    def save_seen_videos(self):
        """Zapisuje listę zobaczonych filmów"""
        try:
            with open(self.seen_videos_file, 'w', encoding='utf-8') as f:
                json.dump({'video_ids': list(self.seen_videos)}, f, indent=2)
        except Exception as e:
            logger.error(f"Błąd zapisywania seen_videos.json: {e}")
    
    def get_channel_latest_videos(self, channel_id: str, channel_name: str, max_results: int = 5) -> List[Dict]:
        """Pobiera najnowsze filmy z kanału używając RSS Feed"""
        try:
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            
            # Pobierz i sparsuj RSS feed
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                logger.warning(f"Problem z parsowaniem RSS dla {channel_name}: {feed.bozo_exception}")
            
            videos = []
            for entry in feed.entries[:max_results]:
                # Wyciągnij video ID z linku
                video_url = entry.link
                video_id = video_url.split('v=')[-1] if 'v=' in video_url else None
                
                if not video_id:
                    continue
                
                video_info = {
                    'video_id': video_id,
                    'title': entry.title,
                    'channel_title': channel_name,
                    'published_at': entry.published,
                    'url': video_url
                }
                videos.append(video_info)
            
            return videos
            
        except Exception as e:
            logger.error(f"Błąd pobierania RSS dla kanału {channel_name}: {e}")
            return []
    
    def send_telegram_message(self, message: str):
        """Wysyła wiadomość na Telegram"""
        url = f"https://api.telegram.org/bot{self.config['telegram_bot_token']}/sendMessage"
        
        payload = {
            'chat_id': self.config['telegram_chat_id'],
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Powiadomienie wysłane na Telegram")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Błąd wysyłania wiadomości Telegram: {e}")
            return False
    
    def is_video_new(self, published_at: str, hours: int = 24) -> bool:
        """Sprawdza czy film jest nowy (opublikowany w ostatnich X godzinach)"""
        try:
            # Parsowanie daty publikacji (format ISO 8601)
            published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            now = datetime.now(published_date.tzinfo)
            
            time_diff = now - published_date
            return time_diff < timedelta(hours=hours)
        except Exception as e:
            logger.warning(f"Błąd parsowania daty: {e}")
            return True  # W razie wątpliwości traktuj jako nowy
    
    def check_for_new_videos(self):
        """Sprawdza wszystkie kanały pod kątem nowych filmów"""
        logger.info("=== Rozpoczynam sprawdzanie kanałów ===")
        
        new_videos_found = []
        
        for channel in self.config['channels']:
            channel_id = channel['channel_id']
            channel_name = channel.get('name', channel_id)
            
            logger.info(f"Sprawdzam kanał: {channel_name}")
            
            videos = self.get_channel_latest_videos(channel_id, channel_name)
            
            for video in videos:
                video_id = video['video_id']
                
                # Sprawdź czy film jest nowy i czy nie był już widziany
                if video_id not in self.seen_videos and self.is_video_new(video['published_at']):
                    new_videos_found.append(video)
                    self.seen_videos.add(video_id)
                    logger.info(f"  ✓ Nowy film znaleziony: {video['title']}")
                    logger.info(f"     🔗 Link: {video['url']}")
        
        # Zapisz zaktualizowaną listę zobaczonych filmów
        if new_videos_found:
            self.save_seen_videos()
            
            # Wyślij powiadomienia
            for video in new_videos_found:
                message = self.format_notification(video)
                self.send_telegram_message(message)
                time.sleep(1)  # Małe opóźnienie między wiadomościami
        else:
            logger.info("Brak nowych filmów")
        
        logger.info(f"=== Sprawdzanie zakończone. Znaleziono {len(new_videos_found)} nowych filmów ===\n")
    
    def format_notification(self, video: Dict) -> str:
        """Formatuje powiadomienie o nowym filmie"""
        message = f"""🎬 <b>Nowy film na YouTube!</b>

📺 <b>Kanał:</b> {video['channel_title']}
🎥 <b>Tytuł:</b> {video['title']}

🔗 <b>Link:</b> {video['url']}

<a href="{video['url']}">👉 Obejrzyj teraz</a>"""
        
        return message
    
    def run_once(self):
        """Uruchamia monitor raz (dla GitHub Actions)"""
        logger.info("🚀 YouTube Monitor (RSS Feed) uruchomiony!")
        logger.info(f"Monitorowanie {len(self.config['channels'])} kanałów")
        
        # Jedno sprawdzenie
        self.check_for_new_videos()
        
    def run(self):
        """Uruchamia monitor w trybie ciągłym"""
        logger.info("🚀 YouTube Monitor (RSS Feed) uruchomiony!")
        logger.info(f"Monitorowanie {len(self.config['channels'])} kanałów")
        logger.info("Sprawdzanie co 1 minutę... (bez limitów API!)")
        
        # Pierwsze sprawdzenie od razu
        self.check_for_new_videos()
        
        # Pętla główna - sprawdzaj co minutę
        while True:
            try:
                time.sleep(60)  # Czekaj minutę
                self.check_for_new_videos()
            except KeyboardInterrupt:
                logger.info("Monitor zatrzymany przez użytkownika")
                break
            except Exception as e:
                logger.error(f"Nieoczekiwany błąd w pętli głównej: {e}")
                time.sleep(60)  # Czekaj minutę przed kolejną próbą


def parser.add_argument('--once', action='store_true', help='Uruchom sprawdzenie raz i wyjdź (dla GitHub Actions)')
    
    args = parser.parse_args()
    
    try:
        monitor = YouTubeMonitor(config_file=args.config, ignore_cache=args.ignore_cache)
        if args.once:
            monitor.run_once()
        else:
        
    args = parser.parse_args()
    
    try:
        monitor = YouTubeMonitor(config_file=args.config, ignore_cache=args.ignore_cache)
        monitor.run()
    except Exception as e:
        logger.critical(f"Krytyczny błąd: {e}")
        raise


if __name__ == "__main__":
    main()
