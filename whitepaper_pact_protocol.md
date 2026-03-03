# PACT: The Protocol for Agentic Commerce and Trust
### A Whitepaper on Commercial Operating System Infrastructure for the Agentic Economy

**Author:** TJ Rosell
**Date:** March 2026
**Status:** Draft v0.1 — Open for Collaboration
**Contact:** trosellv@gmail.com

---

> *"MCP solved how agents connect to tools. PACT solves how agents transact in markets."*

---

## Abstract

Artificial intelligence agents are becoming digital workers — autonomous systems that perform tasks, manage workflows, and increasingly operate with economic consequence. Yet the infrastructure for agents to participate in commerce as independent economic actors does not exist. The dominant wave of agentic payment solutions — from Mastercard Agent Pay to Stripe's Agentic Commerce Suite — addresses the human→agent→merchant layer: a person delegating a purchase to their AI assistant. This paper proposes a fundamentally different layer: **agent→agent commerce**, where an AI agent with a defined mandate can autonomously procure anything a human business has ever bought — compute, software, physical hardware, real estate, logistics, legal services, financial instruments, other agents, and yes, human employees who choose to work under an agent's direction — with verifiable proof that every transaction was logically consistent with its authorization. The scope is intentionally limitless.

We introduce **PACT** — the Protocol for Agentic Commerce and Trust — an open standard comprising three components: a cryptographic **Proof-of-Valid-Purchase (PVP)** format, a developer **SDK** that makes PVP generation trivially easy to integrate into any agent, and a **Registry** that provides agent identity, vendor trust tiers, and on-chain reputation. PACT does not move money. It sits above existing payment rails and defines the decision integrity layer that makes agent-to-agent commerce trustworthy, auditable, and scalable without constant human intervention.

---

## 1. The Problem

### 1.1 Agents Are Becoming Digital Workers — But Can't Get Paid or Pay

The transformation is already underway. AI agents are drafting code, managing calendars, running outreach campaigns, and handling customer support at scale. The logical next step — agents that autonomously procure the resources they need to do their jobs — is technically possible today but commercially unresolved.

Consider what it would mean for an agent to truly function as a digital worker:

- An infrastructure agent that detects it needs more compute and purchases additional cloud capacity
- A procurement agent that identifies the best SaaS tool for a task and subscribes to it
- A project management agent that hires a specialized coding agent to complete a subtask
- A research agent that purchases access to a proprietary data source in real-time
- An operations agent that leases physical office space or a data center rack on behalf of its organization
- A hardware agent that sources and orders physical equipment — servers, robotics components, peripherals
- A legal agent that engages a human attorney or a specialized legal-AI service for contract review
- An HR agent that recruits, contracts, and onboards a human freelancer or full-time employee
- A logistics agent that books freight, warehousing, or last-mile delivery
- A finance agent that purchases financial instruments, hedges, or structured products within its mandate

This list is intentionally incomplete. PACT does not define what agents can purchase — that is the mandate's job. PACT defines only that the decision to purchase was valid. The scope of agentic commerce is, by design, **limitless**: anything a human business has ever procured is a candidate for autonomous agent procurement, including other humans choosing to work under an agent's direction.

None of this requires new AI capabilities. It requires **commercial infrastructure**: the ability for an agent to hold spending authority, prove its purchasing decisions are legitimate, interact with verified sellers, and create an auditable trail that satisfies legal, financial, and governance requirements.

Today, that infrastructure does not exist. Agents either require a human in the loop for every transaction — defeating the efficiency gain — or they operate with unconstrained access to credentials — creating unacceptable fraud and liability risk.

### 1.2 What Exists Today — And Why It Doesn't Solve This

The major financial players are moving fast, but they are building a different layer:

| Player | Product | What It Solves |
|---|---|---|
| Mastercard | Agent Pay / Agentic Tokens | Human delegates consumer purchases to their AI |
| Visa | Trusted Agent Protocol | Distinguishing bots from legitimate consumer agents at checkout |
| Stripe | Agentic Commerce Suite / SPTs | Consumer AI completes purchases using saved payment methods |
| Google | Universal Commerce Protocol | Open standard for AI shopping agents across retail platforms |
| PayPal | Agent Ready | AI agents completing purchases on behalf of consumers |
| Skyfire | KYAPay | Agent identity and payment for human-to-agent-to-merchant flows |

