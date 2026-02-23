# --- Script de Configuración Inicial para Odoo ERP ---

Write-Host "--- Iniciando instalación del ERP ---" -ForegroundColor Cyan

# 1. Crear estructura de carpetas si no existe
$folders = @("data", "data/postgres", "data/odoo", "extra-addons", "config", "backups")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -Path $folder -ItemType Directory
        Write-Host "[+] Carpeta $folder creada." -ForegroundColor Green
    }
}

# 2. Crear archivo .gitkeep en data para mantener la estructura
if (-not (Test-Path "data/.gitkeep")) {
    New-Item -Path "data/.gitkeep" -ItemType File
}

# 3. Limpiar contenedores antiguos para evitar conflictos
Write-Host "[-] Limpiando instalaciones previas..." -ForegroundColor Yellow
docker-compose down --volumes --remove-orphans

# 4. Levantar los servicios
Write-Host "[>] Levantando servidores Docker..." -ForegroundColor Cyan
docker-compose up -d

# 5. Esperar a que el contenedor esté listo e instalar librerías de MuK
Write-Host "[!] Esperando 15 segundos para la inicialización del sistema..." -ForegroundColor Gray
Start-Sleep -Seconds 15

Write-Host "[+] Instalando librerías de Python necesarias (MuK)..." -ForegroundColor Green
docker exec -u root -it $(docker ps -qf "name=web") pip3 install num2words premailer lyra --break-system-packages

Write-Host "---"
Write-Host "¡TODO LISTO!" -ForegroundColor Green
Write-Host "Accede a: http://localhost:8069" -ForegroundColor BrightWhite
Write-Host "Master Password configurada en docker-compose.yml" -ForegroundColor Yellow