import { initNavigation } from "./nav.js";
import { initCopyButtons } from "./copy.js";
import "./theme.js";
import "./search.js";

document.addEventListener("DOMContentLoaded", () => {
  initNavigation();
  initCopyButtons();

  const searchButton = document.querySelector(".search-button");
  if (searchButton) {
    searchButton.addEventListener("click", () => {
      const event = new KeyboardEvent("keydown", { key: "/" });
      document.dispatchEvent(event);
    });
  }

  const navToggle = document.querySelector(".nav-toggle");
  const sidebar = document.getElementById("sidebar");
  if (navToggle && sidebar) {
    navToggle.addEventListener("click", () => {
      sidebar.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(sidebar.classList.contains("is-open")));
    });
  }

  const pageLinks = document.querySelectorAll(".page-toc a");
  pageLinks.forEach((link) => {
    link.addEventListener("click", () => {
      pageLinks.forEach((item) => item.classList.remove("is-active"));
      link.classList.add("is-active");
    });
  });
});