The pattern is consistent: **the human remains the economic principal.** The agent is a proxy — a smarter checkout button. This is valuable and the market is large.

But it is not what we are building.

PACT addresses the layer none of these players have built: **autonomous agent-to-agent (A2A) commercial relationships, where the agent is the economic actor, not the human's delegate.** This is the infrastructure for the B2B economy of AI — where businesses deploy agent fleets, agent fleets procure resources, and the humans only get involved for genuine anomalies, or because they want to work under an agent.

---

## 2. Core Concepts

### 2.1 The Agent as Economic Actor

The shift in framing is critical and must be stated explicitly:

**Current paradigm:** Human intent → Agent action → Merchant transaction
**PACT paradigm:** Organizational policy → Agent mandate → Agent decision → Verified transaction

In the PACT model, an agent is not executing a human's purchase. It is executing its own authorized procurement decision, within a mandate it has been given, with cryptographic proof that the decision is valid before funds are released.

This is analogous to the evolution of corporate finance. A senior employee with a company card isn't asking their CEO whether to buy office supplies. They have a delegated authority, a spending category, a dollar limit, and an expectation that they will exercise judgment. The CEO gets involved only for genuine anomalies. PACT is the infrastructure that makes this possible for AI agents.

### 2.2 Trust Grows With Track Record

Human organizations understand that trust is earned, not assumed. A new employee doesn't get a corporate card on day one. A vendor doesn't get net-60 terms on a first order. PACT's architecture mirrors this:

- Agents begin with constrained spending authority defined by their principal
- Limits expand dynamically as the agent accumulates verified transaction history
- The registry records every verified transaction, building an on-chain reputation score
- Principals set the policy for how their agents' limits evolve — some will be conservative, some permissive, none prescriptive from the protocol level

PACT does not dictate how organizations trust their agents. It provides the infrastructure through which that trust is expressed, verified, and recorded.

### 2.3 The Key Insight: Proof, Not Permission

The bottleneck in today's agentic systems is the approval loop. Every time an agent wants to take a commercially consequential action, it either acts unilaterally (dangerous) or pings a human (inefficient). PACT proposes a third path: **mathematical proof that a decision is valid.**

Before a transaction clears, the purchasing agent generates a cryptographic proof — the Proof of Valid Purchase (PVP) — that demonstrates:

1. The agent is who it claims to be (identity)
2. The agent is authorized to make this category of purchase (mandate)
3. The purchase satisfies the agent's constraints (logical validity)
4. The vendor has been verified or the buyer has acknowledged unverified status (trust tier)

The payment rail checks the proof. If it passes, the transaction clears. No human needed. The proof IS the accountability.

This is not trust like you trust a person. This is trust like you trust a smart contract.

---

### 2.4 Worked Example: Agent Procures Compute Autonomously

*The following traces a complete A2A transaction from agent decision to provisioned resource. It is intended to make the abstract concrete before the full architecture is detailed.*

**The Setup**

NexusAI operates an infrastructure agent, `InfraAgent-7`, responsible for maintaining compute resources for active ML workloads. Its mandate is registered in PACT as follows:

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

This document is registered in the PACT registry. Its hash is what the PVP will reference — not the document itself — so the full mandate can be inspected by any auditor without being embedded in every transaction.

At 2:14 AM, `InfraAgent-7` detects its current GPU allocation will be exhausted in 47 minutes. It needs to act. No human is awake. No human needs to be.

**Step 1 — Registry Lookup**

`InfraAgent-7` queries the PACT registry for Verified vendors in the `cloud_infrastructure` category. Three results are returned. The agent evaluates each against its mandate constraints and selects `ComputeGrid` (registry ID: `vendor_computegrid_001`) — lowest cost-per-TFLOP among Verified vendors, 99.94% uptime track record in the registry.

**Step 2 — PVP Generation**

The agent generates and signs a Proof of Valid Purchase:

