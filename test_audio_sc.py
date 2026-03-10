import soundcard as sc

try:
    default_speaker = sc.default_speaker()
    print("Default Speaker:", default_speaker.name)
    
    mic = sc.get_microphone(id=str(default_speaker.id), include_loopback=True)
    print("Loopback Mic accessible:", mic.name)
except Exception as e:
    print("Error getting loopback:", e)

print("\n--- All Microphones ---")
for m in sc.all_microphones(include_loopback=True):
    print(m.name)

print("\n--- All Speakers ---")
for s in sc.all_speakers():
    print(s.name)
