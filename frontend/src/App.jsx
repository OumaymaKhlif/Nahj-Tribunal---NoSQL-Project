import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomeHero from "./components/HomeHero";
import ExplorerPage from "./components/ExplorerPage";
import Footer from "./components/Footer";
import AnalyticsPage from "./assets/AnalyticsPage";

export default function App(){
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<>
            <HomeHero />
            {/* below hero include StatsCards component if desired */}
          </>} />
          <Route path="/explorer" element={<ExplorerPage />} />
          <Route path="/crime/:id" element={<ExplorerPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </main>
      {/* Footer */}
      <Footer />
    </div>
  )
}

