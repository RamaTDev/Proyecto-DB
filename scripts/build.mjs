import { cp, mkdir, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'front');
const target = path.join(root, 'dist');

const apiUrl = (process.env.API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

await rm(target, { recursive: true, force: true });
await mkdir(target, { recursive: true });
await cp(source, target, { recursive: true });

await writeFile(
  path.join(target, 'js', 'config.js'),
  `// Generado por npm run build. No editar a mano.\nwindow.API_URL = ${JSON.stringify(apiUrl)};\n`,
  'utf8'
);

console.log(`Build listo → dist/ (API_URL=${apiUrl})`);