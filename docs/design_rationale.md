# Design Rationale Document

This document explains the technical design decisions, algorithmic trade-offs, and numeric parameters that govern the Look-Alike Sound-Alike (LASA) safety interface.

## 1. Why Rule-Based Logic Over Machine Learning?

In clinical and pharmaceutical environments, safety gates must be absolute, auditable, and deterministic. An ML-based classifier (e.g., deep neural network or large language model) was rejected in favor of a rule-based, string-similarity system for the following key reasons:

### (a) Auditability and Regulatory Compliance
Every blocked or warned pick must be justified under clinical standards. A rule-based algorithm has a fully auditable decision path. It can output exact mathematical components (e.g., `0.45 name + 0.35 visual + 0.20 shelf = 0.85`) and explainable natural language reasons. This satisfies pharmacy safety boards, which reject "black-box" systems.

### (b) No Training Data Dependency
Formularies change frequently as new brands and biosimilars are introduced. An ML classifier would require retraining, re-calibration, and validation with every new drug addition. The rule-based system requires no historical training data; it evaluates safety immediately upon database entry of a single new SKU.

### (c) Deterministic Behavior
Under safety-critical software engineering, identical inputs must produce identical outputs. Opaque ML models can exhibit non-deterministic behavior or shift predictions due to subtle context changes. The rule-based engine behaves identically under every execution, which is crucial for regulatory software validation.

### (d) Explainable Confidence
Rather than calibrating ML probability scores to estimate confidence, this engine derives confidence directly from discrete **data-quality flags** (e.g., blank name records, missing barcode scans). This provides actionable feedback (e.g. telling a technician that data is missing and they must call the pharmacist) rather than an arbitrary probability.

---

## 2. Numeric Weights and Parameter Justification

The safety engine calculations are guided by a set of carefully calibrated parameters:

```
Confusion Risk = (0.45 * Phonetic) + (0.35 * Visual) + (0.20 * Shelf Proximity) [+ 0.15 Dosing Escalation]
```

### (a) Weights Formulation
*   **Phonetic Weight (0.45):** Naming is the primary identification mechanism. Sound-alike pairs (e.g. *Avenzira* vs *Avenzyla*) represent the highest cognitive confusion point for staff who read prescriptions off a screen or verify verbally.
*   **Visual Weight (0.35):** Color and package shape are dominant visual cues. Similarity in packaging layout and carton color can trick the visual cortex, especially when working fast.
*   **Shelf Proximity Weight (0.20):** Items stored on the same shelf (`1.0`) or adjacent shelves within the same zone (`0.5`) are significantly more likely to be mis-picked due to physical reaching errors.

### (b) Dosing Risk Escalation (+0.15)
*   **Rule:** Added if phonetic similarity > 0.6 AND strengths differ.
*   **Justification:** In dispensing literature, same-drug-family errors with different strengths represent the most dangerous clinical slips (e.g. giving 20mg instead of 5mg). The +0.15 penalty elevates these slips into the **Block** threshold, preventing manual override.

### (c) Threshold Settings
*   **Block Threshold (>= 0.8):** A score of 0.8 or higher indicates critical confusion risk (e.g. same name/different strength stored nearby, or visually identical items stored in the same place). The workflow is locked, forcing a correct re-pick.
*   **Warning Threshold (>= 0.3):** Any score above 0.3 indicates moderate similarity. Additionally, **any SKU mismatch, regardless of score, defaults to at least a Warning** to ensure staff are alerted to the discrepancy.

---

## 3. Simulation & Behavior Parameters

The simulation model (`app/simulation.py`) incorporates operational research parameters representing real-world human factors and scanner failure modes:

*   **Base Slip Rates:**
    *   *Low-experience staff (< 6 months):* **18%**. Represents unfamiliarity with new stock layouts.
    *   *High-experience staff (> 2 years):* **7%**. Represents cognitive auto-pilot slips.
*   **Stressor Multipliers:**
    *   *Interrupted (1.6x):* Distractions break short-term memory, leading to retrieval errors.
    *   *Poor Lighting (1.8x):* Increases visual slip rates and scanner misreads.
    *   *Missing Label (2.4x):* Severely impedes checking, forces manual reading, and disables barcode scanner.
*   **Warning Compliance Rates:**
    *   *No Stressor (80%):* Most warnings are respected, leading to self-correction.
    *   *Under Stressor (62%):* Workload pressure and alert fatigue cause staff to override 38% of warnings.
*   **Scanner Misread Rate:**
    *   *Normal (1.5%):* Baseline hardware sensor failure.
    *   *Stressed (4.0%):* Higher error due to smudges, fast movement, or low lighting.
