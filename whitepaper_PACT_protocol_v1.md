# PACT: The Protocol for Agentic Commerce and Trust
### A Standard for Policy-Bound Agent Procurement and Verifiable Transaction Attestations

**Author:** TJ Rosell
**Date:** March 2026
**Status:** Draft v1.0 — Open for Collaboration
**Contact:** trosellv@gmail.com

---

> *"MCP solved how agents connect to tools. PACT solves how agents transact in markets."*

---

## Abstract

Artificial intelligence agents are becoming digital workers — autonomous systems that perform tasks, manage workflows, and increasingly operate with economic consequence. Yet the infrastructure for agents to participate in commerce as **policy-bound operators acting under delegated authority** does not exist in a usable, open, developer-first form.

The dominant wave of agentic payment solutions — from Mastercard Agent Pay to Stripe's Agentic Commerce Suite — addresses the human→agent→merchant layer: a person delegating a purchase to their AI assistant. This paper proposes a different layer: **agent-initiated procurement under delegated policy**, where an AI agent with a defined mandate can autonomously procure common business resources — compute, SaaS tools, contracted services, data access, physical goods — with verifiable evidence that every transaction was consistent with its authorization.

We introduce **PACT** — the Protocol for Agentic Commerce and Trust — an open standard comprising:

1. **PVP (Proof of Valid Purchase)**: a signed transaction attestation binding the purchase intent to the agent's active mandate and deterministic policy checks
2. A **SDK** that standardizes PVP generation, verification, and policy evaluation
3. An optional, federated **Registry** supporting agent identity, vendor attestations, and reputation signals

PACT does not move money. It sits above existing payment rails and defines a **decision integrity and auditability layer** that makes agent-initiated procurement trustworthy and automatable within bounded risk.

The design choices throughout this specification — optional registry, thin principal model, chain-agnostic anchoring — reflect a deliberate intent: PACT should work whether the company deploying agents is human-run today or agent-run in the future. Like TCP/IP, the protocol does not care who is behind the connection. It standardizes the exchange. The governance layer is expressed through mandates, not baked into the protocol. The structure survives both worlds.

---

## 1. The Problem

### 1.1 Agents Can't Procure Safely Without Breaking Controls

Consider what it means for a company to deploy a fleet of AI agents today:

- An infrastructure agent that needs to provision additional cloud capacity when workloads spike
- A procurement agent that needs to subscribe to SaaS tools for an active project
- A project agent that needs to engage a contracted service provider for a bounded scope
- A data agent that needs to purchase access to a proprietary dataset in real-time
- A logistics agent that needs to book freight or last-mile delivery

Each of these is technically possible. None of them are commercially safe today. Organizations deploying agents currently face two bad options:

**Option A — Human approval for each transaction.** Safe, but defeats the efficiency gain. Agents that can't act without a human in the loop are expensive automation, not autonomous workers.

**Option B — Unconstrained credentials.** Agents given a corporate card or API key with no formal constraint structure. Fast, but a fraud and liability nightmare. One compromised or misbehaving agent can cause serious financial damage with no audit trail to reconstruct what happened or who authorized it.

PACT's goal is not "agents can buy anything." It is: **enable low-risk, policy-bounded procurement with strong audit trails, and force escalation for everything outside that boundary.**

### 1.2 What Exists Today — And Why It Doesn't Solve This

The major financial players are moving fast, but they are building a different layer:

**Consumer delegation layer (human→agent→merchant):**

| Player | Product | What It Solves |
|---|---|---|
| Mastercard | Agent Pay / Agentic Tokens | Human delegates consumer purchases to their AI |
| Visa | Trusted Agent Protocol | Distinguishing bots from legitimate consumer agents at checkout |
| Stripe | Agentic Commerce Suite / SPTs | Consumer AI completes purchases using saved payment methods |
| Google | Universal Commerce Protocol | Open standard for AI shopping agents across retail platforms |
| PayPal | Agent Ready | AI agents completing purchases on behalf of consumers |
| Skyfire | KYAPay | Agent identity and payment for human-to-agent-to-merchant flows |

**Open protocol efforts (agent authorization and identity layer):**

| Project | Approach | Key Difference from PACT |
|---|---|---|
| Google AP2 | Agent Mandates — cryptographically signed verifiable proof of user instructions | Focused on consumer/user delegation; human principal is central to the design |
| Visa Trusted Agent Protocol | Trust establishment between AI agents and merchants at checkout | Solves consumer checkout trust, not enterprise autonomous procurement |
| OAPP (Open Agent Payment Protocol) | Payment Mandates for scoped agent authorization, v0.1 published Oct 2025 | Payment-rail-first; policy evaluation and audit trail not the focus |
| O4DB Protocol | Sovereign agentic commerce, buyer-side ranking, volume-weighted reputation, patent pending | Commerce discovery and reputation; not enterprise mandate/policy architecture |
| Oath Protocol | Cryptographically verifiable human intent, local-first, public domain | Human intent verification; not agent-to-agent autonomous procurement |
| Sanna | Governance rule enforcement at execution time, cryptographic receipts | Execution-time enforcement layer; complementary to PACT's authorization layer |

The pattern across the consumer delegation layer is consistent: **the human remains the economic principal.** The agent is a proxy. This is valuable and the market is large.

But it is not what we are building.

PACT addresses the layer none of these players have fully built: **enterprise-grade autonomous agent procurement**, where the agent is the operational actor, the principal remains legally responsible, and the protocol provides the authorization evidence, audit trail, and vendor attestation infrastructure that makes autonomous procurement safe enough to remove humans from routine approvals. This means machine-readable mandates, deterministic policy checks, structured audit logs, and verifiable authorization evidence that integrates with existing finance and compliance workflows.

The closest existing work is Google's AP2, which introduces the concept of Agent Mandates and is the most technically adjacent to PACT. The key distinction is scope: AP2 is designed for user-delegated consumer purchasing; PACT is designed for enterprise-grade autonomous procurement where agents operate without human approval loops. The two protocols are potentially complementary — an enterprise could use AP2 for consumer-facing agent interactions and PACT for internal fleet procurement — and PACT's architecture is designed to be interoperable with AP2's mandate format where possible.

---

## 2. Core Concepts

### 2.1 The Agent as Policy-Bound Operator

The framing here is precise and intentional:

