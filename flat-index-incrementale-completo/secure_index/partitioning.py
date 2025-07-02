def k_flat(records, k):
    """
    Divide records ordinati in gruppi da k o k+1 (massimizzando gruppi da k).
    Evita gruppi con meno di k elementi.
    """
    if not records:
        return []

    sorted_records = sorted(records)
    n = len(sorted_records)

    q, r = divmod(n, k)  # r gruppi da k+1, (q - r) da k
    groups = []
    idx = 0

    for _ in range(r):
        groups.append(sorted_records[idx:idx + k + 1])
        idx += k + 1
    for _ in range(q - r):
        groups.append(sorted_records[idx:idx + k])
        idx += k

    # Se rimangono elementi < k (caso raro ma gestibile), li scarta con log
    if idx < n:
        print(f"[INFO] {n - idx} record scartati perché < k={k}: {sorted_records[idx:]}")

    return groups
def incremental_k_flat(new_records, existing_partitions, k):
    """
    Aggiunge nuovi record alle partizioni esistenti mantenendo cardinalità k o k+1.
    Massimizza i gruppi da k e minimizza quelli da k+1. Evita gruppi < k.
    """
    updated = [list(group) for group in existing_partitions]
    buffer = list(new_records)

    # Riempie gruppi esistenti con meno di k elementi
    for group in updated:
        while len(group) < k and buffer:
            group.append(buffer.pop(0))

    # Prova ad estendere gruppi da k a k+1, se ci sono record residui
    for group in updated:
        if len(group) == k and buffer:
            group.append(buffer.pop(0))

    # Calcola quanti nuovi gruppi possiamo creare con ciò che resta
    total = len(buffer)
    q, r = divmod(total, k)
    num_kplus1 = r
    num_k = q - r

    index = 0
    for _ in range(num_kplus1):
        updated.append(buffer[index:index + k + 1])
        index += k + 1
    for _ in range(num_k):
        updated.append(buffer[index:index + k])
        index += k

    # Se restano record (< k), loggali ma non scartarli: prova ad aggiungerli a gruppi da k
    leftovers = buffer[index:]
    if leftovers:
        added = False
        for group in updated:
            if len(group) == k and len(leftovers) > 0:
                group.append(leftovers.pop(0))
                added = True
        if leftovers:
            print(f"[INFO] {len(leftovers)} record rimanenti scartati perché < k={k}: {leftovers}")

    # Verifica finale: ogni gruppo deve avere dimensione k o k+1
    for i, group in enumerate(updated):
        if len(group) < k or len(group) > k + 1:
            raise ValueError(f"Gruppo {i} ha dimensione invalida: {len(group)} (attesi k={k} o k+1={k+1})")

    return updated
