# System Architecture Document

This document describes the architectural flow of the Look-Alike Sound-Alike (LASA) safety system. It details how prescription data, barcode hardware, and the similarity analysis engine interact to intercept selection errors at the point of dispensing.

## System Workflow Diagram

```mermaid
graph TD
    %% Define components
    A["Prescription Queue (Rx)"] --> B["Pharmacy Staff Pick Event"]
    B --> C["Barcode Scan Attempt"]
    
    %% Barcode scanner logic
    C -->|Scan Successful| D{"Barcode Matches Database?"}
    C -->|Label Missing / Offline (None)| E["Confidence Capped at 0.6"]
    
    D -->|Yes (True)| F["Secondary Check: Similarity Engine"]
    D -->|No (False)| G["Hard Block (Dispense Prevented)"]
    
    %% Engine evaluation
    E --> F
    F --> H["Phonetic Match Layer (difflib)"]
    F --> I["Visual Match Layer (color/shape/key)"]
    F --> J["Shelf Proximity Layer (location distance)"]
    
    H & I & J --> K["Calculate Risk Score (confusion_risk)"]
    K --> L["Check Dosing Escalation (+0.15 for Diff Strength)"]
    L --> M["check_pick() Decision Logic"]
    
    %% Decision outputs
    M -->|Score >= 0.8 OR Barcode Mismatch| N["Block State (Red Panel)"]
    M -->|Score >= 0.3 OR SKU Mismatch| O["Warning State (Amber Panel)"]
    M -->|Clear Match & Scanner OK| P["OK State (Green Panel)"]
    
    %% Escalation and logging
    N --> Q["Forced Re-Pick (Workflow Locked)"]
    O --> R{"Staff Self-Corrects?"}
    R -->|Yes| Q
    R -->|No (Override)| S["Prompt for Override Reason"]
    
    S & P & Q --> T["Write to Audit Log (Timestamp, SKU, Staff ID)"]
    
    %% Uncertainty notice
    M --> U{"Confidence < 0.5?"}
    U -->|Yes| V["Uncertainty Alert (Escalate to Senior Pharmacist)"]
    V --> S
```

## Description of Architectural Components

1.  **Prescription Queue (Rx):** The entry point. Staff receive a validated order containing the *intended* SKU.
2.  **Pick Event:** The staff member physically retrieves a package from the shelf.
3.  **Barcode Scan Layer:** The primary digital verification.
    *   If the barcode scanner reports a mismatch (`barcode_scan_ok=False`), the system halts immediately and blocks.
    *   If the scanner is bypassed or fails (`barcode_scan_ok=None`), the engine's confidence is capped, and manual label verification is enforced.
    *   If the scanner reports a match (`barcode_scan_ok=True`) but the physical SKUs are different, a `scanner_false_confirmation_suspected` flag is raised, bypassing scanner trust and relying on similarity metrics.
4.  **LASA Similarity Engine:** A deterministic, multi-attribute rule-based model:
    *   **Phonetic:** Checks name similarity using difflib.
    *   **Visual:** Computes weighted overlap of the carton color, packaging shape, and visual signature key.
    *   **Shelf:** Checks whether products are adjacent, which increases visual confusion during retrieval.
5.  **Dosing Risk Escalation:** If two medicines are phonetically similar but have different strengths, a +0.15 dosing risk penalty is added.
6.  **Decision logic (`check_pick`):** Categorizes outcomes into OK (cleared), Warning (requires caution/override), or Block (prevents dispensing).
7.  **Audit Log & Escalation:** Stores all events. If confidence is below 0.5 (unknown SKU or blank database field), it triggers an escalation requiring a senior pharmacist's override.
