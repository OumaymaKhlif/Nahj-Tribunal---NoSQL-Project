import React, { useState, useEffect } from "react";
import axios from "axios";
import CrimeCard from "./CrimeCard";
import { Search, Filter } from "lucide-react";
import "./ExplorerPage.css";
import { useLocation } from "react-router-dom";

export default function ExplorerPage() {
  const location = useLocation();

  // Helper pour lire les query params
  const useQuery = () => new URLSearchParams(location.search);
  const query = useQuery();

  const [q, setQ] = useState(query.get("q") || "");
  const [primaryType, setPrimaryType] = useState(query.get("primary_type") || "");
  const [district, setDistrict] = useState(query.get("district") || "");
  const [dateFrom, setDateFrom] = useState(query.get("date_from") || "");
  const [dateTo, setDateTo] = useState(query.get("date_to") || "");
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [allTypes, setAllTypes] = useState([]);
  const [allDistricts, setAllDistricts] = useState([]);

  const api = "http://localhost:8000";

  // Main search function
  const search = async () => {
  const params = {};
  if (q) params.q = q;
  if (primaryType) params.primary_type = primaryType.toLowerCase();
  if (district) params.district = Number(district);
  if (dateFrom) params.date_from = dateFrom;
  if (dateTo) params.date_to = dateTo;

  console.log("Search params:", params); // debug

  try {
    const res = await axios.get(`${api}/api/search`, { params });
    console.log("Search response:", res.data); // debug
    setResults(res.data.hits);
    setTotal(res.data.total);
  } catch (err) {
    console.error("Search error:", err);
    setResults([]);
    setTotal(0);
  }
};

  // Fetch unique values for dropdown filters
  const fetchFilters = async () => {
    try {
      const res = await axios.get(`${api}/api/aggregations/summary`);
      const types = res.data.by_type?.buckets?.map((b) => b.key) || [];
      const districts = res.data.by_hour?.buckets?.map((b) => b.key) || [];
      setAllTypes(types);
      setAllDistricts(districts);
    } catch (err) {
      console.error("Error fetching filters:", err);
    }
  };

 // Keep this to populate dropdowns
useEffect(() => {
  fetchFilters();
}, []);

// Ajoutez ceci après votre useEffect actuel qui fait fetchFilters et search()
useEffect(() => {
  // Lance la recherche à chaque changement de filtre ou de recherche
  search();
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [q, primaryType, district, dateFrom, dateTo]);


  return (
    <div className="explorer-container">
      <h1 className="explorer-title">
        Crime <span className="yellow">Explorer</span>
      </h1>
      <p className="explorer-subtitle">
        Search and explore crime incidents in Chicago
      </p>

      <div className="filter-card">
        <div className="search-row">
          <div className="input-wrapper">
            <Search className="input-icon" size={20} />
            <input
              type="text"
              placeholder="Search for a crime (e.g., theft...)"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              className="input"
            />
          </div>

          <button onClick={search} className="search-btn">
            <Search size={18} />
            Search
          </button>
        </div>

        <div className="filters-row">
          {/* Crime type dropdown */}
          <select
            value={primaryType}
            onChange={(e) => setPrimaryType(e.target.value)}
            className="input"
          >
            <option value="">All types</option>
            {allTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>

          {/* District dropdown */}
          <select
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            className="input"
          >
            <option value="">All districts</option>
            {allDistricts.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>

          <input
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="input"
          />
        </div>

        <div className="active-filters">
          <Filter size={18} />
          <span>Active filters:</span>
          <span className="value">
            {primaryType || district || dateFrom || dateTo ? "" : "No filters"}
          </span>
        </div>
      </div>

      <p className="results-count">{total} incidents found</p>

      <div
        className="results-list"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: "16px",
        }}
      >
        {results.map((hit) => (
          <CrimeCard key={hit.id} hit={hit} />
        ))}
      </div>
    </div>
  );
}
