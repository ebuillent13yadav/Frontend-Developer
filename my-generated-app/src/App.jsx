import React from 'react';
import { Navbar, Sidebar, MainDashboardBody, Footer } from './components';

const App = () => {
  return (
    <div className="dark">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <MainDashboardBody />
      </div>
      <Footer />
    </div>
  );
};

export default App;