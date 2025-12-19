# enrich_all.py
"""
Génère dans un seul fichier CSV toutes les colonnes dérivées :
- period_of_day
- severity
- victims_count, victim_type_breakdown, num_physical_victims, ...
- risk_location_score (basé sur agrégats par District)
"""
import pandas as pd
import numpy as np
import random

# --------------------------
# Config
# --------------------------
INPUT_CSV = r"C:\Users\USER\OneDrive\Documents\city-safety\data\crimes.csv"
OUTPUT_CSV = r"C:\Users\USER\OneDrive\Documents\city-safety\data\crimes_fully_enriched.csv"
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# --------------------------
# 1. Charger le dataset
# --------------------------
df = pd.read_csv(INPUT_CSV, dtype=str)  # charger en str pour robustesse
 # charger en str pour robustesse
  # charger en str pour robustesse
# conserver colonnes originales, mais créer colonnes utilitaires
# Normaliser noms utiles
if "Primary Type" not in df.columns:
    # gestion de variantes
    for c in df.columns:
        if c.lower().strip() == "primary type" or c.lower().strip()=="primary_type":
            df.rename(columns={c: "Primary Type"}, inplace=True)
            break

# --------------------------
# 2. Parse Date et heure
# --------------------------
df["Date_parsed"] = pd.to_datetime(df["Date"], errors="coerce")
df["hour"] = df["Date_parsed"].dt.hour

def get_period(hour):
    if pd.isna(hour):
        return "Unknown"
    hour = int(hour)
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 22:
        return "Evening"
    else:
        return "Night"

df["period_of_day"] = df["hour"].apply(get_period)

# --------------------------
# 3. severity (score 1..5)
# --------------------------
# mapping inspiré de la discussion précédente (ajuste si tu veux)
severity_map = {
    "HOMICIDE": 5,
    "CRIMINAL SEXUAL ASSAULT": 5,
    "CRIM SEXUAL ASSAULT": 5,
    "HUMAN TRAFFICKING": 5,
    "KIDNAPPING": 5,

    "ROBBERY": 4,
    "WEAPONS VIOLATION": 4,
    "ARSON": 4,
    "BATTERY": 4,
    "ASSAULT": 4,
    "OFFENSE INVOLVING CHILDREN": 4,

    "BURGLARY": 3,
    "MOTOR VEHICLE THEFT": 3,
    "CRIMINAL DAMAGE": 3,
    "NARCOTICS": 3,
    "PUBLIC PEACE VIOLATION": 3,

    "THEFT": 2,
    "DECEPTIVE PRACTICE": 2,
    "CONCEALED CARRY LICENSE VIOLATION": 2,
    "SEX OFFENSE": 2,
    "CRIMINAL TRESPASS": 2,
    "INTERFERENCE WITH PUBLIC OFFICER": 2,

    "LIQUOR LAW VIOLATION": 1,
    "INTIMIDATION": 1,
    "STALKING": 1,
    "GAMBLING": 1,
    "PUBLIC INDECENCY": 1,
    "OTHER OFFENSE": 1,
    "OTHER NARCOTIC VIOLATION": 1,
    "OBSCENITY": 1,
    "PROSTITUTION": 1,

    "NON-CRIMINAL": 0
}

# Appliquer en normalisant le texte
df["Primary Type_norm"] = df["Primary Type"].fillna("").astype(str).str.upper().str.strip()
df["severity"] = df["Primary Type_norm"].map(severity_map).fillna(1).astype(float)

# --------------------------
# 4. victims_count + breakdown réaliste
# --------------------------
#format: "CRIME": (min_victimes, max_victimes, {"physical": p1, "psychological": p2, "property": p3})

