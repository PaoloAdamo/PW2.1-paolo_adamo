import os
import re
import sqlite3
import pandas as pd
from prettytable import PrettyTable

# Usa una regex (espressione regolare) per cercare file con estensione .xlsx
# [.* = qualsiasi carattere ripetuto zero o più volte]
# [\.xlsx = serve per considerare il punto come carattere letterale, xlsx è l'estensione da cercare]
# [$ = fine stringa]
file_xlsx = re.compile(r".*\.xlsx$", re.IGNORECASE) # ignora minuscolo e Maiuscole

# Trova il PRIMO (nell' esempio è anche l'unico) file con estensione xlsx 
# os.listdir() cerca nella directory da cui è lanciato il programma
nome_file = next((file for file in os.listdir() 
                  if file_xlsx.match(file)), None)

# Se il file è None, ovvero non è stato trovato, verrà stampato a schermo l'errore. Verrà inoltre interrotto il programma.
if nome_file is None:
    print("Errore: file .xlsx mancante!")
    exit()

# Salva il basename, cioè il nome privo di estensione (in questo caso 'utenti')
# stringa divisa in due parti: prima e dopo il '.' --> [0] indica di prendere la parte prima
nome_base = nome_file.rsplit('.', 1)[0]

# Legge il file Excel
dataFrame = pd.read_excel(nome_file)

# Aggiunge l'estensione .db al file
nome_db = nome_base + ".db" # concateno .db al nome base, ottenendo il file che conterrà la tabella SQL

# Creo una connessione con SQLite database
# Comprende la sovrascrittura del database, se questo è già esistente
connessione = sqlite3.connect(nome_db)
cursore = connessione.cursor() # oggetto cursore

# Crea la tabella SQL usando le colonne del dataFrame
colonne = dataFrame.columns.tolist()
create_table_query = f"""
CREATE TABLE IF NOT EXISTS utenti (
    {', '.join([f'{col} TEXT' for col in colonne])}
)
"""
cursore.execute(create_table_query)

# Svuota la tabella prima di inserire nuovi dati, per evitare ridondanza
cursore.execute("DELETE FROM utenti")

# Inserimento 
insert_query = f"""
INSERT INTO utenti ({', '.join(colonne)})
VALUES ({', '.join(['?' for _ in colonne])})
"""
cursore.executemany(insert_query, dataFrame.values.tolist())

# Salvataggio dati
connessione.commit()

# Lettura dati e stampa
print("\n Visualizzazione dei dati contenuti nella tabella SQL '"+nome_base+"':")
cursore.execute("SELECT * FROM utenti")
righe = cursore.fetchall()
tabella_Finale = PrettyTable() # PrettyTable serve per avere una stampa più elegante ed immediata alla lettura
tabella_Finale.field_names = colonne
for riga in righe:
    tabella_Finale.add_row(riga)

print(tabella_Finale)
print()

# Stacca la connessione
connessione.close()