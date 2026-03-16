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
    
  
#promněnné
mobil = True
max_doba_tecky = 0.3
max_doba_carky = 1.5
cas_stisku = 0
def pri_stisku(event):
    global cas_stisku, cas_posledni_aktivity, lomitko_zadanee
    cas_posledni_aktivity = time.time()
    lomitko_zadanee = False
    if cas_stisku == 0: # Zabrání opakování při držení klávesy
        cas_stisku = time.time()

def pri_uvolneni(event):
    global cas_stisku, cas_posledni_aktivity, pismeno_ukonceno, pocet_predelu_v_kuse, lomitko_zadanee
    trvani = time.time() - cas_stisku
    pocet_predelu_v_kuse = 0
    lomitko_zadanee = True 
    if trvani < max_doba_tecky:
        vstup2_pole.insert(tk.END, ".")
    elif max_doba_tecky <= trvani < max_doba_carky:
        vstup2_pole.insert(tk.END, "-")
    else:
        vstup2_pole.insert(tk.END, "///")
        lomitko_zadanee = False  
    
    cas_stisku = 0
    cas_posledni_aktivity = time.time()
    
#kopirováni
def kopirovat_text():
    obsah = vstup1_pole.get("1.0", "end-1c")
    okno_aktivni = okno if mobil else p_okno
    okno_aktivni.clipboard_clear()
    okno_aktivni.clipboard_append(obsah)

def kopirovat_morse():
    obsah = vstup2_pole.get("1.0", "end-1c")
    okno_aktivni = okno if mobil else p_okno
    okno_aktivni.clipboard_clear()
    okno_aktivni.clipboard_append(obsah)
    
def zozhrani_mobil():
    global vstup1_pole, vstup2_pole, okno, tlacitko_rezim, vstup1_label, vstup2_label, frame_tlacitka, vytukavac_label
    ##grafika a tlacitka
    # Vytvoření hlavního okna
    okno = tk.Tk()
    okno.title("Převodník do nebo z morseovky mobil")
    okno.geometry("300x500")
    
    # Konfigurace gridu pro responzivitu
    okno.grid_rowconfigure(0, weight=0)  # zmnena rozhraní
    okno.grid_rowconfigure(1, weight=0)  # Label
    okno.grid_rowconfigure(2, weight=0)  # Textové pole
    okno.grid_rowconfigure(3, weight=0)  # Tlačítka
    okno.grid_rowconfigure(4, weight=0)  # Label
    okno.grid_rowconfigure(5, weight=0)  # Textové pole (roztáhne se)
    
    okno.grid_columnconfigure(0, weight=1)  # Sloupec se roztáhne
    
    # Tlačítko pro změnu rozhraní
    tlacitko5 = tk.Button(okno, text="změna rozhraní", bg="red", font=("Arial", 8), command=zmnena_rozhrani)
    tlacitko5.grid(row=0, column=0, pady=(10, 2))
    
    #prepnou rezim buton
    tlacitko_rezim = tk.Button(okno, text="🌙", bg="black", fg="white", font=("Arial", 8), command=prepnout_rezim)
    tlacitko_rezim.grid(row=0, column=1, pady=(10, 2))
    
    # Popisek pro vstup
    vstup1_label = tk.Label(okno, text="Text:", font=("Arial", 12))
    vstup1_label.grid(row=1, column=0, pady=(10, 2))
    
    # Vstupní textové pole - sticky="nsew" = roztáhne se na všechny strany
    vstup1_pole = tk.Text(okno, height=2, font=("Arial", 11))
    vstup1_pole.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
    
    #kopirovací tlac 1
    tlacitko_kop1 = tk.Button(okno, text="kop.", bg="lightyellow", font=("Arial", 4), command=kopirovat_text)
    tlacitko_kop1.grid(row=2, column=1, pady=(0, 40))
    
    # Frame pro tlačítka (aby byla vedle sebe)
    frame_tlacitka = tk.Frame(okno)
    frame_tlacitka.grid(row=3, column=0, pady=8)
    
    # Tlačítko pro převod do morse 
    tlacitko1 = tk.Button(frame_tlacitka, text="↓Do morse↓", bg="lightblue", font=("Arial", 10), command=prevod_do_morse)
    tlacitko1.pack(side="left", padx=5)
    
    # Tlačítko pro smazání všeho
    tlacitko2 = tk.Button(frame_tlacitka, text="smazat", bg="salmon", font=("Arial", 10), command=mazani_vse)
    tlacitko2.pack(side="left", padx=5)
     
    # Tlačítko pro převod nba text
    tlacitko3 = tk.Button(frame_tlacitka, text="↑Na text↑",  bg="lightblue", font=("Arial", 10), command=prevod_na_text)
    tlacitko3.pack(side="left", padx=5)
     
    # Popisek pro výstup
    vstup2_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12))
    vstup2_label.grid(row=4, column=0, pady=(10, 5))
    
    # Výstupní morse pole
    vstup2_pole = tk.Text(okno, height=5, font=("Courier", 10))
    vstup2_pole.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")
    #kopirovaci tlac 2
    tlacitko_kop2 = tk.Button(okno, text="kop.", bg="lightyellow", font=("Arial", 4), command=kopirovat_morse)
    tlacitko_kop2.grid(row=5, column=1, pady=(0, 70))
    
    # Popisek pro vytukavač
    vytukavac_label = tk.Label(okno, text="Tlačítko na zápis morseovky:", font=("Arial", 8))
    vytukavac_label.grid(row=6, column=0, pady=(100, 2))
    
    # Tlačítko pro zapis morse (vytukavac)
    vytukavac = tk.Button(okno, text="ťukej kod", bg="green", font=("Arial", 11))
    vytukavac.bind("<ButtonPress-1>", pri_stisku)
    vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
    vytukavac.grid(row=7, column=0, pady=(2, 20))
    
    
    #tagy barev
    vstup1_pole.tag_config("red", foreground="red")
    vstup2_pole.tag_config("red", foreground="red")
    
    #spustění oddělovače
    kontrola_pauzy()
      
    # Spuštění programu
    okno.mainloop()