```
PVP {
  agent_id:          "did:pact:nexusai:infra-agent-7"
  agent_version:     "sha256:a3f9c2...d841"
  principal_id:      "nexusai_corp"
  mandate_hash:      "sha256:7b2e91...c034"

  transaction_intent: {
    vendor_id:       "vendor_computegrid_001"
    vendor_tier:     "verified"
    amount:          { value: 312.00, currency: "USD" }
    category:        "cloud_infrastructure"
    purpose:         "GPU expansion — ML job nexusai-train-0291, projected 4hr duration"
    constraint_refs: ["cost_cap_1000_daily", "perf_floor_80tflops", "verified_vendor_only"]
  }

  constraint_proof: {
    version:  "v0.1-json-assertion"
    note:     "v0.1 uses hash-verified JSON assertions. ZK proofs replace this in v0.2."
    checks: [
      { ref: "cost_cap_1000_daily",   result: "PASS", detail: "spend_today=688, new=312, cap=1000" },
      { ref: "perf_floor_80tflops",   result: "PASS", detail: "computegrid_tflops_per_dollar=94.2" },
      { ref: "verified_vendor_only",  result: "PASS", detail: "vendor_tier=verified" }
    ]
    proof_hash: "sha256:e7f3a1...8c02"   // hash of checks block + mandate_hash, signed by agent
  }

  timestamp:   "2026-03-03T02:14:33Z"
  expiry:      "2026-03-03T02:19:33Z"
  signature:   "ed25519:3045...f9a2"
  anchor_ref:  "0.0.4829301@1709428473.004"   // Hedera HCS consensus timestamp (optional, enabled by NexusAI)
}
```

*Note on constraint_proof in v0.1:* The proof is a signed JSON assertion block — not a zero-knowledge proof. Any verifier can recompute the hash of the checks block against the mandate and confirm it matches. ZK proofs, which would allow verification without revealing the full reasoning chain, are a Phase 2 upgrade. The schema is forward-compatible.

**Step 3 — HCS Anchoring (optional)**

Before submitting to ComputeGrid, the SDK submits the PVP hash to Hedera Consensus Service. Hedera returns a consensus timestamp in 3.2 seconds. The `anchor_ref` is written into the PVP. NexusAI's CFO can look up this transaction on the HCS mirror node at any point in the future — independently, without asking PACT, ComputeGrid, or NexusAI's own systems.

**Step 4 — Application-Layer Verification at ComputeGrid**

`InfraAgent-7` submits the signed PVP to ComputeGrid's PACT-enabled API endpoint. *PACT verification happens entirely at ComputeGrid's application layer* — before ComputeGrid initiates any payment call to Stripe. ComputeGrid's system runs four checks in under 200ms:

1. **Signature valid** — `InfraAgent-7`'s Ed25519 public key is retrieved from the PACT registry for `did:pact:nexusai:infra-agent-7` and used to verify the signature ✓
2. **Mandate hash matches** — the registry confirms `sha256:7b2e91...c034` is the current active mandate for this agent ✓
3. **Constraint proof valid** — the proof_hash is recomputed against the checks block and mandate_hash; it matches the signed value ✓
4. **Expiry within bounds** — PVP was generated 18 seconds ago; 5-minute window still valid ✓

Only after all four checks pass does ComputeGrid call Stripe to process the $312.00 charge. PACT never touches the payment rail — it sits above it. If any check had failed, Stripe would never have been called and the agent would receive a structured rejection with the specific failed constraint, which the SDK surfaces as a human escalation request.

**Step 5 — Registry Update**

Both parties' registry records update: `InfraAgent-7`'s daily spend counter increments by $312, and `ComputeGrid` receives a verified transaction increment on its reputation score. Total elapsed time from agent decision to compute provisioned: **41 seconds.**

**What didn't happen**

No human approved this. No Slack message was sent at 2 AM. No on-call engineer logged into a cloud console. The agent had a mandate, the purchase satisfied that mandate, the proof was generated and verified at the application layer, and the transaction cleared. If NexusAI's CFO reviews spending at 9 AM, they see a complete line item — agent identity, mandate reference, constraint results, HCS timestamp — without ever having been woken up.

