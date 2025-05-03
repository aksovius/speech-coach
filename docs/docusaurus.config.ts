import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: "Speech Coach",
  tagline: "Powered by AI, Driven by Data",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://speech-coach.alexanderkim.dev",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "aksovius", // Usually your GitHub org/user name.
  projectName: "speech-coach", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/aksovius/speech-coach/tree/main/docs-site/",
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ["rss", "atom"],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/aksovius/speech-coach/tree/main/docs-site/blog/",
          // Useful options to enforce blogging best practices
          onInlineTags: "warn",
          onInlineAuthors: "warn",
          onUntruncatedBlogPosts: "warn",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/speech-coach-social-card.png",
    navbar: {
      title: "Speech Coach",
      logo: {
        alt: "Speech Coach Logo",
        src: "img/logo.svg",
      },
      items: [
        { to: "/about", label: "About", position: "left" },
        { to: "/features", label: "Features", position: "left" },
        { to: "/tech-stack", label: "Tech Stack", position: "left" },
        {
          type: "doc",
          docId: "intro",
          position: "left",
          label: "Docs",
        },
        { to: "/blog", label: "Blog", position: "left" },
        { to: "/contact", label: "Contact", position: "right" },
        {
          href: "https://github.com/aksovius/speech-coach",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            { label: "Introduction", to: "/docs/intro" },
            { label: "Architecture", to: "/docs/architecture/overview" },
            { label: "Getting Started", to: "/docs/getting-started/installation" },
          ],
        },
        {
          title: "Connect",
          items: [
            { label: "GitHub", href: "https://github.com/aksovius/speech-coach" },
            { label: "LinkedIn", href: "https://www.linkedin.com/in/aksovius" },
            { label: "Telegram", href: "https://t.me/aksovius" },
          ],
        },
        {
          title: "More",
          items: [
            { label: "Blog", to: "/blog" },
            { label: "Roadmap", to: "/docs/roadmap" },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Speech Coach. Built by Alexander Kim.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
