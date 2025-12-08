# Import knihoven
import tkinter as tk
from slovnik_prevodnik import slovník_morse
import unicodedata

#zadaní textu
text1 = vstup_pole.get() 

#redukce textu diakritika a velká
def odstran_diakritiku(text):
    normalizovany_text = unicodedata.normalize('NFD', text)
    text_bez_diakritiky = "".join(
        znak for znak in normalizovany_text
        if unicodedata.category(znak) != 'Mn'
    )

    return text_bez_diakritiky.replace("đ", "d").replace("Đ", "D")
text2 = odstran_diakritiku(text1).upper()
print("zredukovaný text:",text2)

# Hlavní funkce pro převod
def prevod_do_morse1():
    morse_vysledek = ""
    for znak in text2:
        if znak in slovník_morse:
            morse_vysledek += slovník_morse[znak]
        else:
            morse_vysledek += "[" + znak + "]" + "/"       
    print("vysledný text",morse_vysledek)
    
# 4. Vymaž předchozí výsledek a zobraz nový
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
tlacitko = tk.Button(okno, text="Převést do morseovky", command=prevod_do_morse, 
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