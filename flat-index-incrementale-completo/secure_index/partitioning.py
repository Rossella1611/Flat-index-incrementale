def k_flat(records, k):
    if not records:
        return []
    sorted_records = sorted(records)
    groups = [sorted_records[i:i + k] for i in range(0, len(sorted_records), k)]
    if len(groups) > 1 and len(groups[-1]) < k:
        groups[-2].extend(groups[-1])
        groups = groups[:-1]
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

    # Calcola quanti nuovi gruppi servono
    total = len(buffer)
    if total == 0:
        return updated

    q, r = divmod(total, k)
    # Minimizza gruppi da k+1: r gruppi da k+1, q-r gruppi da k
    num_kplus1 = r
    num_k = q - r

    index = 0
    for _ in range(num_kplus1):
        updated.append(buffer[index:index + k + 1])
        index += k + 1
    for _ in range(num_k):
        updated.append(buffer[index:index + k])
        index += k

    # Se rimane qualcosa (<k), lo ignora (o logga)
    if index < len(buffer):
        print(f"[INFO] {len(buffer) - index} record rimanenti scartati perché < k={k}: {buffer[index:]}")

    return updated