This is what PACT makes possible.

---

## 3. The PACT Architecture

PACT is a three-component system. Each component can be adopted independently, but they are designed to compound in value when used together.

### 3.1 Component 1: Proof of Valid Purchase (PVP) — The Core Standard

The PVP is a signed data object generated by the purchasing agent before a transaction is submitted. It contains:

```
PVP {
  agent_id:          <DID or registry-issued identifier>
  agent_version:     <hash of agent codebase at time of transaction>
  principal_id:      <organization or human that authorized this agent>
  mandate_hash:      <cryptographic hash of the agent's current mandate document>
  transaction_intent: {
    vendor_id:       <PACT registry ID or unverified identifier>
    vendor_tier:     <verified | unverified | provisional>
    amount:          <value + currency/token>
    category:        <standardized procurement category>
    purpose:         <human-readable intent string>
    constraint_refs: [<C1>, <C2>, ... <Cn>]
  }
  constraint_proof:  <ZK-style proof that transaction satisfies constraints C1..Cn>
  timestamp:         <ISO 8601>
  expiry:            <time window for validity>
  signature:         <Ed25519 signature over canonical PVP hash — agent's private key>
  anchor_ref:        <optional: Hedera Consensus Service transaction ID for tamper-proof audit anchoring>
}
```

The constraint proof is the core innovation. The agent does not just say "I want to buy this." It proves "this purchase satisfies the constraints I was given" — without necessarily revealing the full reasoning chain. Analogous to zero-knowledge proofs in cryptography: proving validity without exposing everything.

**On the signature mechanism:** PACT uses **Ed25519** as the standard signing algorithm. Ed25519 is an open, unencumbered cryptographic standard with no patent restrictions — widely supported across all major languages and platforms. This keeps the PVP format genuinely open: any developer can implement it independently without licensing obligations. The optional `anchor_ref` field is addressed in Section 3.4.

**What verifiers check:**
- Valid signature from a known agent identity
- Mandate hash matches the registry record for that agent
- Constraint proof is mathematically valid against the declared constraints
- Vendor tier is acknowledged correctly
- Timestamp and expiry are within bounds

**What this enables:**
- Payment rail can auto-clear transactions with valid PVPs
- Disputes have a complete evidence chain
- Auditors can verify every spend decision without accessing proprietary agent logic
- Compromised agents produce invalid proofs — automatic fraud detection

### 3.2 Component 2: The PACT SDK

The SDK is PACT's distribution mechanism. Its design principle: **any agent builder should be able to give their agent commercial capability in under 30 minutes.**

The SDK handles:

```python
# Pseudocode — actual SDK to be specified in v0.2
from pact import AgentWallet, PVPGenerator, VendorRegistry

wallet = AgentWallet(
    agent_id="agent_x_001",
    principal="acme_corp",
    mandate=load_mandate("agent_x_mandate.json"),
    payment_rail="stripe"  # or "stablecoin", "brex", etc.
)

# At purchase decision time:
pvp = wallet.generate_pvp(
    vendor="aws_compute",
    amount=450.00,
    category="cloud_infrastructure",
    purpose="ML training job — additional GPU capacity",
    constraints_satisfied=["cost_cap", "performance_floor", "availability"]
)

result = wallet.transact(pvp)
```

The SDK is **rail-agnostic**. It generates PVPs regardless of whether the underlying payment is Stripe, a stablecoin transfer, a corporate card API, or a future PACT-native settlement layer. The standard lives above the rail.

**SDK capabilities at launch (v1):**
- PVP generation and signing
- Registry lookup for vendor verification status
- Agent identity management (key generation, rotation, delegation)
- Transaction logging to principal dashboard
- Human escalation triggers (when agent attempts out-of-mandate purchases)

### 3.3 Component 3: The Registry

The Registry is PACT's network-effect moat. It serves three functions:

**Agent Identity Records**
Every agent registered in PACT has a unique identifier anchored to its principal organization. The registry stores the agent's current mandate hash, delegation chain (if a sub-agent), spending track record, and public key for signature verification.

**Vendor Trust Tiers**