**Current paradigm:** Human intent → Agent action → Merchant transaction
**PACT paradigm:** Principal policy → Agent mandate → Agent decision → **Verifiable authorization evidence** → Transaction

In PACT, the agent is not a legal actor. It is a **delegated operator**. The principal — a company, a human, a legal entity — remains the counterparty and bears legal responsibility. The agent generates standardized evidence that it acted within its delegated authority.

This is analogous to a senior employee with a company card. They are not asking their CEO whether to buy office supplies. They have a delegated authority, a spending category, a dollar limit, and an expectation that they will exercise judgment. The CFO gets involved only for genuine anomalies. PACT is the infrastructure that makes this possible for AI agents — at scale, with cryptographic evidence instead of implicit trust.

The agent is not legally independent. It is **operationally autonomous but economically attributable** — self-directed in execution, but with a clear principal bearing legal and financial responsibility for its actions. That is the realistic near-term target, and it is what makes the protocol commercially credible.

Think of PACT like TCP/IP. TCP doesn't care who owns the server. It just standardizes packet exchange. PACT doesn't care whether the principal behind an agent is a human CFO or a board-level policy agent running an autonomous firm. It standardizes economic intent exchange. The governance layer — who authorized what, under what constraints — is expressed through the mandate. The protocol itself remains neutral about organizational structure.

### 2.2 Trust Grows With Track Record

Human organizations understand that trust is earned, not assumed. A new employee doesn't get a corporate card on day one. A vendor doesn't get net-60 terms on a first order. PACT's architecture mirrors this:

- Agents begin with constrained spending authority defined by their principal
- Limits expand as the agent accumulates verified transaction history
- The registry records verified transactions, building a reputation signal
- Principals set the policy for how their agents' limits evolve

PACT does not dictate how organizations trust their agents. It provides the infrastructure through which that trust is expressed, verified, and recorded.

### 2.3 The Key Insight: Authorization Evidence, Not Permission

The bottleneck in today's agentic systems is the approval loop. Every time an agent wants to take a commercially consequential action, it either acts unilaterally (dangerous) or pings a human (inefficient). PACT proposes a third path: **standardized authorization evidence that a transaction was within delegated policy.**

Before a transaction clears, the purchasing agent generates a PVP — a signed attestation that proves:

1. The agent identity is bound to a principal (identity and delegation)
2. The agent's mandate is active and applicable (authorization)
3. The transaction intent satisfies deterministic policy checks (validity)
4. The vendor status is known (attestation, tier, allowlist)
5. The record is logged for audit and dispute

**Critical clarification for v0.1:** PACT does not "prove reasoning." It proves:
- Which policy checks ran
- What inputs they used
- What outputs they produced
- That they were signed by the agent identity under a known mandate

PACT v0.2+ can add privacy-preserving proofs for specific check families. v0.1 optimizes for adoption, interoperability, and auditability — the shippable thing.

### 2.4 Worked Example: Agent Procures Compute Autonomously

*This traces a complete A2A transaction from agent decision to provisioned resource.*

**The Setup**

NexusAI operates an infrastructure agent, `InfraAgent-7`, responsible for maintaining compute resources for active ML workloads. Its mandate:

```
MANDATE: nexusai_infra_agent_7_v2
{
  principal:       "nexusai_corp"
  categories:      ["cloud_infrastructure"]
  spend_cap:       { daily: 1000, currency: "USD" }
  vendor_require:  "pact_verified_only"
  perf_floor:      { metric: "tflops_per_dollar", min: 80 }
  escalate_above:  750   // USD daily — flag to human if approaching cap
}
mandate_hash: "sha256:7b2e91...c034"
```

At 2:14 AM, `InfraAgent-7` detects its GPU allocation will be exhausted in 47 minutes. No human is awake. No human needs to be.

**Step 1 — Registry Lookup**

`InfraAgent-7` queries the PACT registry for Verified vendors in `cloud_infrastructure`. Three results returned. Agent selects `ComputeGrid` (registry ID: `vendor_computegrid_001`) — lowest cost-per-TFLOP among Verified vendors, 99.94% uptime in registry.

**Step 2 — PVP Generation**

```
PVP {
  pvp_version:     "1.0"
  agent_id:        "did:pact:nexusai:infra-agent-7"
  principal_id:    "nexusai_corp"
  delegation_ref:  null
  mandate_ref: {
    mandate_id:    "nexusai_infra_agent_7_v2"
    mandate_hash:  "sha256:7b2e91...c034"
    issued_at:     "2026-03-01T09:00:00Z"
  }

  transaction_intent: {
    vendor_id:          "vendor_computegrid_001"
    vendor_attestations: ["pact_verified", "kyb_complete"]
    amount:             { value: 312.00, currency: "USD" }
    category:           "cloud_infrastructure"
    purpose:            "GPU expansion — ML job nexusai-train-0291, projected 4hr duration"
  }

  policy_evaluation: {
    policy_engine_id:   "pact_ref_engine_v0.1"
    inputs_hash:        "sha256:a1b2c3...d4e5"
    checks: [
      { check_id: "cost_cap_daily",      result: "PASS", evidence_ref: "spend_today=688, new=312, cap=1000" },
      { check_id: "perf_floor_tflops",   result: "PASS", evidence_ref: "computegrid_tflops_per_dollar=94.2" },
      { check_id: "verified_vendor",     result: "PASS", evidence_ref: "vendor_tier=pact_verified" }
    ]
    evaluation_hash:    "sha256:e7f3a1...8c02"
  }

  audit: {
    created_at:   "2026-03-03T02:14:33Z"
    expires_at:   "2026-03-03T02:19:33Z"
    request_id:   "req_7f3a92b1"
    anchors:      [{ type: "dlttx", network: "hedera", ref: "0.0.4829301@1709428473.004" }]
  }

  signature:  "ed25519:3045...f9a2"
}
```

**Step 3 — Application-Layer Verification at ComputeGrid**

ComputeGrid's PACT-enabled endpoint runs four checks in under 200ms:

1. **Signature valid** — Ed25519 public key retrieved from PACT registry, signature verified ✓
2. **Mandate hash matches** — registry confirms `sha256:7b2e91...c034` is active mandate for this agent ✓
3. **Policy evaluation hashes consistent** — evaluation_hash recomputed against checks block; matches signed value ✓
4. **Expiry within bounds** — PVP generated 18 seconds ago; 5-minute window still valid ✓

