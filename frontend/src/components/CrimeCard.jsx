import React from "react";

// Sévérité
const severityMap = {
  5: "Très critique",
  4: "Critique",
  3: "Élevée",
  2: "Faible",
  1: "Très faible",
};

// Badge coloré selon type
function typeToBadgeStyle(type) {
  const t = (type || "").toLowerCase();
  if (t.includes("theft") || t.includes("motor") || t.includes("robbery"))
    return { background: "#F5C156", color: "#3a2f00" };
  if (t.includes("assault") || t.includes("battery") || t.includes("violent"))
    return { background: "#D9534F", color: "#fff" };
  if (t.includes("burglary")) return { background: "#3B82F6", color: "#fff" };
  if (t.includes("vandalism") || t.includes("damage"))
    return { background: "#7C4DFF", color: "#fff" };
  return { background: "#333", color: "#fff" };
}

// Styles
const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
    gap: "16px",
  },
  card: {
    background: "#0f1720",
    border: "1px solid #222831",
    borderRadius: "12px",
    padding: "16px",
    color: "#e6eef6",
    boxShadow: "0 2px 6px rgba(0,0,0,0.4)",
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  title: { fontSize: "18px", fontWeight: 600 },
  description: { fontSize: "14px", color: "#c9d4da" },
  row: { display: "flex", gap: "16px", flexWrap: "wrap" },
  item: { fontSize: "13px", color: "#c9d4da" },
  label: { fontWeight: 600, marginRight: "4px" },
  badge: { borderRadius: "8px", padding: "4px 10px", fontWeight: 700, fontSize: "12px", alignSelf: "flex-start" },
};

function CrimeCard({ hit }) {
  if (!hit || !hit.source) return null;

  const src = hit.source;
  const primary = src.primary_type || "Unknown";
  const description = src.description || "Pas de description";
  const date = src.date ? new Date(src.date).toLocaleString() : "No date";
  const location = src.location_description ?? src.block ?? "N/A";
  const district = src.district ?? "N/A";
  const victim = src.victim_type_selected || "N/A";
  const arrestRaw = src.Arrest ?? src.arrest; // essaie les deux noms
  let arrest;
  if (arrestRaw === true || arrestRaw === "true") arrest = "Yes";
  else if (arrestRaw === false || arrestRaw === "false") arrest = "No";
  else arrest = "N/A";


  const badgeStyle = typeToBadgeStyle(primary);

  return (
    <div style={styles.card}>
      {/* Primary type */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={styles.title}>{primary}</span>
        <span style={badgeStyle}>{primary}</span>
      </div>

      {/* Description */}
      <div style={styles.description}>{description}</div>

      {/* Date + Location + District */}
      <div style={styles.row}>
        <div style={styles.item}><span style={styles.label}>Date:</span>{date}</div>
        <div style={styles.item}><span style={styles.label}>Location:</span>{location}</div>
        <div style={styles.item}><span style={styles.label}>District:</span>{district}</div>
      </div>

      {/* Victim type + Arrest */}
      <div style={styles.row}>
        <div style={styles.item}><span style={styles.label}>Type of Harm:</span>{victim}</div>
        <div style={styles.item}><span style={styles.label}>Arrest:</span>{arrest}</div>
      </div>
    </div>
  );
}
export default CrimeCard;