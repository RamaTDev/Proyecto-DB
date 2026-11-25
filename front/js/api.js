export const API_URL = 'http://127.0.0.1:8000';

async function apiRequest(method, path, body) {
  const options = { method, headers: {} };

  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(API_URL + path, options);
  } catch {
    throw new Error(`No se pudo conectar con la API. ¿Está corriendo en ${API_URL}?`);
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(getErrorMessage(data, response.status));
  }

  return data;
}

function getErrorMessage(data, status) {
  if (data) {
    if (typeof data.detail === 'string') return data.detail;

    if (Array.isArray(data.detail)) {
      return data.detail.map((e) => `${e.loc.at(-1)}: ${e.msg}`).join(' · ');
    }

    if (typeof data.message === 'string') return data.message;
  }
  return `La API respondió con un error (${status}).`;
}

export async function getProducts() {
  const data = await apiRequest('GET', '/products/');
  return data.products;
}
export const createProduct   = (product)     => apiRequest('POST',   '/products/', product);
export const updateProduct   = (id, product) => apiRequest('PUT',    `/products/${id}`, product);
export const deleteProduct   = (id)          => apiRequest('DELETE', `/products/${id}`);
export const activateProduct = (id)          => apiRequest('POST',   `/products/${id}/activate`);

export async function getSuppliers() {
  const data = await apiRequest('GET', '/suppliers/');
  return data.suppliers;
}
export const createSupplier   = (supplier)     => apiRequest('POST',   '/suppliers/', supplier);
export const updateSupplier   = (id, supplier) => apiRequest('PUT',    `/suppliers/${id}`, supplier);
export const deleteSupplier   = (id)           => apiRequest('DELETE', `/suppliers/${id}`);
export const activateSupplier = (id)           => apiRequest('POST',   `/suppliers/${id}/activate`);

export async function getCategories() {
  const data = await apiRequest('GET', '/categories/');
  return data.categories;
}
export const createCategory = (category)     => apiRequest('POST',   '/categories/', category);
export const updateCategory = (id, category) => apiRequest('PUT',    `/categories/${id}`, category);
export const deleteCategory = (id)           => apiRequest('DELETE', `/categories/${id}`);
export const activateCategory = (id)         => apiRequest('POST',   `/categories/${id}`);
