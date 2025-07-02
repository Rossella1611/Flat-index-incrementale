# Flat Index Incrementale

Estensione incrementale del progetto Flat Index per la gestione di dati cifrati, con partizionamento dinamico ottimizzato a cardinalità k/k+1.

Descrizione
Questa versione introduce una nuova logica di partizionamento incrementale dei dati in gruppi con cardinalità k o k+1, evitando gruppi da k-1 o inferiori, e minimizzando quelli da k+1. È pensata per scenari in cui i dati vengono aggiornati progressivamente e il ripartizionamento completo risulterebbe inefficiente o troppo costoso.

Funzionalità principali
Inserimento incrementale efficiente di nuovi record

Gestione intelligente di buffer residui

Nessun gruppo con cardinalità inferiore a k

Minimizzazione dei gruppi con cardinalità superiore a k

Completamente compatibile con la logica originale di flat-index

Test automatizzati per la nuova funzione

Grafico comparativo integrato

Struttura del progetto
compare_strategies_script/compare_strategies.py: script per confronto visuale tra strategie

incremental-version/test/test_incremental_partitioning.py: test della funzione incrementale

secure_index/partitioning.py: implementazione della funzione incremental_k_flat

comparison_partitioning.png: grafico confronto

requirements.txt: librerie necessarie

run_tests.bat: esecuzione dei test

run_visual.bat: generazione grafico

Esempio: funzione incremental_k_flat
python
Copia
Modifica
def incremental_k_flat(existing_partitions, new_records, k):
    updated = [list(group) for group in existing_partitions]
    buffer = list(new_records)
    for group in updated:
        while len(group) < k and buffer:
            group.append(buffer.pop(0))
    while len(buffer) >= k:
        new_group = buffer[:k]
        buffer = buffer[k:]
        updated.append(new_group)
    for record in buffer:
        for group in updated:
            if len(group) < k + 1:
                group.append(record)
                break
    return updated
Come eseguire i test
Assicurati di avere installato Python 3.8+ e pytest.

Installa le dipendenze con:
pip install -r requirements.txt

Poi esegui i test con:
./run_tests.bat

Come eseguire il confronto visuale
Usa il file run_visual.bat per generare il grafico comparison_partitioning.png che mostra le differenze tra il partizionamento classico e incrementale.
./run_visual.bat


Requisiti
- Python 3.8+
- matplotlib
- pytest
- pandas

Licenza
Questo progetto è distribuito sotto licenza MIT. Puoi usarlo, modificarlo e condividerlo liberamente.

Autrice
Rossella – Università degli Studi del Molise
Tesi triennale
Basato sul progetto originale: https://github.com/unibg-seclab/flat-index
