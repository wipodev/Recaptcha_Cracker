import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Recaptcha Cracker",
  description: "A VitePress Site",
  base: "/Recaptcha_Cracker/",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Tests", link: "/tests" },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/wipodev/Recaptcha_Cracker" }],
  },
});
