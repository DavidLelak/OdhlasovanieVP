import React from 'react';
import ReactDOM from 'react-dom/client';
import AdminUI from './admin_user_ui.jsx';
import VpTerminal from './vp_terminal.jsx';

const path = window.location.hash;

const App = () => {
  if (path.includes("vp")) {
    return <VpTerminal />;
  }
  return <AdminUI />;
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);