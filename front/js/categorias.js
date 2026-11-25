import {
  getCategories, createCategory, updateCategory, deleteCategory, activateCategory,
} from './api.js';
import { showMessage, escapeHtml, badge, emptyRow } from './ui.js';

const COLUMNS = 6;

let categories = [];
let editingId = null;

const form = document.getElementById('category-form');
const formCard = document.getElementById('form-card');
const formTitle = document.getElementById('form-title');
const tableBody = document.getElementById('table-body');
const searchInput = document.getElementById('search');
const statusFilter = document.getElementById('filter-status');
const countLabel = document.getElementById('count');

async function loadData() {
  try {
    categories = await getCategories();
    categories.sort((a, b) => a.categoryid - b.categoryid);
    renderTable();
  } catch (error) {
    tableBody.innerHTML = emptyRow('No se pudieron cargar las categorías.', COLUMNS);
    showMessage(error.message, 'error');
  }
}

function renderTable() {
  const text = searchInput.value.trim().toLowerCase();
  const status = statusFilter.value;

  const visible = categories.filter((c) => {
    if (status === 'active' && c.discontinued) return false;
    if (status === 'inactive' && !c.discontinued) return false;
    return `${c.categoryname} ${c.description}`.toLowerCase().includes(text);
  });

  countLabel.textContent = `${visible.length} de ${categories.length}`;

  if (visible.length === 0) {
    tableBody.innerHTML = emptyRow('No hay categorías para mostrar.', COLUMNS);
    return;
  }

  tableBody.innerHTML = visible.map((c) => `
    <tr class="${c.discontinued ? 'row-inactive' : ''}">
      <td class="num">${c.categoryid}</td>
      <td>${pictureCell(c.picture)}</td>
      <td>${escapeHtml(c.categoryname)}</td>
      <td class="clip" title="${escapeHtml(c.description)}">${escapeHtml(c.description)}</td>
      <td>${c.discontinued ? badge('Dada de baja', 'off') : badge('Activa', 'ok')}</td>
      <td class="actions">${actionButtons(c)}</td>
    </tr>
  `).join('');
}

function pictureCell(picture) {
  if (picture && /^https?:\/\//i.test(picture)) {
    return `<img class="thumb" src="${escapeHtml(picture)}" alt="">`;
  }
  return `<span class="muted">${escapeHtml(picture)}</span>`;
}

function actionButtons(c) {
  if (c.discontinued) {
    return `<button class="btn btn-small btn-success" data-action="activate" data-id="${c.categoryid}">Reactivar</button>`;
  }
  return `
    <button class="btn btn-small" data-action="edit" data-id="${c.categoryid}">Editar</button>
    <button class="btn btn-small btn-danger" data-action="delete" data-id="${c.categoryid}">Dar de baja</button>
  `;
}

tableBody.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;

  const category = categories.find((c) => c.categoryid === Number(button.dataset.id));
  const action = button.dataset.action;

  if (action === 'edit') openForm(category);
  if (action === 'delete') removeCategory(category);
  if (action === 'activate') reactivateCategory(category);
});

searchInput.addEventListener('input', renderTable);
statusFilter.addEventListener('change', renderTable);

function openForm(category = null) {
  editingId = category ? category.categoryid : null;
  form.reset();

  formTitle.textContent = category ? `Editar categoría #${category.categoryid}` : 'Nueva categoría';
  if (category) {
    form.elements.categoryname.value = category.categoryname;
    form.elements.description.value = category.description ?? '';
    form.elements.picture.value = category.picture ?? '';
  }

  formCard.hidden = false;
  formCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  form.elements.categoryname.focus();
}

function closeForm() {
  formCard.hidden = true;
  editingId = null;
  form.reset();
}

function readForm() {
  return {
    categoryname: form.elements.categoryname.value,
    description: form.elements.description.value,
    picture: form.elements.picture.value,
  };
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = readForm();
  const saveButton = form.querySelector('button[type="submit"]');
  saveButton.disabled = true;

  try {
    const result = editingId === null
      ? await createCategory(data)
      : await updateCategory(editingId, data);
    showMessage(result.message);
    closeForm();
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  } finally {
    saveButton.disabled = false;
  }
});

document.getElementById('btn-new').addEventListener('click', () => openForm());
document.getElementById('btn-cancel').addEventListener('click', closeForm);

async function removeCategory(category) {
  if (!confirm(`¿Dar de baja la categoría "${category.categoryname}"?`)) return;

  try {
    const result = await deleteCategory(category.categoryid);
    showMessage(result.message);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

async function reactivateCategory(category) {
  try {
    const result = await activateCategory(category.categoryid);
    showMessage(result.message);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

loadData();
