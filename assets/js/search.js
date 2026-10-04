import { pages } from "./pages.js";

const overlay = document.createElement("div");
overlay.className = "search-overlay";
overlay.setAttribute("aria-hidden", "true");
overlay.innerHTML = `
  <div class="search-panel" role="dialog" aria-modal="true" aria-label="Search documentation">
    <label class="sr-only" for="doc-search">Search docs</label>
    <input id="doc-search" class="search-input" type="search" placeholder="Search docs…" />
    <div class="search-results" id="search-results"></div>
  </div>
`;
document.body.appendChild(overlay);

const input = overlay.querySelector("#doc-search");
const resultsBox = overlay.querySelector("#search-results");

function normalize(value) {
  return (value || "").toLowerCase().trim();
}

function getResults(query) {
  const searchTerm = normalize(query);

  if (!searchTerm) {
    return pages.map((page) => ({
      page,
      matches: [page.summary]
    }));
  }

  return pages
    .map((page) => {
      const haystack = [page.title, page.summary, ...(page.headings || [])].join(" ").toLowerCase();
      const match = haystack.includes(searchTerm);
      return match ? { page, matches: page.headings.filter((heading) => heading.toLowerCase().includes(searchTerm)) } : null;
    })
    .filter(Boolean);
}

function renderResults(query) {
  const hits = getResults(query);

  if (!hits.length) {
    resultsBox.innerHTML = '<div class="empty-state">No matches yet. Try “install”, “keyboard”, or “webhook”.</div>';
    return;
  }

  const groups = [];
  for (const { page, matches } of hits) {
    const group = document.createElement("div");
    group.className = "search-group";
    const title = document.createElement("h3");
    title.textContent = page.group;
    group.appendChild(title);

    const result = document.createElement("a");
    result.className = "search-result";
    result.href = page.path;
    result.innerHTML = `<strong>${page.title}</strong><small>${matches.join(" • ") || page.summary}</small>`;
    group.appendChild(result);

    groups.push(group);
  }

  resultsBox.innerHTML = "";
  groups.forEach((group) => resultsBox.appendChild(group));
}

function openSearch() {
  overlay.classList.add("is-open");
  overlay.setAttribute("aria-hidden", "false");
  input.value = "";
  renderResults("");
  input.focus();
}

function closeSearch() {
  overlay.classList.remove("is-open");
  overlay.setAttribute("aria-hidden", "true");
}

input.addEventListener("input", (event) => renderResults(event.target.value));

overlay.addEventListener("click", (event) => {
  if (event.target === overlay) {
    closeSearch();
  }
});

document.addEventListener("keydown", (event) => {
  const isSlash = event.key === "/" && !event.shiftKey && !event.ctrlKey && !event.metaKey && !event.altKey;
  const isShortcut = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k";

  if (isSlash || isShortcut) {
    event.preventDefault();
    openSearch();
  }

  if (event.key === "Escape" && overlay.classList.contains("is-open")) {
    closeSearch();
  }
});

renderResults("");

export { openSearch, closeSearch };
