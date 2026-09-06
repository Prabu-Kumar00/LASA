# Data Schema Document

This document outlines the data schemas and formats used in the Look-Alike Sound-Alike (LASA) safety engine, simulations, and experiment reports.

## 1. Medicine Dataclass

Defines the structure of a medicine record in the formulary catalog (`data/medicine_catalog.py`).

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `sku` | `str` | Unique stock-keeping unit identifier. | `"MED-AVEN-10"` |
| `name` | `str` | Brand/generic name of the medicine. | `"Avenzira"` |
| `strength` | `str` | Strength or dosage details. | `"10mg"` |
| `form` | `str` | Physical formulation or container description. | `"Carton"` |
| `phonetic_key` | `str` | Phonetic similarity clustering key. | `"PK-AVEN"` |
| `visual_key` | `str` | Visual similarity clustering key. | `"VK-RECT-BLUE"` |
| `cold_chain` | `bool` | Flag indicating cold-chain (2-8°C) storage. | `True` |
| `shelf` | `str` | Bin location on shelves (Format: `Zone-Bin`). | `"R1-A"` |
| `ndc_sim` | `str` | Fictional National Drug Code (simulated barcode). | `"55555-101-10"` |
| `color` | `str` | Dominant hex color code of packaging. | `"#1E3A8A"` |
| `pack_shape` | `str` | Form/shape factor. | `"rectangular carton"` |

## 2. RiskExplanation Dataclass

Constructed by `confusion_risk` in `app/lasa_engine.py` during pick verification.

*   `risk_score` (`float`): Core confusion risk score capped at `1.0`. Calculated from phonetic (45%), visual (35%), and proximity (20%) scores. Includes dosing risk escalation (+0.15).
*   `reasons` (`List[str]`): List of English strings detailing why the risk was evaluated (e.g., color matches, same shelf, dosing risk).
*   `confidence` (`float`): Quantified data quality indicator between `0.0` and `1.0`. Reduced by missing data (e.g. blank name).
*   `data_quality_flags` (`List[str]`): Flags representing data issues (e.g., `"missing_name"`, `"unknown_sku"`).

## 3. check_pick Return Schema

The output of `check_pick()` in `app/lasa_engine.py`, returned as a Python dictionary.

```json
{
  "match": "bool (True if picked SKU equals intended SKU, and no barcode block occurs)",
  "warning": "bool (True if mismatch occurs, risk_score >= 0.3, or barcode scan is False/None)",
  "block": "bool (True if risk_score >= 0.8 or barcode scan is False)",
  "risk_score": "float (Combined risk evaluation between 0.0 and 1.0)",
  "confidence": "float (Data confidence rating between 0.0 and 1.0)",
  "reasons": "array of strings (Contextual reasons for warnings or blocks)",
  "data_quality_flags": "array of strings (Flags indicating system or record anomalies)",
  "uncertainty_message": "string or null (Instructional message if confidence < 0.5 or scan is missing)"
}
```

## 4. Experiment Results JSON Schema

Saved to `reports/experiment_results.json` after running `app/experiment.py`.

```json
{
  "overall": {
    "total_rx": "int",
    "baseline_errors": "int",
    "baseline_error_rate": "float (percentage)",
    "prototype_errors": "int",
    "prototype_error_rate": "float (percentage)",
    "relative_reduction": "float (percentage)",
    "blocks_count": "int",
    "warnings_count": "int",
    "self_corrections_count": "int",
    "overrides_count": "int"
  },
  "cohorts": {
    "low_experience": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    },
    "high_experience": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    },
    "equity_gap_percentage_points": "float",
    "equity_flag": "string"
  },
  "stressors": {
    "none": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    },
    "interrupted": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    },
    "poor_lighting": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    },
    "missing_label": {
      "total": "int",
      "baseline_errors": "int",
      "baseline_error_rate": "float",
      "prototype_errors": "int",
      "prototype_error_rate": "float",
      "relative_reduction": "float"
    }
  }
}
```
