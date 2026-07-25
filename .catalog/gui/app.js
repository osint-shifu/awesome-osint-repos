(() => {
  "use strict";

  const PAGE_SIZE = 36;
  const FAVORITES_KEY = "awesome-osint-tools-saved";

  // Icon paths from Phosphor Icons core, MIT License: https://github.com/phosphor-icons/core
  const ICONS = {
    "star-fill": "M234.29,114.85l-45,38.83L203,211.75a16.4,16.4,0,0,1-24.5,17.82L128,198.49,77.47,229.57A16.4,16.4,0,0,1,53,211.75l13.76-58.07-45-38.83A16.46,16.46,0,0,1,31.08,86l59-4.76,22.76-55.08a16.36,16.36,0,0,1,30.27,0l22.75,55.08,59,4.76a16.46,16.46,0,0,1,9.37,28.86Z",
    "bookmark-simple": "M184,32H72A16,16,0,0,0,56,48V224a8,8,0,0,0,12.24,6.78L128,193.43l59.77,37.35A8,8,0,0,0,200,224V48A16,16,0,0,0,184,32Zm0,177.57-51.77-32.35a8,8,0,0,0-8.48,0L72,209.57V48H184Z",
    "bookmark-simple-fill": "M184,32H72A16,16,0,0,0,56,48V224a8,8,0,0,0,12.24,6.78L128,193.43l59.77,37.35A8,8,0,0,0,200,224V48A16,16,0,0,0,184,32Z",
    "arrow-up-right": "M200,64V168a8,8,0,0,1-16,0V83.31L69.66,197.66a8,8,0,0,1-11.32-11.32L172.69,72H88a8,8,0,0,1,0-16H192A8,8,0,0,1,200,64Z",
    "arrow-right": "M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z",
    "arrow-down": "M205.66,149.66l-72,72a8,8,0,0,1-11.32,0l-72-72a8,8,0,0,1,11.32-11.32L120,196.69V40a8,8,0,0,1,16,0V196.69l58.34-58.35a8,8,0,0,1,11.32,11.32Z",
    "magnifying-glass": "M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z",
    "funnel-simple": "M200,136a8,8,0,0,1-8,8H64a8,8,0,0,1,0-16H192A8,8,0,0,1,200,136Zm32-56H24a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16Zm-80,96H104a8,8,0,0,0,0,16h48a8,8,0,0,0,0-16Z",
    "squares-four": "M104,40H56A16,16,0,0,0,40,56v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V56A16,16,0,0,0,104,40Zm0,64H56V56h48v48Zm96-64H152a16,16,0,0,0-16,16v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V56A16,16,0,0,0,200,40Zm0,64H152V56h48v48Zm-96,32H56a16,16,0,0,0-16,16v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V152A16,16,0,0,0,104,136Zm0,64H56V152h48v48Zm96-64H152a16,16,0,0,0-16,16v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V152A16,16,0,0,0,200,136Zm0,64H152V152h48v48Z",
    "list-bullets": "M80,64a8,8,0,0,1,8-8H216a8,8,0,0,1,0,16H88A8,8,0,0,1,80,64Zm136,56H88a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16Zm0,64H88a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16ZM44,52A12,12,0,1,0,56,64,12,12,0,0,0,44,52Zm0,64a12,12,0,1,0,12,12A12,12,0,0,0,44,116Zm0,64a12,12,0,1,0,12,12A12,12,0,0,0,44,180Z",
    x: "M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z",
    "identification-card": "M200,112a8,8,0,0,1-8,8H152a8,8,0,0,1,0-16h40A8,8,0,0,1,200,112Zm-8,24H152a8,8,0,0,0,0,16h40a8,8,0,0,0,0-16Zm40-80V200a16,16,0,0,1-16,16H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216A16,16,0,0,1,232,56ZM216,200V56H40V200H216Zm-80.26-34a8,8,0,1,1-15.5,4c-2.63-10.26-13.06-18-24.25-18s-21.61,7.74-24.25,18a8,8,0,1,1-15.5-4,39.84,39.84,0,0,1,17.19-23.34,32,32,0,1,1,45.12,0A39.76,39.76,0,0,1,135.75,166ZM96,136a16,16,0,1,0-16-16A16,16,0,0,0,96,136Z",
    "chats-circle": "M232.07,186.76a80,80,0,0,0-62.5-114.17A80,80,0,1,0,23.93,138.76l-7.27,24.71a16,16,0,0,0,19.87,19.87l24.71-7.27a80.39,80.39,0,0,0,25.18,7.35,80,80,0,0,0,108.34,40.65l24.71,7.27a16,16,0,0,0,19.87-19.86ZM62,159.5a8.28,8.28,0,0,0-2.26.32L32,168l8.17-27.76a8,8,0,0,0-.63-6,64,64,0,1,1,26.26,26.26A8,8,0,0,0,62,159.5Zm153.79,28.73L224,216l-27.76-8.17a8,8,0,0,0-6,.63,64.05,64.05,0,0,1-85.87-24.88A79.93,79.93,0,0,0,174.7,89.71a64,64,0,0,1,41.75,92.48A8,8,0,0,0,215.82,188.23Z",
    code: "M69.12,94.15,28.5,128l40.62,33.85a8,8,0,1,1-10.24,12.29l-48-40a8,8,0,0,1,0-12.29l48-40a8,8,0,0,1,10.24,12.3Zm176,27.7-48-40a8,8,0,1,0-10.24,12.3L227.5,128l-40.62,33.85a8,8,0,1,0,10.24,12.29l48-40a8,8,0,0,0,0-12.29ZM162.73,32.48a8,8,0,0,0-10.25,4.79l-64,176a8,8,0,0,0,4.79,10.26A8.14,8.14,0,0,0,96,224a8,8,0,0,0,7.52-5.27l64-176A8,8,0,0,0,162.73,32.48Z",
    network: "M232,112H136V88h8a16,16,0,0,0,16-16V40a16,16,0,0,0-16-16H112A16,16,0,0,0,96,40V72a16,16,0,0,0,16,16h8v24H24a8,8,0,0,0,0,16H56v32H48a16,16,0,0,0-16,16v32a16,16,0,0,0,16,16H80a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16H72V128H184v32h-8a16,16,0,0,0-16,16v32a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V176a16,16,0,0,0-16-16h-8V128h32a8,8,0,0,0,0-16ZM112,40h32V72H112ZM80,208H48V176H80Zm128,0H176V176h32Z",
    "globe-hemisphere-west": "M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm88,104a87.62,87.62,0,0,1-6.4,32.94l-44.7-27.49a15.92,15.92,0,0,0-6.24-2.23l-22.82-3.08a16.11,16.11,0,0,0-16,7.86h-8.72l-3.8-7.86a15.91,15.91,0,0,0-11-8.67l-8-1.73L96.14,104h16.71a16.06,16.06,0,0,0,7.73-2l12.25-6.76a16.62,16.62,0,0,0,3-2.14l26.91-24.34A15.93,15.93,0,0,0,166,49.1l-.36-.65A88.11,88.11,0,0,1,216,128ZM143.31,41.34,152,56.9,125.09,81.24,112.85,88H96.14a16,16,0,0,0-13.88,8l-8.73,15.23L63.38,84.19,74.32,58.32a87.87,87.87,0,0,1,69-17ZM40,128a87.53,87.53,0,0,1,8.54-37.8l11.34,30.27a16,16,0,0,0,11.62,10l21.43,4.61L96.74,143a16.09,16.09,0,0,0,14.4,9h1.48l-7.23,16.23a16,16,0,0,0,2.86,17.37l.14.14L128,205.94l-1.94,10A88.11,88.11,0,0,1,40,128Zm102.58,86.78,1.13-5.81a16.09,16.09,0,0,0-4-13.9,1.85,1.85,0,0,1-.14-.14L120,174.74,133.7,144l22.82,3.08,45.72,28.12A88.18,88.18,0,0,1,142.58,214.78Z",
    eye: "M247.31,124.76c-.35-.79-8.82-19.58-27.65-38.41C194.57,61.26,162.88,48,128,48S61.43,61.26,36.34,86.35C17.51,105.18,9,124,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208s66.57-13.26,91.66-38.34c18.83-18.83,27.3-37.61,27.65-38.4A8,8,0,0,0,247.31,124.76ZM128,192c-30.78,0-57.67-11.19-79.93-33.25A133.47,133.47,0,0,1,25,128,133.33,133.33,0,0,1,48.07,97.25C70.33,75.19,97.22,64,128,64s57.67,11.19,79.93,33.25A133.46,133.46,0,0,1,231.05,128C223.84,141.46,192.43,192,128,192Zm0-112a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Z",
    "shield-check": "M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Zm0,72c0,37.07-13.66,67.16-40.6,89.42A129.3,129.3,0,0,1,128,223.62a128.25,128.25,0,0,1-38.92-21.81C61.82,179.51,48,149.3,48,112l0-56,160,0ZM82.34,141.66a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32l-56,56a8,8,0,0,1-11.32,0Z",
    files: "M213.66,66.34l-40-40A8,8,0,0,0,168,24H88A16,16,0,0,0,72,40V56H56A16,16,0,0,0,40,72V216a16,16,0,0,0,16,16H168a16,16,0,0,0,16-16V200h16a16,16,0,0,0,16-16V72A8,8,0,0,0,213.66,66.34ZM168,216H56V72h76.69L168,107.31v84.53c0,.06,0,.11,0,.16s0,.1,0,.16V216Zm32-32H184V104a8,8,0,0,0-2.34-5.66l-40-40A8,8,0,0,0,136,56H88V40h76.69L200,75.31Zm-56-32a8,8,0,0,1-8,8H88a8,8,0,0,1,0-16h48A8,8,0,0,1,144,152Zm0,32a8,8,0,0,1-8,8H88a8,8,0,0,1,0-16h48A8,8,0,0,1,144,184Z",
    "image-square": "M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM48,48H208v77.38l-24.69-24.7a16,16,0,0,0-22.62,0L53.37,208H48ZM208,208H76l96-96,36,36v60ZM96,120A24,24,0,1,0,72,96,24,24,0,0,0,96,120Zm0-32a8,8,0,1,1-8,8A8,8,0,0,1,96,88Z",
    "map-pin": "M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z",
    "currency-btc": "M178.48,115.7A44,44,0,0,0,152,40.19V24a8,8,0,0,0-16,0V40H120V24a8,8,0,0,0-16,0V40H72a8,8,0,0,0,0,16h8V192H72a8,8,0,0,0,0,16h32v16a8,8,0,0,0,16,0V208h16v16a8,8,0,0,0,16,0V208h8a48,48,0,0,0,18.48-92.3ZM176,84a28,28,0,0,1-28,28H96V56h52A28,28,0,0,1,176,84ZM160,192H96V128h64a32,32,0,0,1,0,64Z",
    binoculars: "M237.2,151.87v0a47.1,47.1,0,0,0-2.35-5.45L193.26,51.8a7.82,7.82,0,0,0-1.66-2.44,32,32,0,0,0-45.26,0A8,8,0,0,0,144,55V80H112V55a8,8,0,0,0-2.34-5.66,32,32,0,0,0-45.26,0,7.82,7.82,0,0,0-1.66,2.44L21.15,146.4a47.1,47.1,0,0,0-2.35,5.45v0A48,48,0,1,0,112,168V96h32v72a48,48,0,1,0,93.2-16.13ZM76.71,59.75a16,16,0,0,1,19.29-1v73.51a47.9,47.9,0,0,0-46.79-9.92ZM64,200a32,32,0,1,1,32-32A32,32,0,0,1,64,200ZM160,58.74a16,16,0,0,1,19.29,1l27.5,62.58A47.9,47.9,0,0,0,160,132.25ZM192,200a32,32,0,1,1,32-32A32,32,0,0,1,192,200Z"
  };

  const CATEGORY_ICONS = {
    Identity: "identification-card",
    "Social Media": "chats-circle",
    "Code Repositories": "code",
    Infrastructure: "network",
    Web: "globe-hemisphere-west",
    "Dark Web": "eye",
    "Threat Intelligence": "shield-check",
    "Documents & Records": "files",
    Media: "image-square",
    Geolocation: "map-pin",
    Cryptocurrency: "currency-btc",
    Investigation: "binoculars"
  };

  const dateFormatter = new Intl.DateTimeFormat("en", { year: "numeric", month: "short", day: "numeric" });
  const numberFormatter = new Intl.NumberFormat("en");

  const elements = {
    activeFilters: document.querySelector("#activeFilters"),
    advancedFilters: document.querySelector("#advancedFilters"),
    agenticCount: document.querySelector("#agenticCount"),
    agenticStat: document.querySelector("#agenticStat"),
    allCount: document.querySelector("#allCount"),
    categoryFilter: document.querySelector("#categoryFilter"),
    categoryNav: document.querySelector("#categoryNav"),
    clearFilters: document.querySelector("#clearFilters"),
    closeDialog: document.querySelector("#closeDialog"),
    dataStatus: document.querySelector("#dataStatus"),
    detailBody: document.querySelector("#detailBody"),
    detailCategory: document.querySelector("#detailCategory"),
    detailDialog: document.querySelector("#detailDialog"),
    detailIcon: document.querySelector("#detailIcon"),
    detailRepository: document.querySelector("#detailRepository"),
    detailSave: document.querySelector("#detailSave"),
    detailTitle: document.querySelector("#detailTitle"),
    emergingCount: document.querySelector("#emergingCount"),
    emergingStat: document.querySelector("#emergingStat"),
    emptyClear: document.querySelector("#emptyClear"),
    emptyState: document.querySelector("#emptyState"),
    errorState: document.querySelector("#errorState"),
    explorerTitle: document.querySelector("#explorerTitle"),
    filterCount: document.querySelector("#filterCount"),
    filterToggle: document.querySelector("#filterToggle"),
    layoutSwitch: document.querySelector(".layout-switch"),
    licenseFilter: document.querySelector("#licenseFilter"),
    loadMore: document.querySelector("#loadMore"),
    loadingState: document.querySelector("#loadingState"),
    referenceDate: document.querySelector("#referenceDate"),
    resultsGrid: document.querySelector("#resultsGrid"),
    resultsSummary: document.querySelector("#resultsSummary"),
    savedCount: document.querySelector("#savedCount"),
    searchInput: document.querySelector("#searchInput"),
    sortSelect: document.querySelector("#sortSelect"),
    sortSummary: document.querySelector("#sortSummary"),
    targetFilter: document.querySelector("#targetFilter"),
    targetStat: document.querySelector("#targetStat"),
    totalStat: document.querySelector("#totalStat"),
    typeFilter: document.querySelector("#typeFilter"),
    updatedFilter: document.querySelector("#updatedFilter"),
    viewTabs: document.querySelector("#viewTabs")
  };

  const state = {
    records: [],
    meta: {},
    query: "",
    category: "",
    target: "",
    type: "",
    license: "",
    updated: "",
    view: "all",
    sort: "stars",
    layout: "cards",
    visible: PAGE_SIZE,
    selectedId: "",
    saved: loadSaved()
  };

  function icon(name) {
    const path = ICONS[name] || ICONS.binoculars;
    return `<svg viewBox="0 0 256 256" fill="currentColor" focusable="false" aria-hidden="true"><path d="${path}"></path></svg>`;
  }

  function hydrateStaticIcons() {
    document.querySelectorAll("[data-icon]").forEach((node) => {
      node.innerHTML = icon(node.dataset.icon);
    });
  }

  function categoryIcon(category) {
    return icon(CATEGORY_ICONS[category] || "binoculars");
  }

  function loadSaved() {
    try {
      return new Set(JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]"));
    } catch {
      return new Set();
    }
  }

  function persistSaved() {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify([...state.saved]));
  }

  function splitValues(value) {
    return String(value || "").split(";").map((item) => item.trim()).filter(Boolean);
  }

  function normalizeText(value) {
    return String(value || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  }

  function displayText(value, fallback = "Not specified") {
    const text = String(value || "").trim();
    return text ? text.replace(/[\u2013\u2014]/g, "-") : fallback;
  }

  function escapeHtml(value) {
    return displayText(value, "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
  }

  function safeUrl(value) {
    try {
      const url = new URL(value);
      return ["http:", "https:"].includes(url.protocol) ? url.href : "#";
    } catch {
      return "#";
    }
  }

  function normalizeRecord(record) {
    const sourceFiles = splitValues(record["Source Files"]);
    const targets = splitValues(record["Target Input"]);
    const types = splitValues(record.Type);
    const licenses = splitValues(record.License);
    return {
      ...record,
      _id: String(record["Repository ID"] || record.Repository),
      _sourceFiles: sourceFiles,
      _targets: targets,
      _types: types,
      _licenses: licenses,
      _stars: Number.parseInt(record.Stars || "0", 10) || 0,
      _searchable: [record.Project, record.Repository, record.Description, record["Target Input"], record.Categories, record.Type, record["AI Agent"], record.License, record.Hosting, record["Discovery Source"]].map(normalizeText).join(" ")
    };
  }

  function optionCounts(field) {
    const counts = new Map();
    state.records.forEach((record) => splitValues(record[field]).forEach((value) => counts.set(value, (counts.get(value) || 0) + 1)));
    return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  }

  function fillSelect(select, field, placeholder) {
    const options = optionCounts(field).map(([value, count]) => `<option value="${escapeHtml(value)}">${escapeHtml(value)} (${count})</option>`).join("");
    select.innerHTML = `<option value="">${placeholder}</option>${options}`;
  }

  function restoreStateFromUrl() {
    const params = new URLSearchParams(window.location.search);
    state.query = params.get("q") || "";
    state.category = params.get("category") || "";
    state.target = params.get("target") || "";
    state.type = params.get("type") || "";
    state.license = params.get("license") || "";
    state.updated = params.get("updated") || "";
    state.view = ["all", "emerging", "agentic", "saved"].includes(params.get("view")) ? params.get("view") : "all";
    state.sort = ["stars", "updated", "added", "created", "name", "category", "target", "type", "relevance"].includes(params.get("sort")) ? params.get("sort") : "stars";
    state.layout = params.get("layout") === "list" ? "list" : "cards";
    elements.searchInput.value = state.query;
    elements.categoryFilter.value = state.category;
    elements.targetFilter.value = state.target;
    elements.typeFilter.value = state.type;
    elements.licenseFilter.value = state.license;
    elements.updatedFilter.value = state.updated;
    elements.sortSelect.value = state.sort;
    if (state.type || state.license || state.updated) setAdvancedOpen(true);
  }

  function syncUrl() {
    const params = new URLSearchParams();
    const entries = { q: state.query, category: state.category, target: state.target, type: state.type, license: state.license, updated: state.updated, view: state.view !== "all" ? state.view : "", sort: state.sort !== "stars" ? state.sort : "", layout: state.layout !== "cards" ? state.layout : "" };
    Object.entries(entries).forEach(([key, value]) => value && params.set(key, value));
    history.replaceState(null, "", params.size ? `?${params}` : window.location.pathname);
  }

  function viewRecords() {
    if (state.view === "emerging") return state.records.filter((record) => record._sourceFiles.includes("EMERGING.md"));
    if (state.view === "agentic") return state.records.filter((record) => record._sourceFiles.includes("AGENTIC.md"));
    if (state.view === "saved") return state.records.filter((record) => state.saved.has(record._id));
    return state.records;
  }

  function searchScore(record, tokens) {
    const fields = [[record.Project, 10], [record.Categories, 5], [record["Target Input"], 5], [record.Type, 4], [record["AI Agent"], 4], [record.Description, 2], [record.Repository, 1]];
    return tokens.reduce((score, token) => score + fields.reduce((fieldScore, [value, weight]) => fieldScore + (normalizeText(value).includes(token) ? weight : 0), 0), 0);
  }

  function dateValue(value) {
    const parsed = new Date(`${value || "1900-01-01"}T00:00:00Z`);
    return Number.isNaN(parsed.valueOf()) ? 0 : parsed.valueOf();
  }

  function filteredRecords() {
    const tokens = normalizeText(state.query).split(/\s+/).filter(Boolean);
    const reference = state.meta.verified ? new Date(`${state.meta.verified}T00:00:00Z`) : new Date();
    const records = viewRecords().filter((record) => {
      if (tokens.some((token) => !record._searchable.includes(token))) return false;
      if (state.category && record.Categories !== state.category) return false;
      if (state.target && !record._targets.includes(state.target)) return false;
      if (state.type && !record._types.includes(state.type)) return false;
      if (state.license && !record._licenses.includes(state.license)) return false;
      if (state.updated) {
        const lastUpdate = new Date(`${record["Last Update"]}T00:00:00Z`);
        const cutoff = new Date(reference);
        cutoff.setUTCDate(cutoff.getUTCDate() - Number(state.updated));
        if (!record["Last Update"] || Number.isNaN(lastUpdate.valueOf()) || lastUpdate < cutoff) return false;
      }
      return true;
    });
    const scored = records.map((record) => ({ record, score: searchScore(record, tokens) }));
    scored.sort((a, b) => {
      if (state.sort === "relevance") return b.score - a.score || b.record._stars - a.record._stars;
      if (state.sort === "updated") return dateValue(b.record["Last Update"]) - dateValue(a.record["Last Update"]) || b.record._stars - a.record._stars;
      if (state.sort === "added") return dateValue(b.record.Added) - dateValue(a.record.Added) || b.record._stars - a.record._stars;
      if (state.sort === "created") return dateValue(b.record.Created) - dateValue(a.record.Created) || b.record._stars - a.record._stars;
      if (state.sort === "name") return a.record.Project.localeCompare(b.record.Project);
      if (state.sort === "category") return a.record.Categories.localeCompare(b.record.Categories) || a.record.Project.localeCompare(b.record.Project);
      if (state.sort === "target") return displayText(a.record["Target Input"]).localeCompare(displayText(b.record["Target Input"])) || a.record.Project.localeCompare(b.record.Project);
      if (state.sort === "type") return displayText(a.record.Type).localeCompare(displayText(b.record.Type)) || a.record.Project.localeCompare(b.record.Project);
      return b.record._stars - a.record._stars || a.record.Project.localeCompare(b.record.Project);
    });
    return scored.map(({ record }) => record);
  }

  function formatDate(value) {
    if (!value) return "Not specified";
    const parsed = new Date(`${value}T00:00:00Z`);
    return Number.isNaN(parsed.valueOf()) ? displayText(value) : dateFormatter.format(parsed);
  }

  function isNew(record) {
    return Boolean(record.Added && state.meta.verified && dateValue(record.Added) >= dateValue(state.meta.verified) - 14 * 86400000);
  }

  function cardTemplate(record, index) {
    const saved = state.saved.has(record._id);
    const target = record._targets.join(", ") || "Not specified";
    const type = record._types.join(", ") || "Not specified";
    return `<div class="tool-card-shell" style="animation-delay:${Math.min(index, 12) * 24}ms">
      <article class="tool-card" data-record-id="${escapeHtml(record._id)}">
        <div class="card-topline">
          <div class="card-category"><span class="card-category-icon">${categoryIcon(record.Categories)}</span><span class="card-category-label">${escapeHtml(record.Categories)}</span>${isNew(record) ? '<span class="new-label">New</span>' : ""}</div>
          <div class="card-actions">
            <button class="icon-action" type="button" data-save-record="${escapeHtml(record._id)}" aria-label="${saved ? "Remove from saved" : "Save tool"}: ${escapeHtml(record.Project)}" aria-pressed="${saved}" title="${saved ? "Remove from saved" : "Save tool"}">${icon(saved ? "bookmark-simple-fill" : "bookmark-simple")}</button>
            <a class="icon-action" href="${safeUrl(record.Repository)}" target="_blank" rel="noopener noreferrer" aria-label="Open ${escapeHtml(record.Project)} repository" title="Open repository">${icon("arrow-up-right")}</a>
          </div>
        </div>
        <div class="card-main">
          <div class="card-copy"><button class="card-title-button" type="button" data-open-record="${escapeHtml(record._id)}" aria-label="View details for ${escapeHtml(record.Project)}">${escapeHtml(record.Project)}</button><p class="card-description">${escapeHtml(record.Description)}</p></div>
          <div class="card-facts"><div class="card-fact"><span>Target input</span><strong title="${escapeHtml(target)}">${escapeHtml(target)}</strong></div><div class="card-fact"><span>Tool type</span><strong title="${escapeHtml(type)}">${escapeHtml(type)}</strong></div></div>
        </div>
        <footer class="card-footer"><span class="star-count">${icon("star-fill")} ${numberFormatter.format(record._stars)}</span><span class="card-update">Updated ${escapeHtml(formatDate(record["Last Update"]))}</span></footer>
      </article>
    </div>`;
  }

  function renderCategories() {
    const categories = Object.entries(state.meta.categories || {}).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    elements.categoryNav.innerHTML = categories.map(([category, count]) => `<button class="category-card" type="button" data-category="${escapeHtml(category)}" aria-current="${state.category === category}"><span class="category-card-top"><span class="category-card-icon">${categoryIcon(category)}</span><span class="category-card-count">${count}</span></span><strong>${escapeHtml(category)}</strong></button>`).join("");
    document.querySelector(".reset-category").setAttribute("aria-current", String(state.category === ""));
  }

  function renderTabs() {
    const counts = {
      all: state.records.length,
      emerging: state.records.filter((record) => record._sourceFiles.includes("EMERGING.md")).length,
      agentic: state.records.filter((record) => record._sourceFiles.includes("AGENTIC.md")).length,
      saved: state.saved.size
    };
    elements.allCount.textContent = counts.all;
    elements.emergingCount.textContent = counts.emerging;
    elements.agenticCount.textContent = counts.agentic;
    elements.savedCount.textContent = counts.saved;
    elements.viewTabs.querySelectorAll("[data-view]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.view === state.view)));
  }

  function activeFilterEntries() {
    const updatedLabels = { 30: "Past 30 days", 180: "Past 6 months", 365: "Past year", 1095: "Past 3 years" };
    return [["category", state.category], ["target", state.target], ["type", state.type], ["license", state.license], ["updated", updatedLabels[state.updated] || ""]].filter(([, value]) => value);
  }

  function renderActiveFilters() {
    const filters = activeFilterEntries();
    elements.activeFilters.innerHTML = filters.map(([key, label]) => `<button class="filter-chip" type="button" data-remove-filter="${key}">${escapeHtml(label)} ${icon("x")}</button>`).join("");
    elements.filterCount.textContent = filters.filter(([key]) => ["type", "license", "updated"].includes(key)).length;
  }

  function renderLayoutState() {
    elements.resultsGrid.classList.toggle("is-list", state.layout === "list");
    elements.layoutSwitch.querySelectorAll("[data-layout]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.layout === state.layout)));
  }

  function renderSortSummary() {
    const labels = { stars: "most starred", updated: "recently updated", added: "recently added", created: "newest repositories", name: "name A-Z", category: "category A-Z", target: "target input A-Z", type: "tool type A-Z", relevance: "search relevance" };
    elements.sortSummary.textContent = `Sorted by ${labels[state.sort]}`;
  }

  function render() {
    const records = filteredRecords();
    const visible = records.slice(0, state.visible);
    elements.loadingState.hidden = true;
    elements.errorState.hidden = true;
    elements.resultsGrid.innerHTML = visible.map(cardTemplate).join("");
    elements.resultsGrid.hidden = records.length === 0;
    elements.emptyState.hidden = records.length !== 0;
    elements.loadMore.hidden = state.visible >= records.length;
    elements.resultsSummary.textContent = `${numberFormatter.format(records.length)} ${records.length === 1 ? "tool" : "tools"} found`;
    elements.explorerTitle.textContent = `Search ${numberFormatter.format(state.records.length)} OSINT tools`;
    renderTabs();
    renderCategories();
    renderActiveFilters();
    renderLayoutState();
    renderSortSummary();
    syncUrl();
  }

  function setFilter(key, value) {
    state[key] = value;
    state.visible = PAGE_SIZE;
    if (key === "query" && value && state.sort === "stars") {
      state.sort = "relevance";
      elements.sortSelect.value = "relevance";
    }
    if (key === "category") elements.categoryFilter.value = value;
    render();
  }

  function clearFilters() {
    Object.assign(state, { query: "", category: "", target: "", type: "", license: "", updated: "", view: "all", sort: "stars", visible: PAGE_SIZE });
    elements.searchInput.value = "";
    elements.categoryFilter.value = "";
    elements.targetFilter.value = "";
    elements.typeFilter.value = "";
    elements.licenseFilter.value = "";
    elements.updatedFilter.value = "";
    elements.sortSelect.value = "stars";
    render();
  }

  function toggleSaved(id) {
    if (state.saved.has(id)) state.saved.delete(id);
    else state.saved.add(id);
    persistSaved();
    render();
    if (state.selectedId === id && elements.detailDialog.open) updateDetailSave(id);
  }

  function detailRows(rows) {
    return `<dl class="detail-list">${rows.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(displayText(value))}</dd></div>`).join("")}</dl>`;
  }

  function openDetail(id) {
    const record = state.records.find((item) => item._id === id);
    if (!record) return;
    state.selectedId = id;
    elements.detailCategory.textContent = displayText(record.Categories);
    elements.detailTitle.textContent = displayText(record.Project);
    elements.detailIcon.innerHTML = categoryIcon(record.Categories);
    elements.detailRepository.href = safeUrl(record.Repository);
    elements.detailBody.innerHTML = `<p class="dialog-description">${escapeHtml(record.Description)}</p>
      <section class="detail-section"><h3>Investigation scope</h3>${detailRows([["Category", record.Categories], ["Target input", record["Target Input"]], ["Type", record.Type], ["AI agent", record["AI Agent"]]])}</section>
      <section class="detail-section"><h3>Repository</h3>${detailRows([["Hosting", record.Hosting], ["License", record.License], ["Stars", numberFormatter.format(record._stars)], ["Created", formatDate(record.Created)], ["Last update", formatDate(record["Last Update"])], ["Added", formatDate(record.Added)]])}</section>
      <section class="detail-section"><h3>CSV database record</h3>${detailRows([["Verified", formatDate(record.Verified)], ["Repository ID", record["Repository ID"]], ["Repository status", record["Repository Status"]], ["Review status", record["Review Status"]], ["Archived", record.Archived], ["Fork", record.Fork], ["Discovery source", record["Discovery Source"]], ["Source files", record["Source Files"]]])}</section>`;
    updateDetailSave(id);
    elements.detailDialog.showModal();
  }

  function updateDetailSave(id) {
    const saved = state.saved.has(id);
    elements.detailSave.innerHTML = `${icon(saved ? "bookmark-simple-fill" : "bookmark-simple")}<span>${saved ? "Remove from saved" : "Save tool"}</span>`;
    elements.detailSave.setAttribute("aria-pressed", String(saved));
  }

  function setAdvancedOpen(open) {
    elements.advancedFilters.hidden = !open;
    elements.filterToggle.setAttribute("aria-expanded", String(open));
  }

  function bindEvents() {
    let searchTimer;
    elements.searchInput.addEventListener("input", () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => setFilter("query", elements.searchInput.value.trim()), 100);
    });
    elements.categoryFilter.addEventListener("change", () => setFilter("category", elements.categoryFilter.value));
    elements.targetFilter.addEventListener("change", () => setFilter("target", elements.targetFilter.value));
    elements.typeFilter.addEventListener("change", () => setFilter("type", elements.typeFilter.value));
    elements.licenseFilter.addEventListener("change", () => setFilter("license", elements.licenseFilter.value));
    elements.updatedFilter.addEventListener("change", () => setFilter("updated", elements.updatedFilter.value));
    elements.sortSelect.addEventListener("change", () => setFilter("sort", elements.sortSelect.value));
    elements.filterToggle.addEventListener("click", () => setAdvancedOpen(elements.advancedFilters.hidden));
    elements.clearFilters.addEventListener("click", clearFilters);
    elements.emptyClear.addEventListener("click", clearFilters);
    elements.loadMore.addEventListener("click", () => { state.visible += PAGE_SIZE; render(); });
    document.querySelector("#categories").addEventListener("click", (event) => {
      const button = event.target.closest("[data-category]");
      if (!button) return;
      setFilter("category", button.dataset.category);
      document.querySelector("#explorer").scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    });
    elements.viewTabs.addEventListener("click", (event) => {
      const button = event.target.closest("[data-view]");
      if (button) setFilter("view", button.dataset.view);
    });
    elements.layoutSwitch.addEventListener("click", (event) => {
      const button = event.target.closest("[data-layout]");
      if (button) setFilter("layout", button.dataset.layout);
    });
    elements.activeFilters.addEventListener("click", (event) => {
      const button = event.target.closest("[data-remove-filter]");
      if (!button) return;
      const key = button.dataset.removeFilter;
      state[key] = "";
      const select = elements[`${key}Filter`];
      if (select) select.value = "";
      render();
    });
    elements.resultsGrid.addEventListener("click", (event) => {
      const save = event.target.closest("[data-save-record]");
      if (save) return toggleSaved(save.dataset.saveRecord);
      const open = event.target.closest("[data-open-record]");
      if (open) openDetail(open.dataset.openRecord);
    });
    elements.closeDialog.addEventListener("click", () => elements.detailDialog.close());
    elements.detailSave.addEventListener("click", () => toggleSaved(state.selectedId));
    elements.detailDialog.addEventListener("click", (event) => { if (event.target === elements.detailDialog) elements.detailDialog.close(); });
    document.addEventListener("keydown", (event) => {
      const typing = ["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement.tagName);
      if (event.key === "/" && !typing) {
        event.preventDefault();
        elements.searchInput.focus();
      }
    });
  }

  async function init() {
    hydrateStaticIcons();
    bindEvents();
    try {
      const response = await fetch("catalog.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`Catalogue returned ${response.status}`);
      const payload = await response.json();
      if (!Array.isArray(payload.records)) throw new Error("Catalogue response is invalid");
      state.records = payload.records.map(normalizeRecord);
      state.meta = payload.meta || {};
      fillSelect(elements.categoryFilter, "Categories", "All categories");
      fillSelect(elements.targetFilter, "Target Input", "Any target input");
      fillSelect(elements.typeFilter, "Type", "Any tool type");
      fillSelect(elements.licenseFilter, "License", "Any license");
      restoreStateFromUrl();
      elements.totalStat.textContent = numberFormatter.format(state.records.length);
      elements.targetStat.textContent = numberFormatter.format(optionCounts("Target Input").length);
      elements.emergingStat.textContent = numberFormatter.format(state.meta.emerging || 0);
      elements.agenticStat.textContent = numberFormatter.format(state.meta.agentic || 0);
      elements.dataStatus.innerHTML = `<i></i>CSV verified ${escapeHtml(state.meta.verified || "current")}`;
      elements.referenceDate.textContent = state.meta.verified ? `Verified ${formatDate(state.meta.verified)}` : "Current source";
      render();
    } catch (error) {
      console.error(error);
      elements.loadingState.hidden = true;
      elements.resultsGrid.hidden = true;
      elements.errorState.hidden = false;
      elements.resultsSummary.textContent = "Catalogue unavailable";
      elements.dataStatus.textContent = "CSV unavailable";
    }
  }

  init();
})();
