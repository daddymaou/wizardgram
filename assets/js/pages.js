export const pages = [
  {
    slug: "welcome",
    title: "Welcome",
    path: "index.html",
    group: "Begin here",
    summary: "Async Telegram bot framework for Python.",
    headings: ["Welcome", "Why wizardgram", "What this site covers"],
    type: "home"
  },
  {
    slug: "install",
    title: "Install",
    path: "docs/install.html",
    group: "Begin here",
    summary: "Install wizardgram and set up your token.",
    headings: ["Install", "Python support", "Token setup"],
    type: "docs"
  },
  {
    slug: "quickstart",
    title: "Quickstart",
    path: "docs/quickstart.html",
    group: "Begin here",
    summary: "Run a minimal bot in a few steps.",
    headings: ["Quickstart", "Bot setup", "Run your bot"],
    type: "docs"
  },
  {
    slug: "middleware",
    title: "Middleware",
    path: "docs/middleware.html",
    group: "Spells",
    summary: "Wrap update handling with middleware.",
    headings: ["Middleware", "Logging middleware", "When to use it"],
    type: "docs"
  },
  {
    slug: "bot-api-coverage",
    title: "Bot API coverage",
    path: "docs/bot-api-coverage.html",
    group: "Spells",
    summary: "Check which Telegram API methods are covered.",
    headings: ["Bot API coverage", "Status check", "Verified methods"],
    type: "docs"
  },
  {
    slug: "scenes-fsm",
    title: "Scenes & FSM",
    path: "docs/scenes-fsm.html",
    group: "Spells",
    summary: "Chain a multi-step flow with scenes and a stage.",
    headings: ["Scenes & FSM", "Stage setup", "Scene state"],
    type: "docs"
  },
  {
    slug: "keyboards",
    title: "Keyboards",
    path: "docs/keyboards.html",
    group: "Spells",
    summary: "Build inline and reply keyboards.",
    headings: ["Keyboards", "Inline keyboard", "Reply keyboard"],
    type: "docs"
  },
  {
    slug: "webhooks",
    title: "Webhooks",
    path: "docs/webhooks.html",
    group: "Spells",
    summary: "Handle Telegram webhooks with your bot.",
    headings: ["Webhooks", "Hook endpoint", "Set and remove webhooks"],
    type: "docs"
  },
  {
    slug: "file-uploads",
    title: "File uploads",
    path: "docs/file-uploads.html",
    group: "Spells",
    summary: "Send photo and file payloads from your bot.",
    headings: ["File uploads", "Photo reply", "When to use it"],
    type: "docs"
  },
  {
    slug: "examples",
    title: "Examples",
    path: "docs/examples.html",
    group: "Grimoire",
    summary: "A quick catalog of the bundled examples.",
    headings: ["Examples", "Available scripts", "How to run them"],
    type: "docs"
  },
  {
    slug: "coverage-confidence",
    title: "Coverage confidence",
    path: "docs/coverage-confidence.html",
    group: "Grimoire",
    summary: "A realistic view of what is verified and what is inferred.",
    headings: ["Coverage confidence", "Method coverage", "Multipart uploads"],
    type: "docs"
  },
  {
    slug: "project-layout",
    title: "Project layout",
    path: "docs/project-layout.html",
    group: "Grimoire",
    summary: "Where the framework source and example apps live.",
    headings: ["Project layout", "src", "examples"],
    type: "docs"
  },
  {
    slug: "contributing",
    title: "Contributing & license",
    path: "docs/contributing.html",
    group: "Grimoire",
    summary: "Development guidance and licensing information.",
    headings: ["Contributing & license", "Contributor guidance", "Apache-2.0"],
    type: "docs"
  }
];

export const pageDictionary = Object.fromEntries(
  pages.map((page) => [page.slug, page])
);

export const groups = [
  { name: "Begin here", pages: pages.filter((page) => page.group === "Begin here") },
  { name: "Spells", pages: pages.filter((page) => page.group === "Spells") },
  { name: "Grimoire", pages: pages.filter((page) => page.group === "Grimoire") }
];
