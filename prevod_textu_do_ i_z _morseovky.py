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
    morse_pole = vstup2_pole.get("1.0", "end-2c").strip()
    seznamkodu = morse_pole.split('/')
    
    morse_vysledek = ""
    
    for kod in seznamkodu:
        if kod in slovnik_zpet:
            morse_vysledek += slovnik_zpet[kod]
        elif kod == "" or kod.isspace(): # Dvojité lomítko // vytvoří prázdný retezec při splitu
            continue 
        else:
            morse_vysledek += kod
    #Vymaž předchozí výsledek a zobraz nový
    vstup1_pole.delete("1.0", tk.END)  # vymaže obsah
    vstup1_pole.insert("1.0", morse_vysledek)  # vloží nový text


# Hlavní funkce pro převod
def prevod_do_morse():
    text1 = vstup1_pole.get("1.0", "end-1c")
    text2 = odstran_diakritiku(text1).upper()
    morse_vysledek = ""
    for znak in text2:
        if znak in slovník_morse:
            morse_vysledek += slovník_morse[znak]
        else:
            morse_vysledek += "[" + znak + "]" + "/"       
    #Vymaž předchozí výsledek a zobraz nový
    vstup2_pole.delete("1.0", tk.END)  # vymaže obsah
    vstup2_pole.insert("1.0", morse_vysledek)  # vloží nový text

def mazani_vse():
    vstup2_pole.delete("1.0", tk.END)
    vstup1_pole.delete("1.0", tk.END)

import time # Musíš přidat na začátek souboru

# Proměnné pro sledování času
cas_stisku = 0
cas_posledni_aktivity = time.time()
pismeno_ukonceno = True

def pri_stisku(event):
    global cas_stisku
    if cas_stisku == 0: # Zabrání opakování při držení klávesy
        cas_stisku = time.time()

def pri_uvolneni(event):
    global cas_stisku, cas_posledni_aktivity, pismeno_ukonceno
    trvani = time.time() - cas_stisku
    
    if trvani < 0.3:
        vstup2_pole.insert(tk.END, ".")
    else:
        vstup2_pole.insert(tk.END, "-")
    
    cas_stisku = 0
    cas_posledni_aktivity = time.time()
    pismeno_ukonceno = True 



#hlavní funkce pro tukani
def zaznam_morse():
    # Proměnné pro sledování času
    cas_stisku = 0
    cas_posledni_aktivity = time.time()
    pismeno_ukonceno = True
    
    tukani = ""
    tukani += "."
    vstup2_pole.insert("1.0", tukani)  # vloží vytukanou spravu

# Vytvoření hlavního okna
okno = tk.Tk()
okno.title("Převodník do nebo z morseovky")
okno.geometry("500x300")  # šířka x výška

# Popisek pro vstup
vstup1_label = tk.Label(okno, text="Text:", font=("Arial", 12))
vstup1_label.place(x=230, y=10)

# Vstupní textové pole
vstup1_pole = tk.Text(okno, height=2, width=50, font=("Arial", 11))
vstup1_pole.place(x=50, y=35)


# Tlačítko pro převod do morse 
tlacitko1 = tk.Button(okno, text="↓ Převést do morse ↓", command=prevod_do_morse, 
                     bg="lightblue", font=("Arial", 11))
tlacitko1.pack(pady=10)
tlacitko1.place(x=330, y=100)

# Tlačítko pro převod nba text
tlacitko2 = tk.Button(okno, text="↑ Převést na text ↑", command=prevod_na_text, 
                     bg="lightblue", font=("Arial", 11))
tlacitko2.place(x=20, y=100)

# Popisek pro výstup
vstup2_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12))
vstup2_label.place(x=205, y=150)

# Výstupní textové pole (větší, pro více řádků)
vstup2_pole = tk.Text(okno, height=5, width=50, font=("Courier", 10))
vstup2_pole.place(x=50, y=180)

# Tlačítko pro smazání všeho 
tlacitko3 = tk.Button(okno, text="smazat vše", command=mazani_vse,
                      bg="salmon", font=("Arial", 11))
tlacitko3.place(x=200, y=100)

# Popisek pro vytukavač
vytukavac_label = tk.Label(okno, text="Tlačítko na zapis morse:", font=("Arial", 12))
vytukavac_label.place(x=560, y=170)

# Tlačítko pro zapis morse (vytukavac)
vytukavac = tk.Button(okno, text="ťukej kod", bg="green", font=("Arial", 11))
vytukavac.bind("<ButtonPress-1>", pri_stisku)
vytukavac.bind("<ButtonRelease-1>", pri_uvolneni)
vytukavac.place(x=600, y=200)

def kontrola_pauzy():
    global cas_posledni_aktivity, pismeno_ukonceno
    nyni = time.time()
    pauza = nyni - cas_posledni_aktivity
    
    # Pokud uživatel nic nedělá déle než 1.2 sekundy, ukonči písmeno
    if not pismeno_ukonceno and pauza > 1.2:
        vstup2_pole.insert(tk.END, "/")
        pismeno_ukonceno = True
    
    # Opakuj kontrolu každých 100ms
    okno.after(100, kontrola_pauzy)

# Spuštění automatické kontroly pauzy
kontrola_pauzy()


okno.geometry("800x300")
# Spuštění programu
okno.mainloop()