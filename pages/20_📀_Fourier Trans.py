"""
Examples of Fourier Transform (by T.-W. Yoon, Feb. 2023)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
# from pydub import AudioSegment
from scipy.io.wavfile import read
from audio_recorder_streamlit import audio_recorder


def note_sound(freq=391.9954, sample_rate=44100, seconds=2):
    """
    Generate a sine wave

    Args:
        freq (float): frequency of the generated wave. Defaults to 'G'.
        sample_rate (float): sampling frequency. Defaults to 44100.
        seconds (int, optional): duration. Defaults to 2.

    Returns:
        np.array: generated sine wave.
    """

    tspan = np.linspace(0, seconds, seconds * sample_rate, False)
    return np.sin(2 * np.pi * freq * tspan)


def do_fft(time_func, sample_rate=44100, max_freq=1000, time_plot=False, max_time=None):
    """
    Perform the fourier transform of time_func, and plot the results

    Args:
        time_func (np.array): function of time to be transformed.
        sample_rate (float): sampling frequency. Defaults to 44100.
        max_freq (float): maximum frequency to be shown. Defaults to 1000.
        time_plot (bool): time_func plotted. Defaults to False
        max_time (float): maximum time to be shown when time_plot = True
    """

    plt.rcParams.update({'font.size': 6})
    time_len = len(time_func)

    # Perform FFT
    fourier = np.fft.fft(time_func / time_len)
    mag_spectrum = np.abs(fourier)

    # Plot the results
    if time_plot:
        if max_time is None:
            max_time = time_len / sample_rate
        else:
            max_time = min(max_time, time_len / sample_rate)

        display_len = int(max_time * sample_rate)
        tspan = np.linspace(0, max_time, display_len)

        fig, axes = plt.subplots(2, 1)
        axes[0].plot(tspan, time_func[:display_len], color='b')
        axes[0].xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Value')
        ax = axes[1]
    else:
        fig, ax = plt.subplots(1, 1)
        
    # There is no point of having max_freq greater than 0.5*sample_rate
    max_freq = min(max_freq, sample_rate / 2)

    freq_len = int(len(mag_spectrum) * max_freq / sample_rate)
    frequency = np.linspace(0, max_freq, freq_len)

    ax.plot(frequency, mag_spectrum[:freq_len], color='#ff7f00')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude')

    st.pyplot(fig)


# def get_audio_data(file):
    # """
    # Return audio as an np.array, and the sampling rate
    # """

    # file_ext = file.name.split(".")[-1]

    # try:
    #    if file_ext.lower() == "wav":
    #        sound = AudioSegment.from_wav(file)
    #    elif file_ext.lower() in ["mp3", "ogg", "aac", "wma", "m4a", "flac"]:
    #        sound = AudioSegment.from_file(file, format=file_ext)
    #    else:
    #        st.error(f"Unsupported file format: {file_ext}", icon="🚨")
    # except Exception as e:
    #    st.error(f"An error occurred: {e}", icon="🚨")
    #    return None, None
    
    # sound = sound.set_channels(1)
    # return np.array(sound.get_array_of_samples()), sound.frame_rate


def show_results(signal, sr):
    """
    Show the results of fourier transforms

    Args:
        signal (np.array): audio signal of a single channel
        sr (float): sampling rate
    """

    left, _, right = st.columns([5, 1, 5])

    max_value_time, max_value_freq = len(signal) / sr, 5000.
    max_time = left.slider(
        label="$\\hspace{0.25em}\\texttt{Time range}$",
        min_value=0.0,
        max_value=max_value_time,
        value=max_value_time,
        step=0.001,
        label_visibility="visible",
    )
    max_freq = right.slider(
        label="$\\hspace{0.25em}\\texttt{Frequency range}$",
        min_value=0.0,
        max_value=max_value_freq,
        value=max_value_freq,
        step=1.0,
        label_visibility="visible",
    )

    do_fft(signal, sample_rate=sr, max_freq=max_freq, time_plot=True, max_time=max_time)


def fourier_transform():
    """
    This app inputs sounds and performs their fourier transforms.
    """

    st.write("## 📀 Fourier Transform of Sound Waves")

    st.write("")
    st.write(
        """
        Fourier transformation establishes a one-to-one correspondence
        between a function of time (or space) and a function of frequency,
        which contain the same information. Fourier transforms are obtained
        by decomposing functions of time (or space) into frequency
        components. Here are some simple examples that show the frequency
        components of sound waves using Fourier transformation.
        """
    )
    st.write("")

    # Frequencies of notes
    note_freq = {
        "C": 261.6256, "D": 293.6648, "E": 329.6276, "F": 349.2282,
        "G": 391.9954, "A": 440.0000, "B": 493.8833
    }

    # Choose the note to consider
    st.write("##### Select a note")
    note = st.radio(
        label="$\\hspace{0.12em}\\texttt{Select a note}$",
        options=('C', 'D', 'E', 'F', 'G', 'A', 'B', 'C+E+G', 'C+F+A'),
        horizontal=True,
        index=4,
        label_visibility="collapsed"
    )

    # Compose a function with the selected note
    sample_rate = 44_100  # 44100 samples per second

    if len(note) == 1:
        time_func = note_sound(freq=note_freq[note], seconds=2)
    else:
        time_func = note_sound(freq=note_freq[note[0]], seconds=2) \
                  + note_sound(freq=note_freq[note[2]], seconds=2) \
                  + note_sound(freq=note_freq[note[4]], seconds=2)

    # Play the sound
    st.audio(time_func[:len(time_func)//2], sample_rate=sample_rate)

    # Do the fourier transform
    do_fft(time_func, time_plot=True, max_time=0.02)

    st.write("---")
    st.write("##### Select a sound wave")
    sound_source = st.radio(
        label="$\\hspace{0.12em}\\texttt{Select a sound wave}$",
        options=("Sample file", "Your file", "Your voice"),
        # horizontal=True,
        label_visibility="collapsed"
    )

    if sound_source == "Sample file":
        sr, signal = read("files/example.wav")
        signal = signal.mean(axis=1)
        st.audio(signal, sample_rate=sr)
    else:
        if sound_source == "Your file":
            audio_file = st.file_uploader(
                label="$\\hspace{0.12em}\\texttt{Upload an audio file}$",
                # type=["wav", "mp3", "ogg", "aac", "wma", "m4a", "flac"],
                type=["wav"],
                label_visibility="collapsed"
            )
            if audio_file is None:
                return None
        else:
            audio_bytes = audio_recorder(
                pause_threshold=3.0,
                # sample_rate=sr,
                text="Click to record",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                # icon_name="user",
                icon_size="2x",
            )
            if audio_bytes is None:
                return None
            else:
                audio_file = "files/recorded_audio.wav"
                with open(audio_file, "wb") as recorded_file:
                    recorded_file.write(audio_bytes)
        try:
            # signal, sr = get_audio_data(audio_file)
            sr, signal = read(audio_file)
        except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")
            return None

        if len(signal.shape) == 2:
            signal = signal.mean(axis=1)
        st.audio(signal, sample_rate=sr)

    show_results(signal, sr)


if __name__ == "__main__":
    fourier_transform()
