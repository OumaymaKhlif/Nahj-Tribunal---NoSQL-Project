import React, { useState, useEffect } from "react";
import { Search, MapPin, Shield } from "lucide-react";
import axios from "axios";
import heroBg from "../assets/hero-bg.jpg";

import { FaDatabase } from "react-icons/fa";
import { SiElasticsearch, SiFastapi, SiMongodb } from "react-icons/si";
import { MdDataExploration, MdManageSearch } from "react-icons/md";

import { useNavigate } from "react-router-dom"

const HomeHero = () => {
  const [queryIncident, setQueryIncident] = useState("");
  const [queryDistrict, setQueryDistrict] = useState("");
  const [totalIncidents, setTotalIncidents] = useState(0);
  const [totalDistricts, setTotalDistricts] = useState(0);
  const [totalTypes, setTotalTypes] = useState(0);

  const apiBase = "http://localhost:8000"; // API URL

   const navigate = useNavigate();

  useEffect(() => {
    // Total incidents
    axios.get(`${apiBase}/api/count`)
      .then(res => {
        if (res.data && typeof res.data.count === "number") {
          setTotalIncidents(res.data.count);
        }
      })
      .catch(err => console.error("Count error:", err));

    // MongoDB stats (unique types & districts)
    axios.get(`${apiBase}/api/mongo_summary`)
      .then(res => {
        if (res.data) {
          setTotalTypes(res.data.totalTypes || 0);
          setTotalDistricts(res.data.totalDistricts || 0);
        }
      })
      .catch(err => console.error("Mongo summary error:", err));
  }, []);

  const handleSearch = () => {
  const params = new URLSearchParams();
  if (queryIncident) params.append("q", queryIncident);
  if (queryDistrict) params.append("district", queryDistrict);
  navigate(`/explorer?${params.toString()}`);
};

  const btnYellow = "255, 214, 88";

  return (
    <div style={{ width: "100%", boxSizing: "border-box" }}>
      {/* Hero Section */}
      <div
        style={{
          width: "100%",
          minHeight: "100vh",
          backgroundImage: `url(${heroBg})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          position: "relative",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          color: "#fff",
        }}
      >
        {/* Dark overlay */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0,0,0,0.5)",
            zIndex: 1,
          }}
        />

        {/* Content */}
        <div style={{ position: "relative", zIndex: 2, textAlign: "center", width: "100%", padding: "0 20px" }}>
          <h1 style={{ fontSize: "3rem", fontWeight: "700", marginBottom: "30px" }}>
            Explore your city's <span style={{ color: `rgb(${btnYellow})` }}>safety</span>
          </h1>
          <p style={{ fontSize: "1.1rem", maxWidth: "600px", margin: "0 auto 50px" }}>
            Explore and analyze crime data with our powerful interactive platform. Easily search, filter, and examine incidents across the city of Chicago, gaining valuable insights into public safety trends.
          </p>

          {/* Search bar */}
          <div style={{ display: "flex", justifyContent: "center", gap: "10px", flexWrap: "wrap", marginBottom: "60px" }}>
            <div style={{ display: "flex", alignItems: "center", padding: "10px", borderRadius: "8px", backgroundColor: "rgba(255,255,255,0.9)", color: "#000", minWidth: "250px" }}>
              <Search size={20} style={{ marginRight: "8px" }} />
              <input
                type="text"
                placeholder="Search for an incident"
                value={queryIncident}
                onChange={(e) => setQueryIncident(e.target.value)}
                style={{ border: "none", outline: "none", flex: 1, fontSize: "1rem", width: "100%" }}
              />
            </div>

            <div style={{ display: "flex", alignItems: "center", padding: "10px", borderRadius: "8px", backgroundColor: "rgba(255,255,255,0.9)", color: "#000", minWidth: "180px" }}>
              <MapPin size={20} style={{ marginRight: "8px" }} />
              <input
                type="text"
                placeholder="District..."
                value={queryDistrict}
                onChange={(e) => setQueryDistrict(e.target.value)}
                style={{ border: "none", outline: "none", flex: 1, fontSize: "1rem", width: "100%" }}
              />
            </div>

            <button
              onClick={handleSearch}
              style={{ padding: "10px 20px", borderRadius: "8px", border: "none", backgroundColor: `rgb(${btnYellow})`, color: "#000", fontWeight: "600", cursor: "pointer", display: "flex", alignItems: "center", gap: "5px" }}
            >
              <Search size={16} /> Search
            </button>
          </div>

          {/* Stats */}
          <div style={{ display: "flex", justifyContent: "center", gap: "20px", flexWrap: "wrap", marginTop: "20px" }}>
            {[
              { label: "Incidents analyzed", value: totalIncidents },
              { label: "Districts covered", value: totalDistricts },
              { label: "Types of crime", value: totalTypes },
            ].map((stat, idx) => (
              <div key={idx} style={{ backgroundColor: "rgba(255,255,255,0.9)", padding: "20px", minWidth: "140px", textAlign: "center", borderRadius: "10px", boxShadow: "0 2px 8px rgba(0,0,0,0.2)", color: "#000" }}>
                <Shield size={30} style={{ marginBottom: "10px" }} />
                <h3 style={{ fontSize: "1.5rem", margin: "0 0 5px 0" }}>{stat.value}</h3>
                <p style={{ margin: 0, fontWeight: "500" }}>{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div
        id="features"
        style={{
          width: "100%",
          backgroundColor: "rgba(7, 17, 31, 0.8)",
          color: "#fff",
          textAlign: "center",
          padding: "4rem 2rem",
        }}
      >
        <h3
          style={{
            fontWeight: "300",
            fontSize: "1.3rem",
            marginBottom: "0.5rem",
            letterSpacing: "1px",
            color: "#ffd658",
          }}
        >
          Features
        </h3>

        <h2
          style={{
            fontWeight: "700",
            fontSize: "2rem",
            marginBottom: "1rem",
          }}
        >
          A <span style={{ color: "#ffd658" }}>complete</span> platform
        </h2>

        <p style={{ maxWidth: "700px", margin: "0 auto", fontSize: "1.1rem" }}>
          Our platform allows you to visualize, analyze, and filter crime data with advanced tools and clear visualizations.
        </p>
      </div>

      {/* Tech / Tools */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "1.5rem",
          padding: "2rem",
        }}
      >
        {[
          {
            icon: <SiMongodb size={35} />,
            title: "MongoDB",
            desc: "Flexible and high-performance NoSQL database. Ideal for handling large datasets quickly."
          },
          {
            icon: <SiElasticsearch size={35} />,
            title: "Elasticsearch",
            desc: "Ultra-fast search and indexing engine. Perfect for analyzing millions of records in real-time."
          },
          {
            icon: <MdDataExploration size={35} />,
            title: "Kibana Visualizations",
            desc: "Visualization tool connected to Elasticsearch. Allows creating dashboards and analyzing crime trends."
          },
          {
            icon: <SiFastapi size={35} />,
            title: "FastAPI",
            desc: "High-performance backend framework for building modern APIs. Optimized for speed and simplicity."
          },
          {
            icon: <FaDatabase size={35} />,
            title: "Data Sources",
            desc: "Data collected from multiple official platforms. Provides a reliable foundation for crime analysis."
          },
          {
            icon: <MdManageSearch size={35} />,
            title: "Advanced Search",
            desc: "Feature to filter and explore crimes. Facilitates investigation and extracting insights."
          }
        ].map((item, idx) => (
          <div
            key={idx}
            style={{
              flex: "1 1 250px",
              backgroundColor: "rgba(0,0,0,0.3)",
              color: "#fff",
              padding: "1.5rem",
              borderRadius: "14px",
              textAlign: "center",
              backdropFilter: "blur(4px)",
            }}
          >
            {item.icon}
            <h3 style={{ marginTop: "0.8rem", fontWeight: "700" }}>{item.title}</h3>
            <p style={{ marginTop: "0.5rem", fontSize: "0.95rem", opacity: 0.9 }}>
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomeHero;
