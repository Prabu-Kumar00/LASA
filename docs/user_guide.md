# User Guide: LASA dispensing safety console

This guide provides operational instructions for dispensing staff using the Look-Alike Sound-Alike (LASA) safety interface.

## 1. Operating Modes Overview

The console runs in two primary modes via a toggle at the top of the interface:

*   **Baseline Mode:** A plain alphabetical text list. There are no active warnings, visual product mockups, or barcode gates. Clicking an item dispenses it immediately. Mismatches display a brief banner but do not halt dispensing. Used to model standard legacy pharmacy operations.
*   **Prototype Mode:** The active clinical safety interface. It displays medicines visually as shelf cards, showing simulated packaging (color/shape), shelf location, cold-chain status, and runs active similarity checks.

---

## 2. Dispensing Workflow in Prototype Mode

### Step 1: Select a Prescription (Rx Queue)
The left panel displays the **Rx Queue** containing prescriptions to fill today. Each row lists the intended medicine, strength, and cold-chain status. Click a prescription to set it as the active order.

### Step 2: Set the Barcode Scanner Condition
Simulate the scanner state using the radio buttons:
*   **Normal:** Scanner works correctly (1.5% misread rate).
*   **Scanner Offline (None):** Simulates a missing, unreadable, or bypassed label.
*   **Scanner False-Confirm:** Simulates a scanner reading a mismatched code as a success.

### Step 3: Pick and Scan the Medicine
On the virtual shelf grid, locate the card matching your physical pick and click it. The system will process your selection:

#### State A: OK (Cleared for Dispensing)
*   **Visual Indicator:** Solid green card overlay and green footer panel.
*   **Action:** No warnings are shown. Click the **Dispense** button to finalize. The transaction is logged as a successful pick.

#### State B: WARNING (Verify Before Dispensing)
*   **Visual Indicator:** Orange/amber panel displaying *"WARNING: VERIFY BEFORE DISPENSING"*.
*   **Explanation:** The engine has detected a mismatch, or the barcode scan was bypassed. The panel lists detailed confusion risk reasons (e.g., phonetic name similarity, same storage color, or shelf location proximity).
*   **Action:** 
    1.  Inspect the physical packaging.
    2.  If you realize you made a mistake, click **Re-Pick Item** to reset and pick the correct item.
    3.  If the pick is correct (such as a generic substitute authorized by the physician), click **Manual Override**. You must select or write a justification reason. Click **Confirm Dispense** to log the override.

#### State C: BLOCKED (Do Not Dispense)
*   **Visual Indicator:** Bright red panel displaying *"BLOCKED: DO NOT DISPENSE"*.
*   **Explanation:** The risk score is 0.8 or higher, or the scanner reported an explicit barcode mismatch. The console locks the dispensing action.
*   **Action:** You *cannot* override a blocked state. Click **Re-Pick Item**, return the incorrect carton to the shelf, and retrieve the correct product.

---

## 3. Responding to Uncertainty Notices

If the data quality check fails (e.g. unknown SKU or missing database information), a warning panel will display:
`"Uncertainty notice for authorised staff: Verify carton labels manually before dispensing."`

### Required Protocol:
1.  **Stop Dispensing:** Do not click override immediately.
2.  **Manual Check:** Check the printed name, NDC number, and strength on the physical carton against the prescription paperwork.
3.  **Supervisor Authorization:** Call a senior pharmacist to review the case.
4.  **Override Documentation:** Enter the senior pharmacist's initials and the reason in the override note field, then confirm.