| Tier | Requirements | Buyer Experience |
|---|---|---|
| **Verified** | Human principal confirmed, KYB completed, PACT compliance review | Low friction — proofs auto-clear, no extra confirmation |
| **Provisional** | Self-registered, unverified | Medium friction — buyer agent flagged, escrow recommended |
| **Unverified** | No registration | High friction — seller's human must confirm each transaction in good faith |

The unverified tier is deliberately included. Excluding it would reduce adoption and ignore commercial reality — not every vendor will register on day one. The key is making the risk visible and creating clear accountability chains.

**Reputation and Track Record**
Every verified transaction increments both buyer and seller reputation. The registry becomes, over time, a credit bureau for agents — a record that principals can use to calibrate how much autonomy to grant their agents and which vendors their agents can engage.

**Seller-Side Verification and Fraud Attribution**

PACT is architected buyer-first — the PVP originates from the purchasing agent. But bad actors will almost always present as sellers, not buyers. This is true in every commercial system that has ever existed, and PACT does not pretend otherwise.

The design philosophy is direct: PACT cannot prevent every bad actor from entering the ecosystem, just as Visa cannot prevent every fraudulent merchant. What PACT can do — and does — is make bad behavior *expensive, visible, and permanently attributable*. That is what makes it safe enough for real commerce.

The seller-side architecture achieves this through three mechanisms:

*Verification as skin in the game.* To become a Verified seller, a human principal must complete KYB, confirm the business is operating in good faith, and accept legal responsibility for their selling agent's conduct. This is not just a technical check — it is a liability transfer. A Verified seller who runs a fraudulent agent has signed documentation confirming their identity and intent. That paper trail is what law enforcement, regulators, and counterparties need.

*Graduated friction by tier.* Unverified sellers face the highest friction by design. A buyer agent dealing with an unverified vendor must have the seller's human explicitly confirm each transaction in good faith before it clears. This doesn't block unverified sellers — excluding them would reduce adoption and ignore commercial reality — but it creates a mandatory accountability moment for every deal. Provisional sellers fall in between: self-registered, flagged to buyer agents, with escrow recommended.

*The audit trail as deterrent.* Every PACT transaction — regardless of tier — generates an immutable record. With optional HCS anchoring, that record is held on a neutral distributed network, not PACT's own servers. A seller agent that manipulates pricing, misrepresents deliverables, or exploits constraint proofs leaves a complete forensic trail. PACT does not need to catch bad actors in real time; it needs to make the cost of being caught so high that the rational choice is compliance.

The honest framing: adversarial sellers are inevitable and will be part of the agentic economy, just as fraudulent merchants are part of the card network economy. The goal is not a fraud-free system. The goal is a system where fraud is attributable, recoverable, and systematically more costly than honest commerce.

### 3.4 Optional Anchoring Layer: Hedera Consensus Service (HCS)

PACT's PVP is cryptographically self-contained — the Ed25519 signature is sufficient to verify a proof's authenticity. However, for use cases requiring an immutable, independently verifiable, and tamper-proof audit trail, PACT supports an optional anchoring layer via the **Hedera Consensus Service (HCS)**.

**What anchoring means in practice:** After a PVP is generated and signed, the agent (or the SDK on its behalf) submits the PVP hash to an HCS topic. Hedera returns a consensus timestamp and sequence number — a globally ordered, tamper-proof record that this specific PVP existed at this specific moment. That HCS transaction ID becomes the `anchor_ref` field in the PVP.

**Why Hedera specifically:** HCS provides consensus finality in approximately 3–5 seconds at a cost of roughly $0.0001 per submission. The audit record is held by a neutral distributed network — not PACT's own servers — making it independently verifiable by any third party, including regulators, auditors, or counterparties in a dispute. This is the same architecture a senior U.S. Department of Transportation official described in a February 2026 patent (US20250378436A1) for a national road-user charging system — explicitly naming hashgraph/Hedera as the preferred anchoring DLT for government-grade auditability. That validation matters for enterprise and public sector buyers.

