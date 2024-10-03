import React from 'react';
import Header from '../components/Header';
import HealthSummary from '../components/HealthSummary';
import AIAlerts from '../components/AIAlerts';
import DiseasePredictor from '../components/DiseasePredictor';
import HealthAssistant from '../components/HealthAssistant';
import Insights from '../components/Insights';
import DoctorRecommendations from '../components/DoctorRecommendations';
import HealthReports from '../components/HealthReports';
import HealthReportDetails from '../components/HealthReportDetails';
import BlogSection from '../components/BlogSection';
import SmartwatchConnectedCard from '../components/SmartwatchCard';

function Dashboard() {
  // Get the name from localStorage (or replace with your own logic)
  const name = localStorage.getItem('name') || 'Guest'; // Fallback to 'Guest' if no name

  return (
    <div className="container">
      {/* Pass the name to the Header component */}
      <Header name={name} />
      {/* <SmartwatchConnectedCard name={name} /> Pass name to the card */}
      {/* <HealthSummary name={name} /> Pass name to HealthSummary */}
      <HealthAssistant />
      <DoctorRecommendations />
      {/* <AIAlerts />
      <DiseasePredictor />
      <Insights />
      
      <HealthReports />
      <HealthReportDetails />
      <BlogSection /> */}
    </div>
  );
}

export default Dashboard;
