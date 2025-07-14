import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/start': 'http://localhost:8000',
      '/stop': 'http://localhost:8000'
    }
  }
});