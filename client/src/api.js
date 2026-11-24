// Backend address, set in client/.env
const API_URL = import.meta.env.VITE_API_URL;

// The access token lives in memory only, it is gone when the page reloads
let accessToken = null;

// Channel used to tell the other tabs when someone logs in or out
const authChannel = new BroadcastChannel("auth");

// Run a callback when another tab logs in or out, returns a function to stop listening
export function onAuthChange(callback) {
  authChannel.onmessage = callback;
  return () => {
    authChannel.onmessage = null;
  };
}

// Send a request to the backend with the access token and the refresh cookie
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

// Read the error message the backend sent back
async function errorMessage(res) {
  const body = await res.json().catch(() => null);
  return typeof body?.detail === "string" ? body.detail : `Error ${res.status}`;
}

// Refresh tokens work only once, so all callers share one refresh request
let refreshing = null;

// Trade the refresh cookie for a new access token (and a new refresh cookie)
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

// Call the backend, and if the access token expired (401) refresh once and retry
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

// Log in with a username and password, keep the access token and tell other tabs
export async function login(username, password) {
  const data = await api("/auth/login", {
    method: "POST",
    body: new URLSearchParams({ username, password }),
  });
  accessToken = data.access_token;
  authChannel.postMessage("login");
  return data.user;
}

// Create a new account
export function register(username, password) {
  return api("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

//Triggers the refresh endpoint to keep new access tokens coming in for active sessions.
export async function restoreSession() {
  return (await refresh()).user;
}

// End the session on the server, clear the access token and tell other tabs
export async function logout() {
  await api("/auth/logout", { method: "POST" }).catch(() => {});
  accessToken = null;
  authChannel.postMessage("logout");
}
