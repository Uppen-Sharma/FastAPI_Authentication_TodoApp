const API_URL = import.meta.env.VITE_API_URL;

// memory only
let accessToken = null;

// Sync between tabs
const authChannel = new BroadcastChannel("auth");

// Listen to other tabs
export function onAuthChange(callback) {
  authChannel.onmessage = callback;
  return () => {
    authChannel.onmessage = null;
  };
}

// Add token and cookie to fetch request
function send(path, options = {}) {
  const isJson = typeof options.body === "string";
  return fetch(`${API_URL}${path}`, {
    ...options,
    credentials: "include",
    headers: {
      ...(isJson ? { "Content-Type": "application/json" } : {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
  });
}

// Reads the error message
async function errorMessage(res) {
  const body = await res.json().catch(() => null);
  return typeof body?.detail === "string" ? body.detail : `Error ${res.status}`;
}

// One refresh at a time
let refreshing = null;

// Get new tokens / new refresh token assigned to memory
function refresh() {
  refreshing ??= send("/auth/refresh", { method: "POST" })
    .then(async (res) => {
      if (!res.ok) throw new Error(await errorMessage(res));
      const data = await res.json();
      if (!data) throw new Error("Not Logged in");
      accessToken = data.access_token;
      return data;
    })
    .finally(() => {
      refreshing = null;
    });
  return refreshing;
}

// On 401, refresh and retry
export async function api(path, options = {}) {
  let res = await send(path, options);

  if (res.status === 401 && accessToken) {
    try {
      await refresh();
      res = await send(path, options);
    } catch {
      accessToken = null;
      window.location.assign("/login");
      throw new Error("Session expired");
    }
  }

  if (!res.ok) throw new Error(await errorMessage(res));
  return res.status === 204 ? undefined : res.json();
}

// Login route
export async function login(username, password) {
  const data = await api("/auth/login", {
    method: "POST",
    body: new URLSearchParams({ username, password }),
  });
  accessToken = data.access_token;
  authChannel.postMessage("login");
  return data.user;
}

// Register route
export function register(username, password) {
  return api("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

// Refresh/restore session route
export async function restoreSession() {
  return (await refresh()).user;
}

// Logout route
export async function logout() {
  await api("/auth/logout", { method: "POST" }).catch(() => {});
  accessToken = null;
  authChannel.postMessage("logout");
}
