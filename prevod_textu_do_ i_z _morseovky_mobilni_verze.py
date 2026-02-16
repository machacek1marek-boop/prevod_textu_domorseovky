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

# Proměnné pro sledování času
cas_stisku = 0
cas_posledni_aktivity = time.time()  
pocet_predelu_v_kuse = 3
lomitko_zadanee = False 

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
okno.geometry("800x1000")  # šířka x výška

# Popisek pro vstup
vstup1_label = tk.Label(okno, text="Text:", font=("Arial", 12)); vstup1_label.place(x=450, y=1)

# Vstupní textové pole
vstup1_pole = tk.Text(okno, height=2, width=28, font=("Arial", 11)); vstup1_pole.place(x=50, y=80)


# Tlačítko pro převod do morse 
tlacitko1 = tk.Button(okno, text="↓ Do morse ↓", command=prevod_do_morse, bg="lightblue", font=("Arial", 11)); tlacitko1.pack(pady=10); tlacitko1.place(x=500, y=280)

# Tlačítko pro převod nba text
tlacitko2 = tk.Button(okno, text="↑Na text ↑", command=prevod_na_text, bg="lightblue", font=("Arial", 11)); tlacitko2.place(x=20, y=280)

# Popisek pro výstup
vstup2_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12)); vstup2_label.place(x=350, y=540)

# Výstupní textové pole (větší, pro více řádků)
vstup2_pole = tk.Text(okno, height=5, width=28, font=("Courier", 10)); vstup2_pole.place(x=50, y=620)

# Tlačítko pro smazání všeho 
tlacitko3 = tk.Button(okno, text="smazat vše", command=mazani_vse, bg="salmon", font=("Arial", 11)); tlacitko3.place(x=290, y=420)

# Popisek pro vytukavač
vytukavac_label = tk.Label(okno, text="Tlačítko na zapis morse:", font=("Arial", 8)); vytukavac_label.place(x=280, y=840)

# Tlačítko pro zapis morse (vytukavac)
vytukavac = tk.Button(okno, text="ťukej kod", bg="green", font=("Arial", 11))
vytukavac.bind("<ButtonPress-1>", pri_stisku)
vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
vytukavac.place(x=350, y=900)

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

#tagy
vstup1_pole.tag_config("red", foreground="red")
vstup2_pole.tag_config("red", foreground="red")

# Spuštění programu
okno.mainloop()