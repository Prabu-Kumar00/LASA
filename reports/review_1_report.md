# Review 1 Submission Report

**Project Title:** Look-Alike Sound-Alike (LASA) Medicine Selection Safety Console  
**Domain:** Healthcare Software & Clinical Decision Support Systems (Software/Algorithmic Simulator & Clinical Web Interface)  
**Target Completion for Review 1:** ~35% of Total Project Lifecycle  

---

## 1. Executive Summary & Hardware Clarification

### Hardware Requirement Clarification
> **Note regarding Hardware:** **No physical hardware components are needed or required for this project.**  
> The LASA Safety Console is entirely a software application consisting of:
> 1. A Python-based deterministic similarity engine (`difflib`, multi-attribute scoring algorithms, and human-factor simulation engines).
> 2. A zero-dependency web-based interactive dispensing console (`app/mvp.html` with vanilla HTML5, CSS3, and JavaScript).
> 3. Procedural visual packaging generation via Python `Pillow`.

Barcode scanning hardware and physical inventory shelves are modeled logically and simulated via software event handlers and barcode payload matching algorithms.

---

## 2. Work Completed So Far (~35% Scope)

For **Review 1**, the primary architectural foundation, core deterministic algorithms, data schema, edge case test suites, and interactive front-end prototype have been fully implemented and verified.

### Summary of Completed Deliverables:
1. **Core LASA Similarity Engine (`app/lasa_engine.py`)**:
   - Implemented a multi-layered similarity detection algorithm combining **Phonetic Similarity** (`difflib.SequenceMatcher`), **Visual Similarity** (color scheme, packaging form factor, visual keyword matching), and **Shelf Proximity** (physical bay and shelf matrix distance).
   - Integrated confidence scoring and risk escalation (e.g., +0.15 score bump for identical strength variations).

2. **Synthetic Medical Catalog & Data Schema (`data/medicine_catalog.py`)**:
   - Created a catalog of 12 synthetic high-risk biologic and insulin drugs forming 4 target LASA confusion pairs (e.g., *Humalog 100 U/mL* vs. *Humulin 100 U/mL*, *Herceptin 150mg* vs. *Kadcyla 100mg*).
   - Designed schema structures (`docs/data_schema.md`) covering barcode mapping, shelf location vectors, and risk profiles.

3. **Procedural Packaging & Mockup Generator (`data/generate_packaging.py`)**:
   - Built a Python Pillow script that dynamically generates visual label assets (`.png`) for all 12 catalog items in `app/static/packaging/` to emulate real-world drug appearance.

4. **Standalone Interactive Dispensing Terminal (`app/mvp.html`)**:
   - Developed a responsive, dark-themed HTML/CSS/JS frontend supporting dual-mode operation:
     - **Baseline Mode**: Alphabetical plain list representing typical unassisted pharmacy picking workflows.
     - **Prototype Mode**: Interactive grid with product packaging images, shelf locations, real-time risk evaluation, visual warning overlays (Amber/Red alerts), override modals, and live audit logging.

5. **Clinical Edge Case Verification Suite (`tests/test_edge_cases.py`)**:
   - Developed 6 comprehensive automated test cases covering unknown SKUs, exact barcode matches, offline/missing barcode reads, visual-only similarity, shelf distance fallbacks, and override logging.
   - **Verification Status:** All 6 test suites pass cleanly (`PASS`).

---

## 3. Key Modules & Features Completed

| Module / Component | File Location | Key Capabilities & Features | Status |
| :--- | :--- | :--- | :--- |
| **Similarity Engine** | [`app/lasa_engine.py`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/app/lasa_engine.py) | Calculates `confusion_risk` and system action (`BLOCK`, `WARN`, `OK`) based on multi-attribute weights. | **Completed** |
| **Medicine Catalog** | [`data/medicine_catalog.py`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/data/medicine_catalog.py) | 12 high-risk synthetic SKUs with physical, phonetic, visual, and barcode attributes. | **Completed** |
| **Packaging Asset Engine** | [`data/generate_packaging.py`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/data/generate_packaging.py) | Draws color-coded packaging labels and cartons via Python `Pillow`. | **Completed** |
| **Dispensing Web UI** | [`app/mvp.html`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/app/mvp.html) | Interactive simulation terminal with baseline/prototype toggle, visual alerts, and audit trail. | **Completed** |
| **Edge Case Test Suite** | [`tests/test_edge_cases.py`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/tests/test_edge_cases.py) | Validates boundary conditions (unknown SKUs, missing barcodes, override trails). | **Completed (6/6 Pass)** |
| **Core Documentation** | [`docs/`](file:///f:/Clg%20Stuff/Project/Sem%205/LASA/docs) | Architecture diagrams, data schemas, risk registers, and design rationales. | **Completed** |

---

## 4. What is Currently Working

1. **Automated Detection & Alert Triggering**:
   - Picking an incorrect item in **Prototype Mode** immediately calculates the risk score and displays appropriate alerts:
     - **Red HARD BLOCK** for barcode mismatch or high confusion risk ($\ge 0.8$).
     - **Amber WARNING** for moderate confusion risk ($\ge 0.3$).
2. **Audit Logging & Override Tracking**:
   - Override inputs (such as supervisor approval or clinical override reasons) are captured with timestamps and logged to an on-screen audit log panel.
3. **Multi-Factor Risk Calculation Engine**:
   - Verified accurate scoring across phonetic, visual, shelf location, and dosage strength attributes.
4. **Edge Case Verification**:
   - Running `python tests/test_edge_cases.py` confirms that 100% of defined edge cases complete successfully without unhandled exceptions or silent failures.

---

## 5. Pending Work & Next Steps (Remaining Scope for Reviews 2 & 3)

The remaining ~65% of the project lifecycle will focus on full Monte Carlo stress testing, statistical analysis, human error modeling, and finalizing the project report:

1. **Full-Scale Human-Factor Monte Carlo Simulation (`app/simulation.py` & `app/experiment.py`)**:
   - Finalize the stochastic simulation loop evaluating 4,000 synthetic prescription transactions across varying operator experience levels (Junior Technicians vs. Senior Pharmacists) and fatigue/stress conditions.
2. **Statistical Validation & Equity Analysis**:
   - Measure error reduction percentages, relative risk reduction, alert fatigue metrics, and ensure the cohort equity gap stays below the 15% threshold.
3. **Export & Analytics Tooling**:
   - Save experimental outputs (`reports/experiment_results.json`) and auto-generate summary statistical figures/charts for inclusion in the final review.
4. **Final Comprehensive Documentation & Packaging**:
   - Complete section updates in `reports/final_report.md` and user operator manuals.

---

## Summary Table for Evaluation

- **Target Review Percentage:** 35%  
- **Hardware Requirement:** **None** (100% Software / Simulation / Web UI)  
- **Completed Components:** Similarity Engine, Dataclass Catalog, Packaging Generator, Standalone Web Console, Unit/Edge-Case Test Suite.  
- **Verification Result:** 6/6 Edge Case Tests Passed (`python tests/test_edge_cases.py`).  