**Why this is optional, not the core:** The Hedera hashgraph consensus algorithm is patented by Swirlds, Inc. Building PACT's proof mechanism on top of the hashgraph algorithm itself would make independent implementation legally encumbered — a fatal flaw for an open standard. PACT uses Hedera as a *network user* (submitting hashes to HCS), not as an *implementer* of the consensus algorithm. This distinction keeps the protocol genuinely open while still benefiting from Hedera's audit infrastructure.

```
PACT Architecture — Three Layers

┌─────────────────────────────────────────────────────┐
│  PVP Core (open standard)                           │
│  Ed25519 signature + JSON constraint proof          │
│  → works with any rail, no patent encumbrance       │
└─────────────────────┬───────────────────────────────┘
                      │ optional
┌─────────────────────▼───────────────────────────────┐
│  Anchoring Layer (Hedera HCS)                       │
│  Submit PVP hash → get consensus timestamp          │
│  → tamper-proof ordering, ~$0.0001/transaction      │
│  → anchor_ref stored in PVP for audit retrieval     │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│  Registry                                           │
│  Agent identity, vendor tiers, reputation           │
│  → can run on Hedera or any chain                   │
│  → PACT stays rail-agnostic at every layer          │
└─────────────────────────────────────────────────────┘
```

**For enterprise and compliance buyers:** An organization subject to financial audit, SOX compliance, or government procurement requirements can point an auditor to the HCS anchor record for any agent transaction — a neutral, time-stamped, independently verifiable proof of what was purchased, by whom, and when — without relying on PACT's own infrastructure or the counterparty's word.

**Phase 1 vs. Phase 2:** The v0.1 SDK implements HCS anchoring as an opt-in flag — off by default, enabled with a single configuration parameter. ZK-based constraint proofs are a Phase 2 upgrade to the `constraint_proof` field — the schema is forward-compatible.

---

## 4. The Policy Delegation Architecture

### 4.1 The Principal Hierarchy

PACT is not opinionated about internal organizational structure. It provides the primitives for principals to build whatever hierarchy makes sense for them. A typical implementation:

```
Human CEO / Organization
    └── Policy Engine (CEO Agent Layer)
            ├── Agent Fleet A — $50K/month — Cloud Infrastructure
            │       ├── Agent A.1 — $10K/month — AWS
            │       └── Agent A.2 — $10K/month — GCP
            ├── Agent Fleet B — $20K/month — SaaS Tools
            └── Agent Fleet C — $5K/month — Specialized Agent Hiring
```

The Policy Engine is not an AI that makes decisions. It is a living policy document that encodes delegation-of-authority rules, adjusts limits dynamically based on track record, and surfaces anomalies — not routine approvals — to the human principal.

The goal: **human involvement becomes rare and high-quality, rather than frequent and low-value.**

### 4.2 Sub-Agent Delegation

When an agent spawns a sub-agent to handle a specific task, the sub-agent's spending authority is always a strict subset of the parent agent's authority. PACT enforces this through delegation chains in the registry:

- Agent A has mandate M_A
- Agent A creates sub-agent A.1 with mandate M_A.1, where M_A.1 ⊆ M_A
- A.1's PVPs must reference the delegation chain
- Any transaction by A.1 that would exceed A's authority is rejected at proof verification

This prevents the scenario where a compromised or misbehaving sub-agent can exceed the scope it was granted.

### 4.3 Human Escalation

When an agent attempts a transaction that does not satisfy its current mandate, PACT does not fail silently. It generates an escalation request to the principal with:

- The proposed transaction details
- Why it fails against the current mandate
- The agent's reasoning for why it believes the transaction is appropriate
- A structured approval interface for the human to expand the mandate or approve the single transaction

The agent pauses and waits. This creates a natural feedback loop through which principals refine agent mandates over time, progressively reducing escalation frequency as agents demonstrate good judgment.

---

## 5. The Complete Commercial OS

PACT is a protocol layer. The full Commercial OS for the Agentic Economy that sits on top of PACT can support **any procurement form that humans have invented:**

