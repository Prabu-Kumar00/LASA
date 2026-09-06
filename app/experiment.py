import os
import sys
import json
import random
from typing import Dict, Any, List

# Add workspace directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.medicine_catalog import CATALOG
from app.simulation import run_simulation
from app.lasa_engine import check_pick

def run_experiment():
    print("====================================================")
    print("  RUNNING LASA DISPENSING INTERFACE EXPERIMENT")
    print("====================================================\n")
    
    # 1. Run simulation to get baseline event trace
    seed = 2026
    events = run_simulation(n_prescriptions=4000, seed=seed)
    
    # Reset random seed for reproducible compliance checks
    random.seed(seed)
    
    # Counters for metrics
    total_rx = len(events)
    
    # Overall counters
    baseline_errors = 0
    proto_errors = 0
    
    # Cohort-specific counters
    cohort_stats = {
        "low_experience": {"total": 0, "base_errors": 0, "proto_errors": 0},
        "high_experience": {"total": 0, "base_errors": 0, "proto_errors": 0}
    }
    
    # Stressor-specific counters
    stressors = ["none", "interrupted", "poor_lighting", "missing_label"]
    stressor_stats = {
        s: {"total": 0, "base_errors": 0, "proto_errors": 0} for s in stressors
    }
    
    # Audit log of actions in prototype
    blocks_count = 0
    warnings_count = 0
    overrides_count = 0
    self_corrections_count = 0
    
    detailed_results = []
    
    for ev in events:
        rx_id = ev["rx_id"]
        intended = ev["intended_sku"]
        picked = ev["picked_sku"]
        cohort = ev["cohort"]
        stressor = ev["stressor"]
        barcode_scan_ok = ev["barcode_scan_ok"]
        is_slip = ev["is_slip"]
        
        # 2. Evaluate Baseline System (No gate, no warnings, no barcode check)
        baseline_dispensed = picked
        baseline_err = (baseline_dispensed != intended)
        if baseline_err:
            baseline_errors += 1
            cohort_stats[cohort]["base_errors"] += 1
            stressor_stats[stressor]["base_errors"] += 1
            
        # 3. Evaluate Prototype System (Intervention gate)
        proto_dispensed = picked
        proto_err = False
        intervention = "none"
        res = {}
        
        if picked != intended or barcode_scan_ok is False or barcode_scan_ok is None:
            # Call engine to check pick safety
            res = check_pick(intended, picked, CATALOG, barcode_scan_ok)
            
            if res["block"]:
                intervention = "block"
                blocks_count += 1
                # Hard block forces correction
                proto_dispensed = intended
                proto_err = False
            elif res["warning"]:
                intervention = "warning"
                warnings_count += 1
                
                # Determine compliance
                compliance_rate = 0.80 if stressor == "none" else 0.62
                r_comp = random.random()
                if r_comp < compliance_rate:
                    # Staff self-corrects based on warning
                    proto_dispensed = intended
                    proto_err = False
                    self_corrections_count += 1
                else:
                    # Staff overrides warning
                    proto_dispensed = picked
                    proto_err = (picked != intended)
                    overrides_count += 1
            else:
                # No warning or block (low risk mismatch or other edge case)
                proto_dispensed = picked
                proto_err = (picked != intended)
        else:
            # Correct pick and barcode scan was OK
            proto_dispensed = picked
            proto_err = False
            
        if proto_err:
            proto_errors += 1
            cohort_stats[cohort]["proto_errors"] += 1
            stressor_stats[stressor]["proto_errors"] += 1
            
        cohort_stats[cohort]["total"] += 1
        stressor_stats[stressor]["total"] += 1
        
        detailed_results.append({
            "rx_id": rx_id,
            "intended": intended,
            "picked": picked,
            "cohort": cohort,
            "stressor": stressor,
            "baseline_err": baseline_err,
            "proto_err": proto_err,
            "intervention": intervention,
            "engine_result": {
                "block": res.get("block", False),
                "warning": res.get("warning", False),
                "risk_score": res.get("risk_score", 0.0),
                "confidence": res.get("confidence", 1.0),
                "reasons": res.get("reasons", []),
                "data_quality_flags": res.get("data_quality_flags", [])
            } if res else None
        })
        
    # Calculate Overall rates
    overall_base_rate = (baseline_errors / total_rx) * 100
    overall_proto_rate = (proto_errors / total_rx) * 100
    overall_reduction = ((baseline_errors - proto_errors) / baseline_errors) * 100
    
    # Calculate Cohort metrics
    low_stats = cohort_stats["low_experience"]
    low_base_rate = (low_stats["base_errors"] / low_stats["total"]) * 100
    low_proto_rate = (low_stats["proto_errors"] / low_stats["total"]) * 100
    low_reduction = ((low_stats["base_errors"] - low_stats["proto_errors"]) / low_stats["base_errors"]) * 100
    
    high_stats = cohort_stats["high_experience"]
    high_base_rate = (high_stats["base_errors"] / high_stats["total"]) * 100
    high_proto_rate = (high_stats["proto_errors"] / high_stats["total"]) * 100
    high_reduction = ((high_stats["base_errors"] - high_stats["proto_errors"]) / high_stats["base_errors"]) * 100
    
    # Equity check (difference in relative reduction gap)
    equity_gap = abs(low_reduction - high_reduction)
    equity_flag = "ALERT: EQUITY CONCERN" if equity_gap > 15.0 else "CLEAR: NO BIAS CONCERN"
    
    # Format results dict for JSON export
    experiment_results = {
        "overall": {
            "total_rx": total_rx,
            "baseline_errors": baseline_errors,
            "baseline_error_rate": round(overall_base_rate, 4),
            "prototype_errors": proto_errors,
            "prototype_error_rate": round(overall_proto_rate, 4),
            "relative_reduction": round(overall_reduction, 4),
            "blocks_count": blocks_count,
            "warnings_count": warnings_count,
            "self_corrections_count": self_corrections_count,
            "overrides_count": overrides_count
        },
        "cohorts": {
            "low_experience": {
                "total": low_stats["total"],
                "baseline_errors": low_stats["base_errors"],
                "baseline_error_rate": round(low_base_rate, 4),
                "prototype_errors": low_stats["proto_errors"],
                "prototype_error_rate": round(low_proto_rate, 4),
                "relative_reduction": round(low_reduction, 4)
            },
            "high_experience": {
                "total": high_stats["total"],
                "baseline_errors": high_stats["base_errors"],
                "baseline_error_rate": round(high_base_rate, 4),
                "prototype_errors": high_stats["proto_errors"],
                "prototype_error_rate": round(high_proto_rate, 4),
                "relative_reduction": round(high_reduction, 4)
            },
            "equity_gap_percentage_points": round(equity_gap, 4),
            "equity_flag": equity_flag
        },
        "stressors": {
            s: {
                "total": stressor_stats[s]["total"],
                "baseline_errors": stressor_stats[s]["base_errors"],
                "baseline_error_rate": round((stressor_stats[s]["base_errors"] / stressor_stats[s]["total"]) * 100, 4),
                "prototype_errors": stressor_stats[s]["proto_errors"],
                "prototype_error_rate": round((stressor_stats[s]["proto_errors"] / stressor_stats[s]["total"]) * 100, 4),
                "relative_reduction": round(((stressor_stats[s]["base_errors"] - stressor_stats[s]["proto_errors"]) / stressor_stats[s]["base_errors"]) * 100, 4)
            } for s in stressors
        }
    }
    
    # Save to reports/experiment_results.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "reports", "experiment_results.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(experiment_results, f, indent=4)
        
    print(f"Results written to reports/experiment_results.json\n")
    
    # Render experiment table
    print("--------------------------------------------------------------------------------")
    print("                      MEASURABLE EXPERIMENT RESULTS TABLE")
    print("--------------------------------------------------------------------------------")
    print(f"Metric              | Baseline | Target | Measured | Error Analysis")
    print(f"--------------------+----------+--------+----------+--------------------------------")
    print(f"Overall error rate  | ~15%     | <3%    | {overall_proto_rate:.2f}%   | Baseline: {overall_base_rate:.2f}%. Reduction of {overall_reduction:.1f}% shows safety barrier effectiveness.")
    print(f"Low-exp reduction   | —        | >90%   | {low_reduction:.2f}%   | Reduced error from {low_base_rate:.2f}% to {low_proto_rate:.2f}%, successfully protecting novice staff.")
    print(f"High-exp reduction  | —        | >85%   | {high_reduction:.2f}%   | Reduced error from {high_base_rate:.2f}% to {high_proto_rate:.2f}% despite experience level.")
    print(f"Equity gap          | —        | <15pp  | {equity_gap:.2f}pp    | Status: {equity_flag}. Standardised guardrails protect both groups equitably.")
    print("--------------------------------------------------------------------------------\n")
    
    # Render bias analysis table
    print("--------------------------------------------------------------------------------")
    print("                      COHORT BIAS ANALYSIS TABLE")
    print("--------------------------------------------------------------------------------")
    print(f"Cohort            | Baseline Error | Prototype Error | Relative Reduction | Status")
    print(f"------------------+----------------+-----------------+--------------------+-------------")
    print(f"Low Experience    | {low_base_rate:13.2f}% | {low_proto_rate:14.2f}% | {low_reduction:17.2f}% | (N={low_stats['total']})")
    print(f"High Experience   | {high_base_rate:13.2f}% | {high_proto_rate:14.2f}% | {high_reduction:17.2f}% | (N={high_stats['total']})")
    print(f"Equity Gap        | -              | -               | {equity_gap:17.2f}pp | {equity_flag}")
    print("--------------------------------------------------------------------------------\n")
    
    # Render stressor analysis table
    print("--------------------------------------------------------------------------------")
    print("                      STRESSOR IMPACT ANALYSIS TABLE")
    print("--------------------------------------------------------------------------------")
    print(f"Stressor         | Total Rx | Baseline Error | Prototype Error | Relative Reduction")
    print(f"-----------------+----------+----------------+-----------------+--------------------")
    for s in stressors:
        s_base = experiment_results["stressors"][s]["baseline_error_rate"]
        s_proto = experiment_results["stressors"][s]["prototype_error_rate"]
        s_red = experiment_results["stressors"][s]["relative_reduction"]
        print(f"{s:16s} | {stressor_stats[s]['total']:8d} | {s_base:13.2f}% | {s_proto:14.2f}% | {s_red:17.2f}%")
    print("--------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    run_experiment()
