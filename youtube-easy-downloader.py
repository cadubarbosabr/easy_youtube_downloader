import os
import json
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style
from threading import Thread

# Function to save the destination folder in the config.json file
def save_config(destination_folder):
    with open('config.json', 'w') as config_file:
        json.dump({'destination_folder': destination_folder}, config_file)

# Function to load the destination folder from the config.json file
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get('destination_folder', '')
    return ''

# Function to update the progress bar
def update_progress(percent, progress_var, progress_bar):
    progress_var.set(percent)
    progress_bar.update()

# Function to clear cache and reset progress bar
def clear_cache_and_progress():
    # Clear cache by removing the config file
    if os.path.exists('config.json'):
        os.remove('config.json')
    # Reset progress bar
    progress_var.set(0)
    status_label.config(text="Aguardando...")

import os

# Function for downloading MP3
def download_mp3(url, destination_folder, progress_var, progress_bar, status_label):
    ffmpeg_path = 'C:/ffmpeg/ffmpeg-release-essentials/bin'  # Adjust this path to your FFmpeg installation directory

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'progress_hooks': [lambda d: progress_hook(d, progress_var, progress_bar, status_label)]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # After downloading MP3, delete the .webm file
            mp3_file_name = ydl.prepare_filename(ydl.extract_info(url, download=False))
            webm_file = mp3_file_name.replace('.mp3', '.webm')
            if os.path.exists(webm_file):
                os.remove(webm_file)
                print(f"{webm_file} deleted.")
        messagebox.showinfo("Download completo", "O download foi concluído com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Function for downloading WAV
def download_wav(url, destination_folder, progress_var, progress_bar, status_label):
    ffmpeg_path = 'C:/ffmpeg/ffmpeg-release-essentials/bin'  # Adjust this path to your FFmpeg installation directory

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}],
        'progress_hooks': [lambda d: progress_hook(d, progress_var, progress_bar, status_label)]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # After downloading WAV, delete the .webm file
            wav_file_name = ydl.prepare_filename(ydl.extract_info(url, download=False))
            webm_file = wav_file_name.replace('.wav', '.webm')
            if os.path.exists(webm_file):
                os.remove(webm_file)
                print(f"{webm_file} deleted.")
        messagebox.showinfo("Download completo", "O download foi concluído com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Function to start downloading WAV
def start_download_wav():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo.")
        return

    destination_folder = destination_folder_var.get()
    if not destination_folder:
        messagebox.showwarning("Aviso", "Por favor, escolha a pasta de destino.")
        return

    save_config(destination_folder)

    download_thread = Thread(target=download_wav, args=(url, destination_folder, progress_var, progress_bar, status_label))
    download_thread.start()


# Function for downloading MP4
def download_mp4(url, destination_folder, progress_var, progress_bar, status_label):
    ffmpeg_path = 'C:/ffmpeg/ffmpeg-release-essentials/bin'  # Adjust this path to your FFmpeg installation directory

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [lambda d: progress_hook(d, progress_var, progress_bar, status_label)]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Download completo", "O download foi concluído com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Function for progress hook
def progress_hook(d, progress_var, progress_bar, status_label):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded_bytes = d.get('downloaded_bytes', 0)
        percent = int(downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0
        speed = d.get('speed', 0) or 0
        size_in_mib = total_bytes / 1024 / 1024 if total_bytes > 0 else 0
        speed_in_kib = speed / 1024 if speed > 0 else 0
        update_progress(percent, progress_var, progress_bar)
        status_label.config(text=f"Baixando: {percent}% - Velocidade: {speed_in_kib:.2f} KiB/s - Tamanho: {size_in_mib:.2f} MiB")
    elif d['status'] == 'finished':
        update_progress(100, progress_var, progress_bar)
        status_label.config(text="Download concluído")

# Function to start the download in a separate thread
def start_download(format_choice):
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo.")
        return

    destination_folder = destination_folder_var.get()
    if not destination_folder:
        messagebox.showwarning("Aviso", "Por favor, escolha a pasta de destino.")
        return

    save_config(destination_folder)

    if format_choice == 'mp3':
        download_thread = Thread(target=download_mp3, args=(url, destination_folder, progress_var, progress_bar, status_label))
    elif format_choice == 'mp4':
        download_thread = Thread(target=download_mp4, args=(url, destination_folder, progress_var, progress_bar, status_label))
    download_thread.start()

# Function to select the destination folder
def select_destination_folder():
    folder = filedialog.askdirectory()
    if folder:
        destination_folder_var.set(folder)

# Open Twitter
def open_twitter():
    import webbrowser
    webbrowser.open("https://x.com/cadubarbosaBR")

# GUI
root = tk.Tk()
root.title("Easy YouTube Downloader")
root.geometry("500x400")

# Grayscale color scheme
bg_color = "#2e2e2e"
fg_color = "#d3d3d3"
btn_bg_color = "#4f4f4f"
btn_fg_color = "#ffffff"

root.configure(bg=bg_color)

# Centralize widgets on the root
frame = tk.Frame(root, bg=bg_color)
frame.pack(expand=True)

# URL Entry
tk.Label(frame, text="Link do vídeo:", bg=bg_color, fg=fg_color).pack(pady=5)
url_entry = tk.Entry(frame, width=60, bg=btn_bg_color, fg=fg_color)
url_entry.pack(pady=5)

# Destination Folder
tk.Label(frame, text="Pasta de Destino:", bg=bg_color, fg=fg_color).pack(pady=5)
destination_folder_var = tk.StringVar()
destination_folder_var.set(load_config())

destination_frame = tk.Frame(frame, bg=bg_color)
destination_frame.pack(pady=5)
tk.Entry(destination_frame, textvariable=destination_folder_var, width=50, bg=btn_bg_color, fg=fg_color).pack(side=tk.LEFT, padx=5)
tk.Button(destination_frame, text="Selecionar", command=select_destination_folder, bg=btn_bg_color, fg=btn_fg_color).pack(side=tk.LEFT, padx=5)

# Progress Bar
tk.Label(frame, text="Progresso:", bg=bg_color, fg=fg_color).pack(pady=5)
progress_var = tk.IntVar()
progress_bar = Progressbar(frame, orient=tk.HORIZONTAL, length=400, mode='determinate', maximum=100, variable=progress_var)
progress_bar.pack(pady=5)

# Status Label
status_label = tk.Label(frame, text="Aguardando...", bg=bg_color, fg=fg_color)
status_label.pack(pady=5)

# Download Buttons for different formats
button_frame = tk.Frame(frame, bg=bg_color)
button_frame.pack(pady=20)
tk.Button(button_frame, text="Baixar MP3", command=lambda: start_download('mp3'), bg=btn_bg_color, fg=btn_fg_color).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Baixar WAV", command=start_download_wav, bg=btn_bg_color, fg=btn_fg_color).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Baixar MP4", command=lambda: start_download('mp4'), bg=btn_bg_color, fg=btn_fg_color).pack(side=tk.LEFT, padx=5)
# New Download Button
new_download_button = tk.Button(frame, text="Fazer novo download", command=clear_cache_and_progress, bg=btn_bg_color, fg=btn_fg_color)
new_download_button.pack(pady=20)

# Contacts - Hyperlinks
contact_frame = tk.Frame(frame, bg=bg_color)
contact_frame.pack(side=tk.BOTTOM, pady=5, padx=5, anchor='se')

twitter_label = tk.Label(contact_frame, text="Siga-me no X", bg=bg_color, fg=fg_color)
twitter_label.grid(row=0, column=1, padx=5)
twitter_label.bind("<Button-1>", lambda event: open_twitter())
twitter_label.config(cursor="hand2")

root.mainloop()