Only after all four checks pass does ComputeGrid call Stripe. PACT never touches the payment rail. If any check had failed, Stripe would never have been called and the agent receives a structured rejection with the specific failed constraint.

**Step 4 — Result**

No human approved this. No Slack message at 2 AM. Total time from agent decision to compute provisioned: 41 seconds. At 9 AM the CFO sees a complete line item — agent identity, mandate reference, policy check results, audit timestamp — without having been woken up.

---

## 3. The PACT Architecture

PACT is a **two-layer standard plus optional network services**:

- **Core Standard (required):** PVP format, verification rules, canonicalization
- **SDK (required):** reference implementation for PVP generation and verification, plus policy evaluation hooks
- **Registry (optional):** agent identity discovery, vendor attestations, reputation signals
- **Anchoring (optional):** public timestamping of PVP hashes — chain-agnostic

This decomposition matters. Making the registry and anchoring optional means the protocol functions without centralized infrastructure, avoids "PACT is a gatekeeper" criticism, and is adoptable inside enterprises that run their own internal registries.

### 3.1 Component 1: Proof of Valid Purchase (PVP) — The Core Standard

The irreducible primitive of PACT is a **canonical, signed, machine-readable Authorization Attestation Object**. Everything else in this standard — the registry, the SDK, the anchoring layer — is infrastructure built around producing, transmitting, and verifying that object. If only one thing gets standardized, it is this. That object is the PVP.

The PVP is the signed data object generated by the purchasing agent before any transaction is submitted. It is the unit of trust in PACT.

```
PVP {
  pvp_version:       "1.0"
  agent_id:          <did:pact:<org-id>:<agent-name> — see Section 3.5>
  principal_id:      <legal principal reference>
  delegation_ref:    <optional: parent agent / chain>
  mandate_ref: {
    mandate_id:      <stable ID>
    mandate_hash:    <hash of mandate document>
    issued_at:       <timestamp>
  }

  transaction_intent: {
    vendor_id:            <vendor identifier>
    vendor_attestations:  [<kyb>, <allowlist>, <catalog_ref>...]
    amount:               <value + currency>
    category:             <standard category>
    line_items:           <optional structured items>
    purpose:              <human-readable string>
  }

  policy_evaluation: {
    policy_engine_id:   <implementation identifier>
    inputs_hash:        <hash of relevant inputs>
    checks: [
      { check_id: "...", result: "PASS|FAIL", evidence_ref: "..." }
    ]
    evaluation_hash:    <hash of normalized checks block>
  }

  audit: {
    created_at:   <ISO 8601>
    expires_at:   <ISO 8601>
    request_id:   <idempotency key>
    anchors:      [<optional timestamp anchors>]
  }

  signature:  <Ed25519 signature over canonical PVP bytes>
}
```

**Verifier requirements (v0.1):**

- Verify Ed25519 signature against the agent's registered public key
- Verify mandate hash matches the presented mandate document (SHA-256)
- Verify policy_evaluation.evaluation_hash matches SHA-256(canonical(checks block))
- Verify policy_evaluation.inputs_hash matches SHA-256(canonical(inputs))
- Optionally re-run policy checks — only when the mandate conforms to the PACT Declarative Policy Profile defined in Section 3.1.1
- Enforce expiry: reject if current time > audit.expires_at
- Enforce idempotency: reject if audit.request_id has been seen within the expiry window

**3.1.1 Policy Language Constraints — PACT Declarative Policy Profile (PDPP)**

The "optionally re-run" verifier clause only applies when mandates conform to the v0.1 PACT Declarative Policy Profile (PDPP). Without a constrained policy language, "deterministic" is meaningless and cross-party interoperability is imaginary. PDPP v0.1 is formally defined below.

**Allowed operators:**

| Operator | Symbol | Applies to |
|---|---|---|
| Equal | `eq` | integers, strings |
| Not equal | `neq` | integers, strings |
| Less than | `lt` | integers |
| Less than or equal | `lte` | integers |
| Greater than | `gt` | integers |
| Greater than or equal | `gte` | integers |
| Member of set | `in` | string against array of strings |
| Not member of set | `not_in` | string against array of strings |

**Rule grammar:**

```
RULE        := SIMPLE | COMPOUND
SIMPLE      := { "field": FIELD_PATH, "op": OPERATOR, "value": LITERAL }
             | { "expr": ARITH_EXPR, "op": OPERATOR, "value": INTEGER }
COMPOUND    := { "all_of": [RULE, ...] }   // logical AND
             | { "any_of": [RULE, ...] }   // logical OR
             | { "not": RULE }             // logical NOT
ARITH_EXPR  := { "add": [FIELD_PATH, FIELD_PATH] }   // integer addition only
             | { "sub": [FIELD_PATH, FIELD_PATH] }   // integer subtraction only
FIELD_PATH  := "inputs.<key>" | "transaction.<key>"
LITERAL     := INTEGER | STRING | [STRING, ...]
```

**What is and is not allowed in v0.1:**
- ✓ Comparison of embedded integer inputs against literal constants
- ✓ Membership check of transaction fields against declared allowlists
- ✓ Nested conditions via `all_of` / `any_of` / `not`
- ✓ Simple integer addition and subtraction (required for spend cap calculations)
- ✗ Multiplication, division, or modulo
- ✗ String manipulation or pattern matching
- ✗ External data lookups at evaluation time
- ✗ Floating point — all amounts in smallest integer currency unit (cents, not dollars)
- ✗ Aggregation functions (sum over history, averages)
- ✗ Conditions dependent on external clocks beyond PVP audit.created_at / expires_at

**How spend counters work without external state:** Running totals (e.g., `amount_today_cents`) are embedded inputs in the PVP's `policy_evaluation.inputs_hash` at signing time. The agent is responsible for providing the current value at signing. Verifiers check that the embedded value produces a PASS; they do not independently fetch or compute the running total. This means spend counters are auditable but not independently enforced — a dishonest agent can lie about `amount_today_cents`. The principal's audit system is the enforcement mechanism; PACT provides the evidence trail.

**Canonical evaluation order:** Checks are evaluated in declaration order. Key ordering within JSON objects follows RFC 8785 (JSON Canonicalization Scheme). The same mandate + same inputs must produce the same evaluation_hash on any conforming implementation.

