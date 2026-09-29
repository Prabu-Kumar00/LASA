# Look-Alike Sound-Alike (LASA) Selection Safety Interface: Clinical Validation Report

This report presents the clinical, statistical, and operational validation of the LASA Safety Interface. The system was evaluated using a simulated trial of 4,000 prescriptions dispensing temperature-sensitive and high-risk medicines under various operational stressors.

---

## 1. Executive Summary

This project establishes a deterministic, multi-layered safety interface to prevent dispensing errors of Look-Alike Sound-Alike (LASA) medicines within a specialty biologics clinic. A validation experiment simulating 4,000 transactions demonstrated that the safety interface reduced the overall selection error rate from **23.38%** in the plain-list baseline to **2.28%** in the prototype. This represents a **90.27%** relative reduction in patient-reaching errors, meeting the target rate of <3.0% and confirming the safety barrier's effectiveness. Crucially, the system protected low-experience and high-experience operators equitably, limiting the cohort equity gap to a negligible **0.52 percentage points**, well below the 15pp safety threshold.

---

## 2. System Architecture

The safety console operates as a gatekeeper at the point of dispensing. When a pick is executed, it passes through sequential validation layers (barcode hardware check and secondary similarity checks) before dispensing is cleared.

```mermaid
graph TD
    A["Prescription Queue (Rx)"] --> B["Pharmacy Staff Pick Event"]
    B --> C["Barcode Scan Attempt"]
    
    C -->|Scan Successful| D{"Barcode Matches Database?"}
    C -->|Label Missing / Offline (None)| E["Confidence Capped at 0.6"]
    
    D -->|Yes (True)| F["Secondary Check: Similarity Engine"]
    D -->|No (False)| G["Hard Block (Dispense Prevented)"]
    
    E --> F
    F --> H["Phonetic Match Layer (difflib)"]
    F --> I["Visual Match Layer (color/shape/key)"]
    F --> J["Shelf Proximity Layer (location distance)"]
    
    H & I & J --> K["Calculate Risk Score (confusion_risk)"]
    K --> L["Check Dosing Escalation (+0.15 for Diff Strength)"]
    L --> M["check_pick() Decision Logic"]
    
    M -->|Score >= 0.8 OR Barcode Mismatch| N["Block State (Red Panel)"]
    M -->|Score >= 0.3 OR SKU Mismatch| O["Warning State (Amber Panel)"]
    M -->|Clear Match & Scanner OK| P["OK State (Green Panel)"]
    
    N --> Q["Forced Re-Pick (Workflow Locked)"]
    O --> R{"Staff Self-Corrects?"}
    R -->|Yes| Q
    R -->|No (Override)| S["Prompt for Override Reason"]
    
    S & P & Q --> T["Write to Audit Log (Timestamp, SKU, Staff ID)"]
    
    M --> U{"Confidence < 0.5?"}
    U -->|Yes| V["Uncertainty Alert (Escalate to Senior Pharmacist)"]
    V --> S
```

---

## 3. LASA Pair Catalog & Risk Scores

The 12 synthetic medicines in the catalog contain 4 targeted high-risk LASA pairs. The table below details their characteristics, calculated risk scores, and system classifications:

