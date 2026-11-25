let hideTimer;

export function showMessage(text, type = 'success') {
  const box = document.getElementById('message');
  box.className = `message message-${type}`;
  box.innerHTML = `<span>${escapeHtml(text)}</span>
                   <button class="message-close" aria-label="Cerrar">×</button>`;
  box.hidden = false;
  box.querySelector('.message-close').onclick = () => { box.hidden = true; };

  clearTimeout(hideTimer);
  if (type === 'success') {
    hideTimer = setTimeout(() => { box.hidden = true; }, 4000);
  }
}

export function hideMessage() {
  clearTimeout(hideTimer);
  document.getElementById('message').hidden = true;
}

export function escapeHtml(value) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  return String(value ?? '').replace(/[&<>"']/g, (ch) => map[ch]);
}

export function formatMoney(value) {
  return '$ ' + Number(value).toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export function badge(text, kind) {
  return `<span class="badge badge-${kind}">${escapeHtml(text)}</span>`;
}

export function emptyRow(text, columns) {
  return `<tr><td colspan="${columns}" class="empty">${escapeHtml(text)}</td></tr>`;
}