def rozhrani_pocitac():
    global vstup1_pole, vstup2_pole, p_okno, tlacitko_rezim, vstup1_label, vstup2_label, frame_tlacitka, vytukavac_label
    ##grafika a tlacitka
    # Vytvoření hlavního okna
    p_okno = tk.Tk()
    p_okno.title("Převodník do nebo z morseovky pocitac")
    p_okno.geometry("700x500")
    
    # Konfigurace gridu pro responzivitu
    p_okno.grid_rowconfigure(0, weight=0)  # zmnena rozhraní
    p_okno.grid_rowconfigure(1, weight=0)  # Label
    p_okno.grid_rowconfigure(2, weight=0)  # Textové pole
    p_okno.grid_rowconfigure(3, weight=0)  # Tlačítka
    p_okno.grid_rowconfigure(4, weight=0)  # Label
    p_okno.grid_rowconfigure(5, weight=1)  # Textové pole (roztáhne se)

    p_okno.grid_columnconfigure(0, weight=1)  # Sloupec se roztáhne
    
    # Tlačítko pro změnu rozhraní
    tlacitko5 = tk.Button(p_okno, text="změna rozhraní", bg="salmon", font=("Arial", 11), command=zmnena_rozhrani)
    tlacitko5.grid(row=0, column=0, pady=(10, 2))
    
    #prepnou rezim buton
    tlacitko_rezim = tk.Button(p_okno, text="🌙", bg="black", fg="white", font=("Arial", 8), command=prepnout_rezim)
    tlacitko_rezim.grid(row=0, column=1, pady=(10, 2))
    
    # Popisek pro vstup
    vstup1_label = tk.Label(p_okno, text="Text:", font=("Arial", 12))
    vstup1_label.grid(row=1, column=0, pady=(10, 2))
    
    # Vstupní textové pole - sticky="nsew" = roztáhne se na všechny strany
    vstup1_pole = tk.Text(p_okno, height=3, font=("Arial", 11))
    vstup1_pole.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
    
    #kopirovaci tlac 1
    tlacitko_kop1 = tk.Button(p_okno, text="📋", bg="lightyellow", font=("Arial", 8), command=kopirovat_text)
    tlacitko_kop1.grid(row=2, column=1,padx=(0, 150), pady=(0, 55))
     
    # Frame pro tlačítka (aby byla vedle sebe)
    frame_tlacitka = tk.Frame(p_okno)
    frame_tlacitka.grid(row=3, column=0, pady=8)
    
    # Tlačítko pro převod do morse 
    tlacitko1 = tk.Button(frame_tlacitka, text="↓Převod do morse↓", bg="lightblue", font=("Arial", 11), command=prevod_do_morse)
    tlacitko1.pack(side="left", padx=5)
    
    # Tlačítko pro smazání všeho
    tlacitko2 = tk.Button(frame_tlacitka, text="smazat vše", bg="salmon", font=("Arial", 11), command=mazani_vse)
    tlacitko2.pack(side="left", padx=5)
     
    # Tlačítko pro převod nba text
    tlacitko3 = tk.Button(frame_tlacitka, text="↑převod na text↑",  bg="lightblue", font=("Arial", 11), command=prevod_na_text)
    tlacitko3.pack(side="left", padx=5)
    # Popisek pro výstup
    vstup2_label = tk.Label(p_okno, text="Morseovka:", font=("Arial", 12))
    vstup2_label.grid(row=4, column=0, pady=(10, 5))
    
    # Výstupní morse pole
    vstup2_pole = tk.Text(p_okno, height=5, font=("Courier", 10))
    vstup2_pole.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="nsew")
    #kopirovaci tlac 2
    tlacitko_kop2 = tk.Button(p_okno, text="📋", bg="lightyellow", font=("Arial", 8), command=kopirovat_morse)
    tlacitko_kop2.grid(row=5, column=1, padx=(0, 150), pady=(0, 220))
    

    # Popisek pro vytukavač
    vytukavac_label = tk.Label(p_okno, text="Tlačítko na zápis morseovky:", font=("Arial", 9))
    vytukavac_label.grid(row=3, column=1, pady=0)

    # Tlačítko pro zapis morse (vytukavac)
    vytukavac = tk.Button(p_okno, text="ťukej kod", bg="green", font=("Arial", 11))
    vytukavac.bind("<ButtonPress-1>", pri_stisku)
    vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
    vytukavac.grid(row=4, column=1, padx=35, pady=0)
    
    #tagy barev
    vstup1_pole.tag_config("red", foreground="red")
    vstup2_pole.tag_config("red", foreground="red")
    
    # spustení oddelovace
    kontrola_pauzy()
    
    # Spuštění programu
    p_okno.mainloop()

