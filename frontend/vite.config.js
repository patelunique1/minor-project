import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // so you can visit http://localhost:3000
    proxy: {
      // forward API calls to Flask (localhost:5000)
      "/generate_patch": "http://localhost:5000",
      "/init_models": "http://localhost:5000",
      "/health": "http://localhost:5000",
    },
  },
});
