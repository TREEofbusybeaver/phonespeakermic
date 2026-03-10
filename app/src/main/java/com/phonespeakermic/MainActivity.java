package com.phonespeakermic;

import android.Manifest;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.AudioTrack;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Context;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {
    private static final int SAMPLE_RATE = 44100;
    private static final int CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO;
    private static final int AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT;
    private static final int PERMISSION_REQUEST_CODE = 200;
    
    private EditText etServerIp;
    private Button btnConnect, btnUsbConnect, btnDisconnect;
    private TextView tvStatus;
    
    private Socket socket;
    private AudioRecord audioRecord;
    private AudioTrack audioTrack;
    private boolean isConnected = false;
    private boolean isRecording = false;
    private Thread sendThread, receiveThread;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        etServerIp = findViewById(R.id.etServerIp);
        btnConnect = findViewById(R.id.btnConnect);
        btnUsbConnect = findViewById(R.id.btnUsbConnect);
        btnDisconnect = findViewById(R.id.btnDisconnect);
        tvStatus = findViewById(R.id.tvStatus);
        
        btnDisconnect.setEnabled(false);
        
        requestPermissions();
        
        btnConnect.setOnClickListener(v -> connectToServer(etServerIp.getText().toString().trim()));
        btnUsbConnect.setOnClickListener(v -> connectToServer("127.0.0.1"));
        btnDisconnect.setOnClickListener(v -> disconnect());
    }
    
    private void requestPermissions() {
        ActivityCompat.requestPermissions(this,
            new String[]{Manifest.permission.RECORD_AUDIO},
            PERMISSION_REQUEST_CODE);
    }
    
    private void connectToServer(String serverIp) {
        if (serverIp.isEmpty()) {
            Toast.makeText(this, "Enter PC IP address", Toast.LENGTH_SHORT).show();
            return;
        }
        
        new Thread(() -> {
            try {
                socket = new Socket(serverIp, 5000);
                socket.setTcpNoDelay(true); // Prevent buffering delay
                isConnected = true;
                
                runOnUiThread(() -> {
                    tvStatus.setText("Connected to PC");
                    btnConnect.setEnabled(false);
                    btnUsbConnect.setEnabled(false);
                    btnDisconnect.setEnabled(true);
                    Toast.makeText(this, "Connected successfully!", Toast.LENGTH_SHORT).show();
                });
                
                // Enable hardware echo cancellation by using VoIP mode
                AudioManager audioManager = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
                audioManager.setMode(AudioManager.MODE_IN_COMMUNICATION);
                audioManager.setSpeakerphoneOn(true); // Force audio to main loud speaker
                
                startAudioStreaming();
                
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    tvStatus.setText("Connection failed: " + e.getMessage());
                    Toast.makeText(this, "Failed to connect", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }
    
    private void startAudioStreaming() {
        // Thread to send mic audio to PC (PC speakers)
        sendThread = new Thread(() -> {
            try {
                int minBufferSize = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_CONFIG, AUDIO_FORMAT);
                int bufferSize = minBufferSize * 4; // Buffer multiplier for smooth capturing
                // VOICE_COMMUNICATION automatically enables hardware Acoustic Echo Cancellation (AEC)
                audioRecord = new AudioRecord(MediaRecorder.AudioSource.VOICE_COMMUNICATION, SAMPLE_RATE, 
                    CHANNEL_CONFIG, AUDIO_FORMAT, bufferSize);
                
                audioRecord.startRecording();
                isRecording = true;
                
                byte[] buffer = new byte[bufferSize];
                OutputStream outputStream = socket.getOutputStream();
                
                while (isRecording && isConnected) {
                    int read = audioRecord.read(buffer, 0, buffer.length);
                    if (read > 0) {
                        outputStream.write(buffer, 0, read);
                        outputStream.flush();
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> tvStatus.setText("Mic streaming error: " + e.getMessage()));
            }
        });
        
        // Thread to receive audio from PC (phone speakers)
        receiveThread = new Thread(() -> {
            try {
                int minBufferSize = AudioTrack.getMinBufferSize(SAMPLE_RATE, 
                    AudioFormat.CHANNEL_OUT_MONO, AUDIO_FORMAT);
                int bufferSize = minBufferSize * 4; // Buffer multiplier to prevent underruns
                
                audioTrack = new AudioTrack(AudioManager.STREAM_MUSIC, SAMPLE_RATE,
                    AudioFormat.CHANNEL_OUT_MONO, AUDIO_FORMAT, bufferSize,
                    AudioTrack.MODE_STREAM);
                
                audioTrack.play();
                
                byte[] buffer = new byte[bufferSize];
                InputStream inputStream = socket.getInputStream();
                
                while (isConnected) {
                    int read = inputStream.read(buffer);
                    if (read > 0) {
                        audioTrack.write(buffer, 0, read);
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> tvStatus.setText("Speaker streaming error: " + e.getMessage()));
            }
        });
        
        sendThread.start();
        receiveThread.start();
    }
    
    private void disconnect() {
        isConnected = false;
        isRecording = false;
        
        try {
            if (audioRecord != null) {
                audioRecord.stop();
                audioRecord.release();
            }
            if (audioTrack != null) {
                audioTrack.stop();
                audioTrack.release();
            }
            if (socket != null) {
                socket.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        AudioManager audioManager = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
        audioManager.setMode(AudioManager.MODE_NORMAL);
        audioManager.setSpeakerphoneOn(false);
        
        runOnUiThread(() -> {
            tvStatus.setText("Disconnected");
            btnConnect.setEnabled(true);
            btnUsbConnect.setEnabled(true);
            btnDisconnect.setEnabled(false);
        });
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        disconnect();
    }
}