tmavy_rezim = False
BARVY_SVETLY = {
    "bg": "#f0f0f0",
    "fg": "black",
    "pole_bg": "white",
    "pole_fg": "black",
    "lable_bg": "#f0f0f0",
    "lable_fg": "black",
    "tlacitko_bg": "#f0f0f0",
    "button_bg": "black",
    "button_fg": "white"}

BARVY_TMAVY = {
    "bg": "black",
    "fg": "white",
    "pole_bg": "#2d2d2d",
    "pole_fg": "white",
    "lable_bg": "black",
    "lable_fg": "white",
    "button_bg": "white",
    "button_fg": "black"}

def prepnout_rezim():
    global tmavy_rezim, tlacitko_rezim, vstup1_label, vstup2_label, frame_tlacitka, vytukavac_label
    tmavy_rezim = not tmavy_rezim
    barvy = BARVY_TMAVY if tmavy_rezim else BARVY_SVETLY
    okno_aktivni = okno if mobil else p_okno
    
    okno_aktivni.config(bg=barvy["bg"])
    vstup1_pole.config(bg=barvy["pole_bg"], fg=barvy["pole_fg"], insertbackground=barvy["pole_fg"])
    vstup2_pole.config(bg=barvy["pole_bg"], fg=barvy["pole_fg"], insertbackground=barvy["pole_fg"])
    vstup2_label.config(bg=barvy["lable_bg"], fg=barvy["lable_fg"])
    vstup1_label.config(bg=barvy["lable_bg"], fg=barvy["lable_fg"])
    vytukavac_label.config(bg=barvy["lable_bg"], fg=barvy["lable_fg"])
    frame_tlacitka.config(bg=barvy["bg"])
    tlacitko_rezim.config(text="☀" if tmavy_rezim else "🌙")
    tlacitko_rezim.config(bg=barvy["button_bg"], fg=barvy["button_fg"])
    
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

# Proměnné pro sledování času
cas_stisku = 0
cas_posledni_aktivity = time.time()  
pocet_predelu_v_kuse = 3
lomitko_zadanee = False
doba_lomitka = 1

def kontrola_pauzy():
    global cas_posledni_aktivity, cas_stisku, pocet_predelu_v_kuse, lomitko_zadanee, mobil
    nyni = time.time()
    pauza = nyni - cas_posledni_aktivity
    
    # Pokud uživatel nic nedělá déle než 1. sekundy, ukonči písmeno
    if lomitko_zadanee and  pauza > doba_lomitka and pocet_predelu_v_kuse <3:
        vstup2_pole.insert(tk.END, "/")      
        cas_posledni_aktivity = time.time() 
        pocet_predelu_v_kuse += 1
    #osetrené opakovaní oddelovace
    try:
        if mobil:
            okno.after(100, kontrola_pauzy)
        else:
            p_okno.after(100, kontrola_pauzy)
    except:
        pass
    
zozhrani_mobil()     