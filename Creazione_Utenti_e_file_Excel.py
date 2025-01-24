import random
from faker import Faker
import pandas as pd

fake = Faker('it_IT') # lingua italiana

# Funzioni per generare un nome/cognome italiano casuale
def generaNome():
    return fake.first_name()

def generaCognome():
    return fake.last_name()

# Funzione per generare un indirizzo email con questo formato: nome.cognome @ dominio_casuale
def generaEmail(nome, cognome):
    return f"{nome.lower()}.{cognome.lower()}@{fake.free_email_domain()}" # il metodo usato da fake serve per generare un dominio random
    # lower serve per avere tutti i caratteri minuscoli

# Funzione per generare un numero di telefono casuale 
# (prefisso +39, un numero di operatore e altri 7 numeri)
def generaNumeroTelefono():
    operatore = ["334", "328", "366", "339", "345"]
    numero = f"{random.randint(0, 9999999):07d}"
    # 07d --> Numero di 7 cifre con zeri iniziali
    return f"+39 {random.choice(operatore)}-{numero}"

# Funzione che genera un'età compresa tra 18 e 70 anni (inclusi)
def generaEtà():
    return f"{random.randint(18,70)}"

# Funzione che genera una città
def generaCittà():
    return f"{fake.city()}"

# ------------------------------------------------------ #

# GENERAZIONE DEI DATI
# chiama le funzione sopra elencate per generare i dati degli utenti
utenti = []
for i in range(10):
    nome = generaNome()
    cognome = generaCognome()
    email = generaEmail(nome, cognome)
    phone = generaNumeroTelefono()
    età = generaEtà()
    città = generaCittà()
    utenti.append({ # unisce alla lista utenti
        "Nome": nome,
        "Cognome": cognome,
        "Email": email,
        "Telefono": phone,
        "Età": età,
        "Città": città
    })

# Creazione di un dataFrame
dataFrame = pd.DataFrame(utenti)

# Salvataggio in un file Excel
file_name = "utenti.xlsx"
dataFrame.to_excel(file_name, index=False)

print(f"\nDati degli utenti salvati correttamente in {file_name}")
print()