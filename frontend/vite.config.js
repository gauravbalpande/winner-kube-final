import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        // In docker-compose, backend is accessible via service name
        // Locally, use localhost (ports are exposed)
        target: process.env.DOCKER_ENV === 'true' 
          ? 'http://backend:8000' 
          : 'http://localhost:8000',
        changeOrigin: true,
        // Strip /api prefix when proxying to backend (backend serves without prefix in dev)
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})