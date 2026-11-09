@dataclass
class AlignmentResult:
    method: str
    predicted_pairs: List[Tuple[int, int]]
    runtime_sec: float
    peak_memory_mb: Optional[float] = None
    score_matrix: Optional[np.ndarray] = None
    cost_matrix: Optional[np.ndarray] = None
    source_embeddings: Optional[np.ndarray] = None
    target_embeddings: Optional[np.ndarray] = None
    # Sparse algorithm-native candidate scores.  Unlike ``score_matrix``, an
    # omitted pair means that the method never retrieved that candidate.
    ranking_candidates: Optional[List[Tuple[int, int, float]]] = None
    larger_is_better: Optional[bool] = None
    # Ephemeral model-native signals consumed by a method-aware partial decoder.
    # They are intentionally not serialized as JSON because they may be dense.
    partial_decoder_data: Optional[Dict[str, np.ndarray]] = None
    metadata: Dict[str, object] = field(default_factory=dict)
    # Optional read-only traces returned by the baseline261023 Alpine model.
    stage_score_matrices: Dict[str, np.ndarray] = field(default_factory=dict)
    stage_diagnostics_metadata: Dict[str, Dict[str, object]] = field(default_factory=dict)

    def validate_shapes(self, num_source_nodes: int, num_target_nodes: int) -> None:
        expected_matrix_shape = (num_source_nodes, num_target_nodes)
        if self.score_matrix is not None and self.score_matrix.shape != expected_matrix_shape:
            raise ValueError(
                f"score_matrix shape {self.score_matrix.shape} != {expected_matrix_shape}"
            )
        if self.cost_matrix is not None and self.cost_matrix.shape != expected_matrix_shape:
            raise ValueError(
                f"cost_matrix shape {self.cost_matrix.shape} != {expected_matrix_shape}"
            )
        if self.source_embeddings is not None and self.source_embeddings.shape[0] != num_source_nodes:
            raise ValueError("source_embeddings row count does not match G1")
        if self.target_embeddings is not None and self.target_embeddings.shape[0] != num_target_nodes:
            raise ValueError("target_embeddings row count does not match G2")
        for stage_name, matrix in self.stage_score_matrices.items():
            if matrix.shape != expected_matrix_shape:
                raise ValueError(
                    f"stage score matrix {stage_name!r} has shape "
                    f"{matrix.shape} != {expected_matrix_shape}"
                )
        if self.ranking_candidates is not None:
            seen = set()
            for source, target, score in self.ranking_candidates:
                pair = (int(source), int(target))
                if not (0 <= pair[0] < num_source_nodes and 0 <= pair[1] < num_target_nodes):
                    raise ValueError("ranking candidate contains an out-of-range node")
                if pair in seen:
                    raise ValueError("ranking_candidates contains a duplicate pair")
                if not np.isfinite(float(score)):
                    raise ValueError("ranking candidate score must be finite")
                seen.add(pair)
