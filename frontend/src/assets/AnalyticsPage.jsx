import React from "react";

// Importer les images depuis assets
import img1 from "./heatmap.png";
import img2 from "./pourcentage.png";
import img3 from "./victim_type_breakdown.png";
import img4 from "./map.png";
import img5 from "./top_crimes.png";
import img6 from "./blocks.png";
import img7 from "./analysis.png";
import img8 from "./courbe.png";

const images = [img1, img2, img3, img4, img5, img6, img7, img8];

const AnalyticsPage = () => {
  return (
    <div style={{ width: "100%", minHeight: "100vh", padding: "20px" }}>
      <h1>Analytics Page</h1>

      {/* Grid container */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)", // 2 images par ligne
          gap: "16px",
        }}
      >
        {images.map((src, index) => (
          <div key={index} style={{ width: "100%" }}>
            <img
              src={src}
              alt={`Analytics ${index + 1}`} // <-- corrigé ici
              style={{ width: "100%", height: "auto", borderRadius: "8px" }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnalyticsPage;
