import { groups, pages } from "./pages.js";

function buildRelativeHref(pagePath) {
  const root = document.body.dataset.root || ".";
  return `${root}/${pagePath}`.replace(/\/\//g, "/");
}

function getCurrentPage() {
  const currentSlug = document.body.dataset.page;
  return pages.find((page) => page.slug === currentSlug) || pages[0];
}

function buildSidebar() {
  const sidebar = document.getElementById("sidebar");
  if (!sidebar) return;

  const html = groups
    .map((group) => {
      const links = group.pages
        .map((page) => {
          const isCurrent = page.slug === getCurrentPage().slug;
          return `
            <li class="sidebar__item">
              <a href="${buildRelativeHref(page.path)}" aria-current="${isCurrent ? "page" : "false"}">${page.title}</a>
            </li>
          `;
        })
        .join("");

      return `
        <ul class="sidebar__group" aria-label="${group.name}">
          <li class="sidebar__label">${group.name}</li>
          ${links}
        </ul>
      `;
    })
    .join("");

  sidebar.innerHTML = html;
}

function buildPageToc() {
  const toc = document.getElementById("page-toc");
  if (!toc) return;

  const headings = [...document.querySelectorAll(".doc h2, .doc h3")];
  if (!headings.length) {
    toc.hidden = true;
    return;
  }

  toc.innerHTML = '<p class="page-toc__title">On this page</p><ul></ul>';
  const list = toc.querySelector("ul");

  headings.forEach((heading) => {
    const text = heading.textContent.trim();
    const id = text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    if (!heading.id) heading.id = id;

    const item = document.createElement("li");
    const link = document.createElement("a");
    link.href = `#${heading.id}`;
    link.textContent = text;
    if (heading.tagName === "H3") {
      link.style.marginLeft = "0.8rem";
    }
    item.appendChild(link);
    list.appendChild(item);
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const activeLink = toc.querySelector(`a[href="#${entry.target.id}"]`);
        if (!activeLink) return;
        document.querySelectorAll(".page-toc a").forEach((anchor) => anchor.classList.remove("is-active"));
        activeLink.classList.add("is-active");
      });
    },
    { rootMargin: "-10% 0% -65% 0%", threshold: [0.2] }
  );

  headings.forEach((heading) => observer.observe(heading));
}

function buildPrevNext() {
  const nav = document.querySelector(".page-nav");
  if (!nav) return;

  const index = pages.findIndex((page) => page.slug === getCurrentPage().slug);
  const prevPage = pages[index - 1];
  const nextPage = pages[index + 1];

  nav.innerHTML = `
    ${prevPage ? `<a class="page-nav__prev" href="${buildRelativeHref(prevPage.path)}">← ${prevPage.title}</a>` : "<span></span>"}
    ${nextPage ? `<a class="page-nav__next" href="${buildRelativeHref(nextPage.path)}">${nextPage.title} →</a>` : "<span></span>"}
  `;
}

function buildHeader() {
  const header = document.getElementById("site-header");
  if (!header) return;

  header.innerHTML = `
    <div class="site-header__inner">
      <div class="site-actions">
        <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Open navigation">Menu</button>
      </div>
      <a class="brand" href="${buildRelativeHref("index.html")}" aria-label="wizardgram home">
        <span class="brand-mark">✦</span>
        <span>wizardgram</span>
      </a>
      <div class="site-actions">
        <a class="top-link" href="https://github.com/daddymaou/wizardgram" target="_blank" rel="noreferrer">GitHub</a>
        <a class="top-link" href="https://pypi.org/project/wizardgram/" target="_blank" rel="noreferrer">PyPI</a>
        <button class="search-button icon-button" type="button" aria-label="Search the docs">Search</button>
        <button class="theme-toggle icon-button" type="button" aria-label="Toggle light and dark theme">
          <span class="theme-toggle__sun">Light</span>
          <span class="theme-toggle__moon">Dark</span>
        </button>
      </div>
    </div>
  `;

  const searchButton = header.querySelector(".search-button");
  if (searchButton) {
    searchButton.addEventListener("click", () => {
      const event = new KeyboardEvent("keydown", { key: "/" });
      document.dispatchEvent(event);
    });
  }
}

function buildFooter() {
  const footer = document.getElementById("site-footer");
  if (!footer) return;

  footer.innerHTML = `
    <div class="site-footer__inner">
      <p>wizardgram is an async Telegram bot framework for Python.</p>
      <p><a href="https://github.com/daddymaou/wizardgram/blob/main/LICENSE">Apache-2.0</a> • <a href="https://github.com/daddymaou/wizardgram/blob/main/CONTRIBUTING.md">Contributing</a></p>
    </div>
  `;
}

function initNavigation() {
  buildHeader();
  buildSidebar();
  buildPageToc();
  buildPrevNext();
  buildFooter();
}

export { initNavigation };