# Profil réaliste par type : (min, max, probs)
victim_profile = {
    "HOMICIDE": (1, 2, {"physical": 0.95, "psychological": 0.95, "property": 0.1}),
    "CRIMINAL SEXUAL ASSAULT": (1, 3, {"physical": 0.8, "psychological": 0.95, "property": 0.05}),
    "CRIM SEXUAL ASSAULT": (1, 3, {"physical": 0.8, "psychological": 0.95, "property": 0.05}),
    "HUMAN TRAFFICKING": (1, 4, {"physical": 0.6, "psychological": 0.95, "property": 0.1}),
    "KIDNAPPING": (1, 2, {"physical": 0.4, "psychological": 0.9, "property": 0.05}),

    "ROBBERY": (1, 2, {"physical": 0.35, "psychological": 0.6, "property": 0.8}),
    "WEAPONS VIOLATION": (1, 1, {"physical": 0.25, "psychological": 0.5, "property": 0.05}),
    "BATTERY": (1, 2, {"physical": 0.8, "psychological": 0.6, "property": 0.1}),
    "ASSAULT": (1, 2, {"physical": 0.75, "psychological": 0.6, "property": 0.05}),
    "OFFENSE INVOLVING CHILDREN": (1, 2, {"physical": 0.5, "psychological": 0.9, "property": 0.05}),

    "BURGLARY": (1, 2, {"physical": 0.05, "psychological": 0.4, "property": 0.95}),
    "MOTOR VEHICLE THEFT": (1, 1, {"physical": 0.02, "psychological": 0.1, "property": 0.98}),
    "CRIMINAL DAMAGE": (1, 1, {"physical": 0.02, "psychological": 0.3, "property": 0.95}),
    "NARCOTICS": (1, 1, {"physical": 0.03, "psychological": 0.2, "property": 0.1}),
    "PUBLIC PEACE VIOLATION": (1, 2, {"physical": 0.05, "psychological": 0.2, "property": 0.1}),

    "THEFT": (1, 1, {"physical": 0.05, "psychological": 0.2, "property": 0.95}),
    "DECEPTIVE PRACTICE": (1, 1, {"physical": 0.0, "psychological": 0.4, "property": 0.8}),
    "CONCEALED CARRY LICENSE VIOLATION": (1, 1, {"physical": 0.1, "psychological": 0.3, "property": 0.05}),
    "CRIMINAL TRESPASS": (1, 1, {"physical": 0.05, "psychological": 0.3, "property": 0.05}),
    "INTERFERENCE WITH PUBLIC OFFICER": (1, 1, {"physical": 0.2, "psychological": 0.4, "property": 0.05}),

    "SEX OFFENSE": (1, 2, {"physical": 0.6, "psychological": 0.9, "property": 0.05}),
    "LIQUOR LAW VIOLATION": (1, 1, {"physical": 0.02, "psychological": 0.2, "property": 0.05}),
    "ARSON": (1, 3, {"physical": 0.25, "psychological": 0.5, "property": 0.9}),
    "PROSTITUTION": (1, 1, {"physical": 0.05, "psychological": 0.2, "property": 0.05}),
    "INTIMIDATION": (1, 1, {"physical": 0.02, "psychological": 0.8, "property": 0.01}),

    "STALKING": (1, 1, {"physical": 0.05, "psychological": 0.85, "property": 0.05}),
    "GAMBLING": (1, 1, {"physical": 0.0, "psychological": 0.05, "property": 0.05}),
    "PUBLIC INDECENCY": (1, 1, {"physical": 0.02, "psychological": 0.3, "property": 0.02}),
    "OTHER NARCOTIC VIOLATION": (1, 1, {"physical": 0.02, "psychological": 0.2, "property": 0.05}),
    "OBSCENITY": (1, 1, {"physical": 0.0, "psychological": 0.4, "property": 0.05}),

    "NON-CRIMINAL": (1, 1, {"physical": 0.0, "psychological": 0.1, "property": 0.0}),

    "OTHER OFFENSE": (1, 1, {"physical": 0.05, "psychological": 0.4, "property": 0.2}),
}


def generate_victims(primary_type):
    pt = str(primary_type).upper().strip()
    if pt in victim_profile:
        mn, mx, probs = victim_profile[pt]
    else:
        mn, mx, probs = 1, 2, {"physical": 0.1, "psychological": 0.5, "property": 0.4}
    mn = max(1, int(mn))
    mx = max(mn, int(mx))
    count = int(np.random.randint(mn, mx + 1))
    physical = psychological = property_loss = 0
    for _ in range(count):
        if random.random() < probs.get("physical", 0):
            physical += 1
        if random.random() < probs.get("psychological", 0):
            psychological += 1
        if random.random() < probs.get("property", 0):
            property_loss += 1
    # garantir au moins un impact si tous nuls
    if physical + psychological + property_loss == 0:
        psychological = 1
    breakdown = f"physical:{physical}|psychological:{psychological}|property:{property_loss}"
    return count, breakdown, physical, psychological, property_loss

victims = df["Primary Type_norm"].apply(lambda t: generate_victims(t))
df["victims_count"] = victims.apply(lambda x: x[0])
df["victim_type_breakdown"] = victims.apply(lambda x: x[1])
df["num_physical_victims"] = victims.apply(lambda x: x[2])
df["num_psychological_victims"] = victims.apply(lambda x: x[3])
df["num_property_victims"] = victims.apply(lambda x: x[4])

