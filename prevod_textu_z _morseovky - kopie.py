#nahravani slovníku prevodníku
from slovnik_prevodnik import slovník_morse
text1 = input("napis text který chces prevest do morseokvy:")

#redukce textu diakritika
import unicodedata
def odstran_diakritiku(text):
    normalizovany_text = unicodedata.normalize('NFD', text)
    text_bez_diakritiky = "".join(
        znak for znak in normalizovany_text
        if unicodedata.category(znak) != 'Mn'
    )

    return text_bez_diakritiky.replace("đ", "d").replace("Đ", "D")

text2 = odstran_diakritiku(text1).upper()

print("zredukovaný text:",text2)

#prevod do morseovky
morse_vysledek = ""

for znak in text2:
    if znak in slovník_morse:
        morse_vysledek += slovník_morse[znak]
    else:
        morse_vysledek += "[" + znak + "]" + "/"
        
print("vysledný text",morse_vysledek)