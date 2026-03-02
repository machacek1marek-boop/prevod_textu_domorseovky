# Import knihoven
import tkinter as tk
from slovnik_prevodnik import slovník_morse
import unicodedata
import time
import threading

# Inicializace pygame zvuku
ZVUK_DOSTUPNY = False
try:
    import pygame
    import numpy as np
    pygame.init()
    pygame.mixer.init()
    ZVUK_DOSTUPNY = True
except:
    pass

# Redukce textu – diakritika a velká písmena
def odstran_diakritiku(text):
    normalizovany_text = unicodedata.normalize('NFD', text)
    text_bez_diakritiky = "".join(
        znak for znak in normalizovany_text
        if unicodedata.category(znak) != 'Mn'
    )
    return text_bez_diakritiky.replace("đ", "d").replace("Đ", "D")

# Vytvoření otočeného slovníku (Morse -> Písmeno)
slovnik_zpet = {hodnota.replace("/", ""): klic for klic, hodnota in slovník_morse.items()}
slovnik_zpet[""] = " "

# Hlavní funkce pro převod morse -> text
def prevod_na_text():
    morse_pole = vstup2_pole.get("1.0", "end-1c").rstrip()
    seznam_kodu = morse_pole.split('/')
    vstup1_pole.delete("1.0", tk.END)
    cast_vysledku = ""
    skip = False

    for i in range(len(seznam_kodu)):
        if skip:
            skip = False
            continue

        kod = seznam_kodu[i].strip()

        if kod == "":
            if i + 1 < len(seznam_kodu) and seznam_kodu[i+1] == "":
                cast_vysledku += "."  # Tečka (///)
                skip = True
            else:
                cast_vysledku += " "  # Mezera (//)
        elif kod in slovnik_zpet:
            cast_vysledku += slovnik_zpet[kod]
        else:
            vstup1_pole.insert(tk.END, cast_vysledku)
            vstup1_pole.insert(tk.END, kod, "red")
            cast_vysledku = ""
    vstup1_pole.insert(tk.END, cast_vysledku.rstrip())

# Hlavní funkce pro převod text -> morse
def prevod_do_morse():
    text1 = vstup1_pole.get("1.0", "end-1c")
    text2 = odstran_diakritiku(text1).upper()

    vstup2_pole.delete("1.0", tk.END)
    for znak in text2:
        if znak in slovník_morse:
            vstup2_pole.insert(tk.END, slovník_morse[znak])
        else:
            vstup2_pole.insert(tk.END, znak + "/", "red")

def mazani_vse():
    vstup2_pole.delete("1.0", tk.END)
    vstup1_pole.delete("1.0", tk.END)

# Vytukávač
cas_stisku = 0
cas_posledni_aktivity = time.time()
pocet_predelu_v_kuse = 3
lomitko_zadanee = False

def pri_stisku(event):
    global cas_stisku, cas_posledni_aktivity, lomitko_zadanee
    cas_posledni_aktivity = time.time()
    lomitko_zadanee = False
    if cas_stisku == 0:
        cas_stisku = time.time()

def pri_uvolneni(event):
    global cas_stisku, cas_posledni_aktivity, pocet_predelu_v_kuse, lomitko_zadanee
    trvani = time.time() - cas_stisku
    pocet_predelu_v_kuse = 0
    lomitko_zadanee = True
    if trvani < 0.3:
        vstup2_pole.insert(tk.END, ".")
    elif 0.3 <= trvani < 1.5:
        vstup2_pole.insert(tk.END, "-")
    else:
        vstup2_pole.insert(tk.END, "///")
        lomitko_zadanee = False

    cas_stisku = 0
    cas_posledni_aktivity = time.time()

def kontrola_pauzy():
    global cas_posledni_aktivity, cas_stisku, pocet_predelu_v_kuse, lomitko_zadanee, mobil
    nyni = time.time()
    pauza = nyni - cas_posledni_aktivity

    if lomitko_zadanee and pauza > 1 and pocet_predelu_v_kuse < 3:
        vstup2_pole.insert(tk.END, "/")
        cas_posledni_aktivity = time.time()
        pocet_predelu_v_kuse += 1

    try:
        if mobil:
            okno.after(100, kontrola_pauzy)
        else:
            p_okno.after(100, kontrola_pauzy)
    except:
        pass

