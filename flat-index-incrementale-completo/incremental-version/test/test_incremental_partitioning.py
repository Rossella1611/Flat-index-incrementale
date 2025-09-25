# test_incremental_partitioning.py

import pytest
from secure_index.partitioning import k_flat, incremental_k_flat, incremental_partition

def test_incremental_k_flat_basic():
    existing = [[1, 2, 3], [4, 5, 6]]
    new = [7, 8]
    k = 3
    updated = incremental_k_flat(new, existing, k)
    assert all(len(g) in (k, k+1) for g in updated)

def test_incremental_partition_lambda_low():
    """Con lambda basso, ci si aspetta una partizione totale."""
    r = list(range(1, 11))      # dataset iniziale di 10 record
    n = list(range(11, 15))     # nuovi 4 record
    k = 3
    lam = 0.0  # privilegia la qualità
    partition, strategy = incremental_partition(r, n, k, lam)
    assert strategy == "totale"
    assert all(len(g) in (k, k+1) for g in partition)

def test_incremental_partition_lambda_high():
    """Con lambda alto, ci si aspetta una partizione parziale."""
    r = list(range(1, 11))
    n = list(range(11, 15))
    k = 3
    lam = 1.0  # privilegia il costo
    partition, strategy = incremental_partition(r, n, k, lam)
    assert strategy == "parziale"
    assert all(len(g) in (k, k+1) for g in partition)
