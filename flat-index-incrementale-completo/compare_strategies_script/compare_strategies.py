
"""
compare_strategies.py

Questo script confronta il comportamento dell'approccio originale (k_flat) e della variante incrementale (incremental_k_flat).
Utile per supportare il Capitolo 7 della tesi: confronto tra partizionamento statico e dinamico.
"""
from secure_index.partitioning import k_flat, incremental_k_flat
import matplotlib.pyplot as plt
import time


def simulate_dataset(n):
    return [(i, f"val_{i}") for i in range(n)]


def count_exact_k(partitions, k):
    return sum(1 for group in partitions if len(group) == k)


def partition_stats(partitions, k):
    sizes = [len(g) for g in partitions]
    exact_k = count_exact_k(partitions, k)
    return {
        "num_groups": len(partitions),
        "exact_k_groups": exact_k,
        "percent_k": round((exact_k / len(partitions)) * 100, 2),
        "group_sizes": sizes,
    }


def plot_group_distributions(original, incremental, k):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist([original["group_sizes"], incremental["group_sizes"]],
            bins=[k-0.5, k+0.5, k+1.5],
            label=["k_flat", "incremental_k_flat"],
            rwidth=0.8)
    ax.set_xticks([k, k+1])
    ax.set_xlabel("Cardinalità dei gruppi")
    ax.set_ylabel("Numero di gruppi")
    ax.set_title("Distribuzione delle cardinalità dei gruppi")
    ax.legend()
    plt.tight_layout()
    plt.savefig("comparison_partitioning.png")

def plot_full_vs_incremental(full_partition_stats, incremental_partition_stats, k):
    fig, ax = plt.subplots(figsize=(8, 4))

    # Qui abbiamo la distribuzione gruppi per la partizione full su 495
    full_sizes = full_partition_stats["group_sizes"]
    # Qui abbiamo la distribuzione gruppi per la partizione incremental combinata (300 + 195)
    incremental_sizes = incremental_partition_stats["group_sizes"]

    ax.hist([full_sizes, incremental_sizes],
            bins=[k-0.5, k+0.5, k+1.5],
            label=["k_flat full 495", "incremental_k_flat 300+195"],
            rwidth=0.8)
    ax.set_xticks([k, k+1])
    ax.set_xlabel("Cardinalità dei gruppi")
    ax.set_ylabel("Numero di gruppi")
    ax.set_title("Confronto distribuzione gruppi: full vs incremental")
    ax.legend()
    plt.tight_layout()
    plt.savefig("comparison_full_vs_incremental.png")


def main():
    import time

    k = 11
    full_data = simulate_dataset(495)      # Dataset completo da 495 record
    initial_data = full_data[:300]         # Dati iniziali (300)
    new_data = full_data[300:]             # Nuovi dati (195)

    # Partizione iniziale su 300 record
    start_init = time.time()
    p_init = k_flat(initial_data, k)
    end_init = time.time()
    p_full = k_flat(full_data, k)

    # Partizione incrementale: partiziona solo i nuovi 195 dati
    # poi unisce le partizioni vecchie e nuove
    start_inc = time.time()
    new_partitions = incremental_k_flat(new_data, [], k)  # partizione solo sui nuovi 195
    p_inc = p_init + new_partitions                         # unione delle partizioni
    end_inc = time.time()

    # Statistiche sulle due partizioni: iniziale (300) vs incrementale completa (300+195)
    stats_init = partition_stats(p_init, k)
    stats_inc = partition_stats(p_inc, k)
    stats_full =partition_stats(p_full, k)

    print("\n=== Risultati partizione iniziale su 300 record ===")
    for key, value in stats_init.items():
        print(f"{key}: {value}")
    print(f"Tempo: {end_init - start_init:.4f} s")

    print("\n=== Risultati partizione incrementale su 495 record (300+195) ===")
    for key, value in stats_inc.items():
        print(f"{key}: {value}")
    print(f"Tempo: {end_inc - start_inc:.4f} s")

    # Grafico comparativo tra la partizione iniziale e quella incrementale
    plot_group_distributions(stats_init, stats_inc, k)
    print("\nGrafico salvato in comparison_partitioning.png")

    # Grafico: confronto tra full e incrementale (495 vs 300+195)
    plot_full_vs_incremental(stats_full, stats_inc, k)
    print("\nGrafico confronto full vs incremental salvato in comparison_full_vs_incremental.png")


if __name__ == "__main__":
    main()
