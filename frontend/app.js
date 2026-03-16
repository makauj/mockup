const state = {
  token: null,
  xUser: null,
};

const $ = (id) => document.getElementById(id);

function log(message, data) {
  const output = $("output");
  const stamp = new Date().toISOString();
  const line = data ? `${stamp} | ${message}\n${JSON.stringify(data, null, 2)}\n` : `${stamp} | ${message}\n`;
  output.textContent = `${line}${output.textContent}`;
}

function getApiBase() {
  return $("api-base").value.trim().replace(/\/$/, "");
}

function authHeaders() {
  if (state.token) {
    return { Authorization: `Bearer ${state.token}` };
  }
  if (state.xUser) {
    return { "X-User": state.xUser };
  }
  return {};
}

async function loginOAuth() {
  const apiBase = getApiBase();
  const username = $("username").value.trim();
  const password = $("password").value;

  if (!username || !password) {
    log("Provide username and password for OAuth2 login.");
    return;
  }

  const body = new URLSearchParams({ username, password });
  const response = await fetch(`${apiBase}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    log("OAuth2 login failed.", payload);
    return;
  }

  state.token = payload.access_token;
  state.xUser = null;
  log("OAuth2 login successful. JWT active.");
}

function setLegacyUser() {
  const xUser = $("x-user").value.trim();
  if (!xUser) {
    log("Provide an X-User value.");
    return;
  }
  state.xUser = xUser;
  state.token = null;
  log(`Using legacy X-User auth: ${xUser}`);
}

async function uploadExcel() {
  const apiBase = getApiBase();
  const fileInput = $("file-input");
  const file = fileInput.files?.[0];
  if (!file) {
    log("Select an Excel file first.");
    return;
  }

  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${apiBase}/upload/`, {
    method: "POST",
    headers: { ...authHeaders() },
    body: form,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    log("Upload failed.", payload);
    return;
  }

  log("Upload successful.", payload);
}

function renderTable(rows) {
  const wrap = $("table-wrap");
  if (!rows.length) {
    wrap.innerHTML = "<p style=\"padding:0.8rem\">No records found.</p>";
    return;
  }

  const headers = ["record_id", "ID", "Name", "Email", "Contact", "Date", "read_only", "last_updated_by", "last_updated_at"];
  const head = headers.map((h) => `<th>${h}</th>`).join("");
  const body = rows.map((row) => `<tr>${headers.map((h) => `<td>${row[h] ?? ""}</td>`).join("")}</tr>`).join("");
  wrap.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

async function loadCollections() {
  const apiBase = getApiBase();
  const id = $("filter-id").value;
  const readOnly = $("filter-read-only").value;
  const limit = $("filter-limit").value || "100";

  const params = new URLSearchParams({ skip: "0", limit });
  if (id) params.set("ID", id);
  if (readOnly) params.set("read_only", readOnly);

  const response = await fetch(`${apiBase}/collections/?${params.toString()}`, {
    headers: { ...authHeaders() },
  });

  const payload = await response.json().catch(() => []);
  if (!response.ok) {
    log("Load collections failed.", payload);
    return;
  }

  renderTable(payload);
  log(`Loaded ${payload.length} collection rows.`);
}

async function updateCollection() {
  const apiBase = getApiBase();
  const recordId = $("update-record-id").value;
  if (!recordId) {
    log("Provide record_id to update.");
    return;
  }

  const data = {};
  const name = $("update-name").value.trim();
  const email = $("update-email").value.trim();
  const contact = $("update-contact").value.trim();
  const date = $("update-date").value;
  if (name) data.Name = name;
  if (email) data.Email = email;
  if (contact) data.Contact = contact;
  if (date) data.Date = date;

  if (!Object.keys(data).length) {
    log("Provide at least one field to update.");
    return;
  }

  const response = await fetch(`${apiBase}/collections/${recordId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(data),
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    log("Update failed.", payload);
    return;
  }

  log("Update successful.", payload);
}

$("login-btn").addEventListener("click", () => loginOAuth().catch((e) => log("OAuth2 login error", { error: String(e) })));
$("set-user-btn").addEventListener("click", setLegacyUser);
$("upload-btn").addEventListener("click", () => uploadExcel().catch((e) => log("Upload error", { error: String(e) })));
$("load-btn").addEventListener("click", () => loadCollections().catch((e) => log("Load error", { error: String(e) })));
$("update-btn").addEventListener("click", () => updateCollection().catch((e) => log("Update error", { error: String(e) })));
