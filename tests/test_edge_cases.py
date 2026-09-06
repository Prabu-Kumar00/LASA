import sys
import os

# Add workspace directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.medicine_catalog import CATALOG, Medicine
from app.lasa_engine import check_pick, confusion_risk

def run_tests():
    print("====================================================")
    print("  RUNNING LASA SAFETY ENGINE EDGE CASE TEST SUITE")
    print("====================================================\n")
    
    passed_all = True
    
    # ----------------------------------------------------
    # Case 1: Unknown SKU (not in catalog)
    # ----------------------------------------------------
    print("Case 1: Unknown SKU Test...")
    res = check_pick("MED-AVEN-10", "MED-UNKNOWN-999", CATALOG, True)
    c1_ok = (
        res["warning"] is True and 
        res["uncertainty_message"] is not None and 
        "unknown_sku" in res["data_quality_flags"] and 
        res["block"] is False
    )
    if c1_ok:
        print("[PASS] Case 1: Unknown SKU correctly flags warning and uncertainty, and is not swallowed.")
    else:
        print("[FAIL] Case 1: Unknown SKU failed assertions.", res)
        passed_all = False

    # ----------------------------------------------------
    # Case 2: Missing barcode scan (scanner=None) on a CORRECT pick
    # ----------------------------------------------------
    print("\nCase 2: Missing barcode scan on correct pick...")
    res = check_pick("MED-AVEN-10", "MED-AVEN-10", CATALOG, None)
    c2_ok = (
        res["match"] is True and 
        res["confidence"] < 1.0 and 
        res["uncertainty_message"] is not None
    )
    if c2_ok:
        print(f"[PASS] Case 2: Missing scan on correct pick reduces confidence ({res['confidence']}) and surfaces uncertainty message.")
    else:
        print("[FAIL] Case 2: Missing scan on correct pick failed assertions.", res)
        passed_all = False

    # ----------------------------------------------------
    # Case 3: Explicit barcode mismatch (scanner=False)
    # ----------------------------------------------------
    print("\nCase 3: Explicit barcode mismatch...")
    # Even if they are identical or highly similar, scanner=False must hard block
    res = check_pick("MED-AVEN-10", "MED-AVEN-10", CATALOG, False)
    c3_ok = (
        res["block"] is True and 
        res["warning"] is True
    )
    if c3_ok:
        print("[PASS] Case 3: Barcode mismatch (scanner=False) triggers a hard block successfully.")
    else:
        print("[FAIL] Case 3: Barcode mismatch (scanner=False) failed assertions.", res)
        passed_all = False

    # ----------------------------------------------------
    # Case 4: Blank medicine name (data entry failure)
    # ----------------------------------------------------
    print("\nCase 4: Blank medicine name...")
    # Create a custom catalog where one medicine has a blank name
    custom_catalog = [m for m in CATALOG]
    bad_med = Medicine(
        sku="MED-BAD-NAME",
        name="",  # blank name
        strength="50mg",
        form="Carton",
        phonetic_key="PK-BAD",
        visual_key="VK-RECT-BLUE",
        cold_chain=False,
        shelf="R1-A",
        ndc_sim="55555-000-00",
        color="#1E3A8A",
        pack_shape="rectangular carton"
    )
    custom_catalog.append(bad_med)
    
    # Try check_pick with this blank name medicine
    try:
        res = check_pick("MED-AVEN-10", "MED-BAD-NAME", custom_catalog, True)
        c4_ok = (
            "missing_name" in res["data_quality_flags"] and 
            res["confidence"] < 0.5 and 
            res["uncertainty_message"] is not None
        )
        if c4_ok:
            print(f"[PASS] Case 4: Blank medicine name did not crash, flagged 'missing_name', and reduced confidence ({res['confidence']}).")
        else:
            print("[FAIL] Case 4: Blank medicine name failed assertions.", res)
            passed_all = False
    except Exception as e:
        print(f"[FAIL] Case 4: Blank medicine name crashed with exception: {e}")
        passed_all = False

    # ----------------------------------------------------
    # Case 5: Scanner false-confirmation
    # ----------------------------------------------------
    print("\nCase 5: Scanner false-confirmation (scanner=True but items differ)...")
    res = check_pick("MED-AVEN-10", "MED-AVEN-50", CATALOG, True)
    c5_ok = (
        "scanner_false_confirmation_suspected" in res["data_quality_flags"] and 
        res["warning"] is True
    )
    if c5_ok:
        print("[PASS] Case 5: Scanner false-confirmation flagged and intercepted by similarity layer.")
    else:
        print("[FAIL] Case 5: Scanner false-confirmation failed assertions.", res)
        passed_all = False

    # ----------------------------------------------------
    # Case 6: Same-family, different-strength pair
    # ----------------------------------------------------
    print("\nCase 6: Same-family, different-strength pair...")
    # MED-GLYC-05 (5mg) and MED-GLYC-20 (20mg) are same-family, different strength
    res = check_pick("MED-GLYC-05", "MED-GLYC-20", CATALOG, True)
    has_dosing_risk = any("DOSING RISK" in reason for reason in res["reasons"])
    c6_ok = (
        res["risk_score"] >= 0.7 and 
        has_dosing_risk
    )
    if c6_ok:
        print(f"[PASS] Case 6: Same-family, different-strength pair gets high risk_score ({res['risk_score']}) and triggers DOSING RISK description.")
    else:
        print("[FAIL] Case 6: Same-family, different-strength pair failed assertions.", res)
        passed_all = False

    print("\n====================================================")
    if passed_all:
        print("  ALL EDGE CASE TESTS PASSED SUCCESSFULLY!")
        print("====================================================")
        sys.exit(0)
    else:
        print("  SOME EDGE CASE TESTS FAILED!")
        print("====================================================")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
