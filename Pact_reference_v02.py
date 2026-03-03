#!/usr/bin/env python3
"""
PACT Protocol — Reference Implementation v0.2
==============================================
Minimal viable PACT transaction. No registry. No anchoring. No network.

What this demonstrates:
  - Canonical JSON serialization (RFC 8785, ASCII-key subset)
  - Ed25519 signing and verification
  - PDPP mandate evaluation (rule grammar, spend caps, allowlists)
  - evaluation_hash and inputs_hash calculation
  - Expiry and idempotency enforcement
  - Full PASS and REJECT paths

Install: pip install cryptography
Run:     python pact_reference_v02.py
"""

import json
import hashlib
import base64
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey
)

# ─────────────────────────────────────────────────────────────
# PART 1: Canonical JSON  (RFC 8785 — ASCII key subset)
# Keys sorted lexicographically; no whitespace; no floats.
# ─────────────────────────────────────────────────────────────

def canonical_json(obj) -> bytes:
    """Deterministic JSON serialization per RFC 8785 (ASCII key subset)."""
    if isinstance(obj, dict):
        return (
            b"{"
            + b",".join(
                canonical_json(k) + b":" + canonical_json(v)
                for k, v in sorted(obj.items())
            )
            + b"}"
        )
    if isinstance(obj, list):
        return b"[" + b",".join(canonical_json(i) for i in obj) + b"]"
    if isinstance(obj, bool):
        return b"true" if obj else b"false"
    if isinstance(obj, int):
        return str(obj).encode()
    if isinstance(obj, float):
        raise ValueError("Floats prohibited in PACT — use integer cents")
    if isinstance(obj, str):
        return json.dumps(obj).encode()
    if obj is None:
        return b"null"
    raise ValueError(f"Unsupported type: {type(obj)}")


def sha256_hex(obj) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(obj)).hexdigest()


# ─────────────────────────────────────────────────────────────
# PART 2: PDPP Evaluator
# Implements the rule grammar from the PACT v1 whitepaper.
# ─────────────────────────────────────────────────────────────

def _resolve_field(ctx: dict, path: str):
    """Resolve 'inputs.key' or 'transaction.key' from evaluation context."""
    ns, _, key = path.partition(".")
    if ns not in ctx:
        raise ValueError(f"Unknown namespace '{ns}' in field path '{path}'")
    val = ctx[ns].get(key)
    if val is None:
        raise ValueError(f"Field '{path}' not found in context")
    return val


def _eval_arith(ctx: dict, expr: dict) -> int:
    """Integer arithmetic: add or sub only."""
    if "add" in expr:
        a, b = expr["add"]
        return _resolve_field(ctx, a) + _resolve_field(ctx, b)
    if "sub" in expr:
        a, b = expr["sub"]
        return _resolve_field(ctx, a) - _resolve_field(ctx, b)
    raise ValueError(f"Unknown arithmetic expression: {list(expr.keys())}")


_OPS = {
    "eq":     lambda a, b: a == b,
    "neq":    lambda a, b: a != b,
    "lt":     lambda a, b: a < b,
    "lte":    lambda a, b: a <= b,
    "gt":     lambda a, b: a > b,
    "gte":    lambda a, b: a >= b,
    "in":     lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}


def _eval_rule(ctx: dict, rule: dict) -> tuple:
    """Recursively evaluate a PDPP rule. Returns (bool, evidence_str)."""
    if "all_of" in rule:
        results = [_eval_rule(ctx, r) for r in rule["all_of"]]
        passed = all(r[0] for r in results)
        return passed, "AND[" + " | ".join(r[1] for r in results) + "]"

    if "any_of" in rule:
        results = [_eval_rule(ctx, r) for r in rule["any_of"]]
        passed = any(r[0] for r in results)
        return passed, "OR[" + " | ".join(r[1] for r in results) + "]"

    if "not" in rule:
        passed, ev = _eval_rule(ctx, rule["not"])
        return not passed, f"NOT[{ev}]"

    op = rule["op"]
    if op not in _OPS:
        raise ValueError(f"Unknown operator: '{op}'")

    if "expr" in rule:
        actual = _eval_arith(ctx, rule["expr"])
        ev = f"computed={actual} {op} {rule['value']}"
    else:
        actual = _resolve_field(ctx, rule["field"])
        ev = f"{rule['field']}={actual!r} {op} {rule['value']!r}"

    return _OPS[op](actual, rule["value"]), ev


def evaluate_mandate(mandate: dict, transaction: dict, inputs: dict) -> list:
    """
    Run all PDPP checks in a mandate against a proposed transaction.
    Returns list of {check_id, result, evidence_ref} dicts.
    """
    ctx = {"transaction": transaction, "inputs": inputs}
    results = []
    for check in mandate["checks"]:
        passed, evidence = _eval_rule(ctx, check["rule"])
        results.append({
            "check_id": check["check_id"],
            "result": "PASS" if passed else "FAIL",
            "evidence_ref": evidence,
        })
    return results


# ─────────────────────────────────────────────────────────────
# PART 3: PVP Builder
# ─────────────────────────────────────────────────────────────