# Zvuk
prehravani_bezi = False
tlacitko_prehrat = None

def generuj_ton(delka_ms, frekvence=800):
    vzorky = int(44100 * delka_ms / 1000)
    t = np.linspace(0, delka_ms / 1000, vzorky, False)
    ton = (np.sin(2 * np.pi * frekvence * t) * 32767).astype(np.int16)
    zvuk = pygame.sndarray.make_sound(ton)
    return zvuk

def prehrat_morse():
    global prehravani_bezi, tlacitko_prehrat

    if prehravani_bezi:
        prehravani_bezi = False
        tlacitko_prehrat.config(text="▶ Přehrát", bg="lightgreen")
        return

    if not ZVUK_DOSTUPNY:
        return

    morse_text = vstup2_pole.get("1.0", "end-1c")
    prehravani_bezi = True
    tlacitko_prehrat.config(text="⏸ Pozastavit", bg="orange")

    TECKA = 100
    POMLCKA = 300
    PAUZA_ZNAK = 100
    PAUZA_PISMENO = 300
    PAUZA_SLOVO = 700

    tecka_zvuk = generuj_ton(TECKA)
    pomlcka_zvuk = generuj_ton(POMLCKA)

    def hraj():
        global prehravani_bezi, tlacitko_prehrat
        i = 0
        while i < len(morse_text):
            if not prehravani_bezi:
                break

            znak = morse_text[i]

            if znak == ".":
                tecka_zvuk.play()
                time.sleep((TECKA + PAUZA_ZNAK) / 1000)
            elif znak == "-":
                pomlcka_zvuk.play()
                time.sleep((POMLCKA + PAUZA_ZNAK) / 1000)
            elif znak == "/":
                if i + 1 < len(morse_text) and morse_text[i + 1] == "/":
                    time.sleep(PAUZA_SLOVO / 1000)
                    i += 1
                else:
                    time.sleep(PAUZA_PISMENO / 1000)
            i += 1

        prehravani_bezi = False
        try:
            tlacitko_prehrat.config(text="▶ Přehrát", bg="lightgreen")
        except:
            pass

    threading.Thread(target=hraj, daemon=True).start()

# Rozhraní mobil
def zozhrani_mobil():
    global vstup1_pole, vstup2_pole, okno, tlacitko_prehrat

    okno = tk.Tk()
    okno.title("Převodník morseovky – mobil")
    okno.geometry("300x560")

    okno.grid_columnconfigure(0, weight=1)

    tlacitko5 = tk.Button(okno, text="změna rozhraní", bg="red", font=("Arial", 8), command=zmnena_rozhrani)
    tlacitko5.grid(row=0, column=0, pady=(10, 2))

    vstup1_label = tk.Label(okno, text="Text:", font=("Arial", 12))
    vstup1_label.grid(row=1, column=0, pady=(10, 2))

    vstup1_pole = tk.Text(okno, height=2, font=("Arial", 11))
    vstup1_pole.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

    frame_tlacitka = tk.Frame(okno)
    frame_tlacitka.grid(row=3, column=0, pady=8)

    tlacitko1 = tk.Button(frame_tlacitka, text="↓Do morse↓", bg="lightblue", font=("Arial", 11), command=prevod_do_morse)
    tlacitko1.pack(side="left", padx=5)

    tlacitko2 = tk.Button(frame_tlacitka, text="smazat", bg="salmon", font=("Arial", 11), command=mazani_vse)
    tlacitko2.pack(side="left", padx=5)

    tlacitko3 = tk.Button(frame_tlacitka, text="↑Na text↑", bg="lightblue", font=("Arial", 11), command=prevod_na_text)
    tlacitko3.pack(side="left", padx=5)

    vstup2_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12))
    vstup2_label.grid(row=4, column=0, pady=(10, 5))

    vstup2_pole = tk.Text(okno, height=5, font=("Courier", 10))
    vstup2_pole.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")

    tlacitko_prehrat = tk.Button(okno, text="▶ Přehrát", bg="lightgreen", font=("Arial", 11), command=prehrat_morse)
    tlacitko_prehrat.grid(row=6, column=0, pady=(5, 2))

    vytukavac_label = tk.Label(okno, text="Tlačítko na zápis morseovky:", font=("Arial", 8))
    vytukavac_label.grid(row=7, column=0, pady=(10, 2))

    vytukavac = tk.Button(okno, text="ťukej kod", bg="green", font=("Arial", 11))
    vytukavac.bind("<ButtonPress-1>", pri_stisku)
    vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
    vytukavac.grid(row=8, column=0, pady=(2, 20))

    vstup1_pole.tag_config("red", foreground="red")
    vstup2_pole.tag_config("red", foreground="red")

    kontrola_pauzy()
    okno.mainloop()

