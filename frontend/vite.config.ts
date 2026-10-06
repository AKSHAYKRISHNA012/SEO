import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // In production, VITE_API_URL env var points to the Render backend
  // In dev, proxy /api to local FastAPI server
  server: {
    port: 5173,
    proxy:
      mode === 'development'
        ? {
            '/api': {
              target: 'http://127.0.0.1:8000',
              changeOrigin: true,
              secure: false,
            },
          }
        : undefined,
  },
  define: {
    // Expose env var to app
    __API_BASE__: JSON.stringify(
      process.env.VITE_API_URL ?? ''
    ),
  },
}));
