import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random
#inserire il tuo percorso file 
spotify_cleaned = pd.read_csv("/Users/daviderivano/Desktop/Spotify-2000.csv")

def recommend_songs_by_preferences():
    mood_choice = mood_var.get()
    energy_choice = energy_var.get()

    valence_range = (3, 99)
    if mood_choice == 1:
        valence_range = (3, 35)
    elif mood_choice == 2:
        valence_range = (36, 66)
    elif mood_choice == 3:
        valence_range = (67, 99)

    energy_range = (3, 100)
    if energy_choice == 1:
        energy_range = (3, 35)
    elif energy_choice == 2:
        energy_range = (36, 66)
    elif energy_choice == 3:
        energy_range = (67, 100)

    filtered_songs = spotify_cleaned[
        (spotify_cleaned["Valence"] >= valence_range[0]) & (spotify_cleaned["Valence"] <= valence_range[1]) &
        (spotify_cleaned["Energy"] >= energy_range[0]) & (spotify_cleaned["Energy"] <= energy_range[1])
    ]

    if filtered_songs.empty:
        messagebox.showinfo("Risultati", "Nessuna canzone corrisponde ai criteri selezionati.")
    else:
        
        shuffled_songs = filtered_songs.sample(frac=1, random_state=random.randint(1, 1000))
        recommendations = shuffled_songs[["Title", "Artist", "Valence", "Energy"]].head(4)

        result_text = "\n".join(
            [f"🎵 {row['Title']} by {row['Artist']}\n   ❤️ Valence: {row['Valence']} | ⚡ Energy: {row['Energy']}" 
             for _, row in recommendations.iterrows()]
        )

        result_display.config(state="normal")
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, result_text)
        result_display.config(state="disabled")

root = tk.Tk()
root.title("Sistema di Raccomandazione Canzoni")
root.geometry("800x700")
root.config(bg="#ecf0f1")

title_label = tk.Label(
    root,
    text="🎶 Scopri Nuove Canzoni 🎶",
    font=("Helvetica", 24, "bold"),
    bg="#ecf0f1",
    fg="#2c3e50"
)
title_label.pack(pady=20)

mood_frame = tk.LabelFrame(root, text="Come ti senti?", bg="#dfe6e9", fg="#2d3436", font=("Helvetica", 14, "bold"))
mood_frame.pack(fill="x", padx=20, pady=10)

mood_var = tk.IntVar()
mood_var.set(2) 

moods = [("Malinconico", "#636e72"), ("Sereno", "#74b9ff"), ("Euforico", "#00cec9")]
for i, (mood, color) in enumerate(moods, start=1):
    tk.Radiobutton(
        mood_frame,
        text=mood,
        variable=mood_var,
        value=i,
        font=("Helvetica", 12),
        bg="#dfe6e9",
        fg=color
    ).pack(anchor="w", padx=10, pady=5)

energy_frame = tk.LabelFrame(root, text="Atmosfera desiderata", bg="#ffeaa7", fg="#2d3436", font=("Helvetica", 14, "bold"))
energy_frame.pack(fill="x", padx=20, pady=10)

energy_var = tk.IntVar()
energy_var.set(2) 

energy_levels = [("Tranquilla", "#b2bec3"), ("Equilibrata", "#fdcb6e"), ("Intensa", "#d63031")]
for i, (level, color) in enumerate(energy_levels, start=1):
    tk.Radiobutton(
        energy_frame,
        text=level,
        variable=energy_var,
        value=i,
        font=("Helvetica", 12),
        bg="#ffeaa7",
        fg=color
    ).pack(anchor="w", padx=10, pady=5)

recommend_button = tk.Button(
    root,
    text="🔍 Suggerisci Canzoni",
    command=recommend_songs_by_preferences,
    font=("Helvetica", 14, "bold"),
    bg="#6c5ce7",
    fg="white",
    relief="flat"
)
recommend_button.pack(pady=20)

result_frame = tk.LabelFrame(root, text="Risultati", bg="#f5f6fa", fg="#2d3436", font=("Helvetica", 14, "bold"))
result_frame.pack(fill="both", padx=20, pady=10, expand=True)

result_display = scrolledtext.ScrolledText(
    result_frame,
    height=10,
    font=("Helvetica", 12),
    wrap="word",
    bg="#ffffff",
    fg="#2d3436",
    relief="flat",
    state="disabled"
)
result_display.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
