import difflib
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os
import sys

# Add workspace directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.medicine_catalog import Medicine

@dataclass
class RiskExplanation:
    risk_score: float
    reasons: List[str]
    confidence: float
    data_quality_flags: List[str]

def phonetic_similarity(name_a: str, name_b: str) -> float:
    """
    Computes name similarity using difflib.SequenceMatcher.
    Returns a float between 0 and 1.
    """
    if not name_a or not name_b:
        return 0.0
    return difflib.SequenceMatcher(None, name_a.strip().lower(), name_b.strip().lower()).ratio()

def visual_similarity(med_a: Medicine, med_b: Medicine) -> float:
    """
    Computes visual similarity based on weighted overlap of:
    - color (0.5)
    - pack_shape (0.3)
    - visual_key (0.2)
    Returns a float between 0 and 1.
    """
    color_score = 1.0 if med_a.color.strip().lower() == med_b.color.strip().lower() else 0.0
    shape_score = 1.0 if med_a.pack_shape.strip().lower() == med_b.pack_shape.strip().lower() else 0.0
    key_score = 1.0 if med_a.visual_key == med_b.visual_key else 0.0
    
    return (0.5 * color_score) + (0.3 * shape_score) + (0.2 * key_score)

def shelf_proximity(med_a: Medicine, med_b: Medicine) -> float:
    """
    Computes shelf proximity score:
    - 1.0 if stored on the exact same shelf
    - 0.5 if stored in the same zone prefix (e.g. R3-A and R3-B share prefix R3)
    - 0.0 otherwise
    """
    if not med_a.shelf or not med_b.shelf:
        return 0.0
    
    s_a = med_a.shelf.strip()
    s_b = med_b.shelf.strip()
    
    if s_a == s_b:
        return 1.0
        
    prefix_a = s_a.split('-')[0]
    prefix_b = s_b.split('-')[0]
    if prefix_a == prefix_b:
        return 0.5
        
    return 0.0

def confusion_risk(med_a: Medicine, med_b: Medicine) -> RiskExplanation:
    """
    Combines phonetic, visual, and shelf proximity similarities into an overall risk score.
    Applies dosing risk escalation (+0.15) if name similarity is > 0.6 and strengths differ.
    Capping overall risk score at 1.0.
    Identifies data quality issues such as blank names.
    """
    reasons = []
    flags = []
    confidence = 1.0
    
    # Check for blank/missing names
    name_a = med_a.name.strip() if med_a.name else ""
    name_b = med_b.name.strip() if med_b.name else ""
    
    if not name_a or not name_b:
        flags.append("missing_name")
        confidence = 0.4
        phon_sim = 0.0
        reasons.append("Data entry failure: One or both medicine names are missing.")
    else:
        phon_sim = phonetic_similarity(name_a, name_b)
        
    vis_sim = visual_similarity(med_a, med_b)
    prox_sim = shelf_proximity(med_a, med_b)
    
    # Base risk score calculation
    # 0.45 * phonetic + 0.35 * visual + 0.20 * shelf
    base_score = (0.45 * phon_sim) + (0.35 * vis_sim) + (0.20 * prox_sim)
    risk_score = base_score
    
    # Detailed reasons construction
    if name_a and name_b:
        if phon_sim > 0.6:
            reasons.append(f"High phonetic name similarity: '{name_a}' and '{name_b}' (Score: {phon_sim:.2f})")
        elif phon_sim > 0.3:
            reasons.append(f"Moderate name similarity: '{name_a}' and '{name_b}' (Score: {phon_sim:.2f})")
            
    if med_a.color.strip().lower() == med_b.color.strip().lower():
        reasons.append(f"Identical carton/vial color: {med_a.color}")
    if med_a.pack_shape.strip().lower() == med_b.pack_shape.strip().lower():
        reasons.append(f"Same packaging shape: {med_a.pack_shape}")
    if med_a.visual_key == med_b.visual_key:
        reasons.append(f"Shared visual signature key: {med_a.visual_key}")
        
    if prox_sim == 1.0:
        reasons.append(f"Stored on the exact same shelf: {med_a.shelf}")
    elif prox_sim == 0.5:
        reasons.append(f"Stored in close proximity: same zone {med_a.shelf.split('-')[0]}")
        
    # Dosing risk escalation (+0.15) if name similarity > 0.6 and strengths differ
    if name_a and name_b and phon_sim > 0.6 and med_a.strength != med_b.strength:
        risk_score += 0.15
        reasons.append(f"DOSING RISK: Similar name but different strengths ({med_a.strength} vs {med_b.strength}).")
        
    # Cap score at 1.0
    risk_score = min(risk_score, 1.0)
    
    return RiskExplanation(
        risk_score=round(risk_score, 4),
        reasons=reasons,
        confidence=confidence,
        data_quality_flags=flags
    )