**Determinism definition:** A policy check is deterministic under PACT v0.1 if and only if: (a) it is expressed in PDPP-conformant format, (b) all inputs are embedded in the PVP, and (c) any verifier running the same check against the same inputs produces an identical PASS/FAIL result with no side effects.

**Formal PDPP mandate example (JSON):**

```json
{
  "mandate_id": "nexusai_infra_agent_7_v2",
  "pdpp_version": "0.1",
  "principal_id": "nexusai_corp",
  "agent_id": "did:pact:nexusai:infra-agent-7",
  "issued_at": "2026-03-01T09:00:00Z",
  "checks": [
    {
      "check_id": "daily_spend_cap",
      "rule": {
        "all_of": [
          { "expr": { "add": ["inputs.amount_today_cents", "transaction.amount_cents"] },
            "op": "lte", "value": 100000 }
        ]
      }
    },
    {
      "check_id": "per_transaction_cap",
      "rule": { "field": "transaction.amount_cents", "op": "lte", "value": 75000 }
    },
    {
      "check_id": "vendor_allowlist",
      "rule": { "field": "transaction.vendor_id", "op": "in",
                "value": ["vendor_computegrid_001", "vendor_aws_001", "vendor_gcp_001"] }
    },
    {
      "check_id": "category_constraint",
      "rule": { "field": "transaction.category", "op": "eq", "value": "cloud_infrastructure" }
    },
    {
      "check_id": "verified_vendor_required",
      "rule": { "field": "transaction.vendor_tier", "op": "eq", "value": "pact_verified" }
    }
  ]
}
```

**PDPP covers the 80% case.** Replayable PDPP mandates are designed to cover the majority of routine autonomous procurement patterns: spend caps (daily, monthly, per-transaction), vendor allowlists, category constraints, and time-bounded subscription renewals. These are the common bounded procurement patterns that enterprises need first. Non-replayable mandates — those requiring real-time FX rates, live inventory checks, external credit scoring, or other dynamic inputs — are valid PACT mandates but cannot be independently re-verified by third parties. They exist for edge cases, not the core. The expectation is that most agent mandates in production will be PDPP-conformant.

Non-conforming policy checks MUST be declared as `non_replayable: true` in the PVP. They remain auditable via signed evidence_ref fields but cannot be replayed by verifiers. This is the v0.1 tradeoff: the policy language is intentionally constrained to guarantee interoperability on the cases that matter most. v0.2 expands the profile.

**v0.1 innovation:** A standard way to represent "what was authorized + what checks ran + what was purchased" so vendors, payment rails, and auditors can automate trust decisions without custom integrations.

**v0.2+ upgrade:** Privacy-preserving proofs for limited check families (e.g., "under spend cap," "vendor allowlisted") without revealing full policy inputs. The schema is forward-compatible.

**On the signature mechanism:** PACT uses **Ed25519** — open, unencumbered, no patent restrictions, supported by all major languages and platforms. Any developer can implement independently without licensing obligations.

**Non-goal (v0.1):** The PVP does not prove that the agent's decision was strategically correct. It proves that the decision was made within declared authority, that the policy checks passed, and that the evidence is attributable to a known identity. Strategic correctness remains the principal's responsibility at mandate design time — the mandate is where an organization encodes what good purchasing looks like for their agents.

### 3.2 Component 2: The PACT SDK

The SDK is PACT's distribution mechanism. Design principle: **any agent builder should be able to give their agent commercial capability in under 30 minutes.**

**SDK must include:**
- Canonicalization, signing, and verification
- Mandate parsing and validation
- Policy evaluation interface (plug-in engines — the SDK defines the interface, not the policy logic)
- Standard error semantics (why a purchase failed — structured, machine-readable)
- Audit log emission format (compatible with finance systems)

**Non-goal (v0.1):** The SDK does not decide what to buy. It standardizes how authorization evidence is generated and verified. The purchasing decision belongs to the agent. The SDK only handles the proof.

The SDK is **rail-agnostic** — it generates PVPs regardless of whether the underlying payment is Stripe, a stablecoin, a corporate card API, or a future PACT-native settlement layer.

```python
# Reference usage — pseudocode
from pact import AgentWallet, PVPGenerator

wallet = AgentWallet(
    agent_id="did:pact:nexusai:infra-agent-7",
    principal="nexusai_corp",
    mandate=load_mandate("nexusai_infra_agent_7_v2.json"),
    payment_rail="stripe"
)

pvp = wallet.generate_pvp(
    vendor="vendor_computegrid_001",
    amount=312.00,
    category="cloud_infrastructure",
    purpose="GPU expansion — ML job nexusai-train-0291"
)

result = wallet.transact(pvp)
# Returns: CLEARED | REJECTED (with structured reason) | ESCALATE (out-of-mandate)
```

### 3.3 Component 3: The Registry (Optional)

The registry provides network services on top of the core standard. It is optional by design — the protocol must function if the registry is unavailable.

**What the registry provides:**
- Agent identity resolution (public keys, delegation pointers)
- Vendor attestations (KYB, allowlist memberships, catalog references)
- Reputation signals (optional, non-authoritative)

**Fallback when registry is unavailable:**
- Embedded mandate documents (hash-verified locally)
- Vendor attestations embedded or referenced via multiple providers
- Local allowlists and enterprise-hosted registries

Enterprises may run their own internal PACT registries. The protocol does not require a central registry — it requires a way to resolve agent identities and vendor attestations. The reference registry is one implementation.

**3.3.1 Cross-Registry Federation — Trust Model Sketch (v0.2 Preview)**

The cross-registry trust problem: how does Company B verify that Company A's agent, registered in Registry A, is legitimate — without requiring both companies to use the same registry?

The v0.2 federation model is based on root key cross-signatures:

```
Registry A                          Registry B
──────────                          ──────────
Root Key Pair (A)                   Root Key Pair (B)
  └── signs → Agent identities        └── signs → Agent identities
  └── signs → Vendor attestations     └── signs → Vendor attestations

Federation link:
  Registry B root key signs Registry A's root public key
  → producing a cross-signature record stored in both registries

Verification chain for a PVP from Registry A, verified by a party trusting Registry B:
  1. PVP signature → verified by Agent's Ed25519 public key
  2. Agent public key → signed by Registry A root key
  3. Registry A root key → cross-signed by Registry B root key
  4. Registry B root key → trusted by verifier
  ✓ Chain valid — PVP accepted
```

