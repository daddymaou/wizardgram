const THEME_KEY = "wizardgram-theme";

function getPreferredTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "light" || saved === "dark") {
      return saved;
    }
  } catch (error) {
    // ignored: localStorage may be unavailable.
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
}

function initTheme() {
  const theme = getPreferredTheme();
  applyTheme(theme);

  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;

    const setButtonState = (value) => {
      const label = toggle.querySelector("span");
      if (label) {
        label.textContent = value === "dark" ? "Dark" : "Light";
      }
    };

    setButtonState(theme);

    toggle.addEventListener("click", () => {
      const nextTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
      setButtonState(nextTheme);

      try {
        localStorage.setItem(THEME_KEY, nextTheme);
      } catch (error) {
        // ignored: storage may be blocked.
      }
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTheme);
} else {
  initTheme();
}

export { applyTheme, getPreferredTheme };