# --------------------------
# 5. Préparer colonnes utilitaires pour risk calc
# --------------------------
# Normaliser Arrest/Domestic (peuvent être "true"/"false"/"Y"/"N"/"1"/"0")
def parse_bool(x):
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    return s in ("true","t","yes","y","1","1.0")

df["Arrest_bool"] = df.get("Arrest", "").apply(parse_bool)
df["Domestic_bool"] = df.get("Domestic", "").apply(parse_bool)

# Convertir District en int si possible
def to_int_safe(x):
    try:
        return int(float(x))
    except Exception:
        return np.nan

df["District_int"] = df.get("District", "").apply(to_int_safe)

# --------------------------
# 6. Agrégats par District (pour calculer risk_location_score)
#    - crime_count per district
#    - avg_severity per district
#    - violent_ratio per district (severity >=4)
#    - night_ratio per district (period_of_day == Night)
# --------------------------
# remplacer NaN District par -1 (zone inconnue)
df["District_group"] = df["District_int"].fillna(-1).astype(int)

agg = df.groupby("District_group").agg(
    crime_count = ("Primary Type_norm", "count"),
    avg_severity = ("severity", "mean"),
    violent_count = ("severity", lambda s: (s>=4).sum()),
    night_count = ("period_of_day", lambda s: (s=="Night").sum())
).reset_index()

# calculs normalisés
agg["crime_count_norm"] = agg["crime_count"] / agg["crime_count"].max()
# severity already in 1..5 -> normalize to 0..1
agg["avg_severity_norm"] = (agg["avg_severity"] - 1) / (5 - 1)
agg["violent_ratio"] = np.where(agg["crime_count"]>0, agg["violent_count"]/agg["crime_count"], 0)
agg["night_ratio"] = np.where(agg["crime_count"]>0, agg["night_count"]/agg["crime_count"], 0)

# combine weights into district risk base (weights tunables)
w_crime = 0.4
w_sev = 0.3
w_violent = 0.2
w_night = 0.1

agg["district_raw_risk"] = (
    w_crime * agg["crime_count_norm"] +
    w_sev * agg["avg_severity_norm"] +
    w_violent * agg["violent_ratio"] +
    w_night * agg["night_ratio"]
)

# Normaliser district_raw_risk 0..1
minv = agg["district_raw_risk"].min()
maxv = agg["district_raw_risk"].max()
if maxv - minv > 0:
    agg["district_risk_norm"] = (agg["district_raw_risk"] - minv) / (maxv - minv)
else:
    agg["district_risk_norm"] = 0.0

# --------------------------
# 7. Mapper les scores de district dans le DataFrame principal
# --------------------------
agg_map = agg.set_index("District_group")["district_risk_norm"].to_dict()
df["district_risk_norm"] = df["District_group"].map(agg_map).fillna(0.0)

# ajouter effets d'arrest/domestic individuels :
# - domestic augmente le risque local (facteur)
# - arrest diminue le risque local (car présence de contrôle)
df["domestic_increase"] = df["Domestic_bool"].apply(lambda x: 0.1 if x else 0.0)
df["arrest_decrease"] = df["Arrest_bool"].apply(lambda x: -0.1 if x else 0.0)

# combine final risk per record: base district score modifié par row-level effects and severity
# weights (tunable)
w_district = 0.6
w_severity_row = 0.3
w_row_effects = 0.1

# normalize severity row to 0..1
df["severity_norm_row"] = (df["severity"] - 1) / (5 - 1)

df["risk_raw"] = (
    w_district * df["district_risk_norm"] +
    w_severity_row * df["severity_norm_row"] +
    w_row_effects * (df["domestic_increase"] + df["arrest_decrease"])
)

# final normalization 0..1 across all records
min_r = df["risk_raw"].min()
max_r = df["risk_raw"].max()
if max_r - min_r > 0:
    df["risk_location_score"] = (df["risk_raw"] - min_r) / (max_r - min_r)
else:
    df["risk_location_score"] = 0.0

# --------------------------
# 8. Catégorie lisible (Low/Medium/High)
# --------------------------
def risk_level(score):
    if score >= 0.66:
        return "High"
    elif score >= 0.33:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df["risk_location_score"].apply(risk_level)

# --------------------------
# 9. Sauvegarde du fichier unique
# --------------------------
# Colonnes à conserver: originales + nouvelles
new_cols = [
    "period_of_day", "hour", "severity",
    "victims_count", "victim_type_breakdown",
    "num_physical_victims","num_psychological_victims","num_property_victims",
    "district_risk_norm","risk_location_score","risk_level",
    "Arrest_bool","Domestic_bool"
]
# écrire tout le DF (original + nouvelles colonnes)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
print(f"Fichier enrichi sauvegardé → {OUTPUT_CSV}")
