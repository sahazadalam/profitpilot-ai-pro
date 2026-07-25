import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Sales } from './pages/sales/Sales';
import { Inventory } from './pages/inventory/Inventory';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div style={{ backgroundColor: '#ffffff', minHeight: '100vh' }}>
          <Routes>
            <Route path="/" element={<Sales />} />
            <Route path="/sales" element={<Sales />} />
            <Route path="/inventory" element={<Inventory />} />
          </Routes>
          <Toaster 
            position="top-right"
            toastOptions={{
              style: {
                background: '#ffffff',
                color: '#0f172a',
                border: '1px solid #e2e8f0',
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;

