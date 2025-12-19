# 🏙️ Nahj Tribunal Monitor  
### Urban Crime Analysis & Decision Support System

---

## 📖 Overview

**Nahj Tribunal Monitor** is a data-driven web platform designed to analyze, search, and visualize urban crime incidents using real-world open data.  
The system enables users to explore crime patterns by **type, time, and location**, access **detailed incident information**, and analyze **spatio-temporal trends** through interactive dashboards.

This project demonstrates a **modern NoSQL and Big Data architecture**, integrating **MongoDB**, **Elasticsearch**, **Kibana**, and a **FastAPI-based backend**, complemented by a lightweight web interface.

---

## 🎯 Project Objectives

- Assess the **safety level of a city**
- Identify **high-risk districts and zones**
- Analyze **crime trends over time**
- Provide **fast and relevant search capabilities**
- Offer **interactive visual analytics**

---

## 🧠 Functional Features

- Search crimes by:
  - Crime type
  - Keywords
  - Date and time
  - District / community area
  - Geographic zone
- View detailed information for each incident
- Visualize crime statistics using Kibana dashboards
- Explore spatial crime distribution using maps

---

## 📊 Dataset Description

### Primary Dataset (Recommended)

**Chicago Crimes Dataset (2024)**  
Source: City of Chicago – Open Data Portal  
🔗 https://data.cityofchicago.org/Public-Safety/Crimes-2024/w98m-zvie

**Key Advantages**
- Real incident-level data
- Clean and well-structured
- Rich temporal and spatial attributes
- Ideal for geospatial analysis and dashboards

> Global datasets were intentionally avoided as they provide aggregated statistics rather than individual crime events, limiting analytical depth.

---

## 🏗️ System Architecture

### Global Data Pipeline