**Properties of this model:**
- Bilateral: each federation link requires explicit consent from both registries
- Revocable: Registry B can revoke its cross-signature of Registry A without affecting either registry's internal agents
- Transitive (optional): Registry C trusting Registry B can optionally accept chains through Registry B → Registry A; transitivity must be explicitly enabled and depth-limited to prevent chain explosion
- No central root: there is no master registry; trust propagates through declared bilateral relationships

**v0.1 position:** Cross-registry federation is deferred to v0.2. In v0.1, agents from different registries transacting with each other require out-of-band key verification or use of the reference registry as a shared anchor. This is a known limitation and is listed in Section 10 (Open Questions). The model above is provided as the design target so implementers can plan ahead.

**Vendor Trust Tiers:**

| Tier | Requirements | Buyer Experience |
|---|---|---|
| **Verified** | KYB complete, PACT compliance review, principal confirmed | Low friction — proofs auto-clear |
| **Provisional** | Self-registered, unverified | Medium friction — buyer agent flagged, escrow recommended |
| **Unverified** | No registration | High friction — seller's human confirms each transaction |

Unverified is deliberately included. Excluding it would reduce adoption and ignore commercial reality. The key is making risk visible and creating clear accountability chains.

**Seller-side accountability:** Verified sellers have signed documentation confirming identity and intent. A verified seller who runs a fraudulent agent leaves a complete forensic trail. Every PACT transaction generates a structured audit record. With optional anchoring enabled, that record is independently verifiable and tamper-resistant.

### 3.4 Optional Anchoring Layer — Chain-Agnostic Timestamps

PACT supports optional anchoring by submitting the PVP hash to one or more timestamping backends. The protocol is chain-agnostic.

```
anchors: [
  { type: "dlttx", network: "hedera",   ref: "0.0.4829301@1709428473.004" },
  { type: "dlttx", network: "ethereum", ref: "0xabc123..." },
  { type: "tlog",  network: "rekor",    ref: "1234567890" }
]
```

**What anchoring adds:** A neutral, independently verifiable timestamp that proves this specific PVP existed at this specific moment — held by infrastructure the transacting parties do not control. This is what CFOs, compliance officers, and regulators need for audit-grade evidence.

**Why optional:** The Ed25519 signature is sufficient to verify a proof's authenticity. Anchoring adds tamper-proof ordering and independent third-party verifiability. Organizations subject to financial audit, SOX compliance, or government procurement requirements will want it. Others may not.

**On Hedera specifically:** Hedera Consensus Service provides finality in ~3–5 seconds at ~$0.0001 per submission. It is referenced as an example backend. The patented hashgraph consensus algorithm (Swirlds, Inc.) is not used — PACT is a network user of HCS (submitting hashes), not an implementer of the algorithm. The protocol stays patent-clean.

```
PACT Architecture — Layers

┌─────────────────────────────────────────────────┐
│  PVP Core (open standard — required)            │
│  Ed25519 signature + policy evaluation record   │
│  Works with any rail, no patent encumbrance     │
└─────────────────────┬───────────────────────────┘
                      │ optional
┌─────────────────────▼───────────────────────────┐
│  SDK (required)                                 │
│  Generation / verification / policy hooks       │
│  Audit log emission / error semantics           │
└─────────────────────┬───────────────────────────┘
                      │ optional
┌─────────────────────▼───────────────────────────┐
│  Registry (optional, federable)                 │
│  Agent identity, vendor tiers, reputation       │
│  Can be self-hosted by enterprise               │
└─────────────────────┬───────────────────────────┘
                      │ optional
┌─────────────────────▼───────────────────────────┐
│  Anchoring (optional, chain-agnostic)           │
│  Submit PVP hash → tamper-proof timestamp       │
│  Hedera, Ethereum, Rekor, or other backends     │
└─────────────────────────────────────────────────┘
```

### 3.5 Agent Identity Specification

Identity is foundational. A PVP is only as trustworthy as the identity system backing the signing key. PACT v0.1 specifies the following explicitly — not as a placeholder.

**Primary identity primitive:** An Ed25519 key pair. The public key is the agent's identity anchor. Every other identity construct in PACT is built on top of this.

**Agent ID format:** PACT v0.1 uses a structured identifier:

```
did:pact:<org-id>:<agent-name>
```

The `org-id` maps to a registered principal. The `agent-name` is a stable, human-readable label. The DID resolves to the agent's current Ed25519 public key via the registry. Example: `did:pact:nexusai:infra-agent-7`.

For deployments without registry access, raw Ed25519 public keys are acceptable as agent identifiers, expressed as base58-encoded strings. Verifiers in registry-free mode must obtain the public key out-of-band. They cannot rely on DID resolution and should apply shorter PVP expiry windows as a compensating control.

**Key rotation:** Rotation requires issuance of a new mandate signed by the principal's root key, referencing the replacement Ed25519 public key. The old mandate remains valid only for PVPs with audit.created_at before the rotation timestamp. Verifiers MUST reject PVPs signed under a rotated-out key if the registry rotation record predates the PVP's creation time.

**Mandate invalidation:** A mandate is invalidated by: (a) explicit revocation record in the registry with timestamp, (b) principal key rotation, or (c) expiry of a time-bounded mandate. PVPs generated after the invalidation timestamp MUST be rejected. The maximum PVP expiry window in v0.1 is 24 hours — this caps the damage window from undetected invalidation regardless of registry availability.

**Compromised key handling:** On key compromise, the principal MUST post an immediate revocation record. PVPs signed under the compromised key after the revocation timestamp are invalid. PVPs signed before the revocation timestamp remain valid unless the principal explicitly posts individual revocations. Verifiers without registry access treat the absence of a revocation check as elevated risk.

**What v0.1 does not specify:** Cross-principal key attestation — how Company A verifies that Company B's agent key is legitimate without a shared registry — is a known gap deferred to v0.2. It is listed explicitly in Section 10 (Open Questions). Protocols die at identity boundaries; this gap is acknowledged rather than papered over.

---

## 4. Policy Delegation Architecture

