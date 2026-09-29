# LASA Project - Phase 3 Roadmap & Review 2 Corrections

## 1. Executive Summary

This report outlines the strategy for the remaining 30% of the Look-Alike Sound-Alike (LASA) Dispensing Safety Console project. It also serves to document the immediate corrective actions taken in response to the Review 2 evaluation feedback.

The final 30% of the project transitions focus from core algorithmic architecture towards deployment robustness, comprehensive validation, and clinical observability. 

---

## 2. Corrections Addressed from Review 2

Following the Review 2 evaluation, the following areas for improvement were identified and immediately rectified in the codebase and documentation:

### 2.1 Granular Technical Documentation on Unit Testing and Error Boundaries
**Feedback**: *"Provide more granular technical documentation on unit testing and error boundaries."*
**Action Taken**: 
- We significantly expanded the central validation report (`final_report.md`) to include a dedicated "Technical Documentation: Unit Testing and Error Boundaries" section.
- This section explicitly details how the `lasa_engine.py` API survives hardware failures and handles missing data. It defines the specific fault boundaries (e.g., `unknown_sku`, `missing_name`, `scanner_false_confirmation_suspected`).
- We mapped these exact software boundaries directly to the 6 clinical edge-case test suites executed in `tests/test_edge_cases.py` to prove deterministic failure handling.

### 2.2 Expanding Code Comments and API/Schema Documentation
**Feedback**: *"Expand code comments and document API endpoints / database schema in README for subsequent reviews."*
**Action Taken**: 
- The project's root `README.md` was rewritten to include a new "Technical Documentation" section.
- We formally documented the `GET /catalog` and `POST /check_pick` FastAPI endpoints, including JSON payload structures (`intended_sku`, `picked_sku`, `barcode_scan_ok`).
- The Python `dataclass` schemas for `OperatorCohort` and `Medicine` were thoroughly documented, outlining their types and purpose in population bias testing.

---

## 3. The Remaining 30% of the Project

The final 30% of the project encompasses four major deliverables designed to bring the system to 100% completion, ready for clinical deployment.

### 3.1 Dockerization & Containerization (10%)
To ensure seamless deployment across varied, highly secure pharmacy IT infrastructures, the system must be containerized.
- **Objective**: Wrap the FastAPI backend, static HTML/JS frontend, and Python execution environments into a unified Docker image.
- **Outcome**: A single `docker-compose up` command will launch the entire clinical console without requiring complex local Python environment setups.

### 3.2 Advanced Analytics Dashboard (10%)
While the safety engine currently intercepts errors, pharmacy managers require macro-level visibility into near-misses.
- **Objective**: Develop a secondary UI view (or dedicated analytics page) to visualize the data generated in the `audit-log`.
- **Outcome**: The dashboard will render actionable heatmaps and bar charts detailing near-miss trends, peak error hours, and most frequently confused LASA pairs, allowing clinical directors to proactively rearrange physical shelves.

### 3.3 PyTest Suite Expansion & CI Pipeline (5%)
Building upon the Review 2 feedback, testing must be expanded to cover the newly introduced REST API layer.
- **Objective**: Expand the automated unit tests to fully cover the new FastAPI endpoints in `app/api.py`.
- **Outcome**: New tests will simulate HTTP request latency, malformed JSON payloads, and stress-test the 24-SKU catalog. These tests will be integrated into a basic Continuous Integration (CI) pipeline (e.g., GitHub Actions) that runs on every commit.

### 3.4 Final User Acceptance Testing (UAT) & Statistical Validation (5%)
The system requires a massive-scale final evaluation to generate conclusive proof of equity and safety.
- **Objective**: Execute a final batch of 10,000+ simulated prescriptions using the formal `OperatorCohort` models.
- **Outcome**: Generate the definitive statistical validation report proving the clinical efficacy (targeting <3.0% residual error rate) and operational equity (targeting <15 percentage points equity gap) across the expanded catalog of 24 SKUs.