# Rozhraní počítač
def rozhrani_pocitac():
    global vstup1_pole, vstup2_pole, p_okno, tlacitko_prehrat

    p_okno = tk.Tk()
    p_okno.title("Převodník morseovky – počítač")
    p_okno.geometry("700x500")

    p_okno.grid_rowconfigure(5, weight=1)
    p_okno.grid_columnconfigure(0, weight=1)

    tlacitko5 = tk.Button(p_okno, text="změna rozhraní", bg="salmon", font=("Arial", 11), command=zmnena_rozhrani)
    tlacitko5.grid(row=0, column=0, pady=(10, 2))

    vstup1_label = tk.Label(p_okno, text="Text:", font=("Arial", 12))
    vstup1_label.grid(row=1, column=0, pady=(10, 2))

    vstup1_pole = tk.Text(p_okno, height=3, font=("Arial", 11))
    vstup1_pole.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

    frame_tlacitka = tk.Frame(p_okno)
    frame_tlacitka.grid(row=3, column=0, pady=8)

    tlacitko1 = tk.Button(frame_tlacitka, text="↓Převod do morse↓", bg="lightblue", font=("Arial", 11), command=prevod_do_morse)
    tlacitko1.pack(side="left", padx=5)

    tlacitko2 = tk.Button(frame_tlacitka, text="smazat vše", bg="salmon", font=("Arial", 11), command=mazani_vse)
    tlacitko2.pack(side="left", padx=5)

    tlacitko3 = tk.Button(frame_tlacitka, text="↑převod na text↑", bg="lightblue", font=("Arial", 11), command=prevod_na_text)
    tlacitko3.pack(side="left", padx=5)

    vstup2_label = tk.Label(p_okno, text="Morseovka:", font=("Arial", 12))
    vstup2_label.grid(row=4, column=0, pady=(10, 5))

    vstup2_pole = tk.Text(p_okno, height=5, font=("Courier", 10))
    vstup2_pole.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="nsew")

    vytukavac_label = tk.Label(p_okno, text="Tlačítko na zápis morseovky:", font=("Arial", 8))
    vytukavac_label.grid(row=3, column=1, pady=0)

    vytukavac = tk.Button(p_okno, text="ťukej kod", bg="green", font=("Arial", 11))
    vytukavac.bind("<ButtonPress-1>", pri_stisku)
    vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
    vytukavac.grid(row=4, column=1, padx=35, pady=0)

    tlacitko_prehrat = tk.Button(p_okno, text="▶ Přehrát", bg="lightgreen", font=("Arial", 11), command=prehrat_morse)
    tlacitko_prehrat.grid(row=5, column=1, padx=35, pady=0)

    vstup1_pole.tag_config("red", foreground="red")
    vstup2_pole.tag_config("red", foreground="red")

    kontrola_pauzy()
    p_okno.mainloop()

# Přepínání rozhraní
mobil = True

def zmnena_rozhrani():
    global mobil
    if mobil:
        okno.destroy()
        mobil = False
        rozhrani_pocitac()
    else:
        p_okno.destroy()
        mobil = True
        zozhrani_mobil()

# Spuštění
zozhrani_mobil()
