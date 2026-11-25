import {
  getProducts, createProduct, updateProduct, deleteProduct, activateProduct,
  getSuppliers, getCategories,
} from './api.js';
import { showMessage, escapeHtml, formatMoney, badge, emptyRow } from './ui.js';

const COLUMNS = 11;

let products = [];
let suppliers = [];
let categories = [];

let editingId = null;

const form = document.getElementById('product-form');
const formCard = document.getElementById('form-card');
const formTitle = document.getElementById('form-title');
const discontinuedField = document.getElementById('discontinued-field');
const tableBody = document.getElementById('table-body');
const searchInput = document.getElementById('search');
const statusFilter = document.getElementById('filter-status');
const countLabel = document.getElementById('count');

async function loadData() {
  try {
    [products, suppliers, categories] = await Promise.all([
      getProducts(), getSuppliers(), getCategories(),
    ]);
    products.sort((a, b) => a.productid - b.productid);
    renderTable();
  } catch (error) {
    tableBody.innerHTML = emptyRow('No se pudieron cargar los productos.', COLUMNS);
    showMessage(error.message, 'error');
  }
}

function supplierName(id) {
  const supplier = suppliers.find((s) => s.supplierid === id);
  return supplier ? supplier.companyname : `#${id}`;
}

function categoryName(id) {
  const category = categories.find((c) => c.categoryid === id);
  return category ? category.categoryname : `#${id}`;
}

function renderTable() {
  const text = searchInput.value.trim().toLowerCase();
  const status = statusFilter.value;

  const visible = products.filter((p) => {
    if (status === 'active' && !p.active) return false;
    if (status === 'inactive' && p.active) return false;
    return p.productname.toLowerCase().includes(text);
  });

  countLabel.textContent = `${visible.length} de ${products.length}`;

  if (visible.length === 0) {
    tableBody.innerHTML = emptyRow('No hay productos para mostrar.', COLUMNS);
    return;
  }

  tableBody.innerHTML = visible.map((p) => `
    <tr class="${p.active ? '' : 'row-inactive'}">
      <td class="num">${p.productid}</td>
      <td>${escapeHtml(p.productname)}</td>
      <td>${escapeHtml(supplierName(p.supplierid))}</td>
      <td>${escapeHtml(categoryName(p.categoryid))}</td>
      <td>${escapeHtml(p.quantityperunit)}</td>
      <td class="num">${formatMoney(p.unitprice)}</td>
      <td class="num">${p.unitsinstock}</td>
      <td class="num">${p.unitsonorder}</td>
      <td class="num">${p.reorderlevel}</td>
      <td>${statusBadges(p)}</td>
      <td class="actions">${actionButtons(p)}</td>
    </tr>
  `).join('');
}

function statusBadges(p) {
  let html = p.active ? badge('Activo', 'ok') : badge('Dado de baja', 'off');
  if (p.discontinued) html += ' ' + badge('Descontinuado', 'warn');
  return html;
}

function actionButtons(p) {
  if (!p.active) {
    return `<button class="btn btn-small btn-success" data-action="activate" data-id="${p.productid}">Reactivar</button>`;
  }
  return `
    <button class="btn btn-small" data-action="edit" data-id="${p.productid}">Editar</button>
    <button class="btn btn-small btn-danger" data-action="delete" data-id="${p.productid}">Dar de baja</button>
  `;
}

tableBody.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;

  const product = products.find((p) => p.productid === Number(button.dataset.id));
  const action = button.dataset.action;

  if (action === 'edit') openForm(product);
  if (action === 'delete') removeProduct(product);
  if (action === 'activate') reactivateProduct(product);
});

searchInput.addEventListener('input', renderTable);
statusFilter.addEventListener('change', renderTable);

function fillSelects(product) {
  const supplierOptions = suppliers.filter((s) => s.active || s.supplierid === product?.supplierid);
  const categoryOptions = categories.filter((c) => !c.discontinued || c.categoryid === product?.categoryid);

  form.elements.supplierid.innerHTML = '<option value="">Elegí un proveedor…</option>' +
    supplierOptions.map((s) => {
      const label = s.companyname + (s.active ? '' : ' (dado de baja)');
      return `<option value="${s.supplierid}">${escapeHtml(label)}</option>`;
    }).join('');

  form.elements.categoryid.innerHTML = '<option value="">Elegí una categoría…</option>' +
    categoryOptions.map((c) => {
      const label = c.categoryname + (c.discontinued ? ' (dada de baja)' : '');
      return `<option value="${c.categoryid}">${escapeHtml(label)}</option>`;
    }).join('');
}

function openForm(product = null) {
  editingId = product ? product.productid : null;
  form.reset();
  fillSelects(product);

  formTitle.textContent = product ? `Editar producto #${product.productid}` : 'Nuevo producto';
  discontinuedField.hidden = !product;

  if (product) {
    const fields = ['productname', 'supplierid', 'categoryid', 'quantityperunit',
      'unitprice', 'unitsinstock', 'unitsonorder', 'reorderlevel'];
    fields.forEach((name) => { form.elements[name].value = product[name]; });
    form.elements.discontinued.checked = product.discontinued;
  }

  formCard.hidden = false;
  formCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  form.elements.productname.focus();
}

function closeForm() {
  formCard.hidden = true;
  editingId = null;
  form.reset();
}

function toNumber(value) {
  return value.trim() === '' ? null : Number(value);
}

function readForm() {
  const f = form.elements;
  return {
    productname: f.productname.value,
    supplierid: toNumber(f.supplierid.value),
    categoryid: toNumber(f.categoryid.value),
    quantityperunit: f.quantityperunit.value,
    unitprice: toNumber(f.unitprice.value),
    unitsinstock: toNumber(f.unitsinstock.value),
    unitsonorder: toNumber(f.unitsonorder.value),
    reorderlevel: toNumber(f.reorderlevel.value),
  };
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = readForm();
  const saveButton = form.querySelector('button[type="submit"]');
  saveButton.disabled = true;

  try {
    if (editingId === null) {
      await createProduct(data);
      showMessage(`Producto "${data.productname}" creado.`);
    } else {
      data.discontinued = form.elements.discontinued.checked;
      await updateProduct(editingId, data);
      showMessage(`Producto #${editingId} actualizado.`);
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

async function removeProduct(product) {
  if (!confirm(`¿Dar de baja "${product.productname}"?`)) return;

  try {
    await deleteProduct(product.productid);
    showMessage(`"${product.productname}" fue dado de baja.`);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

async function reactivateProduct(product) {
  try {
    await activateProduct(product.productid);
    showMessage(`"${product.productname}" fue reactivado.`);
    await loadData();
  } catch (error) {
    showMessage(error.message, 'error');
  }
}

loadData();
