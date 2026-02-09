import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://chatcli.edilsonfreitas.com',
  output: 'static',
  build: {
    assets: 'assets'
  }
});
