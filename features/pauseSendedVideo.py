async def pause_sended_video(event, chat_id, pytgcalls):
    # Stoping the audio
    try:
        if event.is_group:
            await event.reply("⏸ توقف")
            await pytgcalls.pause(chat_id)
    except Exception as e:
        await event.reply("⚠️ يرجى التأكد من أن البوت في الغرفة ")
        print(f"Error: {e}")
        return