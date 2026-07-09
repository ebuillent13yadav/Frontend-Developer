import React, { useState } from 'react';

const StatisticsWidget = ({ title, value, icon }) => (
  <div className="stats-widget">
    <span>{icon}</span>
    <h4>{title}</h4>
    <p>{value}</p>
  </div>
);

const StatsCardsContainer = ({ children }) => (
  <div className="stats-cards-container">
    {children}
  </div>
);

const HeaderSection = ({ pageTitle }) => (
  <header className="header-section">
    <h1>{pageTitle}</h1>
  </header>
);

const DarkThemeWrapper = ({ isDarkMode, children }) => {
  return isDarkMode ? (
    <div
      style={{
        backgroundColor: '#333',
        color: '#fff',
        padding: '20px'
      }}
    >
      {children}
    </div>
  ) : (
    children
  );
};

const DashboardOverviewPage = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);

  return (
    <DarkThemeWrapper isDarkMode={isDarkMode}>
      <HeaderSection pageTitle="Dashboard Overview" />
      <StatsCardsContainer>
        <StatisticsWidget title="Users" value="123456" icon={<span className="icon-user"></span>} />
        <StatisticsWidget title="Active Sessions" value="98765" icon={<span className="icon-session"></span>} />
      </StatsCardsContainer>
    </DarkThemeWrapper>
  );
};

export default DashboardOverviewPage;