# Stakeholder Assumptions Document

This document outlines the operational context, staffing characteristics, and technical and clinical assumptions that define the Look-Alike Sound-Alike (LASA) safety interface.

## 1. Clinical Context
*   **Specialty Unit:** The clinic is a specialty dispensing unit handling high-cost, high-risk, and temperature-sensitive biological products (e.g., monoclonal antibodies, insulin analogs, and biologics).
*   **Cold-Chain Storage:** A significant portion of the formulary requires continuous cold-chain storage at **2–8°C**. Cold-chain breach due to dispensing delays, prolonged exposure, or incorrect picks represents both a safety risk and a severe financial waste.
*   **High Dosing Risk:** LASA selections in this clinic frequently involve identical drug names with vastly different strengths (e.g., 5mg vs 20mg pens) or visually identical vials. Errors here can lead to immediate clinical consequences (e.g., severe hypoglycemia or therapeutic failure).

## 2. Staffing Profiles & Slip Probabilities
*   **Professional Qualification:** All dispensing staff are licensed pharmacists or pharmacy technicians. They are trained in aseptic handling and standard verification workflows.
*   **Formulary Experience Differences:** 
    *   **Low Experience Cohort (< 6 months):** Staff members with less than 6 months of formulary experience have a higher base selection slip rate of **18%**. This is due to unfamiliarity with drug locations, similarities in packaging, and naming conventions.
    *   **High Experience Cohort (> 2 years):** Experienced staff have a lower base selection slip rate of **7%**.
*   **Alert Fatigue and Pressure Compliance:** 
    *   Under normal conditions, staff comply with system warnings (initiating self-correction) at a rate of **80%**.
    *   Under environmental stressors, compliance drops to **62%** due to workload pressure, cognitive overload, and alert fatigue. Non-compliant overrides allow errors to bypass the system.

## 3. Technology and Barcode Scanner Reliability
*   **Hardware Availability:** Handheld barcode scanners are available at each dispensing station to scan the simulated NDC/barcode on cartons.
*   **Imperfection of Barcode Scanners:** 
    *   Under normal conditions, scanners have a **1.5% misread rate**.
    *   Under stressors (e.g., smudged labels, poor lighting, or interruptions), the misread rate increases to **4.0%**.
    *   On misread, the scanner returns the *opposite* of the truth (e.g., false confirmation for an incorrect item, or false mismatch for a correct item).
*   **Scanner Offlines / Missing Labels:** In certain cases, barcodes are missing or damaged (modeled under the `missing_label` stressor). In these cases, the scanner returns `None`.

## 4. Operational and Regulatory Constraints
*   **No Silents Passes:** Every dispensing transaction must go through the safety check. If the scanner is offline, manual verification is mandated, and a warning/uncertainty notice is shown.
*   **Audit Logging:** Regulatory guidelines mandate that every blocked pick, warning, and manual override must be logged with the staff ID, timestamp, intended/picked SKUs, and a reason for override (if applicable).
*   **Escalation Path:** Pharmacist oversight is available. Any confidence score below 0.5 (such as from unknown SKUs or missing drug names) triggers an explicit "Uncertainty notice for authorised staff" requiring a senior pharmacist's signature to override.