### 4.1 The Principal Hierarchy

PACT provides the primitives for principals to build whatever delegation hierarchy fits their organization:

```
Human CEO / Organization
    └── Policy Engine (encodes delegation rules)
            ├── Agent Fleet A — $50K/month — Cloud Infrastructure
            │       ├── Agent A.1 — $10K/month — AWS
            │       └── Agent A.2 — $10K/month — GCP
            ├── Agent Fleet B — $20K/month — SaaS Tools
            └── Agent Fleet C — $5K/month — Contracted Services
```

The Policy Engine is not an AI that makes decisions. It is a living policy document that encodes delegation-of-authority rules, adjusts limits based on track record, and surfaces anomalies — not routine approvals — to the human principal.

The goal: **human involvement becomes rare and high-quality, not frequent and low-value.**

### 4.2 Sub-Agent Delegation

When an agent spawns a sub-agent, the sub-agent's authority is always a subset of the parent agent's authority. PACT enforces this through:

- Parent-signed sub-mandates
- Explicit `delegation_ref` in the sub-agent's PVP
- Registry pointers (optional)

**On containment guarantees:** Sub-mandate authority is verifiably bounded when mandates are machine-readable and policy engines are deterministic. In v0.1, the protocol requires parent-signature and auditability rather than claiming perfect formal containment — a property that cannot be guaranteed in the general case. Violations are detectable and attributable; they are not cryptographically prevented at the protocol layer in v0.1.

### 4.3 Human Escalation

When an agent attempts a transaction outside its current mandate, PACT does not fail silently. It generates a structured escalation request to the principal with:

- The proposed transaction and why it fails the mandate
- The agent's reasoning for why the transaction is appropriate
- A structured approval interface to expand the mandate or approve the single transaction

The agent pauses and waits. This creates a feedback loop through which principals refine mandates over time, progressively reducing escalation frequency.

---

## 5. The Commercial OS — v0.1 Scope and Roadmap

### 5.1 What v0.1 Standardizes

PACT v0.1 standardizes three procurement patterns:

| Pattern | Description |
|---|---|
| **Spot purchase** | PVP generated, single transaction clears |
| **Subscription** | Recurring PVP with time-bounded authorization and renewal constraints |
| **Bounded service engagement** | Capped spend with milestone references, structured rejection at cap |

These cover the majority of routine autonomous agent procurement: compute, SaaS tools, data access, contracted services with defined scope.

### 5.2 Future Profiles (Non-Normative)

Additional procurement patterns are compatible with the PVP format but are not standardized in v0.1:

| Profile | Description |
|---|---|
| **RFP / auction** | Agent broadcasts structured request, evaluates responses, issues PVP to winner |
| **Escrow** | Payment held in smart contract pending proof-of-delivery |
| **Brokerage chain** | Multi-hop A2A transaction where each intermediary generates a PVP; commission structures encoded at each step; full chain traceable in registry |
| **Master Service Agreement** | Registered template governing repeat agent-to-agent transactions |

These are intentionally deferred. Defining them before the core standard has real adoption would add complexity without benefit.

### 5.3 Legal Compatibility

PACT is designed to be compatible with existing commercial law by making the principal explicit and generating audit-grade authorization evidence. Legal enforcement remains in existing contract structures — MSAs, purchase orders, invoices. PACT does not replace commercial law; it generates the machine-readable evidence that makes disputes easier to resolve within it.

---

## 6. Threat Model and Failure Modes

*This section is required for any serious standards proposal. What a protocol explicitly does not solve is as important as what it does.*

### 6.1 What PACT v0.1 Mitigates

- **Unauthorized spend outside mandate** — PVP verification rejects transactions that fail policy checks before payment rails are engaged
- **Replay attacks** — Idempotency keys and expiry windows prevent reuse of valid PVPs
- **Agent impersonation** — Ed25519 signatures bound to registered identity; forged identity produces invalid signature
- **Vendor misrepresentation** — Attestation tiers and allowlists; verified vendors have documented accountability
- **Untraceable spend** — Every transaction produces a structured audit record regardless of tier; optional anchoring provides independent timestamp

### 6.2 What PACT v0.1 Does Not Solve

- **Compromised policy engine** — If the policy engine is controlled by an attacker who fabricates "PASS" results, the PVP will appear valid. v0.1 mitigates this through audit trails and independent re-evaluation; it does not prevent it cryptographically. v0.2 privacy-preserving proofs address a subset of this.
- **Strategic manipulation** — An adversarial vendor can craft offers that satisfy all declared policy checks while still being bad deals. PACT proves authorization, not strategic correctness. The principal's policy design is the defense here.
- **Disputes over deliverables** — Whether a vendor delivered what was purchased is outside PACT's scope. Escrow profiles (future) and existing contract structures handle this.
- **Principal-level fraud** — If the principal itself is acting in bad faith (e.g., using agents to launder transactions), PACT generates an audit trail but does not prevent the underlying fraud. That remains a legal enforcement problem.

Stating these limits explicitly is how a protocol earns trust from technical reviewers. Overclaiming is how it loses it.

---

## 7. Minimal Viable Standard

*What PACT v0.1 must actually specify to be a protocol rather than a vision document.*

### 7.1 v0.1 MUST Standardize

- **Canonical byte representation** — deterministic serialization for signing (canonical JSON or equivalent); without this, signatures are not interoperable
- **Required fields and validation rules** — which PVP fields are mandatory, which are optional, type and format constraints
- **Error codes and rejection semantics** — structured machine-readable reasons why a PVP failed; enables SDK escalation logic
- **Mandate format** — at least one machine-readable mandate profile; without this, policy checks cannot be independently verified
- **Idempotency and expiry rules** — how request_id is scoped, maximum expiry window, replay detection requirements

### 7.2 v0.1 SHOULD Provide

- **Reference registry schema** — so implementers building their own registries maintain interoperability
- **Reference policy engine interface** — the plug-in contract the SDK uses for policy evaluation hooks
- **Reference anchor adapters** — for Hedera HCS and at least one transparency log backend

### 7.3 v0.1 Explicitly Defers

- Privacy-preserving proofs for policy checks (v0.2)
- Cross-registry federation protocol (v0.2)
- Formal mandate containment verification (future)
- Brokerage chain profiles (future)
- Dispute resolution framework (future)

