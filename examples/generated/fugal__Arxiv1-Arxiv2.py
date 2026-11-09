import bpupga as bp

# Run from the repository root with the documented import setup.
data = bp.Dataset.load(
    "baseline_exdit_261029/date_261023/Arxiv1-Arxiv2/bpupga/"
    "rho_s0p6_rho_t0p6/construction_seed_2026")
method = bp.Algorithm(
    "fugal", seed=2026, device="cpu")

# The algorithm receives only graph topology.
result = method.align(data.graph1, data.graph2)
metrics = bp.evaluate(result, data, ks=(1, 5, 10))
print(metrics["pair"])
