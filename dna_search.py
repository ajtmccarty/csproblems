from enum import IntEnum
from typing import List, Tuple

Nucleotide: IntEnum = IntEnum("Nucleotide", ("A", "C", "G", "T"))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]

gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"


def str_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        # codon: Codon = (Nucleotide[i], Nucleotide[i + 1], Nucleotide[i + 2])
        codon: Codon = str_to_codon(s[i : i + 3])
        gene.append(codon)
    return gene


def str_to_codon(s: str) -> Codon:
    if len(s) != 3:
        raise ValueError(f"Input for codon '{s}' must be of length 3")
    return (Nucleotide[s[0]], Nucleotide[s[1]], Nucleotide[s[2]])


def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    """
    >>> gene = str_to_gene(gene_str)
    >>> good_codon = str_to_codon("ACG")
    >>> bad_codon = str_to_codon("CGC")
    >>> assert linear_contains(gene, good_codon)
    >>> assert not linear_contains(gene, bad_codon)
    """
    for codon in gene:
        if codon == key_codon:
            return True
    return False


def binary_contains(sorted_gene: Gene, key_codon: Codon) -> bool:
    """
    >>> gene = sorted(str_to_gene(gene_str))
    >>> good_codon = str_to_codon("ACG")
    >>> bad_codon = str_to_codon("CGC")
    >>> assert binary_contains(gene, good_codon)
    >>> assert not binary_contains(gene, bad_codon)
    """
    low: int = 0
    high: int = len(sorted_gene)
    while low < high:
        mid: int = (low + high) // 2
        if sorted_gene[mid] < key_codon:
            low = mid + 1
        elif sorted_gene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