This decomposition is what separates a v0.1 that can be implemented from a vision document that cannot.

---

## 8. The Long Game: Autonomous Economic Units

*This section is non-normative. It describes the forward-looking vision that motivates PACT's design choices.*

The framing in sections 1–7 describes PACT as infrastructure for enterprises deploying agent fleets today — where humans are principals, agents are operators, and the goal is safer autonomous procurement. That framing is accurate and is what drives near-term adoption.

But the deeper ambition is different.

The question PACT is ultimately trying to answer is: **what happens when the companies themselves are run by agents?**

Consider a world where 80% of operational decisions in a company are made by agents. Where agents manage infrastructure, procurement, HR, and logistics with minimal human intervention. Where the "principal" is increasingly a capital allocator and regulator rather than an operational decision-maker.

In that world, autonomous agents will still need:

- **Identity** — who is this agent, what company does it represent
- **Capability boundaries** — what is it authorized to commit to
- **Spend limits** — what capital exposure can it create
- **Counterparty rules** — which vendors can it engage
- **Reputation accumulation** — has it transacted reliably before
- **Dispute resolution** — what happens when something goes wrong

Autonomy does not remove the need for governance. It makes governance more important — because the speed and scale at which agents operate means governance failures propagate faster than any human oversight system can catch.

The critical reframe: autonomy does not mean no constraints. It means **self-governed constraints**. An agent-run company still has budget caps, risk tolerances, counterparty rules, and delegation hierarchies. They are simply machine-managed rather than human-managed. An economy without constraints is not freedom — it is an agent that bankrupts itself in the first hour of operation. The question PACT answers is not whether constraints should exist. It is how those constraints are expressed, verified, and recorded between machines.

What changes in an agent-run world is not whether governance constraints exist. It is who sets them. In a fully autonomous firm, the "mandate" is generated dynamically by other agents rather than written by a human. The "principal" is the capital layer — shareholders, regulators, credit providers — not an operational manager.

PACT's architecture survives this transition. The protocol does not care whether the mandate was written by a CFO or generated by a board-level policy agent. It standardizes:

1. **Economic intent expression** — what the agent intends to purchase and why
2. **Capability declaration** — what the agent is authorized to commit to, expressed in machine-readable form before any transaction
3. **Governance constraint attestation** — evidence that the transaction satisfies the agent's active mandate and policy checks
4. **Transaction commitment evidence** — a signed, auditable record binding the purchase to a specific identity and mandate
5. **Reputation accrual** — a verifiable track record that principals and counterparties can use to calibrate trust over time

Those five things are required whether companies are 10% agent-run or 100% agent-run. The protocol is infrastructure for the economic handshake between autonomous firms — not just for the safety of current enterprises delegating tasks to agents.

This is the design intention behind making the registry optional, the anchoring chain-agnostic, and the principal model thin. The protocol should not assume a specific organizational structure. It should work whether the principal is a human, a board, or another agent.

---

## 9. Competitive Position

### 9.1 Why This Is a Protocol Play

Products compete on features. Protocols compete on network effects. Every developer who builds an agent with the PACT SDK adds to the registry, expands the vendor network, and makes PACT more valuable for the next developer. Standards are winner-take-most — the second-best authorization evidence format for agent purchases will be worth close to zero.

MCP was not the first protocol for agent tool connectivity. It won because it shipped open, was developer-first, and reached critical adoption before incumbents built proprietary alternatives.

### 9.2 Where PACT Competes — And Why It Can't Be Built Internally by Stripe

Visa, Mastercard, and Stripe own the money movement layer. They will always own it. That is not where PACT competes. PACT is the **decision integrity layer above the money movement** — the standard by which the legitimacy of agentic purchase decisions is verified before any rail is engaged.

A reasonable question from a Stripe infrastructure engineer: why can't Stripe implement signed purchase attestations internally? The answer is that enterprise agent procurement does not flow through one rail. A single organization deploying an agent fleet will typically route transactions across:

- **Stripe** — SaaS subscriptions, API vendor payments
- **Brex or Ramp corporate cards** — expense management, hardware procurement
- **ACH or wire transfers** — large contracts, professional services
- **Stablecoins or on-chain escrow** — cross-border payments, milestone-based contracts
- **Internal ERP or procurement systems** — PO workflows, three-way matching
- **Vendor APIs directly** — compute providers, data marketplaces, logistics platforms

A PVP signed by an agent must be verifiable by any counterparty on any of these rails, in any jurisdiction, without requiring the counterparty to have a relationship with Stripe. If the authorization evidence standard only works inside one payment platform, an enterprise with multi-rail procurement cannot use it. The standard becomes a feature of one vendor, not infrastructure for the market.

This is the structural argument for why PACT must be an open, rail-neutral protocol rather than an internal implementation by any single incumbent. The PVP is the portable unit of authorization evidence — it travels with the transaction regardless of what moves the money. Stripe, Brex, and every other rail are payment execution layers that sit underneath it.

The strategic scenario this creates: incumbent payment rails that want to serve enterprise agentic procurement will find it more practical to recognize PACT PVPs than to build a proprietary attestation standard that only covers their slice of a multi-rail procurement stack. Interoperability is not an idealistic goal — it is the only design that works for how enterprises actually spend money. Partners, not enemies.

### 9.3 Relationship to Blockchain and Smart Contracts

A reasonable question from any technical reviewer: does blockchain already solve this? Smart contracts can execute transactions automatically, create immutable on-chain records, enforce payment conditions, hold escrow, and verify on-chain identity. These are real capabilities that overlap with parts of what PACT addresses. The honest answer is that blockchain solves a different layer, and PACT is designed to work with it rather than compete with it.

**What smart contracts solve well:**
- Settlement and fund movement on-chain
- Escrow with deterministic release conditions
- Immutable on-chain transaction records
- Token-based authorization (e.g., multi-sig wallets)
- Simple conditional payment logic