| Intended SKU | Picked SKU | Similarity Types | Calculated Risk Score | System Action | Risk Analysis Details |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MED-AVEN-10` *(Avenzira)* | `MED-AVEN-50` *(Avenzyla)* | Phonetic | **0.6925** | **Warning** | High phonetic overlap (0.75 name similarity) and dosing risk penalty (+0.15) for strength mismatch, offset by visual shape/color differences. |
| `MED-BAVI-100` *(Bavinex)* | `MED-KRY-200` *(Krysolis)* | Visual | **0.5700** | **Warning** | Identical red color and vial shape, but phonetic name similarity is very low (0.27). |
| `MED-ZILO-50` *(Zilomed)* | `MED-ZILO-100` *(Zilomax)* | Phonetic & Visual | **1.0000** (Capped) | **Block** | High name similarity (0.71), identical green blister packaging, and stored on the exact same shelf (`R3-A`). |
| `MED-GLYC-05` *(Glycopen Mite)* | `MED-GLYC-20` *(Glycopen Forte)* | Family & Strength | **0.9333** | **Block** | Same-family visual pen cartons (yellow), name similarity (0.74), and different strengths (dosing penalty +0.15). |

---

## 4. Experiment Results

The results from the simulation run of 4,000 prescriptions are summarized below:

### Measurable Experiment Table

| Metric | Baseline | Target | Measured | Error Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **Overall error rate** | ~15% | <3% | **2.28%** | Baseline: **23.38%** (935/4000 errors). The prototype intercepted 756 picks via blocks (corrected) and prompted 246 warnings (155 self-corrected, 91 overridden), resulting in **91 residual errors**. |
| **Low-exp reduction** | — | >90% | **90.12%** | Reduced error rate from **33.25%** to **3.29%**, demonstrating excellent protection for novice staff under cognitive stress. |
| **High-exp reduction** | — | >85% | **90.64%** | Reduced error rate from **13.41%** to **1.26%**, proving that standardised software controls mitigate auto-pilot slips in experienced staff. |
| **Equity gap** | — | <15pp | **0.52pp** | Relative reduction difference is **0.52 percentage points**. Status: **CLEAR**. Standardised rules act as an equalizer. |

### Cohort Bias Analysis Table

| Cohort | Total Transactions | Baseline Errors | Prototype Errors | Relative Error Reduction | Bias Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Low Experience** | 2009 | 668 (33.25%) | 66 (3.29%) | **90.12%** | Protected under stress |
| **High Experience** | 1991 | 267 (13.41%) | 25 (1.26%) | **90.64%** | Protected under stress |
| **Equity Gap** | — | — | — | **0.52pp** | **CLEAR: NO BIAS CONCERN** |

### Stressor Impact Analysis Table

| Environmental Stressor | Total Rx | Baseline Error Rate | Prototype Error Rate | Relative Reduction | Clinical Implications |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **None** | 1040 | 15.58% | **0.00%** | **100.00%** | Absolute safety achieved when scanners and packaging are clean and readable. |
| **Interrupted** | 981 | 22.94% | **0.20%** | **99.11%** | Interrupted staff recover errors via warning/block prompts. |
| **Poor Lighting** | 1019 | 23.75% | **0.39%** | **98.35%** | Minor error leaks due to 4% scanner misreads, caught by similarity checks. |
| **Missing Label** | 960 | 31.88% | **8.85%** | **72.22%** | Scanner is offline (`None`). High warning rates and alert fatigue result in 91 overrides, leading to residual errors. |

---

## 5. Technical Documentation: Unit Testing and Error Boundaries

To ensure the deterministic reliability of the decision engine, we implemented a rigorous suite of unit tests (`tests/test_edge_cases.py`) focusing on explicit error boundaries and data quality faults. The engine is engineered to fail gracefully and default to a restrictive safety posture when inputs are missing, corrupted, or contradictory.

### 5.1 System Error Boundaries & Fault Tolerance
The `lasa_engine.py` API establishes specific boundary constraints to prevent software crashes or silent bypasses:
1.  **Null or Blank Identifiers (`missing_name`)**: If the database returns a blank string for a medicine name, the engine does not throw a `TypeError` during sequence matching. It captures the fault, flags `"missing_name"`, forces a pessimistic confidence score of `0.4`, and ensures a warning is surfaced to the pharmacist.
2.  **Unregistered Inventory (`unknown_sku`)**: If an operator scans a barcode that does not exist in the active `CATALOG`, the system safely intercepts the `KeyError`. It caps the confidence at `0.3` and returns a direct error message instructing manual verification, preventing unauthorized dispenses.
3.  **Hardware Contradictions (`scanner_false_confirmation_suspected`)**: The system does not unconditionally trust the barcode scanner. If the scanner reports `True` (Match) but the logical SKU evaluation identifies a discrepancy, the software boundary assumes hardware failure (e.g., a misread or spoofed barcode) and enforces a manual warning.

### 5.2 Unit & Integration Test Results
All clinical edge-case tests compiled in `tests/test_edge_cases.py` execute and pass successfully prior to deployment, guaranteeing the integrity of the above error boundaries:

| Test Case Suite | Description & Targeted Boundary | Expected Output | Status | Validation Detail |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1** | Unknown SKU (Not in Catalog) | Warn + Uncertainty Message + Flag `"unknown_sku"` | **PASS** | Captured successfully; prevents silent passes for unregistered inventory. |
| **Case 2** | Missing Barcode Scan (scanner=None) on Correct Pick | Reduce confidence to 0.6 + uncertainty message | **PASS** | Bypassing scanner lowers transaction confidence and warns staff. |
| **Case 3** | Explicit Barcode Mismatch (scanner=False) | Hard block regardless of similarity | **PASS** | Scanner warning overrides similarity; locks the interface immediately. |
| **Case 4** | Blank Medicine Name (Database Fault) | Do not crash, flag `"missing_name"`, reduce confidence | **PASS** | Fault-tolerant name matching logic; prevents runtime errors. |
| **Case 5** | Scanner False-Confirmation (scanner=True, items differ) | Catch via similarity, flag `"scanner_false_confirmation_suspected"` | **PASS** | The visual/phonetic similarity layer intercepts scanner hardware failures. |
| **Case 6** | Same-Family, Different-Strength Pair | Risk Score >= 0.7 + `"DOSING RISK"` in reason string | **PASS** | Correctly escalates same-family strength mismatches to a hard block. |

---

## 6. Dispensing Workflow: Before-and-After Narrative

### Baseline Workflow (Before)
1.  The operator reads a prescription (e.g., *Avenzira 10mg*) from the screen.
2.  Under noise, lighting, or distraction stressors, the operator walks to shelf `R1` and mis-picks *Avenzyla 50mg* (due to similar names and adjacent shelf locations).
3.  The operator returns to the bench, skips barcode scanning (or the scanner is smudged), and dispenses the drug directly to the patient.
4.  **Result:** The patient receives a 5x overdose of a cold-chain biologic. No logs or warnings exist to trace the event.

### Safety Interface Workflow (After)
1.  The operator selects the prescription for *Avenzira 10mg*.
2.  The operator mis-picks *Avenzyla 50mg*.
3.  The operator clicks the *Avenzyla 50mg* card on the shelf (simulating a barcode scan).
4.  **The Safety Layer Intervenes:**
    *   Since phonetic similarity is high and strengths differ, the system calculates a confusion risk of **0.6925**.
    *   An amber **WARNING** screen overlays the console, displaying: *"WARNING: VERIFY BEFORE DISPENSING. Reason: High phonetic name similarity, same carton shape, stored on adjacent shelves, DOSING RISK."*
5.  **Operator Action:** The warning forces the operator to read the carton. They click **Re-Pick Item**, return the *Avenzyla 50mg* to `R1-B`, grab the correct *Avenzira 10mg*, and scan it.
6.  The green **CLEARED** screen appears.
7.  **Result:** The error is intercepted. The audit log records the correction, ensuring full traceabilty.

---

## 7. Failure State Documentation

Every potential system failure surfaces a clear message to authorized staff:

1.  **Scanner Offline/Missing Barcode (`barcode_scan_ok = None`):** Surfaces an orange warning box: *"Barcode scan missing: Cold-chain barcode could not be read. Uncertainty notice for authorised staff. Verify carton labels manually."* Confidence is reduced to 0.6.
2.  **Blank Medicine Name (`missing_name`):** Surfaces: *"Data quality alert: Missing drug metadata (blank name) prevents full safety checks. Pharmacist escalation required."* Confidence is reduced to 0.4.
3.  **Unknown SKU (`unknown_sku`):** Surfaces: *"Unknown SKU: Picked item is not registered in the active system catalog. Please escalate to the pharmacist for manual verification."* Confidence is reduced to 0.3.
4.  **Scanner False-Confirmation (`scanner_false_confirmation_suspected`):** Logs a warning in the background, bypasses scanner confirmation, and presents similarity warnings to the user.

---

## 8. Limitations & Residual Risks

*   **Alert Fatigue:** Under a high volume of prescriptions, operators might develop override fatigue, especially when barcodes are missing (`missing_label` stressor error rate was 8.85%).
*   **Emergency Bypasses:** In critical code-blue scenarios, senior staff might use general clinical overrides to speed up dispensing, bypassing warnings.
*   **Manual Entry Reliance:** If the database itself is entered incorrectly (e.g., a new biologic color is entered with a typo), the visual similarity logic will compute an incorrect risk score.

---

## 9. User Usability Walkthrough (Simulated)

### Persona A: Sarah (Low-Experience Pharmacy Technician, <6 months)
*   **Context:** Sarah is dispensing under a hectic workflow (Interrupted stressor).
*   **Scenario (LASA Pick):** She has a prescription for *Glycopen Mite 5mg* (refrigerated pen). She slips and picks *Glycopen Forte 20mg* from shelf `R4-B`.
*   **Console Behavior:** When clicked, the console displays a bright red **BLOCKED — DO NOT DISPENSE** panel. The risk score is **0.9333** (due to color, shape, phonetic match, and dosing penalty). The "Override" button is disabled.
*   **Sarah's Actions:** The red block stops her. She reads the warning reason: *"DOSING RISK: Similar name but different strengths (5mg vs 20mg)"*. She returns the Forte pen to the fridge, picks the Mite pen, and scans it. The console turns green and she completes the dispense.

### Persona B: Robert (Senior Pharmacist, >10 years)
*   **Context:** Robert is supervising the dispensing station during a network outage (Scanner Offline).
*   **Scenario (Missing Label):** Tech L-14 tries to scan a correct vial of *Bavinex 100mg* but the label is smudged. The scanner reports offline.
*   **Console Behavior:** The console displays an orange warning panel with a lower confidence rating (0.6) and an amber box: *"Uncertainty notice for authorised staff. Verify carton labels manually."*
*   **Robert's Actions:** Tech L-14 escalates the transaction to Robert. Robert visually inspects the *Bavinex 100mg* vial and matches its details against the paper prescription. Satisfied, he enters his initials `"R.G."` and the reason `"Smudged barcode label manually verified"` into the override text field, then clicks **Manual Override & Dispense**. The audit log records the override, the staff ID, and the text justification.
