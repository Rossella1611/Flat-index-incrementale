
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


def main():
    k = 4
    full_data = simulate_dataset(1000)
    initial_data = full_data[:600]
    new_data = full_data[600:]

    # Partizione completa
    start_full = time.time()
    p_full = k_flat(full_data, k)
    end_full = time.time()

    # Partizione incrementale
    start_inc = time.time()
    p_init = k_flat(initial_data, k)
    p_inc = incremental_k_flat(new_data, p_init, k)
    end_inc = time.time()

    # Statistiche
    stats_full = partition_stats(p_full, k)
    stats_inc = partition_stats(p_inc, k)

    print("\n=== Risultati k_flat ===")
    for key, value in stats_full.items():
        print(f"{key}: {value}")
    print(f"Tempo: {end_full - start_full:.4f} s")

    print("\n=== Risultati incremental_k_flat ===")
    for key, value in stats_inc.items():
        print(f"{key}: {value}")
    print(f"Tempo: {end_inc - start_inc:.4f} s")

    # Grafico comparativo
    plot_group_distributions(stats_full, stats_inc, k)
    print("\nGrafico salvato in comparison_partitioning.png")


if __name__ == "__main__":
    main()