**What smart contracts do not solve:**
- Off-chain mandate management — a complex, evolving policy document describing what an agent is authorized to buy is not a smart contract. It is a structured document with business logic that needs to integrate with enterprise workflows.
- Integration with existing payment rails — the majority of enterprise procurement runs through Stripe, corporate cards, ACH, and bank transfers. Not blockchain wallets. PACT is designed to work above those rails.
- Enterprise compliance requirements — SOX audit trails, finance system integration, and regulatory reporting require structured off-chain records in formats auditors can use. Blockchain records alone do not satisfy these requirements.
- Complex policy evaluation — determining whether a proposed $47,000 vendor engagement satisfies a multi-condition mandate involves business logic that is too contextual and complex for a deterministic smart contract.
- Human escalation flows — when an agent's purchase falls outside its mandate, the protocol needs to surface a structured request to a human. Smart contracts have no escalation mechanism.

**How they fit together:** PACT uses blockchain as an optional anchoring layer — submitting PVP hashes to a public chain for tamper-proof timestamping. The settlement layer underneath a PACT transaction can be a smart contract, Stripe, or any other rail. PACT is the authorization and audit layer above settlement; blockchain is one of several options for the settlement and timestamping layers below it. They are complementary, not competitive.

The differentiation PACT makes is the enterprise off-chain focus — meeting companies where their procurement infrastructure already lives — with optional blockchain integration rather than requiring it.

### 9.4 Adoption Thesis

- Vendors accept PVP because it reduces fraud and authorization disputes
- Enterprises adopt because it reduces approval overhead and improves auditability
- Agent builders adopt because it standardizes procurement integrations across vendors

The protocol succeeds if those three constituencies find independent reasons to implement it. Each adoption reinforces the others.

---

## 10. Open Questions — Inviting Collaboration

PACT is a thesis, not a finished specification. These questions require input from developers, legal experts, and commercial builders.

**10.1 Liability Framework**
When a PVP passes verification but the underlying decision is strategically wrong, who bears the loss? The agent's principal? The protocol has no position on this — but a clear liability stack is required for real commercial adoption and needs community input.

**10.2 Cross-Organization A2A Trust**
When Agent X (Company A) hires Agent Y (Company B), this is effectively a B2B transaction between two organizations. What is the agent-native equivalent of a Master Service Agreement? How does PACT handle cross-principal disputes?

**10.3 The Cold Start Problem**
New agents have no reputation. What is the baseline spending authority for a newly registered agent? How does the protocol support gradual trust expansion without requiring months of low-stakes transactions?

**10.4 Adversarial Robustness**
The proof system must be tested against seller agents optimized to craft offers that satisfy policy checks while still being bad deals. How do we make authorization evidence adversarially robust — not just correct for honest participants?

**10.5 The Primitives Question**
Is PVP format + SDK + registry the right decomposition? Are there simpler primitives — a token standard, a single on-chain attestation format — that would achieve higher adoption at lower complexity cost?

**10.6 Federation Protocol**
How do two independent PACT registries establish mutual trust? What is the minimal federation protocol that allows an enterprise running its own registry to interoperate with the reference registry?

---

## 11. Conclusion

Organizations deploying agent fleets today face a real and unsolved problem: how do you give agents the authority to act without either slowing them down with human approvals or exposing the organization to unconstrained spend risk?

PACT is a proposal for the infrastructure layer that makes this safe. Not by preventing agent autonomy, but by making autonomy auditable — by standardizing the authorization evidence that proves an agent's procurement decision was within its delegated authority, before any payment rail is engaged.

The protocol is designed to be genuinely open: Ed25519 signatures with no patent encumbrance, optional registry and anchoring layers that can be self-hosted, and a minimal v0.1 spec focused on the shippable thing rather than the full vision.

The longer-term ambition is infrastructure that survives the transition to a world where companies themselves are increasingly agent-run. The four things PACT standardizes — economic intent expression, governance constraint attestation, transaction commitment evidence, and reputation accrual — are required in that world whether or not they are required in today's world.

We are building this openly. If you are building agent infrastructure and have hit the procurement problem, we want to build this with you.

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **A2A Commerce** | Agent-to-agent commercial transactions; both operational actors are AI agents, though each represents a legal principal |
| **PVP** | Proof of Valid Purchase — signed transaction attestation binding purchase intent to active mandate and policy checks |
| **Mandate** | The formal specification of what an agent is authorized to purchase, from whom, and under what constraints |
| **Principal** | The human, organization, or legal entity that authorized an agent and bears legal responsibility for its commercial actions |
| **Policy Engine** | The system that evaluates whether a proposed transaction satisfies the agent's mandate constraints |
| **Policy Evaluation** | The structured record of which checks ran, what inputs they used, and what outputs they produced — the audit trail of a procurement decision |
| **Trust Tier** | Classification of vendors in the registry: Verified, Provisional, or Unverified |
| **KYA** | Know Your Agent — the emerging compliance framework for agent identity verification |
| **Delegation Chain** | The verifiable record of authority passed from principal to orchestrator agent to sub-agents |
| **Ed25519** | An open, unpatented elliptic-curve digital signature algorithm used to sign PVPs; no licensing restrictions |
| **Anchoring** | Optional submission of a PVP hash to a timestamping backend (chain-agnostic) for independent audit trail creation |
| **Anchor Ref** | The timestamping backend transaction ID stored in a PVP's `audit.anchors` field |
| **AEU** | Autonomous Economic Unit — an agent or agent-run firm that operates with self-directed execution within a governance framework; the forward-looking framing for PACT's long-term design target |
| **Idempotency Key** | The `request_id` field in a PVP's audit block; prevents replay of valid PVPs across multiple submissions |
| **Escalation** | The structured process by which an agent surfaces an out-of-mandate transaction to its principal for approval or mandate expansion |

## Appendix B: Analogous Standards — How Protocols Win

| Protocol | Problem Solved | How It Won | Outcome |
|---|---|---|---|
| **MCP** (Anthropic, 2024) | Agent tool connectivity | Open-sourced, developer-first, shipped before consolidation | De facto standard; every major AI lab supports it |
| **ERC-20** (Ethereum, 2015) | Token standard | Simple, open, developer-friendly | Powers trillions in token value |
| **OAuth 2.0** | Delegated authorization for APIs | Open standard, adopted by Google/Facebook early | Every API in existence supports it |
| **OpenAPI** | API specification format | Open, tooling-first, neutral | Every major API uses it |

The pattern: **open + developer-first + ships before consolidation = winner-take-most.**

---

*PACT is an open protocol proposal. All feedback, critiques, and contributions are welcome.*
*Contact: trosellv@gmail.com*
*Version: 1.0 — March 2026*
