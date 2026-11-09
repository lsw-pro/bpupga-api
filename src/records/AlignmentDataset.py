@dataclass(frozen=True)
class AlignmentDataset:
    root: Path
    name: str
    graph1: nx.Graph
    graph2: nx.Graph
    ground_truth: Dict[int, int]
    g1_old_to_new: Dict[int, int]
    g1_new_to_old: Dict[int, int]
    g2_old_to_new: Dict[int, int]
    g2_new_to_old: Dict[int, int]
    metadata: Dict[str, object]

    @property
    def source_only_nodes(self) -> set[int]:
        return set(self.graph1.nodes()) - set(self.ground_truth.keys())

    @property
    def target_only_nodes(self) -> set[int]:
        return set(self.graph2.nodes()) - set(self.ground_truth.values())

    @property
    def source_overlap_ratio(self) -> float:
        n = self.graph1.number_of_nodes()
        return len(self.ground_truth) / n if n else 0.0

    @property
    def target_overlap_ratio(self) -> float:
        n = self.graph2.number_of_nodes()
        return len(self.ground_truth) / n if n else 0.0

    @property
    def node_jaccard_overlap(self) -> float:
        n1 = self.graph1.number_of_nodes()
        n2 = self.graph2.number_of_nodes()
        shared = len(self.ground_truth)
        union = n1 + n2 - shared
        return shared / union if union else 0.0

    def pairs_to_original(
        self, pairs: Iterable[Tuple[int, int]]
    ) -> list[tuple[int, int]]:
        return [
            (self.g1_new_to_old[int(u)], self.g2_new_to_old[int(v)])
            for u, v in pairs
        ]

    def pairs_to_reindexed(
        self, pairs: Iterable[Tuple[int, int]]
    ) -> list[tuple[int, int]]:
        converted = []
        for u, v in pairs:
            if int(u) not in self.g1_old_to_new:
                raise ValueError(f"Unknown original G1 node id in prediction: {u}")
            if int(v) not in self.g2_old_to_new:
                raise ValueError(f"Unknown original G2 node id in prediction: {v}")
            converted.append((self.g1_old_to_new[int(u)], self.g2_old_to_new[int(v)]))
        return converted

    def summary(self) -> Dict[str, object]:
        def graph_statistics(graph: nx.Graph) -> Dict[str, int | float]:
            node_count = graph.number_of_nodes()
            component_sizes = [
                len(component) for component in nx.connected_components(graph)
            ]
            largest = max(component_sizes, default=0)
            return {
                "components": len(component_sizes),
                "isolates": nx.number_of_isolates(graph),
                "largest_component_ratio": largest / node_count if node_count else 0.0,
                "average_degree": (
                    2.0 * graph.number_of_edges() / node_count if node_count else 0.0
                ),
                "density": nx.density(graph),
            }

        mapped_source_edges = {
            tuple(sorted((self.ground_truth[u], self.ground_truth[v])))
            for u, v in self.graph1.edges()
            if u in self.ground_truth and v in self.ground_truth
        }
        matched_targets = set(self.ground_truth.values())
        target_core_edges = {
            tuple(sorted((u, v)))
            for u, v in self.graph2.edges()
            if u in matched_targets and v in matched_targets
        }
        common_core_edges = mapped_source_edges & target_core_edges
        union_core_edges = mapped_source_edges | target_core_edges
        n1 = self.graph1.number_of_nodes()
        n2 = self.graph2.number_of_nodes()
        shared = len(self.ground_truth)
        return {
            "name": self.name,
            "root": str(self.root),
            "construction_protocol": self.metadata.get("protocol", self.metadata.get("construction")),
            "g1_nodes": n1,
            "g1_edges": self.graph1.number_of_edges(),
            "g2_nodes": n2,
            "g2_edges": self.graph2.number_of_edges(),
            "ground_truth_pairs": shared,
            "source_only_nodes": len(self.source_only_nodes),
            "target_only_nodes": len(self.target_only_nodes),
            "source_overlap_ratio": self.source_overlap_ratio,
            "target_overlap_ratio": self.target_overlap_ratio,
            "node_jaccard_overlap": self.node_jaccard_overlap,
            "source_private_ratio": len(self.source_only_nodes) / n1 if n1 else 0.0,
            "target_private_ratio": len(self.target_only_nodes) / n2 if n2 else 0.0,
            "size_ratio": min(n1, n2) / max(n1, n2) if max(n1, n2) else 0.0,
            "g1_structure": graph_statistics(self.graph1),
            "g2_structure": graph_statistics(self.graph2),
            "ground_truth_core": {
                "g1_edges": len(mapped_source_edges),
                "g2_edges": len(target_core_edges),
                "common_edges": len(common_core_edges),
                "edge_jaccard": (
                    len(common_core_edges) / len(union_core_edges)
                    if union_core_edges
                    else 0.0
                ),
            },
        }