| Procurement Type | PACT Implementation |
|---|---|
| Spot purchase | PVP generated, single transaction |
| Subscription | Recurring PVP with time-bounded authorization |
| RFP | Agent broadcasts structured request, sellers respond, buyer agent evaluates and issues PVP to winner |
| Auction | Agents bid within mandate constraints, winning bid triggers PVP |
| Master Service Agreement | Smart contract template registered in PACT, governs agent-to-agent repeat transactions |
| Retainer | Recurring authorization with deliverable-based release conditions |
| Escrow | Payment held in smart contract pending proof-of-delivery confirmation |
| Brokerage | A registered broker agent intermediates between buyer and seller agents, earns a commission encoded in the PVP transaction intent |
| Brokerage Chain | Multi-hop transaction where Agent X → Broker Bot 1 → Broker Bot 2 → Agent Y; each hop generates its own PVP, commission structures are encoded at each step, and the full chain is traceable in the registry |

Brokerage chains deserve particular attention as a native agentic commerce pattern. In traditional financial markets, brokerage chains — where multiple intermediaries sit between buyer and seller, each taking a fee — are a foundational mechanism for price discovery, liquidity aggregation, and market access. In PACT, a brokerage bot is itself a registered agent with its own identity, mandate, and reputation. It aggregates seller options, presents them to buyer agents, and facilitates matches for a commission. Multi-hop chains are supported by design: each hop in the chain is a discrete PVP-verified transaction, making the full path of a deal auditable end-to-end even across multiple intermediaries. This is commerce infrastructure that didn't exist for humans in this form until centuries of market evolution — PACT makes it native to agent commerce from day one.

The legal framework for agent-to-agent commerce does not yet exist. This is a feature, not a bug. The builders who establish the norms and the dominant platform before regulation arrives are the ones who influence what regulation looks like. Stripe did this with payments. Airbnb did this with short-term rentals. PACT aims to do this for agentic commerce.

---

## 6. Competitive Moat and Strategic Position

### 6.1 Why This Is a Protocol Play, Not a Product Play

The major incumbents — Visa, Mastercard, Stripe, Google — are building products. Products can be replaced. Protocols, once adopted, become infrastructure. The difference is adoption dynamics.

A product competes on features. A protocol competes on network effects. Every developer who builds an agent with the PACT SDK adds to the registry, expands the vendor network, and makes PACT more valuable for the next developer. Standards are winner-take-most — the second-best proof format for agent purchases will be worth close to zero.

MCP was not the first protocol for agent tool connectivity. It won because it shipped open, was developer-first, and reached critical adoption before incumbents built proprietary alternatives. PACT aims for the same dynamic.

### 6.2 The Moat Is the Proof Standard

Visa, Mastercard, and Stripe own the money movement layer. They will always own it. That is not where PACT competes. PACT owns the **decision integrity layer above the money movement** — the standard by which the legitimacy of agentic purchase decisions is verified.

This creates a strategic scenario where incumbent payment rails must support PACT in order to serve the B2B agentic market, rather than PACT competing with them for money transmission. The natural endpoint is not competition with Stripe — it is acquisition by Stripe.

### 6.3 Why a Solo Founder Can Win This

- Standards are not won by the biggest company. They are won by the fastest mover who gets adoption before incumbents wake up
- The agent-to-agent commerce layer is not a priority for Visa, Mastercard, or Stripe today — they are protecting existing consumer revenue streams
- Open-source, developer-first protocols with genuine technical innovation attract co-builders and early adopters that no enterprise R&D team can replicate
- The whitepaper and proof format spec, published openly, cost nothing to distribute and reach exactly the right people — developers frustrated that their agents can't transact

---

## 7. Open Questions — We Are Inviting Collaboration

PACT is a thesis, not a finished specification. The following questions require input from the developer community, legal experts, and commercial builders. If you have thoughts on any of these, we want to hear from you.

**7.1 Liability Framework**
When a PVP passes verification but the underlying decision is strategically wrong (the agent bought the technically cheapest compute but should have negotiated a contract), who bears the loss? The agent's principal? The protocol? The proof system must eventually have a clear liability stack to support real commercial adoption.

**7.2 Cross-Organization A2A Trust**
When Agent X (Company A) hires Agent Y (Company B), this is effectively a B2B commercial transaction between two organizations. What is the agent-native equivalent of a Master Service Agreement? How does PACT handle cross-principal disputes?

