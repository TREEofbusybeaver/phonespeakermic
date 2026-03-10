import pyaudiowpatch as pyaudio

p = pyaudio.PyAudio()

try:
    # Get default WASAPI info
    wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    
    # Get default WASAPI speakers
    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
    
    if not default_speakers["isLoopbackDevice"]:
        for loopback in p.get_loopback_device_info_generator():
            if default_speakers["name"] in loopback["name"]:
                default_speakers = loopback
                break
            
    print(f"Default loopback: {default_speakers['name']}")

    print("\nAll WASAPI Loopback Devices:")
    for loopback in p.get_loopback_device_info_generator():
        print(f"ID: {loopback['index']}, Name: {loopback['name']}")

    print("\nAll Output Devices:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev["maxOutputChannels"] > 0:
            print(f"ID: {dev['index']}, Name: {dev['name']}")

finally:
    p.terminate()
