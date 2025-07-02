# test_incremental_partitioning.py - test della funzione incremental_k_flat

import pytest
from secure_index.partitioning import k_flat, incremental_k_flat

def test_incremental_k_flat_basic():
    existing = [[1,2,3], [4,5,6]]
    new = [7,8]
    k = 3
    updated = incremental_k_flat(existing, new, k)
    assert all(len(g) >= k and len(g) <= k+1 for g in updated)
