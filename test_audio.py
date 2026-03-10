import pyaudio

p = pyaudio.PyAudio()

wasapi_api_index = None
for i in range(p.get_host_api_count()):
    info = p.get_host_api_info_by_index(i)
    if "WASAPI" in info["name"]:
        wasapi_api_index = info["index"]
        break

print("WASAPI API index:", wasapi_api_index)

print("\n--- Loopback Devices (WASAPI) ---")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info["hostApi"] == wasapi_api_index:
        try:
            if info.get("isLoopbackDevice", False) or info.get("maxInputChannels", 0) > 0:
                print(f"Index {i}: {info['name']} (Channels: {info['maxInputChannels']}, Loopback: {info.get('isLoopbackDevice', False)})")
        except KeyError:
            pass

print("\n--- Speakers (MME/DirectSound) ---")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info["maxOutputChannels"] > 0:
        if "CABLE Input" in info["name"]:
            print(f"Found VB-Audio Cable: Index {i} - {info['name']}")

p.terminate()
