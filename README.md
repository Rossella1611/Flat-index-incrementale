# Flat Index Incrementale
Estensione incrementale del progetto **Flat Index** per la gestione di dati cifrati, con partizionamento dinamico ottimizzato a cardinalità *k/k+1*.

## Descrizione
Questa versione introduce una nuova logica di partizionamento incrementale dei dati in gruppi con cardinalità *k* o *k+1*, evitando gruppi da *k-1* o inferiori, e minimizzando quelli da *k+1*.  
È pensata per scenari in cui i dati vengono aggiornati progressivamente e il ripartizionamento completo risulterebbe inefficiente o troppo costoso.

##  Funzionalità principali
- Inserimento incrementale efficiente di nuovi record  
- Gestione intelligente di buffer residui  
- Nessun gruppo con cardinalità inferiore a *k*  
- Minimizzazione dei gruppi con cardinalità superiore a *k*  
- Completamente compatibile con la logica originale di flat-index  
- **Nuova strategia decisionale basata su λ** per scegliere dinamicamente tra:
  - **Partizione totale** (maggiore qualità, costo più alto)  
  - **Partizione parziale** (costo minore, qualità ridotta)  
- Test automatizzati per entrambe le funzioni (`incremental_k_flat` e `incremental_partition`)  
- Grafici comparativi integrati  

##  Struttura del progetto
- compare_strategies_script/compare_strategies.py # Script per confronto visuale tra strategie
- incremental-version/test/test_incremental_partitioning.py # Test di incremental_k_flat e incremental_partition
- secure_index/partitioning.py # Implementazione funzioni di partizionamento
- comparison_partitioning.png # Grafico confronto
- requirements.txt # Librerie necessarie
- run_tests.bat # Esecuzione test
- run_visual.bat # Generazione grafici

##  Test automatizzati
Sono inclusi test per:
- `incremental_k_flat`: verifica che i gruppi abbiano sempre cardinalità *k* o *k+1*.  
- `incremental_partition`: verifica la scelta corretta della strategia decisionale in base a `λ`.  

Esempio di test (`test_incremental_partitioning.py`):

```python
def test_incremental_partition_lambda_low():
    """Con lambda basso, ci si aspetta una partizione totale."""
    r = list(range(1, 11))      # dataset iniziale
    n = list(range(11, 15))     # nuovi record
    k = 3
    lam = 0.0
    partition, strategy = incremental_partition(r, n, k, lam)
    assert strategy == "totale"
## Come eseguire i test
Assicurati di avere installato Python 3.8+ e pytest.

Installa le dipendenze con:
pip install -r requirements.txt

Poi esegui i test con:
pytest incremental-version/test/test_incremental_partitioning.py -v
oppure usa lo script
./run_tests.bat

Come eseguire il confronto visuale
Usa il file run_visual.bat per generare il grafico comparison_partitioning.png che mostra le differenze tra il partizionamento classico e incrementale.
./run_visual.bat

### Esempio di utilizzo con λ
Esempio di esecuzione della strategia decisionale con λ:
from secure_index.partitioning import incremental_partition

r = list(range(1, 11))     # dataset iniziale
n = list(range(11, 15))    # nuovi record
k = 3
lam = 0.5                  # compromesso tra qualità e costo

partition, strategy = incremental_partition(r, n, k, lam)

print(f"Strategia scelta: {strategy}")
for group in partition:
    print(group)

Output atteso:
Strategia scelta: parziale
[1, 2, 3]
[4, 5, 6]
[7, 8, 9, 10]
[11, 12, 13, 14]

## Requisiti
- Python 3.8+
- matplotlib
- pytest
- pandas

## Licenza
Questo progetto è distribuito sotto licenza MIT. Puoi usarlo, modificarlo e condividerlo liberamente.

## Autrice
Rossella – Università degli Studi del Molise
Tesi triennale
Basato sul progetto originale: https://github.com/unibg-seclab/flat-index

