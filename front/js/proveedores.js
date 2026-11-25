import {
  getSuppliers, createSupplier, updateSupplier, deleteSupplier, activateSupplier,
} from './api.js';
import { showMessage, escapeHtml, badge, emptyRow } from './ui.js';

const COLUMNS = 8;

const FIELDS = [
  'companyname', 'contactname', 'contacttitle', 'address', 'city',
  'region', 'postalcode', 'country', 'phone', 'fax', 'homepage',
];

let suppliers = [];
let editingId = null;

const form = document.getElementById('supplier-form');
const formCard = document.getElementById('form-card');
const formTitle = document.getElementById('form-title');
const tableBody = document.getElementById('table-body');
const searchInput = document.getElementById('search');
const statusFilter = document.getElementById('filter-status');
const countLabel = document.getElementById('count');

async function loadData() {
  try {
    suppliers = await getSuppliers();
    suppliers.sort((a, b) => a.supplierid - b.supplierid);
    renderTable();
  } catch (error) {
    tableBody.innerHTML = emptyRow('No se pudieron cargar los proveedores.', COLUMNS);
    showMessage(error.message, 'error');
  }
}

function renderTable() {
  const text = searchInput.value.trim().toLowerCase();
  const status = statusFilter.value;

  const visible = suppliers.filter((s) => {
    if (status === 'active' && !s.active) return false;
    if (status === 'inactive' && s.active) return false;
    const searchable = `${s.companyname} ${s.contactname} ${s.city} ${s.country}`.toLowerCase();
    return searchable.includes(text);
  });

  countLabel.textContent = `${visible.length} de ${suppliers.length}`;

  if (visible.length === 0) {
    tableBody.innerHTML = emptyRow('No hay proveedores para mostrar.', COLUMNS);
    return;
  }

  tableBody.innerHTML = visible.map((s) => `
    <tr class="${s.active ? '' : 'row-inactive'}">
      <td class="num">${s.supplierid}</td>
      <td>${escapeHtml(s.companyname)}</td>
      <td>${escapeHtml(s.contactname)}<br><span class="muted">${escapeHtml(s.contacttitle)}</span></td>
      <td>${escapeHtml(s.city)}</td>
      <td>${escapeHtml(s.country)}</td>
      <td>${escapeHtml(s.phone)}</td>
      <td>${s.active ? badge('Activo', 'ok') : badge('Dado de baja', 'off')}</td>
      <td class="actions">${actionButtons(s)}</td>
    </tr>
  `).join('');
}

function actionButtons(s) {
  if (!s.active) {
    return `<button class="btn btn-small btn-success" data-action="activate" data-id="${s.supplierid}">Reactivar</button>`;
  }
  return `
    <button class="btn btn-small" data-action="edit" data-id="${s.supplierid}">Editar</button>
    <button class="btn btn-small btn-danger" data-action="delete" data-id="${s.supplierid}">Dar de baja</button>
  `;
}

tableBody.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;

  const supplier = suppliers.find((s) => s.supplierid === Number(button.dataset.id));
  const action = button.dataset.action;

  if (action === 'edit') openForm(supplier);
  if (action === 'delete') removeSupplier(supplier);
  if (action === 'activate') reactivateSupplier(supplier);
});

searchInput.addEventListener('input', renderTable);
statusFilter.addEventListener('change', renderTable);

function openForm(supplier = null) {
  editingId = supplier ? supplier.supplierid : null;
  form.reset();

  formTitle.textContent = supplier ? `Editar proveedor #${supplier.supplierid}` : 'Nuevo proveedor';
  if (supplier) {
    FIELDS.forEach((name) => { form.elements[name].value = supplier[name] ?? ''; });
  }

  formCard.hidden = false;
  formCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  form.elements.companyname.focus();
}

function closeForm() {
  formCard.hidden = true;
  editingId = null;
  form.reset();
}

function readForm() {
  return Object.fromEntries(FIELDS.map((name) => [name, form.elements[name].value]));
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = readForm();
  const saveButton = form.querySelector('button[type="submit"]');
  saveButton.disabled = true;

  try {
    if (editingId === null) {
      await createSupplier(data);
      showMessage(`Proveedor "${data.companyname}" creado.`);
    } else {
      await updateSupplier(editingId, data);
      showMessage(`Proveedor #${editingId} actualizado.`);
    }
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

async function removeSupplier(supplier) {
  const ok = confirm(
    `¿Dar de baja a "${supplier.companyname}"?\n\n` +
    'Todos sus productos quedarán descontinuados y se cancelarán sus unidades en pedido.'
  );
  if (!ok) return;

  try {
    await deleteSupplier(supplier.supplierid);
    showMessage(`"${supplier.companyname}" fue dado de baja.`);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

async function reactivateSupplier(supplier) {
  try {
    await activateSupplier(supplier.supplierid);
    showMessage(`"${supplier.companyname}" fue reactivado.`);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

loadData();
