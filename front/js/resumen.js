import { getResumen, getCategories } from './api.js';
import { showMessage, hideMessage, escapeHtml, formatMoney, badge, emptyRow } from './ui.js';

const COLUMNS = 7;

const LABELS = {
  productname: 'Producto',
  categoryname: 'Categoría',
  discontinued: 'Descontinuado',
  stockmax: 'Stock desde',
  stockmin: 'Stock hasta',
  pricemax: 'Precio desde',
  pricemin: 'Precio hasta',
};

const form = document.getElementById('filter-form');
const tableBody = document.getElementById('table-body');
const countLabel = document.getElementById('count');

async function loadCategories() {
  try {
    const categories = await getCategories();
    categories.sort((a, b) => a.categoryname.localeCompare(b.categoryname));
    form.elements.categoryname.innerHTML = '<option value="">Todas</option>' +
      categories.map((c) => {
        const name = escapeHtml(c.categoryname);
        return `<option value="${name}">${name}</option>`;
      }).join('');
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

function readFilters() {
  const filters = {};
  for (const [name, value] of new FormData(form)) {
    filters[name] = value.trim();
  }
  return filters;
}

function withLabels(message) {
  return message.replace(/\b(productname|categoryname|discontinued|stockmin|stockmax|pricemin|pricemax)\b/g,
    (name) => LABELS[name]);
}

async function search() {
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;

  try {
    const rows = await getResumen(readFilters());
    hideMessage();
    renderTable(rows);
  } catch (error) {
    countLabel.textContent = '';
    tableBody.innerHTML = emptyRow('No se pudo hacer la consulta.', COLUMNS);
    showMessage(withLabels(error.message), 'error');
  } finally {
    button.disabled = false;
  }
}

function statusBadges(row) {
  let html = row.active ? badge('Activo', 'ok') : badge('Dado de baja', 'off');
  if (row.discontinued) html += ' ' + badge('Descontinuado', 'warn');
  return html;
}

function renderTable(rows) {
  countLabel.textContent = rows.length === 1 ? '1 resultado' : `${rows.length} resultados`;

  if (rows.length === 0) {
    tableBody.innerHTML = emptyRow('No hay productos que coincidan.', COLUMNS);
    return;
  }

  tableBody.innerHTML = rows.map((r) => `
    <tr class="${r.active ? '' : 'row-inactive'}">
      <td class="num">${r.productid}</td>
      <td>${escapeHtml(r.product)}</td>
      <td>${escapeHtml(r.category)}</td>
      <td>${escapeHtml(r.supplier)}</td>
      <td class="num">${formatMoney(r.price)}</td>
      <td class="num">${r.stock}</td>
      <td>${statusBadges(r)}</td>
    </tr>
  `).join('');
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  search();
});

document.getElementById('btn-clear').addEventListener('click', () => {
  form.reset();
  search();
});

loadCategories();
search();
