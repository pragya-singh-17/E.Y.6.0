from backend.agents import _confidence_for_candidates


def test_confidence_prefers_stronger_sources():
  cands = [
    {"source": "original", "value": "A"},
    {"source": "npi", "value": "B"},
    {"source": "maps", "value": "B"},
  ]
  res = _confidence_for_candidates(cands)
  assert res["best"] == "B"
  assert res["confidence"] > 0.5
