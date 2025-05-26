import streamlit as st
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.io import wavfile
import io

# Fungsi untuk bandstop filter
def bandstop_filter(data, fs, lowcut, highcut, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    filtered = filtfilt(b, a, data)
    return filtered

st.title("🎧 Bandstop Filter untuk Audio (.wav)")

uploaded_file = st.file_uploader("Unggah file WAV", type=["wav"])

if uploaded_file is not None:
    fs, audio = wavfile.read(uploaded_file)

    # Pastikan audio 1D (mono)
    if audio.ndim > 1:
        audio = audio[:, 0]

    st.audio(uploaded_file, format='audio/wav', start_time=0)
    st.write(f"Sampling rate: {fs} Hz | Durasi: {len(audio)/fs:.2f} detik")

    # Input frekuensi bandstop
    f1 = st.slider("Frekuensi rendah (lowcut)", 20, fs//2 - 10, 980)
    f2 = st.slider("Frekuensi tinggi (highcut)", f1+10, fs//2, 1020)
    order = st.slider("Order Filter", 1, 10, 4)

    if st.button("Terapkan Filter"):
        st.write("Memproses audio...")
        filtered_audio = bandstop_filter(audio, fs, f1, f2, order)

        # Normalisasi dan konversi ke int16
        filtered_audio = np.int16(filtered_audio / np.max(np.abs(filtered_audio)) * 32767)

        # Simpan ke buffer
        buffer = io.BytesIO()
        wavfile.write(buffer, fs, filtered_audio)
        st.audio(buffer, format='audio/wav')
        st.download_button("⬇️ Unduh Hasil Filter", data=buffer, file_name="filtered_audio.wav", mime="audio/wav")
