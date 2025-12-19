import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Home, Search, BarChart2, Info } from "lucide-react";

const Navbar = () => {
  const navigate = useNavigate();
  const [scroll, setScroll] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScroll(window.scrollY > 50);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const btnYellow = "255, 214, 88"; // RGB pour var(--btn-yellow)

  return (
    <header>
      <div
        className="navbar"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "8px 50px",
          backgroundColor: "rgba(7, 17, 31, 0.6)",
          color: "#ffffff",
          transition: "all 0.3s ease",
          zIndex: 999,
          boxSizing: "border-box",
          backdropFilter: "blur(8px)"
        }}
      >
        {/* Logo + Brand */}
        <div
          style={{ display: "flex", alignItems: "center", gap: "12px", cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          <div
            style={{
              width: "36px",
              height: "36px",
              backgroundColor: `rgb(${btnYellow})`,
              borderRadius: "10px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontWeight: "bold",
              color: "black",
              fontSize: "1rem",
            }}
          >
            🛡
          </div>
          <h1 style={{ fontSize: "1.5rem", fontFamily: "serif", fontWeight: "700" }}>
            <span>Nahj</span>
            <span style={{ color: `rgb(${btnYellow})` }}>Tribunal</span>
          </h1>
        </div>

        {/* Navigation Links */}
        <nav style={{ display: "flex", alignItems: "center", gap: "15px" }}>
          {[
            { icon: Home, label: "Home", path: "/" },
            { icon: Search, label: "Crime Explorer", path: "/explorer" },
            { icon: BarChart2, label: "Analytics", path: "/analytics" },
            { icon: Info, label: "About Us", path: "/#features"  },
          ].map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
               onClick={() => {
                if (item.path.startsWith("/#")) {
                  // rester sur home + scroller
                  navigate("/");
                  setTimeout(() => {
                    const section = document.querySelector(item.path.replace("/", ""));
                    if (section) section.scrollIntoView({ behavior: "smooth" });
                  }, 50);
                } else {
                  navigate(item.path);
                }
              }}

                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                  cursor: "pointer",
                  fontSize: "0.9rem",
                  padding: "6px 10px",
                  borderRadius: "6px",
                  transition: "all 0.2s",
                  color: "#ffffff", // couleur de base
                  background: "transparent"
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = `rgba(${btnYellow}, 0.3)`;
                  e.currentTarget.style.color = `rgb(${btnYellow})`;
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = "transparent";
                  e.currentTarget.style.color = "#ffffff";
                }}
              >
                <Icon size={16} /> {item.label}
              </div>
            );
          })}
        </nav>

        {/* Explorer Button */}
        <button
          style={{
            padding: "0.6em 2em",
            fontSize: "1rem",
            borderRadius: "8px",
            backgroundColor: `rgb(${btnYellow})`,
            color: "black",
            fontWeight: "600",
            cursor: "pointer",
            border: "none",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
          onClick={() => navigate("/explorer")}
        >
          <Search size={16} /> Explore
        </button>
      </div>
    </header>
  );
};

export default Navbar;
