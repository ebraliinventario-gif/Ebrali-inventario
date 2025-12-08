const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const DIST = path.join(ROOT, 'dist');

function ensureDist() {
  fs.rmSync(DIST, { recursive: true, force: true });
  fs.mkdirSync(DIST, { recursive: true });
}

function collectDataFiles() {
  return fs
    .readdirSync(ROOT)
    .filter((file) => file.startsWith('dados_') && file.endsWith('.js'));
}

function copyFile(file) {
  const source = path.join(ROOT, file);
  const target = path.join(DIST, file);

  if (!fs.existsSync(source)) {
    console.warn(`[build] Arquivo não encontrado: ${file}`);
    return;
  }

  fs.copyFileSync(source, target);
  console.log(`[build] Copiado ${file}`);
}

function build() {
  ensureDist();

  const staticFiles = [
    'index.html',
    'styles.css',
    'logo_ebrali-2025.png',
    'config.js',
  ];

  const filesToCopy = [...new Set([...staticFiles, ...collectDataFiles()])];
  filesToCopy.forEach(copyFile);

  console.log('\nBuild finalizado. Conteúdo pronto em ./dist');
}

build();
