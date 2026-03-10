import socket
import threading
import sys
import os
import subprocess
import pyaudiowpatch as pyaudio
import numpy as np

# Audio configuration
CHUNK = 2048  # Increased chunk size to prevent chopping/popping
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def get_local_ip():
    """Get the local IP address of this PC"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to determine"

def setup_adb_reverse():
    """Try to run adb reverse to automatically support USB mode"""
    print("\nAttempting to set up USB Cable mode (adb reverse)...")
    
    adb_paths = [
        "adb",
        os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe")
    ]
    
    adb_executable = None
    for path in adb_paths:
        try:
            subprocess.run([path, "version"], capture_output=True, check=True)
            adb_executable = path
            break
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            continue
            
    if not adb_executable:
        print("[!] ADB not found. Make sure Android Platform Tools are installed for USB Mode.")
        return
        
    try:
        result = subprocess.run([adb_executable, "reverse", "tcp:5000", "tcp:5000"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] USB Mode ready. You can press 'USB MODE' in the app!")
        else:
            print(f"[!] USB Mode note: ADB not found or device not plugged in ({result.stderr.strip()})")
    except Exception as e:
        print(f"[!] Error with ADB: {e}")

class AudioServer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.server_socket = None
        self.client_socket = None
        self.is_running = False
        
        self.default_loopback = None
        self.cable_output = None
        
        self._find_devices()
        
    def _find_devices(self):
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            
            if not default_speakers["isLoopbackDevice"]:
                for loopback in self.p.get_loopback_device_info_generator():
                    # Exact string matching can be fragile, so we check if the speaker name is in loopback name
                    if default_speakers["name"] in loopback["name"]:
                        self.default_loopback = loopback
                        break
            else:
                self.default_loopback = default_speakers
                
        except Exception as e:
            print(f"Warning discovering loopback devices: {e}")
            
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev["maxOutputChannels"] > 0 and ("CABLE Input" in dev["name"]):
                self.cable_output = dev
                break

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        host = '0.0.0.0'
        port = 5000
        
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        
        print("=" * 60)
        print("Phone Virtual Audio Server (Low-Latency & USB Support)")
        print("=" * 60)
        print(f"Server started on port {port}")
        print(f"Your PC IP address (for Wi-Fi): {get_local_ip()}")
        
        setup_adb_reverse()
        
        print("-" * 60)
        if self.cable_output:
            print("[OK] Found VB-Audio Virtual Cable (CABLE Input).")
        else:
            print("[!] CABLE Input not found. Audio will play on default speakers.")
            
        print("\nWaiting for phone connection...")
        print("=" * 60)
        
        self.client_socket, addr = self.server_socket.accept()
        # Enable TCP No Delay to prevent packet buffering lag
        self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        print(f"\n✓ Phone connected from {addr[0]}")
        
        cable_name = self.cable_output["name"] if self.cable_output else "Default PC Speakers"
        sys_audio_name = self.default_loopback["name"] if self.default_loopback else "Default PC Mic"
        
        print("\nAudio routing active:")
        print(f"  • PC System Audio ({sys_audio_name}) → Phone Speaker")
        print(f"  • Phone Mic → PC {cable_name}")
        print("\nPress Ctrl+C to stop")
        print("=" * 60)
        
        self.is_running = True
        
        receive_thread = threading.Thread(target=self.receive_audio)
        send_thread = threading.Thread(target=self.send_audio)
        
        receive_thread.start()
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()
    
    def receive_audio(self):
        """Receive audio from phone mic and play on PC Virtual Mic (CABLE Input)"""
        output_idx = self.cable_output["index"] if self.cable_output else None
        
        try:
            stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                output_device_index=output_idx,
                frames_per_buffer=CHUNK
            )
            
            while self.is_running:
                try:
                    data = self.client_socket.recv(CHUNK * 2)
                    if not data:
                        break
                    
                    if len(data) > 0:
                        stream.write(data)
                except Exception as e:
                    if self.is_running:
                        print(f"Socket receive error or disconnected.")
                    break
            
            stream.stop_stream()
            stream.close()
        except Exception as e:
            if self.is_running:
                print(f"Error playing received audio: {e}")
        finally:
            self.stop()
    
    def send_audio(self):
        """Capture PC System Audio loopback and send to phone speakers"""
        input_idx = self.default_loopback["index"] if self.default_loopback else None
        
        try:
            channels = int(self.default_loopback["maxInputChannels"]) if self.default_loopback else CHANNELS
            loopback_rate = int(self.default_loopback["defaultSampleRate"]) if self.default_loopback else RATE
            
            stream = self.p.open(
                format=FORMAT,
                channels=channels,
                rate=loopback_rate,
                input=True,
                input_device_index=input_idx,
                frames_per_buffer=CHUNK
            )
            
            while self.is_running:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    
                    # Convert Stereo loopback safely to Mono without clipping or deprecation warnings!
                    if channels == 2:
                        # Extract left channel exactly: [::2]
                        # Each sample is int16. Take every other sample.
                        arr = np.frombuffer(data, dtype=np.int16)
                        data = arr[0::2].tobytes()
                        
                    # Send to phone
                    self.client_socket.sendall(data)
                except Exception as e:
                    if self.is_running:
                        print(f"[Send] Capture warning or disconnected.")
                    break
                    
            stream.stop_stream()
            stream.close()
        except Exception as e:
            if self.is_running:
                print(f"Error capturing system audio: {e}")
        finally:
            self.stop()
    
    def stop(self):
        self.is_running = False
        print("\nShutting down stream...")
        try:
            if self.client_socket:
                self.client_socket.close()
        except: pass
        try:
            if self.server_socket:
                self.server_socket.close()
        except: pass
        try:
            self.p.terminate()
        except: pass

if __name__ == "__main__":
    server = AudioServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop()
    except Exception as e:
        print(f"Error: {e}")
        server.stop()
        sys.exit(1)
