# Look-Alike Sound-Alike (LASA) Medicine Selection Safety Console

This project implements a clinical safety interface designed to intercept Look-Alike Sound-Alike (LASA) medicine selection errors before they reach patients. It is tailored for specialty clinics dispensing temperature-sensitive biologics, monoclonal antibodies, and insulin analogs. Utilizing a deterministic, multi-attribute similarity engine (phonetic, visual, and shelf proximity layers), it actively monitors scan actions and provides clear visual block and warning screens. In a trial simulation of 4,000 prescriptions, this safety system reduced patient-reaching errors by **90.27%** (bringing the error rate down from **23.38%** to **2.28%**) while ensuring equitable protection for both low-experience and high-experience operators.

---

## Repository Structure

```
lasa-safety/
├── data/
│   ├── medicine_catalog.py       # Dataclass & 12 fictional drug records
│   └── generate_packaging.py     # Pillow script drawing labels & mockups
├── app/
│   ├── lasa_engine.py            # Phonetic, visual, proximity rules engine
│   ├── simulation.py             # Human factor & stressor simulation loop
│   ├── experiment.py             # Experiment runner and results compiler
│   ├── mvp.html                  # Standalone interactive dispensing terminal
│   └── static/
│       └── packaging/            # Folder containing procedurally drawn PNGs
├── tests/
│   └── test_edge_cases.py        # 6 mandatory unit/integration tests
├── docs/
│   ├── stakeholder_assumptions.md # Clinical context and workforce parameters
│   ├── architecture.md           # Flow of decision, logic, and data
│   ├── data_schema.md            # Schema definitions for JSON and engine classes
│   ├── design_rationale.md       # Auditability trade-offs and numeric weights
│   ├── risk_register.md          # Alert fatigue, scanner failure mitigations
│   └── user_guide.md             # Staff manual for operating the console
├── reports/
│   ├── experiment_results.json   # Output data from the simulation run
│   ├── report_2.md               # Phase 2 70% completion report
│   └── final_report.md           # Main validation report
├── requirements.txt              # Project dependencies
└── README.md                     # Setup and usage instructions
```

---

## Setup & Quickstart

Everything is reproducible from a fresh clone. Follow these steps to install dependencies, generate visual assets, execute verification tests, and run the simulation:

### 1. Install Dependencies
Install Python package dependencies (primarily `Pillow` for graphics):
```bash
pip install -r requirements.txt
```

### 2. Generate Packaging Images
Generate the procedural labels and cartons for the 12 synthetic medicines:
```bash
python data/generate_packaging.py
```
*Output: 12 `.png` files saved in `app/static/packaging/`.*

### 3. Run Edge Case Tests
Validate the safety engine against the 6 critical clinical edge cases:
```bash
python tests/test_edge_cases.py
```
*Output: All 6 test suites must print `PASS`.*

### 4. Run the Simulation Experiment
Execute the 4,000-prescription simulation trial to compute overall baseline vs. prototype error rates:
```bash
python app/experiment.py
```
*Output: Generates quantitative evaluation tables in the console and saves raw data to `reports/experiment_results.json`.*

### 5. Launch the Dispensing Console API
Start the FastAPI REST backend which serves the interactive HTML interface:
```bash
python app/api.py
```
Then open the standalone clinical console in any modern web browser:
```bash
# Windows
start http://localhost:8000

# Mac
open http://localhost:8000

# Linux
xdg-open http://localhost:8000
```

---

## Technical Documentation

### API Endpoints
The dispensing console communicates with the engine via a FastAPI backend:
*   `GET /catalog`: Retrieves the complete structured JSON array of all SKUs in the formulary. Used by the frontend to construct the visual shelf grid.
*   `POST /check_pick`: Core decision engine endpoint.
    *   **Payload**: `{ "intended_sku": "str", "picked_sku": "str", "barcode_scan_ok": bool | null }`
    *   **Response**: Returns a comprehensive JSON `RiskExplanation` object outlining `match`, `warning`, `block`, `risk_score`, `confidence`, `reasons`, and any `data_quality_flags`.

### Database Schema
The system models inventory and operators using formal Python `dataclasses`:

**Medicine Schema (`Medicine`)**
*   `sku` (str): Unique identifier.
*   `name`, `strength`, `form` (str): Clinical characteristics.
*   `phonetic_key`, `visual_key` (str): Categorical grouping properties for similarity scoring.
*   `cold_chain` (bool): Environmental constraint flag.
*   `shelf` (str): Location coordinate (e.g. `R1-A`).
*   `color`, `pack_shape` (str): Physical attributes.

**Operator Cohort Schema (`OperatorCohort`)**
*   `id` (str): Staff identifier (e.g., `L-14`).
*   `cohort_name` (str): `low_experience` or `high_experience`.
*   `experience_level` (str): `novice` or `expert`.
*   `fatigue_status` (str): `sleep_deprived` or `rested`.
*   `base_slip` (float): Baseline cognitive slip probability.

---

## Expected Outputs

*   **Console Experiment Table:** Running the experiment yields an overall baseline error rate of **23.38%** which is reduced to **2.28%** in the prototype. The low-experience technician group sees error reduction of **90.12%**, and the senior pharmacist group sees **90.64%** reduction. The equity gap is **0.52 percentage points** (indicating no cohort bias).
*   **Edge Case Tests:** Executing `test_edge_cases.py` prints:
    ```
    ====================================================
      RUNNING LASA SAFETY ENGINE EDGE CASE TEST SUITE
    ====================================================
    Case 1: Unknown SKU Test...
    [PASS] Case 1: Unknown SKU correctly flags warning and uncertainty, and is not swallowed.
    ...
    ====================================================
      ALL EDGE CASE TESTS PASSED SUCCESSFULLY!
    ====================================================
    ```
*   **Interactive HTML Console:**
    *   *Baseline Mode:* Displays an alphabetical plain list. Clicking a mismatched item dispenses it directly and flashes an alert: *"WRONG ITEM DISPENSED — NO WARNING SHOWN"*.
    *   *Prototype Mode:* Renders a grid of colorful medicine cards with packaging layouts and shelf details. Clicking a mismatched or offline-scanned item overlays a red **BLOCKED** or orange **WARNING** panel containing detailed confusion risk scores, reasons, and manual override fields. Logs are rendered dynamically in the footer.