def check_pick(
    intended_sku: str, 
    picked_sku: str, 
    catalog: List[Medicine], 
    barcode_scan_ok: Optional[bool]
) -> Dict[str, Any]:
    """
    Evaluates one pick event.
    Returns a decision dict indicating whether to block, warn, or clear.
    """
    # Initialize response dict
    result = {
        "match": False,
        "warning": False,
        "block": False,
        "risk_score": 0.0,
        "confidence": 1.0,
        "reasons": [],
        "data_quality_flags": [],
        "uncertainty_message": None
    }
    
    # 1. Hard block on explicit barcode scanner mismatch
    if barcode_scan_ok is False:
        result["block"] = True
        result["warning"] = True
        result["risk_score"] = 1.0
        result["reasons"] = ["Barcode scanner reported explicit mismatch. Stop dispensing immediately."]
        return result
        
    # Map catalog by SKU
    catalog_map = {m.sku: m for m in catalog}
    
    # 2. Check for unknown SKUs
    intended_med = catalog_map.get(intended_sku)
    picked_med = catalog_map.get(picked_sku)
    
    if not intended_med or not picked_med:
        result["warning"] = True
        result["data_quality_flags"].append("unknown_sku")
        result["confidence"] = 0.3
        result["risk_score"] = 0.5
        missing_skus = []
        if not intended_med:
            missing_skus.append(intended_sku)
        if not picked_med:
            missing_skus.append(picked_sku)
        result["reasons"] = [f"Unknown SKU(s) encountered in dispensing transaction: {', '.join(missing_skus)}"]
        result["uncertainty_message"] = (
            "Unknown SKU: Picked item is not registered in the active system catalog. "
            "Please escalate to the pharmacist for manual verification."
        )
        return result
        
    # 3. Barcode scanner missing (barcode_scan_ok = None)
    if barcode_scan_ok is None:
        result["confidence"] = 0.6
        result["uncertainty_message"] = (
            "Barcode scan missing: Cold-chain barcode could not be read or was bypassed. "
            "Uncertainty notice for authorised staff. Verify carton labels manually before dispensing."
        )
        
    # 4. Scanner false-confirmation check
    # Scanner reported True, but SKUs differ in catalog database
    if barcode_scan_ok is True and intended_sku != picked_sku:
        result["data_quality_flags"].append("scanner_false_confirmation_suspected")
        # Proceed with similarity logic despite scanner affirmation
        
    # 5. Evaluate pick matching
    if intended_sku == picked_sku:
        result["match"] = True
        # If barcode scan is missing, we still have lower confidence and uncertainty message
        if barcode_scan_ok is None:
            result["warning"] = False  # Matches should not warn under missing scanner if correct SKU
        return result
        
    # Mismatch processing (intended_sku != picked_sku)
    result["match"] = False
    
    # Calculate confusion risk between the intended and picked medicines
    explanation = confusion_risk(intended_med, picked_med)
    
    result["risk_score"] = explanation.risk_score
    result["reasons"].extend(explanation.reasons)
    result["data_quality_flags"].extend(explanation.data_quality_flags)
    
    # Confidence aggregation
    # If barcode was missing, we already lowered confidence to 0.6.
    # Otherwise, use the explanation confidence.
    if barcode_scan_ok is None:
        result["confidence"] = min(result["confidence"], explanation.confidence)
    else:
        result["confidence"] = explanation.confidence
        
    # Uncertainty message for confidence < 0.5
    if result["confidence"] < 0.5:
        # Check if missing name is the cause
        if "missing_name" in result["data_quality_flags"]:
            result["uncertainty_message"] = (
                "Data quality alert: Missing drug metadata (blank name) prevents full safety checks. "
                "Pharmacist escalation required."
            )
        else:
            result["uncertainty_message"] = (
                "Uncertainty notice: Data verification is compromised. "
                "Pharmacist escalation required."
            )
            
    # Apply risk thresholds
    # risk_score >= 0.8 -> Block. risk_score >= 0.3 -> Warning.
    # Any mismatch, even low-risk, must raise at least a Warning.
    if result["risk_score"] >= 0.8:
        result["block"] = True
        result["warning"] = True
    elif result["risk_score"] >= 0.3:
        result["warning"] = True
    else:
        # Mismatch but low risk_score
        result["warning"] = True
        result["reasons"].insert(0, "Item mismatch detected (intended SKU does not match picked SKU).")
        
    return result
