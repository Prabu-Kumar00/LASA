# Risk Register

This document identifies operational, clinical, and technological risks associated with the Look-Alike Sound-Alike (LASA) safety interface, along with their mitigations.

## 1. Safety & System Risk Matrix

| Risk ID | Hazard Description | Likelihood | Impact | Severity | Mitigation & Controls |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Scanner False-Confirmation:** Barcode scanner misreads a mismatched barcode as a match, creating false confirmation. | Medium | Critical | High | Secondary check layer: The similarity engine evaluates all transactions. Even if the scanner reports a match, if database SKUs differ, the engine flags `scanner_false_confirmation_suspected` and warns the user. |
| **RSK-02** | **Alert Fatigue:** Staff override warnings without reading details due to repetitive alerts, leading to error slips. | High | Major | High | Hard block on high-risk confusion pairs (>= 0.8) which prevents overrides. Warn on lower risk pairs, and require staff to type or select an override reason which is logged in the audit trail. |
| **RSK-03** | **Unknown SKU at Point of Pick:** A medicine card is scanned but is not in the system catalog database. | Low | Major | Medium | The system flags `"unknown_sku"`, raises a warning, caps confidence at 0.3, and displays an explicit uncertainty notice instructing the pharmacist to escalate and verify. |
| **RSK-04** | **Catalog Sync Failure:** Discrepancies between the local database and the central inventory system lead to outdated similarity keys. | Low | Major | Medium | Mandate local database synchronization at the start of every shift. If sync fails, the system reverts to offline checking mode and reduces confidence, triggering manual verification. |
| **RSK-05** | **Cold-Chain Breach During Blocks:** A block event locks the dispensing console, causing a queue delay. If cold-chain items are left out on the table, they degrade. | Medium | Major | Medium | Visual "COLD CHAIN" badge flashing red if a block occurs on a cold-chain item, prompting the technician to immediately return the item to the refrigerator while resolving the block. |
| **RSK-06** | **Cohort Equity / Bias Concern:** The engine's safety mechanisms favor one staff experience cohort, leading to disproportionate error rates for novice staff. | Low | Major | Medium | Continuous bias testing (during simulation runs) to monitor that the equity gap in relative error reduction between low and high experience cohorts remains under **15 percentage points**. |

## 2. Risk Mitigation Protocols

### Protocol RSK-01: Scanner False-Confirmation Response
If the barcode scanner reports a success but the database registers different SKUs, the dispensing terminal triggers an orange screen override. The user is prompted:
*   *"Warning: Scanner conflict. Database records mismatch. Inspect carton label and manually select action."*
*   The action is logged in the audit database.

### Protocol RSK-02: Alert Fatigue Reduction
To prevent alert fatigue, the safety interface does *not* pop up warning dialogues for correct picks that have scanned successfully. Warnings are strictly limited to mismatch events. Mismatch events are color-coded based on risk severity so that users distinguish a low-risk generic mismatch from a high-risk LASA mistake.

### Protocol RSK-05: Cold-Chain Protection
For any medicine where `cold_chain = True`, if the safety engine returns a block or warning:
1.  A flashing warning badge appears: `"❄️ COLD CHAIN ITEM: Return to Fridge immediately if delay exceeds 2 minutes."`
2.  The audit log records the time elapsed between the pick event and final resolution.
