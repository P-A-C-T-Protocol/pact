"""
PACT Protocol — Reference Implementation v0.1
Protocol for Agentic Commerce and Trust

This script demonstrates a complete A2A (agent-to-agent) transaction using PACT.
It uses real Ed25519 cryptography — the same signing standard used in production
systems worldwide. No external services, no internet connection, no money moves.

Scenario: InfraAgent-7 (operated by NexusAI) purchases GPU compute from ComputeGrid.

Author: TJ Rosell
Contact: trosellv@gmail.com
Version: 0.1 — March 2026
"""

import json
import hashlib
import datetime
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat, PrivateFormat, NoEncryption
)
from cryptography.exceptions import InvalidSignature


# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def sha256(data: str) -> str:
    """Hash any string to a SHA-256 hex digest."""
    return hashlib.sha256(data.encode()).hexdigest()

def canonical(obj: dict) -> str:
    """Serialize a dict to a stable, sorted JSON string (for consistent hashing)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def now_iso() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def expiry_iso(minutes: int = 5) -> str:
    t = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def header(text: str):
    print(f"\n{'─' * 60}")
    print(f"  {text}")
    print(f"{'─' * 60}")

def ok(text: str):
    print(f"  ✓  {text}")

def info(label: str, value: str):
    print(f"  {label:<28} {value}")

def fail(text: str):
    print(f"  ✗  {text}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — GENERATE AGENT IDENTITY
# ─────────────────────────────────────────────────────────────────────────────

header("STEP 1 / 5  —  Generate Agent Identity")

# In production, this key pair is generated once and stored securely by the
# agent's principal. The private key signs PVPs. The public key is registered
# in the PACT registry so any verifier can confirm signatures.

private_key = Ed25519PrivateKey.generate()
public_key  = private_key.public_key()

pub_bytes = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
pub_hex   = pub_bytes.hex()

AGENT_ID    = "did:pact:nexusai:infra-agent-7"
PRINCIPAL   = "nexusai_corp"

info("Agent ID:",      AGENT_ID)
info("Principal:",     PRINCIPAL)
info("Public Key:",    pub_hex[:32] + "...")
ok("Ed25519 key pair generated — private key stays with agent, public key goes to registry")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — REGISTER MANDATE
# ─────────────────────────────────────────────────────────────────────────────

header("STEP 2 / 5  —  Register Agent Mandate")

# The mandate defines what this agent is authorised to buy.
# In production this is stored in the PACT registry.
# The PVP carries only the hash — auditors look up the full document.

mandate = {
    "mandate_id":       "nexusai_infra_agent_7_v2",
    "principal":        "nexusai_corp",
    "agent_id":         AGENT_ID,
    "categories":       ["cloud_infrastructure"],
    "spend_cap":        {"daily": 1000, "currency": "USD"},
    "vendor_require":   "pact_verified_only",
    "perf_floor":       {"metric": "tflops_per_dollar", "min": 80},
    "escalate_above":   750,
}

MANDATE_HASH = "sha256:" + sha256(canonical(mandate))

info("Mandate ID:",    mandate["mandate_id"])
info("Spend Cap:",     f"${mandate['spend_cap']['daily']}/day USD")
info("Vendor Req:",    mandate["vendor_require"])
info("Perf Floor:",    f">= {mandate['perf_floor']['min']} TFLOPs/$")
info("Escalate At:",   f"${mandate['escalate_above']}/day")
info("Mandate Hash:",  MANDATE_HASH[:40] + "...")
ok("Mandate hashed and registered")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — BUILD THE PVP
# ─────────────────────────────────────────────────────────────────────────────

header("STEP 3 / 5  —  Build Proof of Valid Purchase (PVP)")

# ── Simulate the state at transaction time ────────────────────────────────────
SPEND_TODAY      = 688.00   # already spent today before this transaction
NEW_SPEND        = 312.00   # this purchase
VENDOR_TFLOPS    = 94.2     # TFLOPs per dollar from ComputeGrid's listing
VENDOR_TIER      = "verified"
VENDOR_ID        = "vendor_computegrid_001"
DAILY_CAP        = mandate["spend_cap"]["daily"]
PERF_FLOOR_MIN   = mandate["perf_floor"]["min"]

# ── Run constraint checks ─────────────────────────────────────────────────────
# v0.1: JSON assertion checks. Each check declares its result and supporting
# data. The block is hashed together with the mandate hash — so any tampering
# with either the checks or the mandate breaks the proof_hash verification.
# ZK proofs replace this in v0.2 for privacy-preserving verification.

constraint_checks = [
    {
        "ref":    "cost_cap_1000_daily",
        "result": "PASS" if (SPEND_TODAY + NEW_SPEND) <= DAILY_CAP else "FAIL",
        "detail": f"spend_today={SPEND_TODAY}, new={NEW_SPEND}, cap={DAILY_CAP}, total={SPEND_TODAY + NEW_SPEND}"
    },
    {
        "ref":    "perf_floor_80tflops",
        "result": "PASS" if VENDOR_TFLOPS >= PERF_FLOOR_MIN else "FAIL",
        "detail": f"vendor_tflops_per_dollar={VENDOR_TFLOPS}, floor={PERF_FLOOR_MIN}"
    },
    {
        "ref":    "verified_vendor_only",
        "result": "PASS" if VENDOR_TIER == "verified" else "FAIL",
        "detail": f"vendor_tier={VENDOR_TIER}"
    },
]

all_pass = all(c["result"] == "PASS" for c in constraint_checks)

constraint_proof_block = {
    "version": "v0.1-json-assertion",
    "note":    "v0.1 uses hash-verified JSON assertions. ZK proofs replace this in v0.2.",
    "checks":  constraint_checks,
}

PROOF_HASH = "sha256:" + sha256(canonical(constraint_proof_block) + MANDATE_HASH)
constraint_proof_block["proof_hash"] = PROOF_HASH

TIMESTAMP = now_iso()
EXPIRY    = expiry_iso(minutes=5)

# ── Assemble the full PVP ─────────────────────────────────────────────────────
pvp = {
    "agent_id":      AGENT_ID,
    "agent_version": "sha256:" + sha256("infra-agent-7-codebase-v2.1"),
    "principal_id":  PRINCIPAL,
    "mandate_hash":  MANDATE_HASH,
    "transaction_intent": {
        "vendor_id":       VENDOR_ID,
        "vendor_tier":     VENDOR_TIER,
        "amount":          {"value": NEW_SPEND, "currency": "USD"},
        "category":        "cloud_infrastructure",
        "purpose":         "GPU expansion — ML job nexusai-train-0291, projected 4hr duration",
        "constraint_refs": [c["ref"] for c in constraint_checks],
    },
    "constraint_proof": constraint_proof_block,
    "timestamp":  TIMESTAMP,
    "expiry":     EXPIRY,
    "anchor_ref": "NOT_ENABLED_V01",  # Hedera HCS anchoring — enable in v0.2
}

info("Vendor:",          VENDOR_ID)
info("Amount:",          f"${NEW_SPEND} USD")
info("Category:",        pvp["transaction_intent"]["category"])
info("Timestamp:",       TIMESTAMP)
info("Expiry:",          EXPIRY)
info("Proof Hash:",      PROOF_HASH[:40] + "...")
ok("PVP assembled — all fields populated")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — SIGN THE PVP
# ─────────────────────────────────────────────────────────────────────────────

header("STEP 4 / 5  —  Sign PVP (InfraAgent-7)")

# The agent signs the canonical (sorted, stable) JSON of the PVP body.
# This signature is what ComputeGrid will verify using the public key
# retrieved from the PACT registry.

pvp_body        = canonical(pvp)
pvp_body_bytes  = pvp_body.encode()
signature_bytes = private_key.sign(pvp_body_bytes)
signature_hex   = "ed25519:" + signature_bytes.hex()

pvp["signature"] = signature_hex

info("Signature:",  signature_hex[:48] + "...")
ok("PVP signed with Ed25519 private key — only InfraAgent-7 could produce this")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — VERIFY (ComputeGrid Application Layer)
# ─────────────────────────────────────────────────────────────────────────────

header("STEP 5 / 5  —  Verify PVP (ComputeGrid Application Layer)")
print()
print("  ComputeGrid receives the signed PVP.")
print("  PACT verification runs before any call to Stripe.\n")

verification_passed = True

# ── Check 1: Signature ───────────────────────────────────────────────────────
# ComputeGrid retrieves InfraAgent-7's public key from the PACT registry
# using the agent_id in the PVP, then verifies the signature.

sig_bytes_received = bytes.fromhex(signature_hex.replace("ed25519:", ""))
pvp_without_sig = {k: v for k, v in pvp.items() if k != "signature"}

try:
    public_key.verify(sig_bytes_received, canonical(pvp_without_sig).encode())
    ok("Check 1 — Signature valid (public key from PACT registry confirms InfraAgent-7 signed this)")
except InvalidSignature:
    fail("Check 1 — Signature INVALID")
    verification_passed = False

# ── Check 2: Mandate Hash ────────────────────────────────────────────────────
# ComputeGrid looks up InfraAgent-7's current mandate hash in the registry
# and confirms it matches what's in the PVP.

expected_mandate_hash = "sha256:" + sha256(canonical(mandate))
if pvp["mandate_hash"] == expected_mandate_hash:
    ok("Check 2 — Mandate hash matches registry record (mandate is current and unmodified)")
else:
    fail("Check 2 — Mandate hash MISMATCH — mandate may have been revoked or tampered")
    verification_passed = False

# ── Check 3: Constraint Proof ────────────────────────────────────────────────
# Recompute the proof_hash from the checks block + mandate_hash.
# If it matches the signed value, the constraints were honestly declared.

proof_block_without_hash = {k: v for k, v in constraint_proof_block.items() if k != "proof_hash"}
recomputed_proof_hash = "sha256:" + sha256(canonical(proof_block_without_hash) + MANDATE_HASH)

if recomputed_proof_hash == PROOF_HASH:
    ok("Check 3 — Constraint proof hash verified")
    for c in constraint_checks:
        status = "✓" if c["result"] == "PASS" else "✗"
        print(f"           {status}  {c['ref']}: {c['detail']}")
else:
    fail("Check 3 — Constraint proof hash MISMATCH — proof may have been altered")
    verification_passed = False

# ── Check 4: Expiry ───────────────────────────────────────────────────────────
expiry_dt   = datetime.datetime.strptime(EXPIRY, "%Y-%m-%dT%H:%M:%SZ")
now_dt      = datetime.datetime.utcnow()
seconds_old = (now_dt - datetime.datetime.strptime(TIMESTAMP, "%Y-%m-%dT%H:%M:%SZ")).seconds

if now_dt < expiry_dt:
    ok(f"Check 4 — Expiry valid (PVP is {seconds_old}s old, window is 5 minutes)")
else:
    fail("Check 4 — PVP EXPIRED — transaction window has passed")
    verification_passed = False


# ─────────────────────────────────────────────────────────────────────────────
# RESULT
# ─────────────────────────────────────────────────────────────────────────────

print()
print("  " + "═" * 56)

if verification_passed:
    print()
    print("  ✓  TRANSACTION CLEARED")
    print()
    print(f"  PACT authorises ComputeGrid to charge ${NEW_SPEND} USD")
    print(f"  via configured payment rail (e.g. Stripe).")
    print()
    print(f"  Agent:    {AGENT_ID}")
    print(f"  Vendor:   {VENDOR_ID}")
    print(f"  Amount:   ${NEW_SPEND} USD")
    print(f"  Purpose:  {pvp['transaction_intent']['purpose']}")
    print(f"  Mandate:  {MANDATE_HASH[:40]}...")
    print(f"  Signed:   {signature_hex[:40]}...")
    print()
    print("  PACT never touched the payment rail.")
    print("  Stripe only gets called after this point.")
    print("  No human was involved.")
else:
    print()
    print("  ✗  TRANSACTION REJECTED — one or more checks failed.")
    print("  Stripe will NOT be called.")
    print("  Agent receives structured rejection + escalation request.")

print()
print("  " + "═" * 56)


# ─────────────────────────────────────────────────────────────────────────────
# BONUS: SHOW THE FULL SIGNED PVP
# ─────────────────────────────────────────────────────────────────────────────

print()
print("\n" + "─" * 60)
print("  FULL SIGNED PVP (what ComputeGrid received)")
print("─" * 60)
print(json.dumps(pvp, indent=2))
print()
print("─" * 60)
print("  PACT Protocol v0.1 — reference implementation complete.")
print("  github.com/pact-protocol")
print("─" * 60 + "\n")
