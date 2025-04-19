import asyncio
import yt_dlp
from pytube import Playlist

# get youtube playlist videos
async def get_playlist_videos(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls
        return video_urls
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []

async def play_quran(event, chat_id, pytgcalls):
    
    playlist_url = "https://www.youtube.com/watch?v=oj1dIsucvaU&list=PLBmYhnNemtrxMMJKZ8q6HZYXKMNlfmq_y"

    # Fetch video URLs from the playlist
    video_urls = await get_playlist_videos(playlist_url)
    
    if not video_urls:
        await event.reply("❌ لم يتم العثور على أي فيديوهات في قائمة التشغيل!")
        return

    await event.reply(f"🔄 جاري تشغيل قائمة التشغيل ({len(video_urls)} فيديوهات)...")

    # Play each video in the playlist
    for video_url in video_urls:
        await event.reply(f"🎶 تشغيل: {video_url}")

        # Extract audio URL using yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'extract_audio': True,
            'no_warnings': True,
            'noplaylist': True,
            'quiet': True
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info.get('url', None)
            
        # playing video
        if audio_url:
            try:
                try:
                    await pytgcalls.start()
                    await pytgcalls.play(chat_id, audio_url)
                except:
                    await pytgcalls.play(chat_id, audio_url)
                    
                await asyncio.sleep(info.get('duration', 5))
            except Exception as e:
                await event.reply(f"⚠️ يرجى التأكد من أن الغرفة مفتوحة")
                print(f"ERROR:{e}")
                return