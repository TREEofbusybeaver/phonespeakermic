# Phone Speaker & Mic App

Turn your Android phone into a wireless microphone and speaker for your PC!

## 🎯 What This Does

- **Phone Mic → PC Speakers**: Your phone's microphone sends audio to your PC speakers
- **PC Mic → Phone Speakers**: Your PC's microphone sends audio to your phone speakers
- Works over WiFi (wireless connection)
- Low latency audio streaming
- Simple interface

## 📋 Requirements

### For Android App

- Android phone (Android 5.0 or higher)
- Android Studio to build the app
- Microphone permission

### For PC Server

- Python 3.7 or higher
- Windows, Mac, or Linux
- Phone and PC on the same WiFi network

## 🚀 Setup Instructions

### Part 1: Install PC Server

1. **Install Python** (if not already installed):
   - Download from <https://www.python.org/downloads/>
   - During installation, check "Add Python to PATH"

2. **Install required library**:

```bash
   pip install pyaudio
```

   **If pyaudio fails to install:**

- **Windows**: Download wheel file from <https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio>
- **Mac**: `brew install portaudio`, then `pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`, then `pip install pyaudio`

1. **Run the server**:

```bash
   python pc_server.py
```

1. **Note your PC's IP address** - the server will display it. Example: `192.168.1.100`

### Part 2: Build and Install Android App

1. **Open Android Studio**
   - Download from <https://developer.android.com/studio> if needed

2. **Open the project**:
   - File → Open → Select the `PhoneSpeakerMic` folder

3. **Wait for Gradle sync** to complete

4. **Connect your Android phone**:
   - Enable Developer Options on your phone (tap Build Number 7 times in Settings → About)
   - Enable USB Debugging
   - Connect via USB cable

5. **Build and install**:
   - Click the green "Run" button (▶️) in Android Studio
   - Or use: `./gradlew installDebug`

### Part 3: Connect and Use

1. **Make sure phone and PC are on the same WiFi network**

2. **On PC**: Run `python pc_server.py`
   - Note the IP address displayed

3. **On Phone**:
   - Open the "Phone Speaker Mic" app
   - Enter your PC's IP address (e.g., `192.168.1.100`)
   - Tap "Connect to PC"
   - Grant microphone permission when prompted

4. **You're connected!**
   - Speak into your phone → sound comes out PC speakers
   - Speak into PC mic → sound comes out phone speakers

## 🛠️ Troubleshooting

### Can't connect?

- ✅ Ensure both devices are on the same WiFi network
- ✅ Check firewall settings (allow port 5000)
- ✅ Verify IP address is correct
- ✅ Make sure PC server is running before connecting

### No audio?

- ✅ Check volume on both devices
- ✅ Grant microphone permission on phone
- ✅ Check PC audio settings (correct input/output devices)

### Poor audio quality?

- ✅ Move closer to WiFi router
- ✅ Close other network-intensive applications
- ✅ Ensure stable WiFi connection

### Firewall Issues (Windows)?

If connection fails, allow Python through firewall:

1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Find Python and check both Private and Public
4. Or run: `python -m http.server 5000` to test if port is blocked

## 📱 How to Use After Setup

**Every time you want to use it:**

1. On PC: Open terminal/command prompt and run:

```bash
   python pc_server.py
```

1. On Phone: Open the app and connect using your PC's IP

2. Keep both running - you can now use your phone as PC audio!

## ⚙️ Technical Details

- **Protocol**: TCP socket connection
- **Port**: 5000
- **Audio Format**: PCM 16-bit, 44.1kHz, Mono
- **Latency**: ~100-200ms depending on network

## 🔧 Advanced: Build APK File

To create an installable APK without Android Studio:

```bash
cd PhoneSpeakerMic
./gradlew assembleDebug
```

The APK will be in: `app/build/outputs/apk/debug/app-debug.apk`

Transfer this file to your phone and install it.

## 📝 Notes

- Keep the app running in foreground for best performance
- Battery usage is moderate during active streaming
- Works great for video calls, gaming, or any PC audio needs
- Latency is good for most uses but not ideal for music production

## 🐛 Known Issues

- May disconnect if phone screen locks (keep screen on during use)
- Some Android devices may have audio sync issues
- First connection might take a few seconds

## 💡 Tips

- Use a phone stand to keep your phone positioned as a microphone
- Adjust PC/phone volume for best quality
- Test connection before important calls
- Keep phone plugged in for extended use

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all requirements are met
3. Try restarting both the app and server
4. Check your network connection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Enjoy using your phone as a PC microphone and speaker!** 🎤🔊
