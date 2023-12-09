document.addEventListener("DOMContentLoaded", function() {
  const expand_btn = document.querySelector(".expand-btn");
  if (expand_btn) {
    expand_btn.addEventListener("click", () => {
      document.body.classList.toggle("collapsed");
    });
  } else {
    console.error("Elemento .expand-btn não encontrado.");
  }
});

let activeIndex;

const current = window.location.href;

const allLinks = document.querySelectorAll(".sidebar-links a");

allLinks.forEach((elem) => {
  elem.addEventListener("click", function () {
    const hrefLinkClick = elem.href;

    allLinks.forEach((link) => {
      if (link.href == hrefLinkClick) {
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  });
});

const searchInput = document.querySelector(".search__wrapper input");

searchInput.addEventListener("focus", (e) => {
  document.body.classList.remove("collapsed");
});