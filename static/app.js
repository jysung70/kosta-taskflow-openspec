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

// 로그인 성공 후 team_id 분기
function redirectAfterAuth(user) {
  if (user && user.team_id) {
    window.location.href = `/kanban?team=${user.team_id}`;
  } else {
    window.location.href = '/teams';
  }
}

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

// 필드 하단 인라인 에러
function showFieldError(fieldId, msg) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  let errEl = document.getElementById(fieldId + '-error');
  if (!errEl) {
    errEl = document.createElement('p');
    errEl.id = fieldId + '-error';
    errEl.className = 'text-red-500 text-xs mt-1';
    field.parentNode.appendChild(errEl);
  }
  errEl.textContent = msg;
  errEl.classList.remove('hidden');
}
function clearFieldError(fieldId) {
  const errEl = document.getElementById(fieldId + '-error');
  if (errEl) errEl.textContent = '';
}

// 버튼 로딩 상태
function setLoading(btn, loading) {
  if (loading) {
    btn.disabled = true;
    btn.dataset.orig = btn.textContent;
    btn.textContent = '처리 중...';
    btn.classList.add('opacity-70');
  } else {
    btn.disabled = false;
    btn.textContent = btn.dataset.orig || btn.textContent;
    btn.classList.remove('opacity-70');
  }
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

// 탭 네비게이션 렌더 (kanban|chat|members)
function renderTabNav(active) {
  const teamId = getTeamId();
  const tabs = [
    { id: 'kanban', label: '칸반', href: `/kanban?team=${teamId}` },
    { id: 'chat',   label: '채팅', href: `/chat?team=${teamId}` },
    { id: 'members',label: '멤버', href: `/members?team=${teamId}` },
  ];
  return tabs.map(t => {
    const isActive = t.id === active;
    const base = 'px-4 py-2 text-sm font-medium rounded transition';
    const cls = isActive
      ? `${base} bg-teal-600 text-white`
      : `${base} text-gray-600 hover:bg-gray-100`;
    return `<a href="${t.href}" class="${cls}">${t.label}</a>`;
  }).join('');
}
