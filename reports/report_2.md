# LASA Project - Phase 2 Progress Report (70% Completion Milestone)

## 1. Executive Summary

This report documents the second phase of the Look-Alike Sound-Alike (LASA) Dispensing Safety Console project. Following the feedback received during the initial review phase, critical architectural, structural, and evaluative enhancements have been successfully implemented. The project has now reached a **70% completion milestone**. 

The core focus of this phase was to mature the system from a localized prototype into a scalable, decoupled client-server architecture, while simultaneously strengthening the rigor of our simulated testing environments. By migrating the core decision engine to a RESTful API, formalizing testing cohorts, and doubling the simulated medication inventory, we have built a highly robust foundation capable of accommodating realistic pharmacy environments.

---

## 2. Architectural Evolution: Client-Server Decoupling

Previously, the `mvp.html` prototype operated as a monolithic simulation where both the user interface and the business logic (risk calculation, phonetic scoring, visual similarity evaluation) were tightly coupled in client-side JavaScript. This presented significant limitations for scalability, security, and version control of the safety algorithms.

### 2.1 Implementation of a Lightweight REST Backend (FastAPI)
We have completely transitioned the architecture to a robust client-server model by integrating **FastAPI**:
- **Centralized Engine (`app/api.py`)**: The `lasa_engine.py` logic is now exclusively hosted on the server. The backend natively exposes the evaluation functions via HTTP REST endpoints.
- **API Endpoints Created**:
  - `GET /catalog`: Allows the frontend to dynamically fetch the active formulary. This ensures the UI is always synchronized with the backend inventory without requiring manual frontend updates.
  - `POST /check_pick`: The core evaluation endpoint. The client sends a JSON payload containing `intended_sku`, `picked_sku`, and `barcode_scan_ok`. The backend responds with a detailed risk analysis, confidence score, and intervention directives (block, warn, or clear).
- **Static Asset Management**: Packaging imagery and localized CSS/JS assets are now dynamically served through FastAPI's `StaticFiles` middleware.

### 2.2 Dynamic Frontend Binding
The `app/mvp.html` file has been significantly refactored:
- Removed over 200 lines of duplicated client-side engine logic.
- The interface now utilizes asynchronous JavaScript (`async/await` and the `Fetch API`) to communicate with the backend. 
- The UI renders intervention screens based solely on the standardized JSON responses from the server, establishing a true separation of concerns.

---

## 3. Data Schema Formalization: Population Bias Testing

To satisfy the stringent requirement for population bias testing, the simulation engine required an upgrade from loosely structured dictionaries to strict data definitions. This ensures our experimental results (e.g., measuring equity gaps between different user groups) are statistically sound and reproducible.

### 3.1 The `OperatorCohort` Schema
We introduced a formal `OperatorCohort` schema utilizing Python's `dataclasses` within `app/simulation.py`. The schema enforces strict typing for the following operator attributes:
- `id`: A unique identifier for the simulated staff member (e.g., "L-01", "H-22").
- `cohort_name`: Categorization of the group (e.g., "low_experience", "high_experience").
- `experience_level`: A qualitative flag (e.g., "novice", "expert") dictating baseline familiarity with LASA risks.
- `fatigue_status`: An environmental variable (e.g., "sleep_deprived", "rested") that dynamically alters error probabilities during simulation runs.
- `base_slip`: A base float probability representing the intrinsic error rate before stressors are applied.

By migrating to this schema, the simulation engine can now easily iterate over highly specific, multi-variable cohorts (e.g., a "Novice / Sleep-Deprived" cohort vs. an "Expert / Rested" cohort), allowing for deep dives into how the safety console protects vulnerable staff under adverse conditions.

---

## 4. Formulary Expansion and Collision Stress-Testing

A primary critique of the initial iteration was the small catalog size (12 SKUs), which artificially limited the probability of random collisions and made the engine's job relatively easy.

### 4.1 Expanding to 24 SKUs
We doubled the size of the medicine catalog in `data/medicine_catalog.py` to 24 SKUs. The expansion was not merely random; it deliberately introduced complex new LASA vectors:
- **Phonetic Twins**: Added pairs like *Omeprazol* (20mg) and *Omepramax* (40mg).
- **Varying Packaging Norms**: Introduced new form factors like "bottles" alongside the existing blisters, pens, and cartons.
- **Cardiovascular & Psychiatric Medications**: Added standard high-volume pharmacy items (Lisinopril, Amlodipine, Atorvastatin, Simvastatin, Seroquel, Celebrex) to serve as "noise" data. 

### 4.2 Impact on Engine Evaluation
The introduction of these 12 new items exponentially increases the number of potential combinations the `lasa_engine.py` must evaluate. Initial stress tests confirm that:
- The backend continues to accurately identify and isolate high-risk pairs (e.g., flagging an Amlodipine 5mg vs 10mg mismatch) without misflagging safe, unrelated items (e.g., Atorvastatin vs. Seroquel).
- API response times remain well within the acceptable threshold (<50ms per transaction), validating the scalability of the backend algorithm under a denser inventory table.

---

## 5. Next Steps Towards 100% Completion

To bring this project to final completion, the following deliverables are planned for Phase 3:

1. **Dockerization & Containerization**: Wrap the FastAPI backend and HTML frontend into a Docker container to ensure seamless deployment across different pharmacy IT environments.
2. **Advanced Analytics Dashboard**: Develop a secondary view in the frontend (or a separate page) to visualize the data generated in the `audit-log`, providing pharmacy managers with actionable insights on near-misses.
3. **Comprehensive Unit Testing**: Expand the PyTest suite to cover the new API endpoints and ensure the newly added 12 SKUs are fully covered under all edge-case scenarios (e.g., missing labels, offline scanners).
4. **Final User Acceptance Testing (UAT)**: Run a final batch of 10,000 simulated prescriptions to generate the final statistical report proving the efficacy and equity of the system.
