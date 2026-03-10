# Quick Start Guide - Phone Speaker & Mic

## ⚡ Super Simple Setup (15 minutes)

### Step 1: Setup Your PC (5 minutes)

1. **Install Python**:
   - Go to <https://python.org/downloads>
   - Click the big yellow "Download Python" button
   - Run the installer
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom!
   - Click "Install Now"

2. **Install Audio Library**:
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `pip install pyaudio` and press Enter
   - Wait for it to finish

3. **Find Your Files**:
   - Download/extract the PhoneSpeakerMic folder
   - Open Command Prompt/Terminal
   - Navigate to the folder: `cd path/to/PhoneSpeakerMic`

4. **Start the Server**:
   - Type: `python pc_server.py`
   - You'll see your IP address like: `192.168.1.100`
   - **Write this down!** You'll need it for your phone

### Step 2: Setup Your Phone (10 minutes)

#### Option A: Using Android Studio (Recommended)

1. **Install Android Studio**:
   - Go to <https://developer.android.com/studio>
   - Download and install

2. **Open the Project**:
   - Launch Android Studio
   - Click "Open"
   - Navigate to the PhoneSpeakerMic folder
   - Click OK

3. **Connect Your Phone**:
   - On your phone: Go to Settings → About Phone
   - Tap "Build Number" 7 times (enables Developer Mode)
   - Go to Settings → Developer Options
   - Turn on "USB Debugging"
   - Connect phone to PC with USB cable
   - Allow USB debugging when prompted

4. **Install the App**:
   - In Android Studio, click the green ▶️ (Run) button
   - Wait for the app to install on your phone

#### Option B: Quick Install (If you have the APK)

1. Transfer `app-debug.apk` to your phone
2. Open the file and install
3. Allow "Install from Unknown Sources" if asked

### Step 3: Connect & Use! (2 minutes)

1. **Make sure both devices are on the same WiFi**

2. **On your PC**:
   - Open terminal
   - Run: `python pc_server.py`
   - See the IP address displayed

3. **On your phone**:
   - Open "Phone Speaker Mic" app
   - Enter the IP address from Step 2 (e.g., 192.168.1.100)
   - Tap "Connect to PC"
   - Allow microphone permission

4. **Test it**:
   - Speak into your phone → hear it from PC speakers ✅
   - Speak into PC mic → hear it from phone speakers ✅

---

## 🎯 Daily Use

**Every time you want to use your phone as PC audio:**

1. On PC: `python pc_server.py`
2. On Phone: Open app → Enter IP → Connect
3. Done! 🎉

---

## ❓ Common Questions

**Q: Why can't I connect?**

- Make sure both devices are on the same WiFi
- Check if PC firewall is blocking (try turning it off temporarily)
- Verify the IP address is correct

**Q: No sound?**

- Check volume on both devices
- Make sure you allowed microphone permission
- Try restarting both app and server

**Q: Can I use this over the internet?**

- No, both devices must be on the same local network (same WiFi)

**Q: Is there a wired option?**

- This version is wireless only (WiFi required)
- For wired, you'd need USB tethering (more complex setup)

**Q: Battery drain?**

- Moderate usage - recommend keeping phone plugged in for long sessions

---

## 🔧 Troubleshooting

### "pip install pyaudio" fails?

**Windows:**

```bash
pip install pipwin
pipwin install pyaudio
```

**Mac:**

```bash
brew install portaudio
pip install pyaudio
```

**Linux:**

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

### Firewall blocking connection (Windows)?

1. Open Windows Security
2. Click "Firewall & network protection"
3. Click "Allow an app through firewall"
4. Find Python, check both Private and Public boxes
5. Click OK

### Phone screen keeps turning off?

1. Go to Settings → Display
2. Increase screen timeout
3. Or enable "Stay awake while charging" in Developer Options

---

## 💡 Pro Tips

- Position your phone like a desktop microphone for video calls
- Keep phone plugged in during use
- For best quality, stay close to WiFi router
- Test the connection before important calls

---

**Need more help?** Check the full README.md file!
