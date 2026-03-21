#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from googleapiclient.discovery import build

# Załaduj konfigurację
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Inicjalizuj YouTube API
youtube = build('youtube', 'v3', developerKey=config['youtube_api_key'])

print("=" * 80)
print("🎬 NAJNOWSZE FILMY NA KANAŁACH")
print("=" * 80)

# Przejdź przez każdy kanał
for channel in config['channels']:
    channel_name = channel['name']
    channel_id = channel['channel_id']
    
    print(f"\n📺 Kanał: {channel_name}")
    print("-" * 80)
    
    try:
        # Pobierz najnowsze 3 filmy
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=3,
            order='date',
            type='video'
        )
        response = request.execute()
        
        if response.get('items'):
            for idx, item in enumerate(response['items'], 1):
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                published = item['snippet']['publishedAt']
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                print(f"\n  {idx}. {title}")
                print(f"     📅 {published[:10]}")
                print(f"     🔗 {url}")
        else:
            print("  ❌ Brak filmów na tym kanale")
            
    except Exception as e:
        print(f"  ❌ Błąd: {str(e)}")

print("\n" + "=" * 80)
