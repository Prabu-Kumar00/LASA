# LASA Project - Phase 3 Roadmap & Review 2 Corrections

## 1. Executive Summary

This report outlines the strategic roadmap for completing the final 30% of the Look-Alike Sound-Alike (LASA) Dispensing Safety Console project. Furthermore, it serves as the formal documentation of the immediate corrective actions implemented in response to the "Review 2" evaluation feedback.

While the first 70% of the project successfully established the core algorithmic architecture, formalized the data schemas, and proved basic clinical efficacy through simulation, the final 30% shifts the focus entirely toward **enterprise deployment robustness, extensive automated validation, and clinical observability**.

---

## 2. Corrections Addressed from Review 2

Following the Review 2 evaluation, two primary areas for improvement were identified. Both have been immediately rectified within the codebase and documentation to ensure compliance with the academic and clinical evaluation rubrics.

### 2.1 Granular Technical Documentation on Unit Testing and Error Boundaries
**Feedback**: *"Provide more granular technical documentation on unit testing and error boundaries."*

**Corrective Action Taken**: 
- We significantly expanded the central validation report (`final_report.md`) to include a dedicated **"Technical Documentation: Unit Testing and Error Boundaries"** section.
- **Fault Boundary Mapping**: The documentation now explicitly details how the `lasa_engine.py` API survives hardware failures and missing data. It defines specific fault boundaries:
  - `unknown_sku`: Safely intercepting unregistered inventory without crashing.
  - `missing_name`: Applying a fault-tolerant sequence matching bypass when database entries are corrupt.
  - `scanner_false_confirmation_suspected`: Hardware contradiction logic that refuses to blindly trust a scanner "beep" if the algorithm detects a mismatch.
- **Test Suite Alignment**: We mapped these exact software boundaries directly to the 6 clinical edge-case test suites executed in `tests/test_edge_cases.py`, proving that the system deterministically defaults to a restrictive safety posture under failure conditions.

### 2.2 Expanding Code Comments and API/Schema Documentation
**Feedback**: *"Expand code comments and document API endpoints / database schema in README for subsequent reviews."*

**Corrective Action Taken**: 
- The project's root `README.md` was completely rewritten to include a new, expansive **"Technical Documentation"** section.
- **REST API Documentation**: We formally documented the `GET /catalog` and `POST /check_pick` FastAPI endpoints. This includes the exact JSON payload structures expected by the server (e.g., `{ "intended_sku": "str", "picked_sku": "str", "barcode_scan_ok": bool | null }`) and the `RiskExplanation` response object format.
- **Database Schema Definitions**: The Python `dataclass` schemas for `OperatorCohort` and `Medicine` were thoroughly documented. We explicitly outlined the data types and the clinical purpose behind fields like `fatigue_status`, `base_slip`, and `visual_key`, which are critical for population bias testing.

---

## 3. The Remaining 30% of the Project

The final 30% of the project encompasses four major technical deliverables designed to bring the system to 100% completion, transitioning it from a research prototype to a production-ready clinical tool.

### 3.1 Enterprise Dockerization & Containerization (10%)
To ensure seamless deployment across varied, highly secure, and often antiquated pharmacy IT infrastructures, the system must be fully containerized.
- **Technical Approach**: We will implement a multi-stage Docker build. The backend will utilize the official `python:3.11-slim` image to run the FastAPI/Uvicorn server.
- **Environment Management**: Configuration variables (such as strictness thresholds and port bindings) will be extracted into a `.env` file, allowing pharmacy IT departments to adjust the engine's sensitivity without altering the codebase.
- **Outcome**: A single `docker-compose up -d` command will launch the entire clinical console, completely eliminating "it works on my machine" environmental discrepancies.

### 3.2 Advanced Analytics & Observability Dashboard (10%)
While the safety engine currently intercepts errors at the point of dispensing, pharmacy managers require macro-level visibility to address systemic issues (e.g., poorly designed physical shelves).
- **Technical Approach**: We will develop a secondary UI view (the "Manager's Dashboard") utilizing a lightweight charting library like Chart.js or D3.js. This dashboard will parse the local `audit-log` data in real-time.
- **Key Metrics to Track**:
  - **Peak Error Hours**: A time-series chart mapping the frequency of blocked/warned dispenses against the time of day (to identify fatigue spikes).
  - **Time-to-Override**: Tracking how long staff spend reading a warning before overriding it (measuring alert fatigue).
  - **High-Risk Pairs**: A heatmap highlighting the specific SKUs most frequently confused by staff, allowing clinical directors to proactively rearrange physical inventory.

### 3.3 PyTest Suite Expansion & CI/CD Pipeline (5%)
Building upon the Review 2 feedback, automated testing must be expanded to cover the newly introduced REST API layer and ensure zero regressions during future development.
- **Technical Approach**: We will utilize the `httpx` library and FastAPI's `TestClient` to programmatically hammer the API endpoints.
- **Fuzzing & Latency Simulation**: New tests will simulate malformed JSON payloads (fuzz testing), missing HTTP headers, and network latency to ensure the frontend degrades gracefully (e.g., showing a loading spinner rather than freezing).
- **Pipeline Integration**: These tests will be integrated into a GitHub Actions Continuous Integration (CI) pipeline, enforcing a rule that no code can be merged into `main` unless 100% of the safety tests pass.

### 3.4 Final User Acceptance Testing (UAT) & Statistical Validation (5%)
The system requires a massive-scale final evaluation to generate conclusive proof of equity and safety for regulatory and academic submission.
- **Technical Approach**: We will execute a final batch of 10,000+ simulated prescriptions using the formalized `OperatorCohort` models across the newly expanded 24-SKU catalog.
- **Statistical Rigor**: The results will be subjected to statistical significance testing (calculating p-values) to ensure that the observed reduction in errors is not due to random chance. 
- **Target Metrics**: 
  - Achieve a residual patient-reaching error rate of **<3.0%**.
  - Achieve an equity gap of **<15 percentage points** between novice and expert cohorts, proving that the software barrier protects all staff uniformly.
