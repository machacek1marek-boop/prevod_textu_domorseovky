# Import knihoven
import tkinter as tk
from slovnik_prevodnik import slovník_morse

# Vytvoření otočeného slovníku (Morse -> Písmeno)
# Musíme odstranit lomítka z hodnot v původním slovníku pro správné porovnání
slovnik_zpet = {hodnota.replace("/", ""): klic for klic, hodnota in slovník_morse.items()}# Ručně přidáme mezeru, která je v původním slovníku definovaná jako "/"
slovnik_zpet[""] = " "



# Hlavní funkce pro převod
def prevod_z_morse():
    text1 = vstup_pole.get().strip()
    print(text1)
    seznamkodu = text1.split('/')
    
    morse_vysledek = ""
    
    for kod in seznamkodu:
        if kod in slovnik_zpet:
            morse_vysledek += slovnik_zpet[kod]
        elif kod == "": # Dvojité lomítko // vytvoří prázdný řetězec při splitu
            continue
        else:
            morse_vysledek += "[" + kod + "]" + "/"       
    print("vysledný text",morse_vysledek)
    #Vymaž předchozí výsledek a zobraz nový
    vystup_pole.delete("1.0", tk.END)  # vymaže obsah
    vystup_pole.insert("1.0", morse_vysledek)  # vloží nový text

# Vytvoření hlavního okna
okno = tk.Tk()
okno.title("Převodník do morseovky")
okno.geometry("500x300")  # šířka x výška

# Popisek pro vstup
vstup_label = tk.Label(okno, text="Zadej text k převodu:", font=("Arial", 12))
vstup_label.pack(pady=5)

# Vstupní textové pole
vstup_pole = tk.Entry(okno, width=50, font=("Arial", 11))
vstup_pole.pack(pady=5)

# Tlačítko pro převod
tlacitko = tk.Button(okno, text="Převést z morseovky", command=prevod_z_morse, 
                     bg="lightblue", font=("Arial", 11))
tlacitko.pack(pady=10)

# Popisek pro výstup
vystup_label = tk.Label(okno, text="Morseovka:", font=("Arial", 12))
vystup_label.pack(pady=5)

# Výstupní textové pole (větší, pro více řádků)
vystup_pole = tk.Text(okno, height=5, width=50, font=("Courier", 10))
vystup_pole.pack(pady=5)

# Spuštění programu
okno.mainloop()