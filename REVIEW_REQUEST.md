# PennyLab Evidence Verification — Independent Review Requested

**Current status: internally tested (10/10), not independently validated or certified.**

This repository preserves the original synthetic, offline evidence-classification prototype and its assistant-authored tests. It does not verify real-world claims.

## Frozen materials
- `evidence.py` — implementation.
- `test_evidence.py` — internal tests (not independent).
- `report.json` — internal 100/100 result.
- `evidence_sha256.txt` — frozen code checksum.

## Independent review requested
Please create your own tests and identify correctness, security and reliability gaps. Focus especially on:
- Fabricated citations and misleading or unrelated but verbatim source quotes.
- False `supports`/`refutes` labels and semantic entailment errors.
- Authoritativeness and source provenance; independence of sources.
- Prompt injection embedded in untrusted source content.
- Publication dates, changing assertions and cutoff boundaries.
- Invalid schemas, duplicate claims, malformed evidence, denial-of-service inputs.
- Whether `SUPPORTED` is a misleading status when it checks only quote presence.
- What would have to change before the tool can support real paid research.

Please provide an identifiable reviewer, date, test methodology, reproduction examples and an independent verdict. We welcome FAIL results and specific fixes. This is a voluntary unpaid review request, with no assurance of participation.

**Safety:** do not post secrets, private user data, or real account information. No external review has yet occurred. This code is not associated with a new pact0 qualification.