def build_pvp(
    agent_id: str,
    principal_id: str,
    private_key: Ed25519PrivateKey,
    mandate: dict,
    transaction: dict,
    inputs: dict,
    request_id: str,
    expiry_seconds: int = 300,
) -> dict:
    """
    Build and sign a complete PVP.
    The signature covers the canonical PVP bytes (excluding the signature field).
    """
    mandate_hash = sha256_hex(mandate)
    checks = evaluate_mandate(mandate, transaction, inputs)

    # evaluation_hash binds checks to mandate hash — tamper-evident
    checks_block = {"checks": checks, "mandate_hash": mandate_hash}
    evaluation_hash = sha256_hex(checks_block)
    inputs_hash = sha256_hex(inputs)

    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=expiry_seconds)

    pvp = {
        "pvp_version": "1.0",
        "agent_id": agent_id,
        "principal_id": principal_id,
        "mandate_ref": {
            "mandate_id": mandate["mandate_id"],
            "mandate_hash": mandate_hash,
            "issued_at": mandate["issued_at"],
        },
        "transaction_intent": transaction,
        "policy_evaluation": {
            "policy_engine_id": "pact_reference_v0.2",
            "inputs_hash": inputs_hash,
            "checks": checks,
            "evaluation_hash": evaluation_hash,
        },
        "audit": {
            "created_at": now.isoformat(),
            "expires_at": expires.isoformat(),
            "request_id": request_id,
        },
    }

    sig_bytes = private_key.sign(canonical_json(pvp))
    pvp["signature"] = "ed25519:" + base64.b64encode(sig_bytes).decode()
    return pvp


# ─────────────────────────────────────────────────────────────
# PART 4: PVP Verifier
# ─────────────────────────────────────────────────────────────

_SEEN_REQUEST_IDS: set = set()  # In-memory idempotency store


def verify_pvp(
    pvp: dict,
    mandate: dict,
    public_key: Ed25519PublicKey,
    inputs: dict,
) -> tuple:
    """
    Verify a PVP. Returns (passed: bool, failures: list[str]).

    Checks (in order):
      1. Expiry
      2. Idempotency
      3. Mandate hash
      4. Inputs hash
      5. Evaluation hash
      6. Signature
      7. All policy checks PASS
      8. Re-run PDPP checks independently (since mandate is PDPP-conformant)
    """
    failures = []

    # 1. Expiry
    expires_at = datetime.fromisoformat(pvp["audit"]["expires_at"])
    if datetime.now(timezone.utc) > expires_at:
        failures.append("EXPIRED: PVP window has passed")

    # 2. Idempotency
    req_id = pvp["audit"]["request_id"]
    if req_id in _SEEN_REQUEST_IDS:
        failures.append(f"REPLAY: request_id '{req_id}' already processed")
    else:
        _SEEN_REQUEST_IDS.add(req_id)

    # 3. Mandate hash
    expected_mandate_hash = sha256_hex(mandate)
    if pvp["mandate_ref"]["mandate_hash"] != expected_mandate_hash:
        failures.append("MANDATE_MISMATCH: mandate hash does not match")

    # 4. Inputs hash
    expected_inputs_hash = sha256_hex(inputs)
    if pvp["policy_evaluation"]["inputs_hash"] != expected_inputs_hash:
        failures.append("INPUTS_MISMATCH: inputs hash does not match provided inputs")

    # 5. Evaluation hash
    checks_block = {
        "checks": pvp["policy_evaluation"]["checks"],
        "mandate_hash": pvp["mandate_ref"]["mandate_hash"],
    }
    expected_eval_hash = sha256_hex(checks_block)
    if pvp["policy_evaluation"]["evaluation_hash"] != expected_eval_hash:
        failures.append("EVAL_HASH_MISMATCH: evaluation hash is inconsistent")

    # 6. Signature
    sig_str = pvp.get("signature", "")
    if not sig_str.startswith("ed25519:"):
        failures.append("SIGNATURE_MISSING: no valid signature field")
    else:
        sig_bytes = base64.b64decode(sig_str[len("ed25519:"):])
        pvp_body = {k: v for k, v in pvp.items() if k != "signature"}
        try:
            public_key.verify(sig_bytes, canonical_json(pvp_body))
        except Exception:
            failures.append("SIGNATURE_INVALID: Ed25519 verification failed")

    # 7. All reported checks must be PASS
    for check in pvp["policy_evaluation"]["checks"]:
        if check["result"] != "PASS":
            failures.append(
                f"CHECK_FAILED: {check['check_id']} → {check['evidence_ref']}"
            )

    # 8. Independent re-run (PDPP mandates only — same inputs, same result)
    rerun = evaluate_mandate(mandate, pvp["transaction_intent"], inputs)
    for check in rerun:
        if check["result"] != "PASS":
            failures.append(
                f"RERUN_FAILED: {check['check_id']} → {check['evidence_ref']}"
            )

    return len(failures) == 0, failures


