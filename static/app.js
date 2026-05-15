const TOKEN_KEY = 'taskflow_token';
const USER_KEY = 'taskflow_user';

// JWT / 사용자 유틸
function saveAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}
function getToken() { return localStorage.getItem(TOKEN_KEY); }
function getUser() {
  const u = localStorage.getItem(USER_KEY);
  return u ? JSON.parse(u) : null;
}
function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}
function isLoggedIn() { return !!getToken(); }

// API 공통 호출 (Authorization 헤더 자동 주입)
async function api(method, path, body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data?.detail?.msg || data?.msg || '오류가 발생했습니다');
    err.status = res.status;
    err.code = data?.detail?.code || data?.code;
    throw err;
  }
  return data;
}

// 에러 메시지 표시
function showError(msg, elId = 'error-msg') {
  const el = document.getElementById(elId);
  if (!el) { alert(msg); return; }
  el.textContent = msg;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 4000);
}

// 로그인 필요 페이지 가드
function requireAuth() {
  if (!isLoggedIn()) { window.location.href = '/'; return false; }
  return true;
}

// 팀 ID (URL 파라미터)
function getTeamId() {
  return new URLSearchParams(window.location.search).get('team');
}
