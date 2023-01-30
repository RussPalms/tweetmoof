import { backendLookup } from "../lookup";

export function apiMoofCreate(newMoof, callback) {
  backendLookup("POST", "/moofs/create/", callback, { content: newMoof });
}

export function apiMoofAction(moofId, action, callback) {
  const data = { id: moofId, action: action };
  backendLookup("POST", "/moofs/action/", callback, data);
}

export function apiMoofDetail(moofId, callback) {
  backendLookup("GET", `/moofs/${moofId}/`, callback);
}

export function apiMoofList(username, callback, nextUrl) {
  let endpoint = "/moofs/";
  if (username) {
    endpoint = `/moofs/?username=${username}`;
  }
  if (nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("http://127.0.0.1:8000/api", "");
  }
  backendLookup("GET", endpoint, callback);
}

export function apiMoofFeed(callback, nextUrl) {
  let endpoint = "/moofs/feed";
  if (nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("http://127.0.0.1:8000/api", "");
  }
  backendLookup("GET", endpoint, callback);
}