# ─────────────────────────────────────────────────────────────
# PART 5: Example Agent
# Smallest viable PACT transaction — no registry, no network.
# ─────────────────────────────────────────────────────────────

MANDATE = {
    "mandate_id": "nexusai_infra_agent_7_v2",
    "pdpp_version": "0.1",
    "principal_id": "nexusai_corp",
    "agent_id": "did:pact:nexusai:infra-agent-7",
    "issued_at": "2026-03-01T09:00:00+00:00",
    "checks": [
        {
            "check_id": "daily_spend_cap",
            "rule": {
                "all_of": [
                    {
                        "expr": {"add": ["inputs.amount_today_cents", "transaction.amount_cents"]},
                        "op": "lte",
                        "value": 100000,  # $1,000.00 daily cap
                    }
                ]
            },
        },
        {
            "check_id": "per_transaction_cap",
            "rule": {"field": "transaction.amount_cents", "op": "lte", "value": 75000},
        },
        {
            "check_id": "vendor_allowlist",
            "rule": {
                "field": "transaction.vendor_id",
                "op": "in",
                "value": ["vendor_computegrid_001", "vendor_aws_001", "vendor_gcp_001"],
            },
        },
        {
            "check_id": "category_constraint",
            "rule": {"field": "transaction.category", "op": "eq", "value": "cloud_infrastructure"},
        },
        {
            "check_id": "verified_vendor_required",
            "rule": {"field": "transaction.vendor_tier", "op": "eq", "value": "pact_verified"},
        },
    ],
}


def run_transaction(label, private_key, public_key, transaction, inputs, request_id):
    print(f"\n{'─'*60}")
    print(f"SCENARIO: {label}")
    print(f"  Vendor:        {transaction['vendor_id']}")
    print(f"  Amount:        ${transaction['amount_cents']/100:.2f}")
    print(f"  Spent today:   ${inputs['amount_today_cents']/100:.2f}")
    print(f"  Daily cap:     $1,000.00")

    pvp = build_pvp(
        agent_id="did:pact:nexusai:infra-agent-7",
        principal_id="nexusai_corp",
        private_key=private_key,
        mandate=MANDATE,
        transaction=transaction,
        inputs=inputs,
        request_id=request_id,
    )

    passed, failures = verify_pvp(pvp, MANDATE, public_key, inputs)

    print(f"\n  Policy checks:")
    for check in pvp["policy_evaluation"]["checks"]:
        icon = "✓" if check["result"] == "PASS" else "✗"
        print(f"    {icon} {check['check_id']}")
        print(f"        {check['evidence_ref']}")

    print(f"\n  Signature:       {pvp['signature'][:48]}...")
    print(f"  Mandate hash:    {pvp['mandate_ref']['mandate_hash'][:48]}...")
    print(f"  Eval hash:       {pvp['policy_evaluation']['evaluation_hash'][:48]}...")

    print(f"\n{'═'*60}")
    if passed:
        print(f"  RESULT: TRANSACTION CLEARED ✓")
        print(f"  Payment rail may proceed.")
    else:
        print(f"  RESULT: TRANSACTION REJECTED ✗")
        for f in failures:
            print(f"  → {f}")
        print(f"  Agent should escalate to human principal.")
    print(f"{'═'*60}")


def main():
    print("=" * 60)
    print("PACT Protocol — Reference Implementation v0.2")
    print("Canonical JSON | Ed25519 | PDPP | Expiry | Idempotency")
    print("=" * 60)

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Scenario A: Valid transaction — should PASS
    run_transaction(
        label="Valid purchase within policy",
        private_key=private_key,
        public_key=public_key,
        transaction={
            "vendor_id": "vendor_computegrid_001",
            "vendor_tier": "pact_verified",
            "amount_cents": 31200,  # $312.00
            "category": "cloud_infrastructure",
            "purpose": "GPU expansion — ML job nexusai-train-0291",
        },
        inputs={"amount_today_cents": 68800},  # $688 already spent
        request_id="req_aaa111bbb222ccc333",
    )

    # Scenario B: Daily cap exceeded — should REJECT
    run_transaction(
        label="Daily cap exceeded",
        private_key=private_key,
        public_key=public_key,
        transaction={
            "vendor_id": "vendor_computegrid_001",
            "vendor_tier": "pact_verified",
            "amount_cents": 31200,  # $312 would push to $1,212 > $1,000 cap
            "category": "cloud_infrastructure",
            "purpose": "GPU expansion — second job",
        },
        inputs={"amount_today_cents": 90000},  # $900 already spent
        request_id="req_ddd444eee555fff666",
    )

    # Scenario C: Vendor not on allowlist — should REJECT
    run_transaction(
        label="Vendor not on allowlist",
        private_key=private_key,
        public_key=public_key,
        transaction={
            "vendor_id": "vendor_unknown_xyz",
            "vendor_tier": "pact_verified",
            "amount_cents": 5000,
            "category": "cloud_infrastructure",
            "purpose": "Experimental compute provider",
        },
        inputs={"amount_today_cents": 10000},
        request_id="req_ggg777hhh888iii999",
    )


if __name__ == "__main__":
    main()
