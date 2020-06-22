import random
import sys


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self.bit_string: int = 0
        self._compress(gene)

    def __str__(self) -> str:
        return self._decompress()

    def _compress(self, gene: str) -> None:
        self.bit_string = 0b1
        for nucleotide in gene:
            self.bit_string <<= 2
            if nucleotide == "A":
                self.bit_string |= 0b00
            elif nucleotide == "C":
                self.bit_string |= 0b01
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError(f"Invalid nucleotide: '{nucleotide}'")

    def _decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = (self.bit_string >> i) & 0b11
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
        return gene[::-1]


def random_gene(length: int = 1000) -> str:
    gene: str = ""
    while len(gene) < length:
        gene += random.choice("ACGT")
    return gene


if __name__ == "__main__":
    try:
        gene = sys.argv[1]
    except IndexError:
        gene = random_gene()
    print("=== Gene Start ===")
    print(gene)
    print("==== Gene End ====")
    print(f"Uncompressed size: {sys.getsizeof(gene)}")
    cg = CompressedGene(gene)
    print(f"Compressed size: {sys.getsizeof(cg.bit_string)}")
    print(f"Compressed and uncompressed are the same: {gene == str(cg)}")