**7.3 The Cold Start Problem**
New agents have no reputation. What is the baseline spending authority for a newly registered agent? How does the protocol support gradual trust expansion without requiring every new agent to go through months of low-stakes transactions before it becomes useful?

**7.4 Adversarial Robustness**
The proof system must be tested against seller agents optimized to craft offers that satisfy buyer constraint proofs while still being bad deals. How do we make the proof system adversarially robust — not just correct for honest participants, but resistant to strategic exploitation?

**7.5 The Primitive Question**
PACT currently frames itself as proof format + SDK + registry. Is this the right decomposition? Are there simpler primitives — a token standard, a single on-chain attestation format — that would achieve higher adoption at lower complexity cost?

---

## 8. Conclusion

The agent economy is not coming. It is here. AI agents are becoming digital workers, and digital workers need to participate in markets. The infrastructure for that participation — identity, authorization, proof of valid decision, reputation, multi-form procurement support — does not currently exist in a usable, open, developer-first form.

PACT is our proposal for what that infrastructure looks like. It is not a payment processor. It is not a wallet. It is the commercial operating system layer that makes every form of agentic commerce trustworthy, auditable, and scalable: the proof that an agent's spending was legitimate, wrapped in an SDK any developer can use, anchored to a registry that becomes more valuable with every participant.

The opportunity is to do for agent economic participation what MCP did for agent tool connectivity — define the open standard before the market consolidates around a proprietary alternative.

We are building this openly. If you are a developer building agent infrastructure and you have bumped into the payment problem, we want to build this with you.

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **A2A Commerce** | Agent-to-agent commercial transactions where both buyer and seller are AI agents |
| **PVP** | Proof of Valid Purchase — cryptographic certificate of a legitimate agent purchase decision |
| **Mandate** | The formal specification of what an agent is authorized to purchase, from whom, and under what constraints |
| **Principal** | The human or organization that authorized an agent and is ultimately responsible for its commercial actions |
| **Policy Engine** | The CEO-agent layer that encodes delegation-of-authority rules for an agent fleet |
| **Trust Tier** | Classification of vendors in the PACT registry: Verified, Provisional, or Unverified |
| **KYA** | Know Your Agent — the emerging compliance framework for agent identity verification |
| **Delegation Chain** | The verifiable record of authority passed from principal to orchestrator agent to sub-agents |
| **Ed25519** | An open, unpatented elliptic-curve digital signature algorithm used to sign PVPs; supported by all major languages and platforms with no licensing restrictions |
| **HCS** | Hedera Consensus Service — a distributed ledger service providing tamper-proof, ordered timestamps for submitted data hashes; used as PACT's optional anchoring layer |
| **Anchor Ref** | The Hedera HCS transaction ID stored in a PVP's `anchor_ref` field, enabling independent third-party verification of when a proof was created |
| **Anchoring Layer** | The optional PACT component that submits PVP hashes to HCS for neutral, immutable audit trail creation — separate from and above the core cryptographic proof mechanism |
| **Swirlds** | The company holding the patent on the hashgraph consensus algorithm; PACT uses Hedera as a network user (submitting hashes to HCS) rather than implementing the algorithm, avoiding patent encumbrance |

## Appendix B: Analogous Standards — How Protocols Win

| Protocol | Problem Solved | How It Won | Outcome |
|---|---|---|---|
| **MCP** (Anthropic, 2024) | Agent tool connectivity | Open-sourced, developer-first, shipped before proprietary standards consolidated | Became the de facto standard; every major AI lab supports it |
| **ERC-20** (Ethereum, 2015) | Token standard on Ethereum | Simple, open, developer-friendly — shipped before alternatives | Powers trillions in token value |
| **OAuth 2.0** | Delegated authorization for APIs | Open standard, adopted by Google/Facebook early | Every API in existence supports it |
| **OpenAPI** | API specification format | Open, tooling-first, neutral | Every major API uses it |

The pattern: **open + developer-first + ships before consolidation = winner-take-most.**

---

*PACT is an open protocol proposal. All feedback, critiques, and contributions are welcome.*
*Contact: trosellv@gmail.com*
*Version: 0.1 — March 2026*
