# 1. Verificar si Docker esta activo
$dockerReady = $false
$retries = 0

while (-not $dockerReady -and $retries -lt 10) {
    docker info >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        $dockerReady = $true
        Write-Host "Docker esta ONLINE."
    } else {
        Write-Host "Esperando a Docker... ($($retries + 1)/10)"
        if (-not (Get-Process "Docker Desktop" -ErrorAction SilentlyContinue)) {
            Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        }
        Start-Sleep -Seconds 10
        $retries++
    }
}

if (-not $dockerReady) {
    Write-Host "ERROR: Docker no arranco correctamente."
    exit
}

# 2. Limpieza de contenedores y volumenes viejos
Write-Host "Limpiando instalaciones previas..."
docker-compose down -v --remove-orphans

# 3. Crear carpetas de datos
$folders = @("data", "data/postgres", "data/odoo", "extra-addons", "config", "backups")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -Path $folder -ItemType Directory -Force
    }
}

# 4. Levantar el proyecto
Write-Host "Levantando contenedores..."
docker-compose up -d --build --force-recreate

# 5. Pausa para que el sistema cargue
Write-Host "Esperando 25 segundos..."
Start-Sleep -Seconds 25

# 6. Instalacion de librerias Python necesarias
$containerName = docker ps --filter "name=web" --format "{{.Names}}" | Select-Object -First 1

if ($containerName) {
    Write-Host "Instalando librerias en $containerName"
    docker exec -u root -t $containerName pip3 install num2words premailer lyra --break-system-packages
    Write-Host "LISTO: Accede a http://localhost:8069"
} else {
    Write-Host "ERROR: El contenedor web no se encuentra ejecutandose."
}