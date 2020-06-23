from dataclasses import dataclass


@dataclass
class Edge:
    u: int
    v: int

    def reversed(self) -> "Edge":
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> "WeightedEdge":
        return WeightedEdge(u=self.v, v=self.u, weight=self.weight)

    def __lt__(self, other: "WeightedEdge") -> bool:
        return self.weight < other.weight

    def __str__(self) -> str:
        return f"{self.u} {self.weight}> {self.v}"
