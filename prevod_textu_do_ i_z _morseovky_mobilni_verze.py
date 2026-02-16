#import slovníku
import os
    # Získá cestu ke složce, kde běží tento skript
current_dir = os.path.dirname(os.path.abspath(__file__))
    # Spojí cestu se jménem tvého souboru
file_path = os.path.join(current_dir, 'slovnik_prevodnik.py')
with open(file_path, 'r') as f:
    print(f.read())

# Import knihoven
import tkinter as tk
from slovnik_prevodnik import slovník_morse
import unicodedata
import time

#redukce textu diakritika a velká
def odstran_diakritiku(text):
    normalizovany_text = unicodedata.normalize('NFD', text)
    text_bez_diakritiky = "".join(
        znak for znak in normalizovany_text
        if unicodedata.category(znak) != 'Mn'
    )

    return text_bez_diakritiky.replace("đ", "d").replace("Đ", "D")

# Vytvoření otočeného slovníku (Morse -> Písmeno)
# Musíme odstranit lomítka z hodnot v původním slovníku pro správné porovnání
slovnik_zpet = {hodnota.replace("/", ""): klic for klic, hodnota in slovník_morse.items()}# Ručně přidáme mezeru, která je v původním slovníku definovaná jako "/"
slovnik_zpet[""] = " "

# Hlavní funkce pro převod
def prevod_na_text():
    # Načtení a vyčištění (používáme end-1c dle tvých souborů)
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
                cast_vysledku += "." # Tečka (///)
                skip = True 
            else:
                cast_vysledku += " " # Mezera (//)
        elif kod in slovnik_zpet:
            # Vložíme znak ze slovníku
            cast_vysledku += slovnik_zpet[kod]
        else:
            # Tady vložíme text s barvou bez nutnosti složité proměnné
            vstup1_pole.insert(tk.END, cast_vysledku)
            vstup1_pole.insert(tk.END, kod, "red")
            cast_vysledku = ""
    vstup1_pole.insert(tk.END, cast_vysledku.rstrip())

# Hlavní funkce pro převod
def prevod_do_morse():
    text1 = vstup1_pole.get("1.0", "end-1c")
    text2 = odstran_diakritiku(text1).upper()
    
    vstup2_pole.delete("1.0", tk.END)  # vymaže obsah
    for znak in text2:
        if znak in slovník_morse:
            vstup2_pole.insert(tk.END, slovník_morse[znak])
        else:
            vstup2_pole.insert(tk.END, znak, "red","/")

def mazani_vse():
    vstup2_pole.delete("1.0", tk.END)
    vstup1_pole.delete("1.0", tk.END)

def pri_stisku(event):
    global cas_stisku, pauza, cas_posledni_aktivity, lomitko_zadanee
    cas_posledni_aktivity = time.time()
    lomitko_zadanee = False
    if cas_stisku == 0: # Zabrání opakování při držení klávesy
        cas_stisku = time.time()

def pri_uvolneni(event):
    global cas_stisku, cas_posledni_aktivity, pismeno_ukonceno, pocet_predelu_v_kuse, lomitko_zadanee
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

    ##grafika a tlacitka
# Vytvoření hlavního okna
okno = tk.Tk()
okno.title("Převodník do nebo z morseovky")
okno.geometry("800x600")

# Konfigurace gridu pro responzivitu
okno.grid_rowconfigure(0, weight=0)  # Label
okno.grid_rowconfigure(1, weight=0)  # Textové pole
okno.grid_rowconfigure(2, weight=0)  # Tlačítka
okno.grid_rowconfigure(3, weight=0)  # Label
okno.grid_rowconfigure(4, weight=1)  # Textové pole (roztáhne se)
okno.grid_rowconfigure(5, weight=0)  # Lable
okno.grid_rowconfigure(6, weight=0)  # Vytukávač

okno.grid_columnconfigure(0, weight=1)  # Sloupec se roztáhne

# Popisek pro vstup
vstup1_label = tk.Label(okno, text="Text:", font=("Arial", 12))
vstup1_label.grid(row=0, column=0, pady=(10, 2))

# Vstupní textové pole - sticky="nsew" = roztáhne se na všechny strany
vstup1_pole = tk.Text(okno, height=2, font=("Arial", 11))
vstup1_pole.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

# Frame pro tlačítka (aby byla vedle sebe)
frame_tlacitka = tk.Frame(okno)
frame_tlacitka.grid(row=2, column=0, pady=8)

# Tlačítko pro převod do morse 
tlacitko1 = tk.Button(frame_tlacitka, text="↓ Převést do morse ↓", bg="lightblue", font=("Arial", 11), command=prevod_do_morse)
tlacitko1.pack(side="left", padx=5)

# Tlačítko pro smazání všeho
tlacitko2 = tk.Button(frame_tlacitka, text="smazat vše", bg="salmon", font=("Arial", 11), command=mazani_vse)
tlacitko2.pack(side="left", padx=5)
 
# Tlačítko pro převod nba text
tlacitko3 = tk.Button(frame_tlacitka, text="↑ Převést na text ↑",  bg="lightblue", font=("Arial", 11), command=prevod_na_text)
tlacitko3.pack(side="left", padx=5)


# Popisek pro výstup
vstup2_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12))
vstup2_label.grid(row=3, column=0, pady=(10, 5))

# Výstupní morse pole
vstup2_pole = tk.Text(okno, height=5, font=("Courier", 10))
vstup2_pole.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")

# Popisek pro vytukavač
vytukavac_label = tk.Label(okno, text="Tlačítko na zapis morse:", font=("Arial", 8))
vytukavac_label.grid(row=5, column=0, pady=(20, 5))

# Tlačítko pro zapis morse (vytukavac)
vytukavac = tk.Button(okno, text="ťukej kod", bg="green", font=("Arial", 11))
vytukavac.bind("<ButtonPress-1>", pri_stisku)
vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
vytukavac.grid(row=6, column=0, pady=(5, 50))

#tagy barev
vstup1_pole.tag_config("red", foreground="red")
vstup2_pole.tag_config("red", foreground="red")


# Proměnné pro sledování času
cas_stisku = 0
cas_posledni_aktivity = time.time()  
pocet_predelu_v_kuse = 3
lomitko_zadanee = False

def kontrola_pauzy():
    global cas_posledni_aktivity, cas_stisku, pocet_predelu_v_kuse, pauza, lomitko_zadanee
    nyni = time.time()
    pauza = nyni - cas_posledni_aktivity
    
    # Pokud uživatel nic nedělá déle než 1. sekundy, ukonči písmeno
    if lomitko_zadanee and  pauza > 1 and pocet_predelu_v_kuse <3:
        vstup2_pole.insert(tk.END, "/")      
        cas_posledni_aktivity = time.time() 
        pocet_predelu_v_kuse += 1
    # Opakuj kontrolu každých 100ms
    okno.after(100, kontrola_pauzy)

# Spuštění automatické kontroly pauzy
kontrola_pauzy()

# Spuštění programu
okno.mainloop()