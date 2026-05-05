"""
AgriExpert — Cardamom Knowledge Base
Extracted from:
  1. "Cardamom — The Genus Elettaria"
     Ravindran & Madhusoodanan (Eds.), Taylor & Francis, 2002
     Ch.4 Agronomy, Ch.6 Viral Diseases, Ch.7 Fungal/Nematode, Ch.8 Pests
  2. "The Geography of Cardamom (Elettaria cardamomum M.)" Vol.2
     Kodoth Prabhakaran Nair, Springer, 2020
     Ch.4 Agronomy, Ch.6 Diseases & Pests
"""

CARDAMOM_KB = {

    # ══════════════════════════════════════════════════════════════════════
    # DISEASES
    # ══════════════════════════════════════════════════════════════════════
    "diseases": {

        "Azhukal / Capsule Rot": {
            "type":      "Fungal",
            "local_name":"Azhukal (Malayalam: 'rotting')",
            "causal":    "Phytophthora meadii McRae; P. nicotianae var. nicotianae Waterhouse",
            "parts":     "Capsules, young leaves, panicles, tender shoots, rhizomes",
            "first_reported": "Menon et al. (1972) — Idukki district, Kerala",
            "distribution":   "Idukki and Wynad districts of Kerala; Anamalai hills, Tamil Nadu. NOT found in Karnataka.",
            "severity":  "Most serious fungal disease of cardamom. Up to 40% crop loss in severely affected plantations (Anonymous 1989a). Nambiar and Sarma 1976 reported 30% loss.",
            "season":    "Onset after SW monsoon; peak June–August. High disease incidence at 320–400mm rainfall, soil moisture 34.3–37.6%, temp 20.4–21.3°C, RH 83–90.6%.",
            "conditions":"High/continuous rainfall, low temperature, high RH, waterlogging, thick shade, close spacing, high soil inoculum level",
            "symptoms": [
                "First visible symptom: discoloured water-soaked lesions on young leaves or capsules",
                "Lesions enlarge; infected capsules turn brownish, decay and drop off with foul smell",
                "Foliage: water-soaked lesions at leaf tips or margins that enlarge to form large patches",
                "Immature unopened leaves fail to unfurl after infection",
                "As disease advances: lesion areas turn necrotic, leaves decay, shrivel, give shredded appearance",
                "In extreme cases: entire panicle or pseudostem decays completely",
                "Severe cases: rotting extends to underground rhizomes; entire plant collapses",
                "All capsule ages susceptible; young capsules most severely affected",
            ],
            "management": {
                "chemical": [
                    "Preventive: 1% Bordeaux mixture spray — must be applied BEFORE primary infection (before June onset)",
                    "0.3% Aliette (Fosetyl-Aluminium) — 2–3 rounds including one prophylactic spray",
                    "0.2% Copper oxychloride — foliar spray (Menon et al. 1973; Nair 1979)",
                    "0.2% Dexon (Bay-5072) at 4 kg/ha — reported by Alagianagalingam and Kandaswamy (1981)",
                    "Thomas et al. (1989, 1991a): 2–3 spray rounds with 1% Bordeaux mixture or 0.3% Aliette after phytosanitation most effective",
                ],
                "biological": [
                    "Trichoderma viride and T. harzianum — field control demonstrated (Suseela Bhai et al. 1993)",
                    "T. harzianum in carrier medium (FYM + coffee husk) — effective for field application (Thomas et al. 1997)",
                    "Native Trichoderma sp. strains from cardamom soils have high biocontrol potential (Dhanapal and Thomas 1996)",
                ],
                "cultural": [
                    "Phytosanitation: remove and destroy infected plant material before spraying",
                    "Improve drainage to prevent waterlogging",
                    "Reduce shade density in plantation",
                    "Avoid close spacing",
                ],
            },
            "sources": ["Elettaria Ch.7 (Thomas & Suseela Bhai)", "Geography Vol.2 Ch.6"],
        },

        "Rhizome Rot / Clump Rot": {
            "type":      "Fungal",
            "local_name":"Clump Rot",
            "causal":    "Primary: Pythium vexans, Rhizoctonia solani Kühn, Fusarium oxysporum. Associated with nematodes.",
            "parts":     "Rhizomes, tillers, roots, aerial shoots",
            "first_reported": "Park (1937); Subba Rao (1938) described as clump rot",
            "distribution":   "Widely distributed throughout cardamom plantations in Kerala and Karnataka; heavy rainfall areas of Tamil Nadu (Anamalai hills)",
            "severity":  "Up to 20% disease incidence in severely affected areas. Peak during July–August.",
            "season":    "Appears during SW monsoon — typically by middle of June. Worst in July–August.",
            "conditions":"Presence of inoculum in soil and plant debris, overcrowding of plants, thick shade, waterlogged conditions",
            "symptoms": [
                "First symptom: pale yellow colour in foliage; premature death of older leaves with wilting",
                "Collar portion of aerial shoots becomes brittle — tiller breaks off at slight disturbance",
                "Collar region becomes soft and brown coloured at rotting stage",
                "Affected aerial shoots fall off emitting foul smell",
                "Tender shoots and young tillers turn brown and rot completely",
                "As disease advances: all affected aerial shoots fall from base; panicles and young shoots also affected",
                "Rotting extends to rhizomes and roots in advanced cases",
            ],
            "management": {
                "chemical": [
                    "Soil drenching with 1% Bordeaux mixture — pre-monsoon (1 round) + post-monsoon (2 rounds at monthly interval)",
                    "Soil drenching with 0.25% Copper oxychloride — same schedule as Bordeaux",
                    "Neem oil cake at 500g per plant",
                    "Application of superphosphate at 300–400g per plant (Anonymous 1955)",
                ],
                "biological": [
                    "T. viride and T. harzianum — reported to reduce rhizome rot incidence (Thomas et al. 1991b)",
                    "T. harzianum in FYM + coffee husk carrier medium for integrated disease management (Thomas et al. 1997)",
                ],
                "cultural": [
                    "Phytosanitation is primary control measure",
                    "Remove overcrowding of plants",
                    "Reduce shade density",
                    "Improve drainage",
                ],
            },
            "sources": ["Elettaria Ch.7 (Thomas & Suseela Bhai)"],
        },

        "Chenthal / Leaf Blight": {
            "type":      "Fungal",
            "local_name":"Chenthal",
            "causal":    "Colletotrichum gloeosporioides (Penz.) Penz and Sacc. — confirmed by Govindaraju et al. (1996). NOTE: Originally incorrectly attributed to Corynebacterium sp. (bacterial) by George and Jayasankar (1977).",
            "parts":     "Leaves only — does NOT affect plant height, panicle emergence or crop yield (Govindaraju et al. 1996)",
            "first_reported": "George et al. (1976) — Idukki district, Kerala",
            "distribution":   "Many cardamom plantations; spreading to newer areas. Faster spread in partially deforested/less shaded areas.",
            "severity":  "Was considered minor disease of limited spread; now becoming major problem in many areas.",
            "season":    "Appears mostly during post-monsoon period; becomes severe during summer months",
            "conditions":"Post-monsoon and summer; partially deforested areas; less shaded plantations",
            "symptoms": [
                "Symptoms develop on foliage as water-soaked rectangular lesions",
                "Lesions later elongate to form parallelly arranged streaks of a few mm to 5cm length",
                "Lesion areas become yellowish-brown to orange-red in colour",
                "Central portions of lesions often become necrotic",
                "IMPORTANT: The TWO YOUNGEST leaves are NOT attacked by the disease",
                "As disease advances: more lesions on older leaves; adjacent lesions coalesce; areas begin to dry up",
                "Severely infected plants show a burnt appearance",
            ],
            "management": {
                "chemical": [
                    "Three sprays at monthly intervals with Carbendazim (Bavistin) 0.3% — most effective (Govindaraju et al. 1996)",
                    "Three sprays at monthly intervals with Mancozeb 0.3%",
                    "Three sprays at monthly intervals with Copper oxychloride 0.25%",
                    "NOTE: Penicillin spray (originally recommended for bacterial cause) is NOT effective",
                ],
                "biological": [],
                "cultural": [
                    "Maintain adequate shade density",
                    "Avoid deforestation/excessive canopy removal",
                ],
            },
            "sources": ["Elettaria Ch.7 (Thomas & Suseela Bhai)"],
        },

        "Katte / Cardamom Mosaic Disease": {
            "type":      "Viral",
            "local_name":"Katte (Kannada: 'criss-cross pattern')",
            "causal":    "Cardamom Mosaic Virus (car-MV) — poty virus group",
            "vector":    "Cardamom aphid Pentalonia nigronervosa f. caladii — transmits in non-persistent manner",
            "parts":     "Systemic — entire plant",
            "severity":  "83% natural infection within 6 months in Guatemala (Dimitman 1981). Plants decline and become unproductive.",
            "season":    "Year-round; alate (winged) aphids responsible for random spread, particularly active Nov–May",
            "incubation":"23–120 days (23–168 days by some accounts) to express visible symptoms",
            "spread": [
                "Primary spread: incoming alate (winged) viruliferous aphids from infected plantations",
                "Random spread observed in new plantations up to 600m from infected source (some accounts up to 2000m)",
                "Secondary spread within plantation: centrifugal (apterous forms) and random (alate forms)",
                "Rate of secondary spread: concentrated near sources within ~100m; shallow gradient in next 100m",
                "NOT transmitted through seed, soil, leaves, roots, mechanical contact or farm implements",
            ],
            "symptoms": [
                "Characteristic mosaic / chlorotic mottling on leaves",
                "Light and dark green patches in alternating pattern — classic mosaic symptom",
                "Stunting of plants",
                "Reduced yield; plants become unproductive",
                "Progressive plant decline and eventual death",
            ],
            "management": {
                "chemical": [
                    "NO chemical cure for the virus itself",
                    "Insecticides do NOT effectively reduce secondary spread — aphid transmits virus during brief probing before insecticide can act (Rajan et al. 1989)",
                    "34 insecticides evaluated — none effective in checking virus acquisition and transmission even on day of application",
                ],
                "biological": [
                    "Neem products significantly reduced aphid population even at 0.1% concentration (Mathew et al. 1997, 1999a,b)",
                    "Aqueous extracts of Acorus calamus, Annona squamosa, Lawsonia inermis — reduce aphid settling",
                    "Entomogenous fungi: Beauveria bassiana, Verticillium chlamydosporium, Paecilomyces lilacinus — promising without causing aphid hyperactivity (Mathew et al. 1998)",
                ],
                "cultural": [
                    "ROGUE AND DESTROY infected plants IMMEDIATELY — most effective management",
                    "Phytosanitation: periodic removal of old parts of rhizomatous crop to reduce aphid breeding sites",
                    "Remove natural aphid hosts: Colocasia sp., Caladium sp. from swampy areas of plantation",
                    "Use only certified virus-free planting material",
                    "Raise nurseries in isolated sites: minimum 200m isolation from virus sources for car-MV",
                    "Avoid movement of planting material from infected zones",
                    "Avoid planting from volunteers (self-sown seedlings from infected plantations)",
                    "If disease <10%: intensive survey and rouging at shorter intervals (3-4 months) until new outbreaks reduce (Naidu and Venugopal 1982)",
                    "Survey intervals can be extended once new infections drop to 2-3% per annum",
                ],
            },
            "sources": ["Elettaria Ch.6 (Venugopal)", "Geography Vol.2 Ch.6"],
        },

        "Kokke Kandu / Cardamom Vein Clearing Disease": {
            "type":      "Viral",
            "local_name":"Kokke Kandu (Kannada: 'hook-like tiller')",
            "causal":    "Cardamom Vein Clearing Virus (car-VCV) — possibly poty virus group based on ELISA (Venugopal et al. 1997b). Exact etiology not yet fully established.",
            "vector":    "Pentalonia nigronervosa f. caladii — semi-persistent or persistent manner",
            "parts":     "Systemic — all plant stages from seedling to bearing",
            "severity":  "62–84% yield reduction in first year of peak crop (NRCS 1994). Under mixed crop with arecanut: 68–94% yield loss at different infection stages. Plants perish within 1–2 years of infection.",
            "distribution": "Endemic pockets in Kodagu, Hassan, Chickmagalur, Shimoga and North Canara districts of Karnataka. In 381 plantations surveyed, widespread in 375 (0.1–82% incidence). Also found in Kerala.",
            "season":    "All seasons; summer shows only faint discontinuous vein clearing symptoms",
            "incubation":"22–128 days; single viruliferous aphid can transmit to plants of all stages",
            "spread": [
                "Random spread in new plantations up to 2000m from infected plantations",
                "Alate forms responsible for random spread; apterous forms for centrifugal spread",
                "Rate of spread: 1.3–8.5% per year in infected plantations",
                "Disease gradient steep near sources (within 100m), shallow in next 100m",
                "NOT transmitted through seed, soil, leaves, roots, mechanical contact",
                "As high as 73.33% incidence in nurseries (Govindaraju et al. 1994)",
            ],
            "symptoms": [
                "Characteristic continuous or discontinuous intraveinal clearing on symptomatic leaves",
                "Stunting, rosetting, loosening of leaf sheath, shredding of leaves",
                "Leafy stems exhibit clear mottling in all seasons",
                "Clear light-green patches with three shallow grooves on immature capsules",
                "Cracking of fruits and partial sterility of seeds",
                "New leaves get entangled in older leaves — forms hook-like tiller (the defining 'Kokke Kandu' symptom)",
                "Summer: newly infected plants show only faint discontinuous vein clearing",
            ],
            "management": {
                "chemical": ["Same limitations as Katte — no chemical cure; insecticides not effective for secondary spread"],
                "biological": ["Same biopesticide options as for Katte management"],
                "cultural": [
                    "ROGUE IMMEDIATELY — more urgent than Katte due to higher yield loss",
                    "Isolation of more than 200m from virus sources for nurseries",
                    "Comprehensive approach: healthy seedlings + periodic survey by trained gang + prompt removal and destruction",
                    "Community approach recommended in contiguous holdings: total removal followed by replanting and surveillance",
                ],
            },
            "sources": ["Elettaria Ch.6 (Venugopal)"],
        },

        "Nilgiri Necrosis Disease": {
            "type":      "Viral",
            "local_name":"Nilgiri Necrosis Virus (NNV)",
            "causal":    "Flexuous particles 570–700nm × 10–12nm — Carla virus group (Naidu and Thomas 1994)",
            "vector":    "Infected rhizomes/seedlings are primary inoculum. Aphid, thrips and whitefly transmission not recorded.",
            "parts":     "Systemic",
            "severity":  "55% yield reduction in early infected plants; total yield loss in late infected plants (Sridhar et al. 1991). Rapid decline.",
            "distribution": "Nilgiris (up to 80% incidence in Conoor), Anamalais, Cardamom Hills, Biligiri Rangan hills. Some estates in Munnar and Thondimalai areas of Idukki, Kerala (4.6% and 1.46% incidence).",
            "symptoms": [
                "Young leaves: whitish-yellowish continuous or broken streaks proceeding from midrib to leaf margins",
                "In advanced stages: streaks turn reddish-brown",
                "Leaf shredding along streaks",
                "Leaves reduced in size with distorted margins",
                "Early infected plants: produce few panicles and capsules",
                "Advanced stage: tillers highly stunted; fail to bear panicles",
                "Plants in early infection: 55% yield reduction; late infected: total yield loss",
            ],
            "management": {
                "chemical": ["No chemical cure"],
                "biological": [],
                "cultural": [
                    "Rouging of infected plants results in near total elimination (demonstrated in test plantations)",
                    "Avoid planting infected rhizomes",
                    "Do not use seedlings from diseased nurseries",
                    "Pattern of spread similar to Katte but rate lower (3.3%/year) — rouging more feasible",
                ],
            },
            "sources": ["Elettaria Ch.6 (Venugopal)"],
        },

        "Root Knot Nematode": {
            "type":      "Nematode",
            "causal":    "Meloidogyne incognita (primary); also Pratylenchus coffeae (lesion nematode) and Radopholus similis (burrowing nematode) in mixed plantations",
            "parts":     "Roots (underground galling); aerial symptoms on leaves and overall plant",
            "severity":  "Crop losses up to 80% (Ramana and Eapen 1992). High in nurseries where same site is repeatedly used.",
            "season":    "Nematode population high during post-monsoon period (September–January). Heavy shade, moist warm humid weather = predisposing factors.",
            "distribution": "Widely observed in almost all cardamom plantations and nurseries",
            "symptoms": [
                "AERIAL: Stunting of plants, reduced tillering, rosetting, narrowing of leaves",
                "Yellow banding on leaf blades",
                "Drying of leaf tips or leaf margins",
                "Delayed flowering; immature fruit dropping",
                "UNDERGROUND: Pronounced root galling — spherical/ovoid swellings on tender root tips",
                "In nurseries: severe galling, marginal yellowing and drying of leaves, stunting, reduced tillering, leaves become narrow, leaf tips show upward curling",
                "Poor seed germination in infested nursery soils",
            ],
            "management": {
                "chemical": [
                    "Aldicarb at 5g ai per plant — twice yearly",
                    "Carbofuran at 5g ai per plant — twice yearly",
                    "Phorate at 5g ai per plant — twice yearly (Ali 1984)",
                    "Nursery pre-treatment: Methyl bromide at 500g per 10m² OR soil drenching with 2% formalin",
                    "Solarization of nursery beds reported to reduce nematode populations",
                ],
                "biological": [
                    "Trichoderma + Paecilomyces lilacinus biocontrol schedule for nurseries (Eapen and Venugopal 1995)",
                ],
                "cultural": [
                    "Avoid transplanting nematode-infected seedlings",
                    "Use new nursery sites; avoid repeated use of same site",
                ],
            },
            "sources": ["Elettaria Ch.7 (Thomas & Suseela Bhai)"],
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SEASONAL CALENDAR — Idukki District context
    # ══════════════════════════════════════════════════════════════════════
    "seasonal": {
        1:  {"risk": "High", "diseases": "Chenthal HIGH, Nematode HIGH, Leaf Rust",
             "activity": "Late harvest rounds, post-harvest management"},
        2:  {"risk": "Medium", "diseases": "Chenthal moderate, Leaf Rust tapering",
             "activity": "Last harvest rounds, soil conservation work, pruning"},
        3:  {"risk": "Low", "diseases": "Low disease pressure — summer season",
             "activity": "Pre-monsoon irrigation, shade regulation, weeding"},
        4:  {"risk": "Medium", "diseases": "Aphid population rising (Katte/Kokke Kandu vector risk)",
             "activity": "NPK fertiliser application (pre-monsoon dose), pit preparation"},
        5:  {"risk": "High", "diseases": "Aphid peak; PREPARE AZHUKAL PREVENTIVE SPRAY",
             "activity": "Preventive Azhukal spray before monsoon onset — CRITICAL"},
        6:  {"risk": "Very High", "diseases": "Azhukal ACTIVE, Rhizome Rot onset",
             "activity": "SW monsoon onset — Azhukal sprays; drainage management"},
        7:  {"risk": "Critical", "diseases": "Azhukal CRITICAL, Rhizome Rot CRITICAL",
             "activity": "Peak monsoon — monitor disease daily; drainage essential"},
        8:  {"risk": "High", "diseases": "Azhukal HIGH on capsules; harvest begins",
             "activity": "Harvest season begins; monitor capsules closely"},
        9:  {"risk": "Medium", "diseases": "Disease tapering; Nematode build-up begins",
             "activity": "Harvest ongoing; post-monsoon fertiliser application"},
        10: {"risk": "High", "diseases": "Phytophthora Leaf Blight onset, Chenthal onset, Nematode HIGH",
             "activity": "Harvest peak; post-monsoon operations"},
        11: {"risk": "High", "diseases": "Chenthal HIGH, Leaf Blight, Aphid rising",
             "activity": "Harvest peak; shade regulation"},
        12: {"risk": "Medium", "diseases": "Chenthal, Leaf Blight, Nematode ongoing",
             "activity": "Late harvest; weeding; soil work"},
    },

    # ══════════════════════════════════════════════════════════════════════
    # DIAGNOSTIC KEY — match symptoms to disease
    # ══════════════════════════════════════════════════════════════════════
    "diagnostic": {
        "capsules_rotting_dropping": {
            "likely":   "Azhukal / Capsule Rot (Phytophthora)",
            "confirm":  "Water-soaked lesions, foul smell, during June–August, Idukki/Wynad location",
            "urgency":  "High",
            "action":   "1% Bordeaux mixture spray immediately. Improve drainage. Remove infected material.",
        },
        "leaves_shredded_rotting": {
            "likely":   "Azhukal foliar phase OR Phytophthora Leaf Blight (post-monsoon)",
            "confirm":  "Azhukal: June–Sep; Leaf Blight: Oct–Jan. Check capsules for concurrent infection.",
            "urgency":  "High",
            "action":   "1% Bordeaux mixture spray; reduce shade.",
        },
        "shoots_falling_foul_smell": {
            "likely":   "Rhizome Rot / Clump Rot (Pythium/Rhizoctonia)",
            "confirm":  "July–August; collar region soft and brown; foul odour at base",
            "urgency":  "High",
            "action":   "0.25% Copper oxychloride soil drench immediately. Remove affected clumps. Trichoderma application.",
        },
        "leaves_mosaic_mottling_stunting": {
            "likely":   "Katte Disease (Cardamom Mosaic Virus) — NO CURE",
            "confirm":  "Light/dark green alternating patches; stunted plant; check for aphid colonies on leaf sheaths",
            "urgency":  "Critical",
            "action":   "ROGUE PLANT IMMEDIATELY. Mark and monitor 40m radius. Control aphids in surrounding area.",
        },
        "new_leaves_hook_vein_clearing": {
            "likely":   "Kokke Kandu / Cardamom Vein Clearing Virus — NO CURE",
            "confirm":  "Hook-like tiller; continuous/discontinuous vein clearing; light-green patches on capsules",
            "urgency":  "Critical",
            "action":   "ROGUE IMMEDIATELY. Higher yield loss than Katte — act within 24 hours.",
        },
        "leaf_yellowing_root_galls": {
            "likely":   "Root Knot Nematode (Meloidogyne incognita)",
            "confirm":  "Dig sample roots — look for spherical/ovoid galls on root tips; yellow banding on leaves",
            "urgency":  "Medium",
            "action":   "Carbofuran or phorate 5g ai per plant. Trichoderma + Paecilomyces lilacinus biocontrol.",
        },
        "orange_yellow_leaf_streaks": {
            "likely":   "Chenthal / Leaf Blight (Colletotrichum gloeosporioides)",
            "confirm":  "Post-monsoon/summer; youngest 2 leaves NOT affected; parallelly arranged streaks",
            "urgency":  "Medium",
            "action":   "Carbendazim (Bavistin) 0.3% — 3 monthly sprays. OR Mancozeb 0.3% — 3 monthly sprays.",
        },
        "whitish_yellow_streaks_midrib": {
            "likely":   "Nilgiri Necrosis Disease (NNV) — especially in Munnar/Thondimalai areas",
            "confirm":  "Streaks from midrib to leaf margins; turn reddish-brown in advanced stage; shredding",
            "urgency":  "High",
            "action":   "Rogue infected plants. Do not use material from diseased plants.",
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # SPRAY SCHEDULE REFERENCE
    # ══════════════════════════════════════════════════════════════════════
    "spray_schedule": {
        "Preventive Azhukal Spray": {
            "timing":    "Before June monsoon onset (May)",
            "chemical":  "1% Bordeaux mixture OR 0.3% Aliette (Fosetyl-Al)",
            "frequency": "1 round prophylactic; repeat monthly June–August",
            "target":    "Azhukal / Capsule Rot (Phytophthora meadii)",
            "source":    "Thomas et al. 1989, 1991a",
        },
        "Rhizome Rot Drench": {
            "timing":    "Pre-monsoon (1 round) + Post-monsoon (2 rounds at monthly interval)",
            "chemical":  "1% Bordeaux mixture OR 0.25% Copper oxychloride",
            "frequency": "3 rounds per year",
            "target":    "Rhizome Rot / Clump Rot (Pythium/Rhizoctonia)",
            "source":    "Thomas and Vijayan 1994",
        },
        "Chenthal Control": {
            "timing":    "Post-monsoon at first symptom observation",
            "chemical":  "Carbendazim (Bavistin) 0.3% OR Mancozeb 0.3% OR Copper oxychloride 0.25%",
            "frequency": "3 sprays at monthly intervals",
            "target":    "Chenthal / Leaf Blight (Colletotrichum gloeosporioides)",
            "source":    "Govindaraju et al. 1996",
        },
        "Nematode Treatment": {
            "timing":    "Twice yearly",
            "chemical":  "Aldicarb OR Carbofuran OR Phorate at 5g ai per plant",
            "frequency": "2 times per year",
            "target":    "Root Knot Nematode (Meloidogyne incognita)",
            "source":    "Ali 1984",
        },
    },
}


def get_disease_kb(condition_name):
    """
    Find the best matching KB entry for an AI-identified condition.
    Returns (disease_name, disease_dict) or (None, None).
    """
    condition_lower = condition_name.lower()
    diseases = CARDAMOM_KB["diseases"]

    # Direct match first
    for name, data in diseases.items():
        if any(part.lower() in condition_lower
               for part in name.split("/")[0].split() if len(part) > 3):
            return name, data

    # Fuzzy keyword match
    keywords = {
        "azhukal":   "Azhukal / Capsule Rot",
        "capsule rot":"Azhukal / Capsule Rot",
        "phytophthora":"Azhukal / Capsule Rot",
        "rhizome":   "Rhizome Rot / Clump Rot",
        "clump":     "Rhizome Rot / Clump Rot",
        "katte":     "Katte / Cardamom Mosaic Disease",
        "mosaic":    "Katte / Cardamom Mosaic Disease",
        "car-mv":    "Katte / Cardamom Mosaic Disease",
        "kokke":     "Kokke Kandu / Cardamom Vein Clearing Disease",
        "vein clear":"Kokke Kandu / Cardamom Vein Clearing Disease",
        "car-vcv":   "Kokke Kandu / Cardamom Vein Clearing Disease",
        "chenthal":  "Chenthal / Leaf Blight",
        "leaf blight":"Chenthal / Leaf Blight",
        "colletotrichum":"Chenthal / Leaf Blight",
        "nematode":  "Root Knot Nematode",
        "root knot": "Root Knot Nematode",
        "meloidogyne":"Root Knot Nematode",
        "nilgiri":   "Nilgiri Necrosis Disease",
        "necrosis":  "Nilgiri Necrosis Disease",
    }
    for kw, disease_name in keywords.items():
        if kw in condition_lower:
            return disease_name, diseases.get(disease_name)

    return None, None


def get_seasonal_advisory(month):
    return CARDAMOM_KB["seasonal"].get(month, {
        "risk": "Unknown", "diseases": "Monitor regularly", "activity": "Standard management"
    })


def get_diagnostic(symptom_key):
    return CARDAMOM_KB["diagnostic"].get(symptom_key)
