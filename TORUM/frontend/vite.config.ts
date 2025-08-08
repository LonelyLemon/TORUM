import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'ec2-3-106-239-219.ap-southeast-2.compute.amazonaws.com'
    ]
  },
  envPrefix: 'VITE_',
})
