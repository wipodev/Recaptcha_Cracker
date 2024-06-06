import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Recaptcha Cracker",
  description: "Documentation for Recaptcha Cracker",
  base: "/Recaptcha_Cracker/",
  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Getting Started", link: "/guide/getting-started" },
      { text: "Reference", link: "/guide/reference" },
    ],
    sidebar: {
      "/": [
        {
          text: "Guide",
          items: [
            { text: "Getting Started", link: "/guide/getting-started" },
            { text: "Reference", link: "/guide/reference" },
            { text: "Tests", link: "/tests" },
          ],
        },
      ],
    },
    socialLinks: [{ icon: "github", link: "https://github.com/wipodev/Recaptcha_Cracker" }],
  },
});
