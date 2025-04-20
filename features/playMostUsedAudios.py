import yt_dlp

# Get youtube video urls
def get_audio_stream_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'cookies': './cookies.txt'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict['url']

VIDEO_URLS = {
    "/البقرة": "https://www.youtube.com/watch?v=k9NDKEw5slo",
    "/يوسف": "https://www.youtube.com/watch?v=pENMnDp_XLc",
    "/الكهف": "https://www.youtube.com/watch?v=DrTaNX51xF0",
    "/الملك": "https://www.youtube.com/watch?v=1SOzkCdDrz0",
    "/دعاء": "https://www.youtube.com/watch?v=2hEntR9k5pE",
    "/مستجاب": "https://www.youtube.com/watch?v=MHHkxeOJxQE",
    "/اذكار": "https://www.youtube.com/watch?v=xrZALrmabb0",
}

async def play_most_used_audios(event, chat_id, pytgcalls):
    
    # Get command
    command = event.text.strip()
    
    video_url = VIDEO_URLS.get(command)
    
    # Check if the video exists
    if not video_url:
        await event.reply("❌ لم يتم العثور على الفيديو")
        return

    try:
        youtube_url = get_audio_stream_url(video_url)
    except Exception as e:
        await event.reply("⚠️ خطأ في تحميل الصوت من يوتيوب")
        print(f"yt-dlp error: {e}")
        return

    await event.reply(f"🔄 جاري تشغيل {video_url}...")
    
    try:
        try:
            await pytgcalls.start()
            await pytgcalls.play(chat_id, youtube_url)
        except:
            await pytgcalls.play(chat_id, youtube_url)
            
        await event.reply("🎥 تم تشغيل الفيديو بنجاح")
        
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن الغرفة مفتوحة")
        print(f"Error: {e}")
        return