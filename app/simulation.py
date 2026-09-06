import random
from typing import List, Dict, Any, Tuple, Optional
import os
import sys

# Add workspace directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.medicine_catalog import CATALOG, Medicine, get_lasa_pairs
from app.lasa_engine import check_pick

def run_simulation(
    n_prescriptions: int = 4000, 
    seed: int = 2026
) -> List[Dict[str, Any]]:
    """
    Simulates a series of prescription dispensing events.
    Returns a list of dictionaries recording details of each simulated event.
    """
    random.seed(seed)
    
    # 1. Setup staff cohorts
    # 40 low experience (L-01 to L-40), base slip prob = 0.18
    # 40 high experience (H-01 to H-40), base slip prob = 0.07
    staff_pool = []
    for i in range(1, 41):
        staff_pool.append({
            "id": f"L-{i:02d}",
            "cohort": "low_experience",
            "base_slip": 0.18
        })
        staff_pool.append({
            "id": f"H-{i:02d}",
            "cohort": "high_experience",
            "base_slip": 0.07
        })
        
    # Stressors definition
    stressors = ["none", "interrupted", "poor_lighting", "missing_label"]
    
    # Map of catalog for fast SKU lookup
    catalog_map = {m.sku: m for m in CATALOG}
    skus = list(catalog_map.keys())
    
    # Get LASA pairs for targeted slip simulation
    lasa_pairs = get_lasa_pairs()
    lasa_map = {}
    for sku in skus:
        lasa_map[sku] = []
    for sku_a, sku_b in lasa_pairs:
        lasa_map[sku_a].append(sku_b)
        lasa_map[sku_b].append(sku_a)
        
    events = []
    
    for rx_id in range(n_prescriptions):
        # Select intended medicine
        intended_sku = random.choice(skus)
        
        # Select staff member and stressor
        staff = random.choice(staff_pool)
        stressor = random.choice(stressors)
        
        # Setup stressor parameters
        if stressor == "none":
            slip_mult = 1.0
            scanner_misread = 0.015
            barcode_scan_ok_default = True
        elif stressor == "interrupted":
            slip_mult = 1.6
            scanner_misread = 0.040
            barcode_scan_ok_default = True
        elif stressor == "poor_lighting":
            slip_mult = 1.8
            scanner_misread = 0.040
            barcode_scan_ok_default = True
        elif stressor == "missing_label":
            slip_mult = 2.4
            scanner_misread = 0.0  # scan fails entirely
            barcode_scan_ok_default = None  # scanner offline/label missing
            
        # Calculate total experience-based slip probability
        slip_prob = staff["base_slip"] * slip_mult
        
        picked_sku = intended_sku
        slip_type = "none"
        
        # Determine if a base selection slip occurs
        r_slip = random.random()
        if r_slip < slip_prob:
            # A selection slip occurs
            # 70% chance of slipping to a LASA partner (if any exist)
            partners = lasa_map[intended_sku]
            r_type = random.random()
            if r_type < 0.70 and partners:
                picked_sku = random.choice(partners)
                slip_type = "lasa_slip"
            else:
                # 30% chance of general mis-pick (or if no partners exist)
                other_skus = [s for s in skus if s != intended_sku]
                picked_sku = random.choice(other_skus)
                slip_type = "general_slip"
                
        # Independently check for small random non-LASA mis-pick (1-3% model noise)
        # We model this at a constant rate of 2% to represent random errors the engine 
        # is not expected to intercept via high-risk categories.
        r_noise = random.random()
        if r_noise < 0.02:
            # Forces a mis-pick of an unrelated item
            non_lasa_skus = [s for s in skus if s != intended_sku and s not in lasa_map[intended_sku]]
            if non_lasa_skus:
                picked_sku = random.choice(non_lasa_skus)
                slip_type = "non_lasa_noise_slip"
                
        # Simulate barcode scanner behaviour
        if barcode_scan_ok_default is None:
            # Barcode cannot be scanned (label missing)
            barcode_scan_ok = None
        else:
            # Scanner works but has misread_rate
            r_scan = random.random()
            if r_scan < scanner_misread:
                # Misread: scanner reports the OPPOSITE of reality
                barcode_scan_ok = not (picked_sku == intended_sku)
            else:
                # Scanner reports truth
                barcode_scan_ok = (picked_sku == intended_sku)
                
        # Record details for this simulation event
        events.append({
            "rx_id": rx_id,
            "intended_sku": intended_sku,
            "picked_sku": picked_sku,
            "staff_id": staff["id"],
            "cohort": staff["cohort"],
            "stressor": stressor,
            "slip_type": slip_type,
            "barcode_scan_ok": barcode_scan_ok,
            "is_slip": (picked_sku != intended_sku)
        })
        
    return events
