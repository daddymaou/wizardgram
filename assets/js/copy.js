function escapeHtml(input) {
  return input
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;");
}

function syntaxHighlight(code, language) {
  const text = escapeHtml(code);

  if (language === "python") {
    return text
      .replace(/(#.*$)/gm, '<span class="token-comment">$1</span>')
      .replace(/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/g, '<span class="token-string">$1</span>')
      .replace(/(^|\s)(async|await|import|from|def|class|return|if|else|elif|for|while|with|as|True|False|None|in|not|and|or|try|except|finally|pass|raise|lambda)(?=\s|$)/g, '$1<span class="token-keyword">$2</span>')
      .replace(/(^|\s)(@\w+)/g, '$1<span class="token-decorator">$2</span>')
      .replace(/\b(\d+)\b/g, '<span class="token-number">$1</span>');
  }

  if (language === "bash" || language === "shell") {
    return text
      .replace(/(#.*$)/gm, '<span class="token-comment">$1</span>')
      .replace(/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/g, '<span class="token-string">$1</span>')
      .replace(/(^|\s)(pip|install|python|uvicorn|export|set|WIZARDGRAM_TOKEN|bot|ctx|await|from|import|cd)(?=\s|$)/g, '$1<span class="token-keyword">$2</span>');
  }

  return text;
}

function initCopyButtons() {
  document.querySelectorAll("pre code").forEach((block) => {
    if (block.parentElement && block.parentElement.querySelector(".copy-button")) {
      return;
    }

    const language = block.dataset.lang || block.className.replace("language-", "") || "text";
    const content = block.textContent || "";
    const wrapper = block.parentElement;

    if (!wrapper || wrapper.classList.contains("code-block")) {
      return;
    }

    const codeBlock = document.createElement("div");
    codeBlock.className = "code-block";

    const header = document.createElement("div");
    header.className = "code-block__header";
    const lang = document.createElement("span");
    lang.className = "code-block__lang";
    lang.textContent = language;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.setAttribute("aria-label", "Copy code block");
    button.textContent = "Copy";

    const highlighted = document.createElement("code");
    highlighted.innerHTML = syntaxHighlight(content, language);
    highlighted.dataset.lang = language;

    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(content);
        button.textContent = "Copied";
        button.classList.add("copied");
        window.setTimeout(() => {
          button.textContent = "Copy";
          button.classList.remove("copied");
        }, 1200);
      } catch (error) {
        button.textContent = "Copy failed";
      }
    });

    header.appendChild(lang);
    header.appendChild(button);
    codeBlock.appendChild(header);
    codeBlock.appendChild(highlighted);
    wrapper.replaceWith(codeBlock);
  });
}

export { initCopyButtons };
