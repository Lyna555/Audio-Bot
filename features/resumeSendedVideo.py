async def resume_sended_videos(event, chat_id, pytgcalls):
    # Resuming the audio
    try:
        if event.is_group:
            await event.reply("▶ أكمل")
            await pytgcalls.resume(chat_id)
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن البوت في الغرفة ")
        print(f"Error: {e}")
        return