(() => {
  "use strict";

  const elements = {
    // Top Views
    landingPage: document.getElementById("landing-page"),
    workspaceView: document.getElementById("workspace-view"),

    // Landing Page Navigation & CTAs
    btnCornerTry: document.getElementById("btn-corner-try"),
    landingBtnSignin: document.getElementById("landing-btn-signin"),
    landingBtnSignup: document.getElementById("landing-btn-signup"),
    btnHeroLaunch: document.getElementById("btn-hero-launch"),
    btnHeroSignup: document.getElementById("btn-hero-signup"),
    btnReplaySim: document.getElementById("btn-replay-sim"),
    btnSimTry: document.getElementById("btn-sim-try"),
    btnBottomTry: document.getElementById("btn-bottom-try"),

    // Workspace Navigation & Topbar
    btnNavHome: document.getElementById("btn-nav-home"),
    brandLinkWorkspace: document.getElementById("brand-link-workspace"),
    activeName: document.getElementById("active-document-name"),
    chatScroll: document.getElementById("chat-scroll"),
    characterCount: document.getElementById("character-count"),
    chatToolsBar: document.getElementById("chat-tools-bar"),
    composer: document.getElementById("composer"),
    btnComposerUpload: document.getElementById("btn-composer-upload"),
    documentList: document.getElementById("document-list"),
    documentTotal: document.getElementById("document-total"),
    fileInput: document.getElementById("file-input"),
    libraryCount: document.getElementById("library-count"),
    libraryEmpty: document.getElementById("library-empty"),
    messageList: document.getElementById("message-list"),
    mobileOverlay: document.getElementById("mobile-overlay"),
    mobileSidebarToggle: document.getElementById("mobile-sidebar-toggle"),
    newChatButton: document.getElementById("new-chat-button"),
    promptGrid: document.getElementById("prompt-grid"),
    questionInput: document.getElementById("question-input"),
    readyPill: document.getElementById("ready-pill"),
    recentChatList: document.getElementById("recent-chat-list"),
    recentChatTotal: document.getElementById("recent-chat-total"),
    recentEmpty: document.getElementById("recent-empty"),
    sendButton: document.getElementById("send-button"),
    sidebar: document.getElementById("sidebar"),
    sidebarClose: document.getElementById("sidebar-close"),
    toastRegion: document.getElementById("toast-region"),
    uploadProgress: document.getElementById("upload-progress"),
    uploadProgressLabel: document.getElementById("upload-progress-label"),
    uploadZone: document.getElementById("upload-zone"),
    uploadZoneTitle: document.getElementById("upload-zone-title"),
    uploadZoneSubtitle: document.getElementById("upload-zone-subtitle"),
    uploadZoneMeta: document.getElementById("upload-zone-meta"),
    welcomeState: document.getElementById("welcome-state"),
    welcomeUploadBtn: document.getElementById("welcome-upload-btn"),

    // Metadata & Productivity Badges
    docMetadataBadge: document.getElementById("doc-metadata-badge"),
    docPageBadge: document.getElementById("doc-page-badge"),
    docChunkBadge: document.getElementById("doc-chunk-badge"),
    btnExportChat: document.getElementById("btn-export-chat"),
    barBtnExportPdf: document.getElementById("bar-btn-export-pdf"),
    barBtnExportWord: document.getElementById("bar-btn-export-word"),
    dropdownBtnHome: document.getElementById("dropdown-btn-home"),
    documentSearchInput: document.getElementById("document-search-input"),
    clearSearchBtn: document.getElementById("clear-search-btn"),
    sidebarBtnNewChat: document.getElementById("sidebar-btn-new-chat"),
    sidebarDocCard: document.getElementById("sidebar-doc-card"),
    sidebarDocTitle: document.getElementById("sidebar-doc-title"),
    sidebarDocMeta: document.getElementById("sidebar-doc-meta"),
    sidebarExportPdf: document.getElementById("sidebar-export-pdf"),
    sidebarExportWord: document.getElementById("sidebar-export-word"),
    sidebarFooterHome: document.getElementById("sidebar-footer-home"),

    // Landing Header & Mobile Hamburger Navigation
    landingHamburgerBtn: document.getElementById("landing-hamburger-btn"),
    landingMobileNav: document.getElementById("landing-mobile-nav"),
    landingMobileSignin: document.getElementById("landing-mobile-signin"),

    // Export Modal Bottom Sheet
    exportModalBackdrop: document.getElementById("export-modal-backdrop"),
    exportModalSheet: document.getElementById("export-modal-sheet"),
    modalExportPdf: document.getElementById("modal-export-pdf"),
    modalExportWord: document.getElementById("modal-export-word"),
    btnCloseExportModal: document.getElementById("btn-close-export-modal"),
    btnCancelExportModal: document.getElementById("btn-cancel-export-modal"),

    // Wisdom Topbar Ticker Elements
    topbarWisdomTicker: document.getElementById("topbar-wisdom-ticker"),
    topbarWisdomText: document.getElementById("topbar-wisdom-text"),
    topbarWisdomNext: document.getElementById("topbar-wisdom-next"),

    // Auth & User Profile Elements
    authLoggedOut: document.getElementById("auth-logged-out"),
    authLoggedIn: document.getElementById("auth-logged-in"),
    btnOpenSignin: document.getElementById("btn-open-signin"),
    btnOpenSignup: document.getElementById("btn-open-signup"),
    authModalBackdrop: document.getElementById("auth-modal-backdrop"),
    authModalCard: document.getElementById("auth-modal-card"),
    btnCloseAuthModal: document.getElementById("btn-close-auth-modal"),
    authModalTitle: document.getElementById("auth-modal-title"),
    authModalSubtitle: document.getElementById("auth-modal-subtitle"),
    authForm: document.getElementById("auth-form"),
    groupFullName: document.getElementById("group-fullname"),
    authFullName: document.getElementById("auth-fullname"),
    authEmail: document.getElementById("auth-email"),
    authPassword: document.getElementById("auth-password"),
    btnTogglePwd: document.getElementById("btn-toggle-pwd"),
    googleSigninButton: document.getElementById("google-signin-button"),
    googleAuthStatus: document.getElementById("google-auth-status"),
    passwordHint: document.getElementById("password-hint"),
    authErrorMsg: document.getElementById("auth-error-msg"),
    btnAuthSubmit: document.getElementById("btn-auth-submit"),
    authSubmitText: document.getElementById("auth-submit-text"),
    authSwitchPrompt: document.getElementById("auth-switch-prompt"),
    btnSwitchAuthMode: document.getElementById("btn-switch-auth-mode"),
    userPill: document.getElementById("user-pill"),
    userAvatarBadge: document.getElementById("user-avatar-badge"),
    userPillName: document.getElementById("user-pill-name"),
    userDropdown: document.getElementById("user-dropdown"),
    dropdownAvatar: document.getElementById("dropdown-avatar"),
    dropdownUserName: document.getElementById("dropdown-user-name"),
    dropdownUserEmail: document.getElementById("dropdown-user-email"),
    btnLogout: document.getElementById("btn-logout"),

    // 3D Simulation Elements
    simDocCard: document.getElementById("sim-doc-card"),
    simCoreContainer: document.getElementById("sim-core-container"),
    simScanStatusText: document.getElementById("sim-scan-status-text"),
    simResultCard: document.getElementById("sim-result-card"),
    simResultText: document.getElementById("sim-result-text"),
    btnReplaySim: document.getElementById("btn-replay-sim"),
    btnSimTry: document.getElementById("btn-sim-try"),
  };

  const state = {
    activeView: "landing",
    documents: [],
    chats: [],
    selectedId: null,
    chatId: null,
    history: [],
    busy: false,
    uploading: false,
    currentUser: null,
    authToken: null,
    authMode: "signup", // Streamlined: default to sign up
    googleClientId: null,
    googleInitialized: false,
    googleScriptPromise: null,
    googleButtonRendered: false,
    wisdomIndex: 0,
    searchQuery: "",
    simTimer: null,
    simInterval: null,
    simPaused: false,
    simTime: 0,
  };

  const themeStorageKey = "documind-theme";
  const activeChatStorageKey = "documind-active-chat";
  const authTokenStorageKey = "documind-auth-token";
  const authUserStorageKey = "documind-auth-user";

  // High-Impact Research Value & Principles (100% English)
  const wisdomQuotes = [
    {
      text: "Transform Any PDF into Deep Intelligence. Instant answers, exact citations & fast research.",
      sub: "Turn complex textbooks, research papers, and technical reports into instant breakthrough clarity.",
    },
    {
      text: "Read 10x faster: Turn complex textbooks, research papers, and reports into instant answers.",
      sub: "Pinpoint crucial signals, uncover buried patterns, and synthesize deep knowledge effortlessly.",
    },
    {
      text: "Zero guesswork: Every single answer is grounded in document facts with exact page citations.",
      sub: "No hallucinations, no assumptions — pure document evidence delivered with precision.",
    },
    {
      text: "Seek knowledge with unwavering integrity — truth is the supreme hallmark of intelligence.",
      sub: "Rigorous source grounding and ethical clarity illuminate every genuine breakthrough.",
    },
    {
      text: "Your private AI research vault: Documents are indexed securely in isolated local storage.",
      sub: "Confidentiality and workspace privacy are strictly respected by design.",
    },
    {
      text: "Uncover critical dates, numerical metrics, and executive summaries at the speed of thought.",
      sub: "Transform passive document reading into an active, intelligent conversation.",
    },
  ];

  const fileIcon = `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 3.75h6.2L18 8.6v11.65H7V3.75Z"></path>
      <path d="M13 4v5h4.8M9.5 13h6M9.5 16h6"></path>
    </svg>`;
  const deleteIcon = `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 7h16M10 11v6m4-6v6M5.5 7l1 13h11l1-13M9 7V4h6v3"></path>
    </svg>`;
  const chatIcon = `
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H7l-3 2v-5.2A7.5 7.5 0 1 1 20 11.5Z"></path>
      <path d="M8 11h8M8 14.5h5"></path>
    </svg>`;
  const checkIcon = `
    <svg viewBox="0 0 18 18" aria-hidden="true">
      <path d="m3.5 9 3.4 3.4 7.6-7.2"></path>
    </svg>`;
  const sourceIcon = `
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <path d="M4 2.5h5l3 3v8H4v-11Z"></path>
      <path d="M9 2.7v3h2.8"></path>
    </svg>`;
  const moreIcon = `
    <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16" aria-hidden="true">
      <circle cx="4" cy="10" r="1.8"/>
      <circle cx="10" cy="10" r="1.8"/>
      <circle cx="16" cy="10" r="1.8"/>
    </svg>`;

  const pinnedDocsStorageKey = "documind-pinned-docs";
  const pinnedChatsStorageKey = "documind-pinned-chats";

  function getPinnedDocIds() {
    try {
      return JSON.parse(localStorage.getItem(pinnedDocsStorageKey) || "[]");
    } catch {
      return [];
    }
  }

  function togglePinDoc(docId) {
    let pinned = getPinnedDocIds();
    if (pinned.includes(docId)) {
      pinned = pinned.filter((id) => id !== docId);
      showToast("Document unpinned.");
    } else {
      pinned.unshift(docId);
      showToast("Document pinned to top! 📌", "success");
    }
    try {
      localStorage.setItem(pinnedDocsStorageKey, JSON.stringify(pinned));
    } catch {}
    renderDocuments();
  }

  function getPinnedChatIds() {
    try {
      return JSON.parse(localStorage.getItem(pinnedChatsStorageKey) || "[]");
    } catch {
      return [];
    }
  }

  function togglePinChat(chatId) {
    let pinned = getPinnedChatIds();
    if (pinned.includes(chatId)) {
      pinned = pinned.filter((id) => id !== chatId);
      showToast("Chat unpinned.");
    } else {
      pinned.unshift(chatId);
      showToast("Chat pinned to top! 📌", "success");
    }
    try {
      localStorage.setItem(pinnedChatsStorageKey, JSON.stringify(pinned));
    } catch {}
    renderChats();
  }

  function closeAllItemMenus() {
    document.querySelectorAll(".item-dropdown-menu").forEach((m) => m.remove());
  }

  function openItemMenu(event, options) {
    event.stopPropagation();
    closeAllItemMenus();
    const trigger = event.currentTarget;
    const parent = trigger.closest(".document-item, .recent-chat-item") || trigger.parentElement;
    if (!parent) return;

    if (window.getComputedStyle(parent).position === "static") {
      parent.style.position = "relative";
    }

    const menu = document.createElement("div");
    menu.className = "item-dropdown-menu";

    const rect = trigger.getBoundingClientRect();
    if (rect.bottom + 95 > window.innerHeight) {
      menu.style.bottom = "32px";
    } else {
      menu.style.top = "32px";
    }

    options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "item-menu-option";
      if (opt.danger) btn.classList.add("danger-option");

      const icon = document.createElement("span");
      icon.className = "menu-opt-icon";
      icon.textContent = opt.icon;

      const label = document.createElement("span");
      label.textContent = opt.label;

      btn.append(icon, label);
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        closeAllItemMenus();
        opt.action();
      });
      menu.appendChild(btn);
    });

    parent.appendChild(menu);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[character]);
  }

  // --- Theme Management ---
  function setTheme(theme, persist = true) {
    const selectedTheme = theme === "dark" ? "dark" : "light";
    document.documentElement.dataset.theme = selectedTheme;
    const isDark = selectedTheme === "dark";

    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.setAttribute("aria-label", `Switch to ${isDark ? "light" : "dark"} theme`);
      btn.title = `Switch to ${isDark ? "light" : "dark"} theme`;
    });

    document.querySelector('meta[name="theme-color"]')?.setAttribute(
      "content",
      isDark ? "#07090e" : "#f8fafc",
    );

    if (persist) {
      try {
        localStorage.setItem(themeStorageKey, selectedTheme);
      } catch {
        // Storage unavailable
      }
    }
  }

  // --- View Switcher (Landing Homepage vs Workspace App) ---
  function showView(viewName) {
    state.activeView = viewName;
    if (viewName === "workspace") {
      if (elements.landingPage) elements.landingPage.hidden = true;
      if (elements.workspaceView) elements.workspaceView.hidden = false;
      window.scrollTo({ top: 0, behavior: "smooth" });
      updateComposer();
    } else {
      if (elements.landingPage) elements.landingPage.hidden = false;
      if (elements.workspaceView) elements.workspaceView.hidden = true;
      window.scrollTo({ top: 0, behavior: "smooth" });
      startSimulationLoop();
    }
  }

  // --- Markdown Parser ---
  function safeInlineMarkdown(value) {
    let html = escapeHtml(value);
    html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
    html = html.replace(/\[([^\]]+)\]\((https:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    html = html.replace(/(^|[\s(])(https:\/\/[^\s<]+)/g, '$1<a href="$2" target="_blank" rel="noopener noreferrer">$2</a>');
    return html;
  }

  function renderMarkdown(markdown) {
    const lines = String(markdown).replace(/\r\n?/g, "\n").split("\n");
    const blocks = [];
    let paragraph = [];
    let list = [];
    let code = [];
    let inCode = false;

    function flushParagraph() {
      if (paragraph.length) {
        blocks.push(`<p>${paragraph.map(safeInlineMarkdown).join("<br>")}</p>`);
        paragraph = [];
      }
    }
    function flushList() {
      if (list.length) {
        blocks.push(`<ul>${list.map((item) => `<li>${safeInlineMarkdown(item)}</li>`).join("")}</ul>`);
        list = [];
      }
    }
    function flushCode() {
      if (code.length) {
        blocks.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
        code = [];
      }
    }

    for (const line of lines) {
      if (line.trim().startsWith("```")) {
        if (inCode) {
          flushCode();
          inCode = false;
        } else {
          flushParagraph();
          flushList();
          inCode = true;
        }
        continue;
      }
      if (inCode) {
        code.push(line);
        continue;
      }
      const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);
      if (headingMatch) {
        flushParagraph();
        flushList();
        const level = headingMatch[1].length;
        blocks.push(`<h${level}>${safeInlineMarkdown(headingMatch[2])}</h${level}>`);
        continue;
      }
      const listMatch = line.match(/^[-*]\s+(.*)$/);
      if (listMatch) {
        flushParagraph();
        list.push(listMatch[1]);
        continue;
      }
      if (line.trim() === "") {
        flushParagraph();
        flushList();
        continue;
      }
      flushList();
      paragraph.push(line);
    }
    flushParagraph();
    flushList();
    flushCode();
    return blocks.join("") || "<p></p>";
  }

  // --- Toast Notifications ---
  function showToast(message, kind = "info") {
    if (!elements.toastRegion) return;
    const toast = document.createElement("div");
    toast.className = `toast${kind === "error" ? " is-error" : kind === "success" ? " is-success" : ""}`;
    const icon = kind === "error" ? "!" : kind === "success" ? "✓" : "✳";
    const iconElement = document.createElement("span");
    iconElement.className = "toast-icon";
    iconElement.textContent = icon;
    const text = document.createElement("span");
    text.textContent = message;
    toast.append(iconElement, text);
    elements.toastRegion.append(toast);
    window.setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-5px)";
      window.setTimeout(() => toast.remove(), 220);
    }, 4200);
  }

  // --- API Client ---
  async function api(path, options = {}) {
    const headers = options.headers ? { ...options.headers } : {};
    let token = state.authToken;
    if (!token) {
      try {
        token = localStorage.getItem(authTokenStorageKey);
        if (token) state.authToken = token;
      } catch {}
    }
    if (token && !headers["Authorization"]) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    const response = await fetch(path, { ...options, headers, credentials: "include" });
    if (!response.ok) {
      let message = `Request failed (${response.status}).`;
      try {
        const payload = await response.json();
        if (typeof payload.detail === "string") message = payload.detail;
      } catch {
        // Fallback to generic message
      }
      throw new Error(message);
    }
    return response.status === 204 ? null : response.json();
  }

  // --- Wisdom Ticker System ---
  function renderWisdom(index = state.wisdomIndex) {
    const quote = wisdomQuotes[index % wisdomQuotes.length];
    if (!quote) return;
    state.wisdomIndex = index % wisdomQuotes.length;

    if (elements.topbarWisdomText) {
      elements.topbarWisdomText.style.opacity = "0";
      window.setTimeout(() => {
        elements.topbarWisdomText.textContent = quote.text;
        elements.topbarWisdomText.style.opacity = "1";
      }, 150);
    }
  }

  function cycleWisdom() {
    renderWisdom(state.wisdomIndex + 1);
  }

  // --- Authentication System ---
  function getInitials(name = "") {
    if (!name) return "US";
    const parts = name.trim().split(/\s+/);
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
  }

  function updateUploadZoneState() {
    if (!elements.uploadZone) return;
    const isGated = !state.currentUser;
    const hasActiveDocument = Boolean(state.selectedId && state.documents && state.documents.some((d) => d.id === state.selectedId));

    if (isGated) {
      elements.uploadZone.classList.add("upload-gated");
      elements.uploadZone.classList.remove("is-uploaded");
      if (elements.uploadZoneTitle) {
        elements.uploadZoneTitle.innerHTML = '<strong class="upload-highlight-badge">DRAG &amp; DROP PDF (SIGN IN)</strong>';
      }
      if (elements.uploadZoneSubtitle) {
        elements.uploadZoneSubtitle.innerHTML = '<span class="highlight-browse">Sign up free</span> with Gmail to analyze documents';
      }
      if (elements.welcomeUploadBtn) {
        elements.welcomeUploadBtn.classList.remove("is-uploaded");
        elements.welcomeUploadBtn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
          </svg>
          <span>Upload PDF Document</span>
        `;
        elements.welcomeUploadBtn.title = "Choose a PDF to analyze";
      }
      return;
    }

    elements.uploadZone.classList.remove("upload-gated");

    if (hasActiveDocument) {
      // Automatic Green state when file is uploaded and active
      elements.uploadZone.classList.add("is-uploaded");
      const activeDoc = state.documents.find((d) => d.id === state.selectedId) || state.documents[0];
      const docName = activeDoc ? activeDoc.filename : "PDF Document";
      const shortName = docName.length > 20 ? docName.substring(0, 18) + "…" : docName;
      if (elements.uploadZoneTitle) {
        elements.uploadZoneTitle.innerHTML = '<strong class="upload-highlight-badge">✓ PDF UPLOADED — READY</strong>';
      }
      if (elements.uploadZoneSubtitle) {
        elements.uploadZoneSubtitle.innerHTML = `Active: <strong style="color:var(--text-main); font-weight:700;">${escapeHtml(shortName)}</strong> · <span class="highlight-browse">add another</span>`;
      }
      if (elements.welcomeUploadBtn) {
        elements.welcomeUploadBtn.classList.add("is-uploaded");
        elements.welcomeUploadBtn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span>Uploaded ✓</span>
        `;
        elements.welcomeUploadBtn.title = "PDF uploaded & active! Click to upload or switch document.";
      }
    } else {
      // Red default state when awaiting file upload
      elements.uploadZone.classList.remove("is-uploaded");
      if (elements.uploadZoneTitle) {
        elements.uploadZoneTitle.innerHTML = '<strong class="upload-highlight-badge">DRAG &amp; DROP PDF HERE</strong>';
      }
      if (elements.uploadZoneSubtitle) {
        elements.uploadZoneSubtitle.innerHTML = 'or <span class="highlight-browse">click to browse</span> from device';
      }
      if (elements.welcomeUploadBtn) {
        elements.welcomeUploadBtn.classList.remove("is-uploaded");
        elements.welcomeUploadBtn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
          </svg>
          <span>Upload PDF Document</span>
        `;
        elements.welcomeUploadBtn.title = "Choose a PDF to analyze";
      }
    }
  }

  function updateAuthUI() {
    const user = state.currentUser;
    if (user) {
      if (elements.authLoggedOut) elements.authLoggedOut.hidden = true;
      if (elements.authLoggedIn) elements.authLoggedIn.hidden = false;
      const initials = getInitials(user.full_name || user.email);
      if (elements.userAvatarBadge) elements.userAvatarBadge.textContent = initials;
      if (elements.dropdownAvatar) elements.dropdownAvatar.textContent = initials;
      if (elements.userPillName) elements.userPillName.textContent = user.full_name || user.email.split("@")[0];
      if (elements.dropdownUserName) elements.dropdownUserName.textContent = user.full_name || "DocuMind Member";
      if (elements.dropdownUserEmail) elements.dropdownUserEmail.textContent = user.email;

      // Update Landing Header Button if user is logged in
      if (elements.landingBtnSignin) {
        elements.landingBtnSignin.textContent = "Open Workspace";
        elements.landingBtnSignin.title = `Signed in as ${user.email}`;
      }

      // Restore Active Upload Zone (Red or Green based on documents)
      updateUploadZoneState();
    } else {
      if (elements.authLoggedOut) elements.authLoggedOut.hidden = false;
      if (elements.authLoggedIn) elements.authLoggedIn.hidden = true;
      if (elements.userDropdown) elements.userDropdown.hidden = true;
      if (elements.dropdownUserEmail) elements.dropdownUserEmail.textContent = "";
      if (elements.dropdownUserName) elements.dropdownUserName.textContent = "";

      // Landing Header Button
      if (elements.landingBtnSignin) {
        elements.landingBtnSignin.textContent = "Sign In";
        elements.landingBtnSignin.title = "Sign in to your account";
      }

      // Enforce Upload Account Gate UI (Red)
      updateUploadZoneState();
    }
  }

  async function checkAuthSession() {
    let savedToken = null;
    let savedUser = null;
    try {
      savedToken = localStorage.getItem(authTokenStorageKey);
      const rawUser = localStorage.getItem(authUserStorageKey);
      if (rawUser) savedUser = JSON.parse(rawUser);
    } catch {
      // Storage unavailable
    }

    if (savedToken) {
      state.authToken = savedToken;
      if (savedUser) {
        state.currentUser = savedUser;
        updateAuthUI();
      }
    }

    try {
      const data = await api("/api/auth/me");
      if (data && data.authenticated && data.user) {
        state.currentUser = data.user;
        if (savedToken) state.authToken = savedToken;
        try {
          localStorage.setItem(authUserStorageKey, JSON.stringify(data.user));
          if (state.authToken) localStorage.setItem(authTokenStorageKey, state.authToken);
        } catch {}
      } else {
        // Only clear if backend explicitly says not authenticated
        state.currentUser = null;
        state.authToken = null;
        try {
          localStorage.removeItem(authTokenStorageKey);
          localStorage.removeItem(authUserStorageKey);
        } catch {}
      }
      updateAuthUI();
    } catch {
      // If network temporarily fails, keep local session so user is not logged out
    }
  }

  function openAuthModal(mode = "signup") {
    state.authMode = mode;
    if (elements.authErrorMsg) {
      elements.authErrorMsg.hidden = true;
      elements.authErrorMsg.textContent = "";
    }

    if (mode === "signup") {
      if (elements.authModalTitle) elements.authModalTitle.textContent = "Create Your Free Account";
      if (elements.authModalSubtitle) elements.authModalSubtitle.textContent = "Create an account to start analyzing PDFs";
      if (elements.groupFullName) elements.groupFullName.hidden = false;
      if (elements.passwordHint) elements.passwordHint.hidden = false;
      if (elements.authSubmitText) elements.authSubmitText.textContent = "🚀 Create Free Account";
      if (elements.authSwitchPrompt) elements.authSwitchPrompt.textContent = "Already have an account?";
      if (elements.btnSwitchAuthMode) elements.btnSwitchAuthMode.textContent = "Sign In";
    } else {
      if (elements.authModalTitle) elements.authModalTitle.textContent = "Welcome Back to DocuMind";
      if (elements.authModalSubtitle) elements.authModalSubtitle.textContent = "Sign in to access your saved documents & research";
      if (elements.groupFullName) elements.groupFullName.hidden = true;
      if (elements.passwordHint) elements.passwordHint.hidden = true;
      if (elements.authSubmitText) elements.authSubmitText.textContent = "⚡ Sign In";
      if (elements.authSwitchPrompt) elements.authSwitchPrompt.textContent = "Don't have an account yet?";
      if (elements.btnSwitchAuthMode) elements.btnSwitchAuthMode.textContent = "Sign Up Free";
    }

    if (elements.authModalBackdrop) elements.authModalBackdrop.hidden = false;
    initializeGoogleSignIn().catch((error) => {
      if (elements.googleAuthStatus) {
        elements.googleAuthStatus.textContent = error.message;
        elements.googleAuthStatus.hidden = false;
      }
    });
    if (elements.authEmail) elements.authEmail.focus();
  }

  function closeAuthModal() {
    if (elements.authModalBackdrop) elements.authModalBackdrop.hidden = true;
    if (elements.authErrorMsg) {
      elements.authErrorMsg.hidden = true;
      elements.authErrorMsg.textContent = "";
    }
  }

  async function activateAuthenticatedUser(data, fallbackMessage) {
    state.currentUser = data.user;
    state.authToken = data.token;
    try {
      if (data.token) localStorage.setItem(authTokenStorageKey, data.token);
      if (data.user) localStorage.setItem(authUserStorageKey, JSON.stringify(data.user));
    } catch (e) {
      console.warn("Could not persist session to localStorage", e);
    }
    updateAuthUI();
    closeAuthModal();
    showToast(data.message || fallbackMessage, "success");
    await loadDocuments();
    await loadChats(true);
    showView("workspace");
  }

  async function initializeGoogleSignIn() {
    if (!elements.googleSigninButton || !elements.googleAuthStatus) return;

    if (!state.googleClientId) {
      let config;
      try {
        config = await api("/api/auth/config");
      } catch (error) {
        elements.googleAuthStatus.textContent = `Google Sign-In configuration could not be loaded: ${error.message}`;
        elements.googleAuthStatus.hidden = false;
        return;
      }
      state.googleClientId = config.google_client_id;
    }
    if (!state.googleClientId) {
      elements.googleSigninButton.hidden = true;
      elements.googleAuthStatus.textContent = "Google Sign-In is not configured yet. Set GOOGLE_CLIENT_ID in the server environment.";
      elements.googleAuthStatus.hidden = false;
      return;
    }

    if (!window.google?.accounts?.id) {
      if (!state.googleScriptPromise) {
        state.googleScriptPromise = new Promise((resolve, reject) => {
          const script = document.createElement("script");
          script.src = "https://accounts.google.com/gsi/client";
          script.async = true;
          script.defer = true;
          script.onload = resolve;
          script.onerror = () => {
            state.googleScriptPromise = null;
            reject(new Error("Google Identity Services could not be loaded."));
          };
          document.head.append(script);
        });
      }
      await state.googleScriptPromise;
    }

    if (!window.google?.accounts?.id) {
      throw new Error("Google Identity Services did not initialize.");
    }
    if (!state.googleInitialized) {
      window.google.accounts.id.initialize({
        client_id: state.googleClientId,
        callback: async (response) => {
          try {
            const data = await api("/api/auth/google", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ credential: response.credential }),
            });
            await activateAuthenticatedUser(data, "Signed in with Google successfully.");
          } catch (error) {
            elements.authErrorMsg.textContent = error.message;
            elements.authErrorMsg.hidden = false;
          }
        },
      });
      state.googleInitialized = true;
    }
    if (!state.googleButtonRendered) {
      elements.googleSigninButton.replaceChildren();
      window.google.accounts.id.renderButton(elements.googleSigninButton, {
        type: "standard",
        theme: "outline",
        size: "large",
        text: "continue_with",
        shape: "rectangular",
        width: Math.min(360, elements.authModalCard?.clientWidth || 360),
      });
      state.googleButtonRendered = true;
    }
    elements.googleAuthStatus.hidden = true;
  }

  async function handleAuthSubmit(event) {
    event.preventDefault();
    if (elements.authErrorMsg) elements.authErrorMsg.hidden = true;

    const email = elements.authEmail?.value.trim() || "";
    const password = elements.authPassword?.value || "";
    const fullName = elements.authFullName?.value.trim() || "";

    if (!email || !password) {
      if (elements.authErrorMsg) {
        elements.authErrorMsg.textContent = "Please fill in all required fields.";
        elements.authErrorMsg.hidden = false;
      }
      return;
    }

    const isSignUp = state.authMode === "signup";
    const endpoint = isSignUp ? "/api/auth/register" : "/api/auth/login";
    const payload = isSignUp
      ? { email, password, full_name: fullName || email.split("@")[0] }
      : { email, password };

    try {
      const data = await api(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      await activateAuthenticatedUser(
        data,
        isSignUp ? "Account created successfully!" : "Signed in successfully!",
      );
    } catch (error) {
      if (elements.authErrorMsg) {
        if (error.message.includes("Account not found")) {
          elements.authErrorMsg.replaceChildren(document.createTextNode(`${error.message} `));
          const signupButton = document.createElement("button");
          signupButton.type = "button";
          signupButton.className = "inline-auth-action";
          signupButton.textContent = "Create an account";
          signupButton.addEventListener("click", () => openAuthModal("signup"));
          elements.authErrorMsg.append(signupButton);
        } else {
          elements.authErrorMsg.textContent = error.message;
        }
        elements.authErrorMsg.hidden = false;
      }
    }
  }

  async function logoutUser() {
    try {
      await api("/api/auth/logout", { method: "POST" });
    } catch {}
    state.currentUser = null;
    state.authToken = null;
    try {
      localStorage.removeItem(authTokenStorageKey);
      localStorage.removeItem(authUserStorageKey);
    } catch {}
    if (elements.userDropdown) elements.userDropdown.hidden = true;
    state.documents = [];
    state.chats = [];
    state.selectedId = null;
    state.chatId = null;
    state.history = [];
    renderDocuments();
    renderChats();
    clearConversation();
    updateAuthUI();
    showToast("You have been signed out.", "info");
    showView("landing");
  }

  // --- Export State Helper ---
  function setExportButtonsDisabled(disabled) {
    const hasHistory = state.history && state.history.length > 0;
    const isDisabled = disabled || !hasHistory || !state.selectedId;
    if (elements.btnExportChat) {
      elements.btnExportChat.disabled = isDisabled;
      elements.btnExportChat.classList.toggle("is-dimmed", isDisabled);
    }
    if (elements.barBtnExportPdf) {
      elements.barBtnExportPdf.disabled = isDisabled;
      elements.barBtnExportPdf.classList.toggle("is-dimmed", isDisabled);
    }
    if (elements.barBtnExportWord) {
      elements.barBtnExportWord.disabled = isDisabled;
      elements.barBtnExportWord.classList.toggle("is-dimmed", isDisabled);
    }
    if (elements.sidebarExportPdf) {
      elements.sidebarExportPdf.disabled = isDisabled;
      elements.sidebarExportPdf.classList.toggle("is-dimmed", isDisabled);
    }
    if (elements.sidebarExportWord) {
      elements.sidebarExportWord.disabled = isDisabled;
      elements.sidebarExportWord.classList.toggle("is-dimmed", isDisabled);
    }
  }

  // --- Export Modal Controller ---
  function openExportModal() {
    if (elements.exportModalBackdrop) {
      elements.exportModalBackdrop.hidden = false;
    }
  }

  function closeExportModal() {
    if (elements.exportModalBackdrop) {
      elements.exportModalBackdrop.hidden = true;
    }
  }

  // --- Document Selection & UI Updates ---
  function setSelectedDocument(documentId) {
    state.selectedId = documentId;
    const selected = state.documents.find((document) => document.id === documentId);
    if (elements.activeName) {
      elements.activeName.textContent = selected ? selected.filename : "No document selected";
    }
    if (elements.questionInput) {
      elements.questionInput.disabled = !selected || state.busy;
      elements.questionInput.placeholder = selected
        ? `Ask anything about ${selected.title || selected.filename}…`
        : "Choose a document to get started…";
    }
    elements.promptGrid?.querySelectorAll(".prompt-card").forEach((button) => {
      button.disabled = !selected || state.busy;
    });
    elements.chatToolsBar?.querySelectorAll(".chat-tool-btn").forEach((button) => {
      button.disabled = !selected || state.busy;
    });
    if (elements.sendButton) {
      elements.sendButton.disabled = !selected || state.busy || !elements.questionInput.value.trim();
    }

    setExportButtonsDisabled(!state.chatId || state.history.length === 0);

    if (selected && elements.docMetadataBadge) {
      elements.docMetadataBadge.hidden = false;
      if (elements.docPageBadge) {
        elements.docPageBadge.textContent = `${selected.page_count} ${selected.page_count === 1 ? "Page" : "Pages"}`;
      }
      if (elements.docChunkBadge) {
        elements.docChunkBadge.textContent = `${selected.chunk_count} Chunks`;
      }
    } else if (elements.docMetadataBadge) {
      elements.docMetadataBadge.hidden = true;
    }

    if (elements.sidebarDocCard) {
      if (selected) {
        elements.sidebarDocCard.hidden = false;
        if (elements.sidebarDocTitle) elements.sidebarDocTitle.textContent = selected.filename || selected.title;
        if (elements.sidebarDocMeta) {
          elements.sidebarDocMeta.textContent = `${selected.page_count || 1} Pages · ${selected.chunk_count || 0} Chunks Indexed`;
        }
      } else {
        elements.sidebarDocCard.hidden = true;
      }
    }

    // Dynamic Welcome State feedback for Current Document
    const welcomeTitle = document.getElementById("welcome-title-compact");
    const welcomeDesc = document.getElementById("welcome-desc-compact");
    if (welcomeDesc) {
      if (selected) {
        welcomeDesc.innerHTML = `Current document: <strong style="color:var(--accent-mint); font-weight:700;">${escapeHtml(selected.filename)}</strong> (${selected.page_count} ${selected.page_count === 1 ? "page" : "pages"})`;
      } else {
        welcomeDesc.textContent = "Select or upload a PDF document to begin.";
      }
    }
    if (welcomeTitle) {
      welcomeTitle.textContent = selected ? `Ready to analyze ${selected.filename}` : "Ready to analyze your PDF";
    }

    // Synchronize selection and Current Document badge in library list
    elements.documentList?.querySelectorAll(".document-item").forEach((item) => {
      const isCurrent = item.dataset.id === documentId;
      item.classList.toggle("is-selected", isCurrent);
      const docNameEl = item.querySelector(".document-name");
      const existingPill = docNameEl?.querySelector(".current-doc-pill");
      if (isCurrent && !existingPill && docNameEl) {
        const pill = document.createElement("span");
        pill.className = "current-doc-pill";
        pill.textContent = "Current";
        docNameEl.appendChild(pill);
      } else if (!isCurrent && existingPill) {
        existingPill.remove();
      }
    });

    updateUploadZoneState();
  }

  function renderDocuments() {
    if (!elements.documentList) return;
    elements.documentList.querySelectorAll(".document-item").forEach((item) => item.remove());
    const query = state.searchQuery.toLowerCase().trim();
    const documents = state.documents.filter((doc) => {
      if (!query) return true;
      return doc.filename.toLowerCase().includes(query) || doc.title.toLowerCase().includes(query);
    });

    const pinnedDocIds = getPinnedDocIds();
    // Sort pinned documents to top
    documents.sort((a, b) => {
      const aPinned = pinnedDocIds.includes(a.id);
      const bPinned = pinnedDocIds.includes(b.id);
      if (aPinned && !bPinned) return -1;
      if (!aPinned && bPinned) return 1;
      return 0;
    });

    if (elements.libraryEmpty) elements.libraryEmpty.hidden = documents.length > 0;
    if (elements.documentTotal) elements.documentTotal.textContent = String(state.documents.length);
    if (elements.libraryCount) elements.libraryCount.textContent = String(state.documents.length);

    documents.forEach((doc) => {
      const isPinned = pinnedDocIds.includes(doc.id);
      const isCurrent = doc.id === state.selectedId;

      const item = document.createElement("div");
      item.className = "document-item";
      if (isPinned) item.classList.add("is-pinned");
      if (isCurrent) item.classList.add("is-selected");
      item.dataset.id = doc.id;
      item.tabIndex = 0;
      item.setAttribute("role", "button");
      item.setAttribute("aria-label", `Select ${doc.filename}`);

      const icon = document.createElement("span");
      icon.className = "file-icon";
      icon.innerHTML = fileIcon;

      const copy = document.createElement("span");
      copy.className = "document-copy";
      const name = document.createElement("span");
      name.className = "document-name";
      name.textContent = doc.filename;
      name.title = doc.filename;

      if (isPinned) {
        const pinBadge = document.createElement("span");
        pinBadge.className = "pinned-indicator";
        pinBadge.textContent = "📌";
        pinBadge.title = "Pinned document";
        name.appendChild(pinBadge);
      }

      if (isCurrent) {
        const currentPill = document.createElement("span");
        currentPill.className = "current-doc-pill";
        currentPill.textContent = "Current";
        name.appendChild(currentPill);
      }

      const meta = document.createElement("span");
      meta.className = "document-meta";
      meta.textContent = `${doc.page_count} ${doc.page_count === 1 ? "page" : "pages"} · ${formatDate(doc.created_at)}`;
      copy.append(name, meta);

      const check = document.createElement("span");
      check.className = "document-check";
      check.innerHTML = checkIcon;

      // 3-dot More Options Button (Pin, Delete)
      const moreBtn = document.createElement("button");
      moreBtn.type = "button";
      moreBtn.className = "item-more-btn";
      moreBtn.setAttribute("aria-label", `Options for ${doc.filename}`);
      moreBtn.setAttribute("title", "Options (Pin, Delete)");
      moreBtn.innerHTML = moreIcon;
      moreBtn.addEventListener("click", (event) => {
        openItemMenu(event, [
          {
            icon: isPinned ? "📍" : "📌",
            label: isPinned ? "Unpin document" : "Pin to top",
            action: () => togglePinDoc(doc.id),
          },
          {
            icon: "🗑️",
            label: "Delete document",
            danger: true,
            action: () => deleteDocument(doc.id),
          },
        ]);
      });

      item.append(icon, copy, check, moreBtn);
      item.addEventListener("click", () => selectDocument(doc.id));
      item.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          selectDocument(doc.id);
        }
      });
      elements.documentList.append(item);
    });

    setSelectedDocument(state.selectedId);
  }

  function formatDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "recently added";
    return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" }).format(date);
  }

  async function loadDocuments() {
    try {
      const result = await api("/api/documents");
      state.documents = result.documents;
      if (!state.documents.some((document) => document.id === state.selectedId)) {
        state.selectedId = state.documents[0]?.id ?? null;
      }
      renderDocuments();
      if (state.selectedId) {
        setSelectedDocument(state.selectedId);
        const matchingChat = state.chats?.find((c) => c.document_id === state.selectedId);
        if (matchingChat && !state.chatId) {
          await openChat(matchingChat.id, false);
        }
      }
    } catch (error) {
      showToast(error.message, "error");
    }
  }

  function closeMobileSidebar() {
    if (elements.sidebar) elements.sidebar.classList.remove("is-open");
    if (elements.mobileOverlay) elements.mobileOverlay.classList.remove("is-visible");
  }

  function openMobileSidebar() {
    if (elements.sidebar) elements.sidebar.classList.add("is-open");
    if (elements.mobileOverlay) elements.mobileOverlay.classList.add("is-visible");
  }

  async function selectDocument(documentId) {
    if (state.busy || state.uploading) return;
    const changed = state.selectedId !== documentId;
    setSelectedDocument(documentId);

    // If an existing conversation exists for this document, resume it smoothly
    const matchingChat = state.chats.find((c) => c.document_id === documentId);
    if (matchingChat) {
      await openChat(matchingChat.id, true);
    } else {
      if (changed) clearConversation();
      closeMobileSidebar();
    }

    const doc = state.documents.find((d) => d.id === documentId);
    if (doc) {
      showToast(`“${doc.filename}” set as Current Document ✓`, "success");
    }
  }

  function clearConversation() {
    state.history = [];
    state.chatId = null;
    try {
      localStorage.removeItem(activeChatStorageKey);
    } catch {}
    if (elements.messageList) elements.messageList.replaceChildren();
    if (elements.welcomeState) elements.welcomeState.hidden = false;
    if (elements.chatScroll) elements.chatScroll.scrollTop = 0;
    setExportButtonsDisabled(true);
    renderChats();
  }

  function renderChats() {
    if (!elements.recentChatList) return;
    elements.recentChatList.querySelectorAll(".recent-chat-item").forEach((item) => item.remove());
    const pinnedChatIds = getPinnedChatIds();
    const conversations = [...state.chats].sort((a, b) => {
      const aPinned = pinnedChatIds.includes(a.id);
      const bPinned = pinnedChatIds.includes(b.id);
      if (aPinned && !bPinned) return -1;
      if (!aPinned && bPinned) return 1;
      return 0;
    });

    if (elements.recentChatTotal) elements.recentChatTotal.textContent = String(conversations.length);
    if (elements.recentEmpty) elements.recentEmpty.hidden = conversations.length > 0;

    conversations.forEach((conversation, index) => {
      const isPinned = pinnedChatIds.includes(conversation.id);
      const item = document.createElement("div");
      item.className = "recent-chat-item";
      if (isPinned) item.classList.add("is-pinned");
      item.dataset.id = conversation.id;
      item.classList.toggle("is-active", conversation.id === state.chatId);
      item.tabIndex = 0;
      item.setAttribute("role", "button");
      item.setAttribute("aria-label", `Open chat ${conversation.title}`);

      const glyph = document.createElement("span");
      glyph.className = "recent-chat-glyph";
      glyph.innerHTML = chatIcon;
      const copy = document.createElement("span");
      copy.className = "recent-chat-copy";
      const title = document.createElement("span");
      title.className = "recent-chat-title";
      title.textContent = conversation.title;
      title.title = conversation.title;

      if (isPinned) {
        const pinBadge = document.createElement("span");
        pinBadge.className = "pinned-indicator";
        pinBadge.textContent = "📌";
        pinBadge.title = "Pinned chat";
        title.appendChild(pinBadge);
      }

      const meta = document.createElement("span");
      meta.className = "recent-chat-meta";
      meta.textContent = `${conversation.document_filename} · ${formatDate(conversation.updated_at)}`;
      copy.append(title, meta);

      // 3-dot More Options Button (Pin, Delete)
      const moreBtn = document.createElement("button");
      moreBtn.type = "button";
      moreBtn.className = "item-more-btn";
      moreBtn.setAttribute("aria-label", `Options for ${conversation.title}`);
      moreBtn.setAttribute("title", "Options (Pin, Delete)");
      moreBtn.innerHTML = moreIcon;
      moreBtn.addEventListener("click", (event) => {
        openItemMenu(event, [
          {
            icon: isPinned ? "📍" : "📌",
            label: isPinned ? "Unpin chat" : "Pin chat to top",
            action: () => togglePinChat(conversation.id),
          },
          {
            icon: "🗑️",
            label: "Delete chat",
            danger: true,
            action: () => deleteChat(conversation.id),
          },
        ]);
      });

      item.append(glyph, copy, moreBtn);
      item.addEventListener("click", () => openChat(conversation.id));
      item.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openChat(conversation.id);
        }
      });
      item.style.animationDelay = `${Math.min(index, 8) * 25}ms`;
      elements.recentChatList.append(item);
    });
  }

  async function loadChats(restoreLastChat = false) {
    try {
      const result = await api("/api/chats");
      state.chats = result.conversations;
      renderChats();
      if (restoreLastChat) {
        let lastChatId = null;
        try {
          lastChatId = localStorage.getItem(activeChatStorageKey);
        } catch {}
        if (lastChatId && state.chats.some((conversation) => conversation.id === lastChatId)) {
          await openChat(lastChatId, false);
        } else if (state.selectedId) {
          const matchingChat = state.chats.find((conversation) => conversation.document_id === state.selectedId);
          if (matchingChat) await openChat(matchingChat.id, false);
        }
      }
    } catch (error) {
      showToast(`Couldn't load recent chats: ${error.message}`, "error");
    }
  }

  async function createChat() {
    // Starting a new chat requires uploading a new PDF document per user request
    state.selectedId = null;
    state.chatId = null;
    state.history = [];
    try {
      localStorage.removeItem(activeChatStorageKey);
    } catch {}

    if (elements.messageList) elements.messageList.replaceChildren();
    if (elements.welcomeState) elements.welcomeState.hidden = false;
    if (elements.chatScroll) elements.chatScroll.scrollTop = 0;

    if (elements.activeName) elements.activeName.textContent = "No document selected";
    if (elements.sidebarDocCard) elements.sidebarDocCard.hidden = true;
    if (elements.docMetadataBadge) elements.docMetadataBadge.hidden = true;

    const welcomeTitle = document.getElementById("welcome-title-compact");
    const welcomeDesc = document.getElementById("welcome-desc-compact");
    if (welcomeTitle) welcomeTitle.textContent = "Start New Chat — Upload PDF";
    if (welcomeDesc) welcomeDesc.textContent = "Please upload a new PDF document to begin this fresh chat session.";

    elements.documentList?.querySelectorAll(".document-item").forEach((item) => {
      item.classList.remove("is-selected");
      item.querySelector(".current-doc-pill")?.remove();
    });

    updateUploadZoneState();

    if (elements.questionInput) {
      elements.questionInput.disabled = true;
      elements.questionInput.placeholder = "Upload a PDF document to begin new chat…";
    }
    elements.promptGrid?.querySelectorAll(".prompt-card").forEach((b) => (b.disabled = true));
    elements.chatToolsBar?.querySelectorAll(".chat-tool-btn").forEach((b) => (b.disabled = true));
    if (elements.sendButton) elements.sendButton.disabled = true;
    setExportButtonsDisabled(true);

    closeMobileSidebar();
    showToast("Please upload a PDF document for this new chat.", "info");
    handlePdfUploadTrigger();
  }

  async function openChat(chatId, closeSidebar = true) {
    if (state.busy || state.uploading) return;
    try {
      const conversation = await api(`/api/chats/${encodeURIComponent(chatId)}`);
      if (!state.documents.some((document) => document.id === conversation.document_id)) {
        showToast("The document for this chat is no longer in your library.", "error");
        await loadChats();
        return;
      }
      state.chatId = conversation.id;
      state.selectedId = conversation.document_id;
      state.history = conversation.messages.map(({ role, content, sources }) => ({ role, content, sources: sources || [] }));
      if (elements.messageList) elements.messageList.replaceChildren();
      if (elements.welcomeState) elements.welcomeState.hidden = conversation.messages.length > 0;
      conversation.messages.forEach((message) => {
        addMessage(message.role, message.content, message.sources, message.created_at);
      });
      if (conversation.messages.length === 0 && elements.welcomeState) elements.welcomeState.hidden = false;
      setSelectedDocument(state.selectedId);
      setExportButtonsDisabled(state.history.length === 0);
      renderDocuments();
      renderChats();
      if (closeSidebar) closeMobileSidebar();
      try {
        localStorage.setItem(activeChatStorageKey, conversation.id);
      } catch {}
      if (elements.chatScroll) elements.chatScroll.scrollTop = elements.chatScroll.scrollHeight;
    } catch (error) {
      showToast(`Couldn't open this chat: ${error.message}`, "error");
    }
  }

  async function deleteChat(chatId) {
    if (state.busy) return;
    try {
      await api(`/api/chats/${encodeURIComponent(chatId)}`, { method: "DELETE" });
      state.chats = state.chats.filter((conversation) => conversation.id !== chatId);
      if (state.chatId === chatId) {
        state.chatId = null;
        state.history = [];
        if (elements.messageList) elements.messageList.replaceChildren();
        if (elements.welcomeState) elements.welcomeState.hidden = false;
        setExportButtonsDisabled(true);
        try {
          localStorage.removeItem(activeChatStorageKey);
        } catch {}
      }
      renderChats();
      showToast("Chat deleted.", "success");
    } catch (error) {
      showToast(`Couldn't delete this chat: ${error.message}`, "error");
    }
  }

  // --- Strict Upload Gate Enforcement ---
  async function uploadFile(file) {
    // 1. Account Gate Check
    if (!state.currentUser) {
      showToast("Account required: Please create a free account to upload PDF documents.", "error");
      openAuthModal("signup");
      return;
    }

    if (state.uploading) return;
    if (!file || (!file.name.toLowerCase().endsWith(".pdf") && file.type !== "application/pdf")) {
      showToast("Choose a PDF file to upload.", "error");
      return;
    }

    state.uploading = true;
    elements.uploadZone?.classList.add("is-uploading");
    if (elements.fileInput) elements.fileInput.disabled = true;
    if (elements.uploadProgress) elements.uploadProgress.hidden = false;
    if (elements.uploadProgressLabel) elements.uploadProgressLabel.textContent = "Reading and indexing your PDF…";

    const form = new FormData();
    form.append("file", file);
    try {
      const document = await api("/api/documents", { method: "POST", body: form });
      state.documents.unshift(document);
      state.selectedId = document.id;

      // Automatically create a new conversation for this new PDF
      try {
        const conversation = await api("/api/chats", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ document_id: document.id }),
        });
        state.chats.unshift(conversation);
        state.chatId = conversation.id;
        try {
          localStorage.setItem(activeChatStorageKey, state.chatId);
        } catch {}
      } catch {}

      state.history = [];
      if (elements.messageList) elements.messageList.replaceChildren();
      if (elements.welcomeState) elements.welcomeState.hidden = false;
      renderDocuments();
      setSelectedDocument(document.id);
      updateUploadZoneState();
      if (elements.uploadZone) {
        elements.uploadZone.classList.add("upload-just-success");
        window.setTimeout(() => {
          elements.uploadZone?.classList.remove("upload-just-success");
        }, 1200);
      }
      showToast(`“${document.filename}” uploaded & ready for chat! ✓`, "success");
      if (elements.uploadProgressLabel) elements.uploadProgressLabel.textContent = "Your document is ready.";
      elements.questionInput?.focus();
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      state.uploading = false;
      elements.uploadZone?.classList.remove("is-uploading");
      if (elements.fileInput) {
        elements.fileInput.disabled = false;
        elements.fileInput.value = "";
      }
      window.setTimeout(() => {
        if (elements.uploadProgress) elements.uploadProgress.hidden = true;
      }, 850);
    }
  }

  async function deleteDocument(documentId) {
    if (state.busy || state.uploading) return;
    const document = state.documents.find((item) => item.id === documentId);
    if (!document) return;
    try {
      await api(`/api/documents/${encodeURIComponent(documentId)}`, { method: "DELETE" });
      state.documents = state.documents.filter((item) => item.id !== documentId);
      const removedChatIds = new Set(
        state.chats
          .filter((conversation) => conversation.document_id === documentId)
          .map((conversation) => conversation.id),
      );
      state.chats = state.chats.filter((conversation) => conversation.document_id !== documentId);
      if (removedChatIds.has(state.chatId)) clearConversation();
      if (state.selectedId === documentId) {
        state.selectedId = state.documents[0]?.id ?? null;
        clearConversation();
      }
      renderDocuments();
      showToast("Document removed from your library.", "success");
    } catch (error) {
      showToast(error.message, "error");
    }
  }

  // --- High-Performance Text-to-Speech (TTS) Controller ---
  const speechController = {
    activeSpeechBtn: null,
    activePauseBtn: null,
    activeStopBtn: null,
    isPaused: false,

    stop() {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      this.isPaused = false;
      window.__documindSpeech = null;
      this.resetUI();
    },

    resetUI() {
      if (this.activeSpeechBtn) {
        this.activeSpeechBtn.classList.remove("is-playing", "is-paused");
        this.activeSpeechBtn.innerHTML = "<span>🔊 Listen</span>";
        this.activeSpeechBtn.title = "Read aloud (Audio TTS)";
      }
      if (this.activePauseBtn) {
        this.activePauseBtn.hidden = true;
        this.activePauseBtn.classList.remove("is-paused");
        this.activePauseBtn.innerHTML = "<span>⏸ Pause</span>";
      }
      if (this.activeStopBtn) {
        this.activeStopBtn.hidden = true;
      }
      this.activeSpeechBtn = null;
      this.activePauseBtn = null;
      this.activeStopBtn = null;
      this.isPaused = false;
    },

    play(text, speechBtn, pauseBtn, stopBtn) {
      if (!("speechSynthesis" in window)) {
        showToast("Speech synthesis is not supported in this browser.", "info");
        return;
      }

      // If already playing this utterance, toggle stop
      if (this.activeSpeechBtn === speechBtn && window.speechSynthesis.speaking && !this.isPaused) {
        this.stop();
        return;
      }

      this.stop();

      const cleanText = text
        .replace(/\[Page\s*\d+\]/gi, "")
        .replace(/[`*#_~>]/g, "")
        .replace(/https?:\/\/\S+/gi, "")
        .trim();
      if (!cleanText) return;

      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      // Retain utterance in global window to safeguard against Chromium garbage collection mid-speech
      window.__documindSpeech = utterance;
      this.isPaused = false;
      this.activeSpeechBtn = speechBtn;
      this.activePauseBtn = pauseBtn;
      this.activeStopBtn = stopBtn;

      speechBtn.classList.add("is-playing");
      speechBtn.innerHTML = "<span>🔊 Playing</span>";
      speechBtn.title = "Audio is playing — click to stop";

      pauseBtn.hidden = false;
      pauseBtn.classList.remove("is-paused");
      pauseBtn.innerHTML = "<span>⏸ Pause</span>";
      pauseBtn.title = "Pause audio readout";

      stopBtn.hidden = false;
      stopBtn.title = "Stop audio readout";

      utterance.onend = () => {
        this.stop();
      };
      utterance.onerror = () => {
        this.stop();
      };

      window.speechSynthesis.speak(utterance);
    },

    togglePause() {
      if (!("speechSynthesis" in window)) return;

      if (this.isPaused) {
        window.speechSynthesis.resume();
        this.isPaused = false;
        if (this.activePauseBtn) {
          this.activePauseBtn.innerHTML = "<span>⏸ Pause</span>";
          this.activePauseBtn.classList.remove("is-paused");
          this.activePauseBtn.title = "Pause audio readout";
        }
        if (this.activeSpeechBtn) {
          this.activeSpeechBtn.classList.remove("is-paused");
          this.activeSpeechBtn.classList.add("is-playing");
          this.activeSpeechBtn.innerHTML = "<span>🔊 Playing</span>";
        }
      } else if (window.speechSynthesis.speaking) {
        window.speechSynthesis.pause();
        this.isPaused = true;
        if (this.activePauseBtn) {
          this.activePauseBtn.innerHTML = "<span>▶ Resume</span>";
          this.activePauseBtn.classList.add("is-paused");
          this.activePauseBtn.title = "Resume audio readout";
        }
        if (this.activeSpeechBtn) {
          this.activeSpeechBtn.classList.remove("is-playing");
          this.activeSpeechBtn.classList.add("is-paused");
          this.activeSpeechBtn.innerHTML = "<span>⏸ Paused</span>";
        }
      }
    },
  };

  // --- Message Rendering ---
  function addMessage(role, content, sources = [], createdAt = null) {
    if (!elements.messageList) return null;
    const row = document.createElement("article");
    row.className = `message ${role}`;
    const avatar = document.createElement("span");
    avatar.className = "message-avatar";
    avatar.textContent = role === "assistant" ? "dm" : (state.currentUser ? getInitials(state.currentUser.full_name) : "you");

    const body = document.createElement("div");
    body.className = "message-body";
    const name = document.createElement("span");
    name.className = "message-name";
    name.textContent = role === "assistant" ? "DocuMind AI" : (state.currentUser?.full_name || "You");
    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = role === "assistant" ? renderMarkdown(content) : `<p>${escapeHtml(content).replace(/\n/g, "<br>")}</p>`;
    body.append(name, bubble);

    if (sources.length) {
      const sourceList = document.createElement("div");
      sourceList.className = "source-list";
      sources.forEach((source) => {
        const chip = document.createElement("span");
        chip.className = "source-chip";
        chip.innerHTML = sourceIcon;
        const label = document.createElement("span");
        label.textContent = `Page ${source.page}`;
        chip.append(label);
        chip.title = source.excerpt;
        sourceList.append(chip);
      });
      body.append(sourceList);
    }

    // Assistant Action Toolbar: Copy, Listen, Pause, Stop
    if (role === "assistant") {
      const actions = document.createElement("div");
      actions.className = "message-actions";

      const copyBtn = document.createElement("button");
      copyBtn.type = "button";
      copyBtn.className = "msg-action-btn";
      copyBtn.innerHTML = `<span>📋 Copy</span>`;
      copyBtn.title = "Copy answer to clipboard";
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(content).then(() => {
          copyBtn.innerHTML = `<span>✓ Copied!</span>`;
          window.setTimeout(() => { copyBtn.innerHTML = `<span>📋 Copy</span>`; }, 2000);
        });
      });

      const speechBtn = document.createElement("button");
      speechBtn.type = "button";
      speechBtn.className = "msg-action-btn speech-btn";
      speechBtn.innerHTML = `<span>🔊 Listen</span>`;
      speechBtn.title = "Read aloud (Audio TTS)";

      const pauseBtn = document.createElement("button");
      pauseBtn.type = "button";
      pauseBtn.className = "msg-action-btn speech-pause-btn";
      pauseBtn.hidden = true;
      pauseBtn.innerHTML = `<span>⏸ Pause</span>`;
      pauseBtn.title = "Pause audio readout";

      const stopBtn = document.createElement("button");
      stopBtn.type = "button";
      stopBtn.className = "msg-action-btn speech-stop-btn";
      stopBtn.hidden = true;
      stopBtn.innerHTML = `<span>⏹ Stop</span>`;
      stopBtn.title = "Stop audio readout";

      speechBtn.addEventListener("click", () => speechController.play(content, speechBtn, pauseBtn, stopBtn));
      pauseBtn.addEventListener("click", () => speechController.togglePause());
      stopBtn.addEventListener("click", () => speechController.stop());

      actions.append(copyBtn, speechBtn, pauseBtn, stopBtn);
      body.append(actions);
    }

    const time = document.createElement("span");
    time.className = "message-time";
    const messageDate = createdAt ? new Date(createdAt) : new Date();
    time.textContent = new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(messageDate);
    body.append(time);
    row.append(avatar, body);
    elements.messageList.append(row);
    if (elements.chatScroll) elements.chatScroll.scrollTop = elements.chatScroll.scrollHeight;
    setExportButtonsDisabled(state.history.length === 0);
    return row;
  }

  function addTypingIndicator() {
    if (!elements.messageList) return null;
    const row = document.createElement("article");
    row.className = "message assistant";
    row.dataset.typing = "true";
    const avatar = document.createElement("span");
    avatar.className = "message-avatar";
    avatar.textContent = "dm";
    const body = document.createElement("div");
    body.className = "message-body";
    const name = document.createElement("span");
    name.className = "message-name";
    name.textContent = "DocuMind AI is analyzing document";
    const indicator = document.createElement("div");
    indicator.className = "message-bubble typing-indicator";
    indicator.setAttribute("aria-label", "DocuMind AI is thinking");
    indicator.innerHTML = "<span></span><span></span><span></span>";
    body.append(name, indicator);
    row.append(avatar, body);
    elements.messageList.append(row);
    if (elements.chatScroll) elements.chatScroll.scrollTop = elements.chatScroll.scrollHeight;
    return row;
  }

  function setBusy(busy) {
    state.busy = busy;
    if (elements.readyPill) {
      elements.readyPill.classList.toggle("is-thinking", busy);
      elements.readyPill.lastChild.textContent = busy ? " Thinking" : " Ready";
    }
    if (elements.questionInput) elements.questionInput.disabled = busy || !state.selectedId;
    elements.promptGrid?.querySelectorAll(".prompt-card").forEach((button) => {
      button.disabled = busy || !state.selectedId;
    });
    elements.chatToolsBar?.querySelectorAll(".chat-tool-btn").forEach((button) => {
      button.disabled = busy || !state.selectedId;
    });
    if (elements.btnSmartSummary) elements.btnSmartSummary.disabled = busy || !state.selectedId;
    updateComposer();
  }

  function updateComposer() {
    if (!elements.questionInput) return;
    if (elements.characterCount) {
      elements.characterCount.textContent = `${elements.questionInput.value.length} / 4000`;
    }
    if (elements.sendButton) {
      elements.sendButton.disabled = !state.selectedId || state.busy || !elements.questionInput.value.trim();
    }
  }

  async function sendQuestion(questionValue = elements.questionInput?.value || "") {
    const question = questionValue.trim();
    if (!question || !state.selectedId || state.busy) return;
    const documentId = state.selectedId;
    if (elements.questionInput) {
      elements.questionInput.value = "";
      elements.questionInput.style.height = "auto";
    }
    updateComposer();
    setBusy(true);
    let typing = null;

    try {
      if (!state.chatId) {
        const conversation = await api("/api/chats", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ document_id: documentId }),
        });
        state.chatId = conversation.id;
        state.chats.unshift(conversation);
        try {
          localStorage.setItem(activeChatStorageKey, state.chatId);
        } catch {}
        renderChats();
      }
      if (elements.welcomeState) elements.welcomeState.hidden = true;
      addMessage("user", question);
      typing = addTypingIndicator();
      const result = await api("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_id: documentId,
          chat_id: state.chatId,
          question,
          history: state.history.slice(-8),
        }),
      });
      state.history.push({ role: "user", content: question }, { role: "assistant", content: result.answer, sources: result.sources || [] });
      typing?.remove();
      addMessage("assistant", result.answer, result.sources);
      setExportButtonsDisabled(false);
      await loadChats();
    } catch (error) {
      typing?.remove();
      showToast(error.message, "error");
      if (state.chatId) await loadChats();
    } finally {
      setBusy(false);
      elements.questionInput?.focus();
      if (elements.chatScroll) elements.chatScroll.scrollTop = elements.chatScroll.scrollHeight;
    }
  }

  // --- Smart Summary Trigger ---
  function triggerSmartSummary() {
    if (!state.selectedId || state.busy) return;
    sendQuestion("Please provide a comprehensive executive summary of this document, including its primary objectives, top 5 key takeaways, and actionable conclusions.");
  }

  // --- Export Chat as PDF or Word (.docx / .doc) ---
  async function exportChat(format) {
    if (!state.history.length) {
      showToast("No conversation to export yet. Please select a document and ask a question first.", "info");
      return;
    }
    const selectedDoc = state.documents.find((d) => d.id === state.selectedId);
    const docName = selectedDoc ? selectedDoc.filename : "Document";
    const cleanDocName = docName.replace(/\.pdf$/i, "").replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "_") || "Report";
    const ts = Date.now();

    if (elements.exportModalBackdrop) elements.exportModalBackdrop.hidden = true;

    if (format === "docx" || format === "word") {
      showToast("Generating Word document (.docx/.doc)...", "info");
      exportChatWordFallback(docName, cleanDocName, ts);
    } else {
      showToast("Preparing printable PDF document...", "info");
      exportChatPdfFallback(docName);
    }
  }

  function exportChatWordFallback(docName, cleanDocName, ts) {
    const dateStr = new Date().toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
    let html = `<!DOCTYPE html><html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head><meta charset='utf-8'><title>DocuMind Research Export</title>
<style>
  body { font-family: Calibri, 'Segoe UI', Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #1e293b; margin: 40px; }
  h1 { color: #1d4ed8; font-size: 20pt; border-bottom: 2px solid #2563eb; padding-bottom: 8px; margin-bottom: 12px; }
  .meta { color: #64748b; font-size: 10pt; margin-bottom: 24px; }
  .question-box { background: #eff6ff; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 18px 0 10px; border-radius: 4px; }
  .question-title { color: #1e40af; font-weight: bold; font-size: 12pt; margin-bottom: 4px; }
  .answer-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 14px 18px; margin-bottom: 24px; border-radius: 4px; }
  .answer-title { color: #0f172a; font-weight: bold; font-size: 11.5pt; margin-bottom: 6px; }
  .citation { display: inline-block; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-size: 9pt; font-weight: bold; margin-top: 8px; }
  hr { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }
</style></head><body>
<h1>DocuMind AI Research Export</h1>
<div class="meta">
  <strong>Document:</strong> ${escapeHtml(docName)}<br/>
  <strong>Export Date:</strong> ${dateStr}<br/>
  <strong>Method:</strong> Grounded neural vector search with verified citations
</div><hr/>`;

    let qIdx = 1;
    state.history.forEach((turn) => {
      if (turn.role === "user") {
        html += `<div class="question-box"><div class="question-title">Question ${qIdx}:</div><div>${escapeHtml(turn.content)}</div></div>`;
        qIdx++;
      } else {
        html += `<div class="answer-box"><div class="answer-title">DocuMind Grounded Answer:</div><div>${escapeHtml(turn.content).replace(/\n/g, '<br/>')}</div>`;
        if (turn.sources && turn.sources.length) {
          const srcList = turn.sources.map(s => `Page ${s.page || '?'}`).join(', ');
          html += `<div class="citation">Sources: ${escapeHtml(srcList)}</div>`;
        }
        html += `</div>`;
      }
    });

    html += `</body></html>`;
    const blob = new Blob([html], { type: "application/msword;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `DocuMind_Export_${cleanDocName}_${ts}.doc`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showToast("Conversation exported as Word document (.doc)!", "success");
  }

  function exportChatPdfFallback(docName) {
    const dateStr = new Date().toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
    const printWin = window.open("", "_blank");
    if (!printWin) {
      showToast("Pop-up blocked. Please allow popups to export PDF.", "error");
      return;
    }
    let html = `<!DOCTYPE html><html><head><title>DocuMind_Export_${escapeHtml(docName)}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #0f172a; margin: 30px; }
  h1 { color: #1d4ed8; font-size: 18pt; margin-bottom: 6px; }
  .meta { color: #64748b; font-size: 9.5pt; margin-bottom: 20px; border-bottom: 1px solid #cbd5e1; padding-bottom: 12px; }
  .q { font-weight: bold; color: #1e40af; margin-top: 16px; margin-bottom: 4px; font-size: 12pt; }
  .a { background: #f8fafc; border-left: 3px solid #2563eb; padding: 10px 14px; margin-bottom: 18px; border-radius: 4px; }
  .src { font-size: 9pt; color: #0369a1; font-weight: bold; margin-top: 6px; }
  @media print { body { margin: 1.5cm; } button { display: none; } }
</style></head><body>
<h1>DocuMind AI Research Report</h1>
<div class="meta">Document: ${escapeHtml(docName)} | Exported: ${dateStr}</div>`;

    let qIdx = 1;
    state.history.forEach((turn) => {
      if (turn.role === "user") {
        html += `<div class="q">Question ${qIdx}: ${escapeHtml(turn.content)}</div>`;
        qIdx++;
      } else {
        html += `<div class="a"><div>${escapeHtml(turn.content).replace(/\n/g, '<br/>')}</div>`;
        if (turn.sources && turn.sources.length) {
          const srcList = turn.sources.map(s => `Page ${s.page || '?'}`).join(', ');
          html += `<div class="src">Verified Sources: ${escapeHtml(srcList)}</div>`;
        }
        html += `</div>`;
      }
    });

    html += `<script>window.onload = function() { window.print(); };<\/script></body></html>`;
    printWin.document.write(html);
    printWin.document.close();
    showToast("Print-to-PDF ready! Select 'Save as PDF' to save.", "success");
  }

  // --- 3D Interactive Simulation Sequence ---
  const simulationFullText = "Key Findings: Enterprise gross margins expanded by 34.2% YoY. Operational resilience achieved across four decoupled regional clouds with full data confidentiality.";
  const simDuration = 6000; // 6.0 seconds per cycle

  function stopSimulationLoop() {
    if (state.simInterval) {
      window.clearInterval(state.simInterval);
      state.simInterval = null;
    }
    if (state.simTimer) {
      window.clearTimeout(state.simTimer);
      state.simTimer = null;
    }
  }

  function startSimulationLoop() {
    stopSimulationLoop();
    state.simTime = 0;

    function step() {
      state.simTime += 50;
      if (state.simTime > simDuration) {
        state.simTime = 0; // Seamless loop
      }

      // Phase 1: Laser scanning document input (0ms - 1800ms)
      if (state.simTime <= 1800) {
        if (elements.simDocCard) elements.simDocCard.classList.add("is-scanning");
        if (elements.simCoreContainer) elements.simCoreContainer.classList.remove("is-active");
        if (elements.simResultCard) elements.simResultCard.classList.remove("is-streaming");
        if (elements.simScanStatusText) elements.simScanStatusText.textContent = "Analyzing Document...";
        if (elements.simResultText && state.simTime < 300) {
          elements.simResultText.textContent = "";
        }
        const citation1 = document.getElementById("citation-pill-1");
        const citation2 = document.getElementById("citation-pill-2");
        if (citation1) citation1.classList.remove("highlight");
        if (citation2) citation2.classList.remove("highlight");
      }
      // Phase 2: Neural vector embedding in core (1800ms - 3200ms)
      else if (state.simTime <= 3200) {
        if (elements.simDocCard) elements.simDocCard.classList.remove("is-scanning");
        if (elements.simCoreContainer) elements.simCoreContainer.classList.add("is-active");
        if (elements.simResultCard) elements.simResultCard.classList.remove("is-streaming");
        if (elements.simScanStatusText) elements.simScanStatusText.textContent = "Vector Embedding (ChromaDB)...";
      }
      // Phase 3: Rapid grounded typewriter output (3200ms - 6000ms)
      else {
        if (elements.simDocCard) elements.simDocCard.classList.remove("is-scanning");
        if (elements.simCoreContainer) elements.simCoreContainer.classList.add("is-active");
        if (elements.simResultCard) elements.simResultCard.classList.add("is-streaming");
        if (elements.simScanStatusText) elements.simScanStatusText.textContent = "⚡ Verified Result (0.8s)";

        const textProgress = Math.min(1, (state.simTime - 3200) / 1800);
        const charsToShow = Math.floor(simulationFullText.length * textProgress);
        if (elements.simResultText) {
          if (charsToShow >= simulationFullText.length) {
            elements.simResultText.innerHTML = `Key Findings: Enterprise gross margins expanded by <strong>34.2% YoY</strong>. Operational resilience achieved across four decoupled regional clouds with full data confidentiality.`;
          } else {
            elements.simResultText.textContent = simulationFullText.slice(0, charsToShow) + "▋";
          }
        }

        const citation1 = document.getElementById("citation-pill-1");
        const citation2 = document.getElementById("citation-pill-2");
        if (citation1) citation1.classList.toggle("highlight", state.simTime > 4200);
        if (citation2) citation2.classList.toggle("highlight", state.simTime > 4800);
      }
    }

    state.simInterval = window.setInterval(step, 50);
  }

  // --- Event Binding ---
  function bindEvents() {
    // Theme Toggles (Workspace & Landing Header)
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.addEventListener("click", () => {
        const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        setTheme(nextTheme);
      });
    });

    // Landing Page Navigation & View Transitions
    elements.btnCornerTry?.addEventListener("click", () => showView("workspace"));
    elements.btnHeroLaunch?.addEventListener("click", () => showView("workspace"));
    elements.btnBottomTry?.addEventListener("click", () => showView("workspace"));
    elements.btnSimTry?.addEventListener("click", () => showView("workspace"));

    // Homepage Hero & Header Auth Buttons
    elements.landingBtnSignin?.addEventListener("click", () => {
      if (state.currentUser) {
        showView("workspace");
      } else {
        openAuthModal("signin");
      }
    });
    elements.landingBtnSignup?.addEventListener("click", () => openAuthModal("signup"));
    elements.btnHeroSignup?.addEventListener("click", () => openAuthModal("signup"));

    // Workspace Return to Home Button & Brand
    elements.btnNavHome?.addEventListener("click", () => showView("landing"));
    elements.brandLinkWorkspace?.addEventListener("click", (e) => {
      e.preventDefault();
      showView("landing");
    });

    // Replay Simulation Button
    elements.btnReplaySim?.addEventListener("click", () => {
      startSimulationLoop();
      showToast("Simulation restarted!", "info");
    });

    // 3D Card Hover Tilt Effects
    const tiltContainers = [elements.promptGrid, elements.authModalCard];
    tiltContainers.forEach((container) => {
      if (!container) return;
      container.addEventListener("pointermove", (event) => {
        if (event.pointerType !== "mouse" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        const target = event.target.closest(".prompt-card, .feature-card, .auth-modal-card");
        if (!target || target.disabled) return;
        const bounds = target.getBoundingClientRect();
        const x = (event.clientX - bounds.left) / bounds.width - 0.5;
        const y = (event.clientY - bounds.top) / bounds.height - 0.5;
        target.style.setProperty("--tilt-x", `${-y * 8}deg`);
        target.style.setProperty("--tilt-y", `${x * 9}deg`);
      });
      container.addEventListener("pointerleave", (event) => {
        const target = event.target.closest(".prompt-card, .feature-card, .auth-modal-card");
        if (target) {
          target.style.removeProperty("--tilt-x");
          target.style.removeProperty("--tilt-y");
        }
      });
    });

    // Wisdom interactions
    elements.topbarWisdomTicker?.addEventListener("click", cycleWisdom);
    elements.topbarWisdomNext?.addEventListener("click", (e) => {
      e.stopPropagation();
      cycleWisdom();
    });
    window.setInterval(cycleWisdom, 10000);

    // Auth Modal Triggers
    elements.btnOpenSignin?.addEventListener("click", () => openAuthModal("signin"));
    elements.btnOpenSignup?.addEventListener("click", () => openAuthModal("signup"));
    elements.btnCloseAuthModal?.addEventListener("click", closeAuthModal);
    elements.authModalBackdrop?.addEventListener("click", (e) => {
      if (e.target === elements.authModalBackdrop) closeAuthModal();
    });
    elements.btnSwitchAuthMode?.addEventListener("click", () => {
      openAuthModal(state.authMode === "signup" ? "signin" : "signup");
    });
    elements.authForm?.addEventListener("submit", handleAuthSubmit);
    elements.btnTogglePwd?.addEventListener("click", () => {
      if (!elements.authPassword) return;
      const isPwd = elements.authPassword.type === "password";
      elements.authPassword.type = isPwd ? "text" : "password";
      elements.btnTogglePwd.textContent = isPwd ? "🙈" : "👁️";
    });

    // User Dropdown
    elements.userPill?.addEventListener("click", (e) => {
      e.stopPropagation();
      if (elements.userDropdown) elements.userDropdown.hidden = !elements.userDropdown.hidden;
    });
    document.addEventListener("click", (e) => {
      if (elements.userDropdown && !elements.userDropdown.contains(e.target) && elements.userPill && !elements.userPill.contains(e.target)) {
        elements.userDropdown.hidden = true;
      }
    });
    elements.btnLogout?.addEventListener("click", logoutUser);

    // Document Search in Library
    elements.documentSearchInput?.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      if (elements.clearSearchBtn) elements.clearSearchBtn.hidden = !state.searchQuery;
      renderDocuments();
    });
    elements.clearSearchBtn?.addEventListener("click", () => {
      if (elements.documentSearchInput) elements.documentSearchInput.value = "";
      state.searchQuery = "";
      elements.clearSearchBtn.hidden = true;
      renderDocuments();
    });

    // Export Trigger
    elements.btnExportChat?.addEventListener("click", () => {
      if (elements.btnExportChat.disabled || elements.btnExportChat.classList.contains("is-dimmed")) return;
      openExportModal();
    });

    // Quick Research Bar Export Buttons
    elements.barBtnExportPdf?.addEventListener("click", () => {
      if (!elements.barBtnExportPdf.disabled) exportChat("pdf");
    });
    elements.barBtnExportWord?.addEventListener("click", () => {
      if (!elements.barBtnExportWord.disabled) exportChat("docx");
    });

    // Export Modal Bottom Sheet Actions
    elements.modalExportPdf?.addEventListener("click", () => {
      closeExportModal();
      exportChat("pdf");
    });
    elements.modalExportWord?.addEventListener("click", () => {
      closeExportModal();
      exportChat("docx");
    });
    elements.btnCloseExportModal?.addEventListener("click", closeExportModal);
    elements.btnCancelExportModal?.addEventListener("click", closeExportModal);
    elements.exportModalBackdrop?.addEventListener("click", (e) => {
      if (e.target === elements.exportModalBackdrop) closeExportModal();
    });

    elements.dropdownBtnHome?.addEventListener("click", () => {
      if (elements.userDropdown) elements.userDropdown.hidden = true;
      showView("landing");
    });

    // Landing 3-Line Mobile Hamburger Menu Toggle
    elements.landingHamburgerBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!elements.landingMobileNav) return;
      const isHidden = elements.landingMobileNav.hidden;
      elements.landingMobileNav.hidden = !isHidden;
      elements.landingHamburgerBtn.setAttribute("aria-expanded", String(isHidden));
    });

    // Landing Mobile Nav Links (Smooth Scroll & Close)
    elements.landingMobileNav?.querySelectorAll(".landing-mobile-nav-item").forEach((anchor) => {
      anchor.addEventListener("click", (e) => {
        const href = anchor.getAttribute("href");
        if (href && href.startsWith("#")) {
          e.preventDefault();
          if (elements.landingMobileNav) elements.landingMobileNav.hidden = true;
          elements.landingHamburgerBtn?.setAttribute("aria-expanded", "false");
          const targetEl = document.querySelector(href);
          if (targetEl) {
            targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });
    });

    // Landing Mobile Nav Sign In
    elements.landingMobileSignin?.addEventListener("click", () => {
      if (elements.landingMobileNav) elements.landingMobileNav.hidden = true;
      elements.landingHamburgerBtn?.setAttribute("aria-expanded", "false");
      openAuthModal("signin");
    });

    document.addEventListener("click", (e) => {
      closeAllItemMenus();
      if (elements.exportMenu && !elements.exportDropdownWrap?.contains(e.target)) {
        elements.exportMenu.hidden = true;
      }
      if (elements.landingMobileNav && !elements.landingMobileNav.hidden && !elements.landingHamburgerBtn?.contains(e.target) && !elements.landingMobileNav.contains(e.target)) {
        elements.landingMobileNav.hidden = true;
        elements.landingHamburgerBtn?.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeAllItemMenus();
      }
    });

    // Support Drag and Drop PDF onto Chat Workspace
    if (elements.chatScroll) {
      elements.chatScroll.addEventListener("dragover", (event) => {
        event.preventDefault();
      });
      elements.chatScroll.addEventListener("drop", (event) => {
        event.preventDefault();
        const file = event.dataTransfer?.files?.[0];
        if (file) uploadFile(file);
      });
    }

    // Quick Chat Composer & Chat Box Welcome State PDF Upload Buttons
    function handlePdfUploadTrigger() {
      if (!state.currentUser) {
        showToast("Account required: Please create a free account to upload and analyze PDF documents.", "info");
        openAuthModal("signup");
        return;
      }
      elements.fileInput?.click();
    }
    elements.btnComposerUpload?.addEventListener("click", handlePdfUploadTrigger);
    elements.welcomeUploadBtn?.addEventListener("click", handlePdfUploadTrigger);

    // Strict Account Gated File Upload Zone
    if (elements.uploadZone) {
      elements.uploadZone.addEventListener("click", (event) => {
        if (event.target === elements.fileInput) return;
        if (!state.currentUser) {
          event.preventDefault();
          showToast("Account required: Please create a free account to upload and analyze PDF documents.", "info");
          openAuthModal("signup");
          return;
        }
        elements.fileInput?.click();
      });

      elements.uploadZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        elements.uploadZone.classList.add("is-dragging");
      });
      elements.uploadZone.addEventListener("dragleave", (event) => {
        if (!elements.uploadZone.contains(event.relatedTarget)) {
          elements.uploadZone.classList.remove("is-dragging");
        }
      });
      elements.uploadZone.addEventListener("drop", (event) => {
        event.preventDefault();
        elements.uploadZone.classList.remove("is-dragging");
        if (!state.currentUser) {
          showToast("Account required: Please create a free account to upload and analyze PDF documents.", "error");
          openAuthModal("signup");
          return;
        }
        uploadFile(event.dataTransfer.files?.[0]);
      });
    }

    if (elements.fileInput) {
      elements.fileInput.addEventListener("click", (event) => {
        if (!state.currentUser) {
          event.preventDefault();
          showToast("Account required: Please create a free account to upload and analyze PDF documents.", "info");
          openAuthModal("signup");
        }
      });
      elements.fileInput.addEventListener("change", (event) => uploadFile(event.target.files?.[0]));
    }

    // Composer Input & Send
    elements.sendButton?.addEventListener("click", () => sendQuestion());
    elements.questionInput?.addEventListener("input", () => {
      elements.questionInput.style.height = "auto";
      elements.questionInput.style.height = `${Math.min(elements.questionInput.scrollHeight, 130)}px`;
      updateComposer();
    });
    elements.questionInput?.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendQuestion();
      }
    });

    // Prompt Card Shortcuts (Welcome State)
    elements.promptGrid?.addEventListener("click", (event) => {
      const prompt = event.target.closest("[data-prompt]");
      if (prompt && !prompt.disabled) sendQuestion(prompt.dataset.prompt);
    });

    // Persistent Quick Research Tools Bar (Accessible at ANY time during active chat)
    elements.chatToolsBar?.addEventListener("click", (event) => {
      const prompt = event.target.closest("[data-prompt]");
      if (prompt && !prompt.disabled) sendQuestion(prompt.dataset.prompt);
    });

    // Navigation, Sidebar & Mobile Actions
    elements.newChatButton?.addEventListener("click", createChat);
    elements.sidebarBtnNewChat?.addEventListener("click", createChat);
    elements.sidebarFooterHome?.addEventListener("click", () => {
      closeMobileSidebar();
      showView("landing");
    });
    elements.sidebarExportPdf?.addEventListener("click", () => {
      closeMobileSidebar();
      exportConversation("pdf");
    });
    elements.sidebarExportWord?.addEventListener("click", () => {
      closeMobileSidebar();
      exportConversation("word");
    });
    elements.mobileSidebarToggle?.addEventListener("click", openMobileSidebar);
    elements.sidebarClose?.addEventListener("click", closeMobileSidebar);
    elements.mobileOverlay?.addEventListener("click", closeMobileSidebar);
    window.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMobileSidebar();
        closeAuthModal();
        closeExportModal();
      }
    });
  }

  // --- App Initialization ---
  setTheme(document.documentElement.dataset.theme || "dark", false);
  renderWisdom(0);
  bindEvents();
  updateComposer();
  checkAuthSession().then(async () => {
    if (state.currentUser) {
      await loadDocuments();
      await loadChats(true);
    } else {
      renderDocuments();
      renderChats();
    }
  });
  startSimulationLoop();
})();
