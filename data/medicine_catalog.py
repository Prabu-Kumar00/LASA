from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Medicine:
    sku: str
    name: str
    strength: str
    form: str
    phonetic_key: str
    visual_key: str
    cold_chain: bool
    shelf: str
    ndc_sim: str
    color: str
    pack_shape: str

# Catalog of 12 synthetic medicines
# All names, packaging details, and codes are fictional.
CATALOG: List[Medicine] = [
    # 1. Phonetically similar pair (different strengths, different visual layouts)
    Medicine(
        sku="MED-AVEN-10",
        name="Avenzira",
        strength="10mg",
        form="Carton",
        phonetic_key="PK-AVEN",
        visual_key="VK-RECT-BLUE",
        cold_chain=True,
        shelf="R1-A",
        ndc_sim="55555-101-10",
        color="#1E3A8A",  # Dark Blue
        pack_shape="rectangular carton"
    ),
    Medicine(
        sku="MED-AVEN-50",
        name="Avenzyla",
        strength="50mg",
        form="Carton",
        phonetic_key="PK-AVEN",
        visual_key="VK-RECT-ORANGE",
        cold_chain=True,
        shelf="R1-B",
        ndc_sim="55555-101-50",
        color="#EA580C",  # Orange
        pack_shape="rectangular carton"
    ),

    # 2. Visually similar pair (same color and shape, unrelated names)
    Medicine(
        sku="MED-BAVI-100",
        name="Bavinex",
        strength="100mg",
        form="Vial",
        phonetic_key="PK-BAVI",
        visual_key="VK-VIAL-RED",
        cold_chain=True,
        shelf="R2-A",
        ndc_sim="55555-202-10",
        color="#DC2626",  # Red
        pack_shape="vial"
    ),
    Medicine(
        sku="MED-KRY-200",
        name="Krysolis",
        strength="200mg",
        form="Vial",
        phonetic_key="PK-KRYS",
        visual_key="VK-VIAL-RED",
        cold_chain=True,
        shelf="R2-B",
        ndc_sim="55555-303-20",
        color="#DC2626",  # Red
        pack_shape="vial"
    ),

    # 3. Phonetically and visually confusable pair (same name/form, same color/shape, stored closely)
    Medicine(
        sku="MED-ZILO-50",
        name="Zilomed",
        strength="50mg",
        form="Blister",
        phonetic_key="PK-ZILO",
        visual_key="VK-BLIS-GREEN",
        cold_chain=False,
        shelf="R3-A",
        ndc_sim="55555-404-50",
        color="#16A34A",  # Green
        pack_shape="blister"
    ),
    Medicine(
        sku="MED-ZILO-100",
        name="Zilomax",
        strength="100mg",
        form="Blister",
        phonetic_key="PK-ZILO",
        visual_key="VK-BLIS-GREEN",
        cold_chain=False,
        shelf="R3-A",  # Stored on same shelf bin
        ndc_sim="55555-404-99",
        color="#16A34A",  # Green
        pack_shape="blister"
    ),

    # 4. Same-drug-family, different-strength pair (high dosing risk, same visual form)
    Medicine(
        sku="MED-GLYC-05",
        name="Glycopen Mite",
        strength="5mg",
        form="Pen",
        phonetic_key="PK-GLYC",
        visual_key="VK-PEN-YELLOW",
        cold_chain=True,
        shelf="R4-A",
        ndc_sim="55555-505-05",
        color="#EAB308",  # Yellow
        pack_shape="pen carton"
    ),
    Medicine(
        sku="MED-GLYC-20",
        name="Glycopen Forte",
        strength="20mg",
        form="Pen",
        phonetic_key="PK-GLYC",  # Share phonetic key for family
        visual_key="VK-PEN-YELLOW",  # Share visual key for pen carton style
        cold_chain=True,
        shelf="R4-B",
        ndc_sim="55555-505-20",
        color="#EAB308",  # Yellow
        pack_shape="pen carton"
    ),

    # 5-12. Non-LASA medicines to complete the catalog of 12
    Medicine(
        sku="MED-NEUR-300",
        name="Neurogard",
        strength="300mg",
        form="Carton",
        phonetic_key="PK-NEUR",
        visual_key="VK-RECT-PURPLE",
        cold_chain=False,
        shelf="R5-A",
        ndc_sim="55555-606-30",
        color="#7C3AED",  # Purple
        pack_shape="rectangular carton"
    ),
    Medicine(
        sku="MED-CALC-500",
        name="Calcitone",
        strength="500mg",
        form="Blister",
        phonetic_key="PK-CALC",
        visual_key="VK-BLIS-GRAY",
        cold_chain=False,
        shelf="R5-B",
        ndc_sim="55555-707-50",
        color="#4B5563",  # Gray
        pack_shape="blister"
    ),
    Medicine(
        sku="MED-VENT-100",
        name="Ventirex",
        strength="100mcg",
        form="Pen",
        phonetic_key="PK-VENT",
        visual_key="VK-PEN-TEAL",
        cold_chain=False,
        shelf="R6-A",
        ndc_sim="55555-808-10",
        color="#0D9488",  # Teal
        pack_shape="pen carton"
    ),
    Medicine(
        sku="MED-FLUX-20",
        name="Fluxamine",
        strength="20mg",
        form="Carton",
        phonetic_key="PK-FLUX",
        visual_key="VK-RECT-PINK",
        cold_chain=False,
        shelf="R6-B",
        ndc_sim="55555-909-20",
        color="#DB2777",  # Pink
        pack_shape="rectangular carton"
    ),
    # 13-24. New SKUs to expand catalog
    Medicine(sku="MED-OMEP-20", name="Omeprazol", strength="20mg", form="Bottle", phonetic_key="PK-OMEP", visual_key="VK-BOT-WHITE", cold_chain=False, shelf="R7-A", ndc_sim="55555-1010-20", color="#FFFFFF", pack_shape="bottle"),
    Medicine(sku="MED-OMEP-40", name="Omepramax", strength="40mg", form="Bottle", phonetic_key="PK-OMEP", visual_key="VK-BOT-WHITE", cold_chain=False, shelf="R7-B", ndc_sim="55555-1010-40", color="#FFFFFF", pack_shape="bottle"),
    Medicine(sku="MED-LISI-10", name="Lisinopril", strength="10mg", form="Blister", phonetic_key="PK-LISI", visual_key="VK-BLIS-YELLOW", cold_chain=False, shelf="R8-A", ndc_sim="55555-1111-10", color="#EAB308", pack_shape="blister"),
    Medicine(sku="MED-LISI-20", name="Lisinopril", strength="20mg", form="Blister", phonetic_key="PK-LISI", visual_key="VK-BLIS-YELLOW", cold_chain=False, shelf="R8-A", ndc_sim="55555-1111-20", color="#EAB308", pack_shape="blister"),
    Medicine(sku="MED-AMLO-5", name="Amlodipine", strength="5mg", form="Blister", phonetic_key="PK-AMLO", visual_key="VK-BLIS-BLUE", cold_chain=False, shelf="R9-A", ndc_sim="55555-1212-05", color="#1E3A8A", pack_shape="blister"),
    Medicine(sku="MED-AMLO-10", name="Amlodipine", strength="10mg", form="Blister", phonetic_key="PK-AMLO", visual_key="VK-BLIS-BLUE", cold_chain=False, shelf="R9-B", ndc_sim="55555-1212-10", color="#1E3A8A", pack_shape="blister"),
    Medicine(sku="MED-ATOR-20", name="Atorvastatin", strength="20mg", form="Bottle", phonetic_key="PK-ATOR", visual_key="VK-BOT-WHITE", cold_chain=False, shelf="R10-A", ndc_sim="55555-1313-20", color="#FFFFFF", pack_shape="bottle"),
    Medicine(sku="MED-ATOR-40", name="Atorvastatin", strength="40mg", form="Bottle", phonetic_key="PK-ATOR", visual_key="VK-BOT-WHITE", cold_chain=False, shelf="R10-B", ndc_sim="55555-1313-40", color="#FFFFFF", pack_shape="bottle"),
    Medicine(sku="MED-SIMV-20", name="Simvastatin", strength="20mg", form="Bottle", phonetic_key="PK-SIMV", visual_key="VK-BOT-WHITE", cold_chain=False, shelf="R10-C", ndc_sim="55555-1414-20", color="#FFFFFF", pack_shape="bottle"),
    Medicine(sku="MED-SERO-50", name="Seroquel", strength="50mg", form="Carton", phonetic_key="PK-SERO", visual_key="VK-RECT-WHITE", cold_chain=False, shelf="R11-A", ndc_sim="55555-1515-50", color="#FFFFFF", pack_shape="rectangular carton"),
    Medicine(sku="MED-SERO-100", name="Seroquel", strength="100mg", form="Carton", phonetic_key="PK-SERO", visual_key="VK-RECT-WHITE", cold_chain=False, shelf="R11-B", ndc_sim="55555-1515-10", color="#FFFFFF", pack_shape="rectangular carton"),
    Medicine(sku="MED-CELE-200", name="Celebrex", strength="200mg", form="Carton", phonetic_key="PK-CELE", visual_key="VK-RECT-BLUE", cold_chain=False, shelf="R12-A", ndc_sim="55555-1616-20", color="#1E3A8A", pack_shape="rectangular carton")
]

def get_lasa_pairs() -> List[Tuple[str, str]]:
    """
    Returns all SKU pairs that share a phonetic_key OR a visual_key.
    Avoids duplicate pairings (returns sorted unique pairs).
    """
    pairs = set()
    for i in range(len(CATALOG)):
        for j in range(i + 1, len(CATALOG)):
            med_a = CATALOG[i]
            med_b = CATALOG[j]
            if (med_a.phonetic_key == med_b.phonetic_key) or (med_a.visual_key == med_b.visual_key):
                pair = tuple(sorted([med_a.sku, med_b.sku]))
                pairs.add(pair)
    return sorted(list(pairs))
