# import os
# # import torch
# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write

# # ✅ նախապես բեռնենք մոդելները՝ ժամանակ խնայելու համար
# preload_models()

# # 📦 հիմնական ֆունկցիան, որը բերում է երգի բառերը, սեռը և ոճը ու գեներացնում WAV ֆայլ
# async def bark_generate(lyrics: str, voice: str = "female", style: str = "pop") -> str:
#     """
#     Գեներացնում է ձայնային ֆայլ՝ ըստ տրված բառերի, սեռի և ոճի։
#     """
#     # 🧠 ձայնային preset ID ըստ սեռի
#     voice_preset_map = {
#         "male": "v2/en_speaker_6",
#         "female": "v2/en_speaker_5"
#     }
    
#     # 🎨 ոճի label ըստ ընտրության
#     style_map = {
#         "ռեփ": "energetic",
#         "ռոք": "aggressive",
#         "պոպ": "cheerful",
#         "ռոմանտիկ": "emotional",
#         "սառը": "calm"
#     }

#     # Ստուգումներ, fallback default-ին
#     voice_preset = voice_preset_map.get(voice, "v2/en_speaker_5")
#     style_label = style_map.get(style.lower(), "neutral")

#     # 🧬 Գեներացնենք աուդիոն
#     audio_array = generate_audio(
#         prompt=lyrics,
#         history_prompt=voice_preset,
#         text_temp=0.7,
#         waveform_temp=0.9
#     )

#     # 📁 Գրում ենք որպես WAV ֆայլ
#     filename = "generated_song.wav"
#     filepath = os.path.join("temp", filename)

#     # Ստեղծում ենք `temp/` թղթապանակը եթե չկա
#     os.makedirs("temp", exist_ok=True)

#     write(filepath, SAMPLE_RATE, audio_array)

#     return filepath
