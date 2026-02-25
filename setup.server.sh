#!/bin/bash

# 1. Verificar si Docker está activo
echo "Verificando estado de Docker..."
retries=0
until docker info >/dev/null 2>&1 || [ $retries -eq 10 ]; do
    echo "Esperando a Docker... ($((retries+1))/10)"
    sudo systemctl start docker
    sleep 5
    ((retries++))
done

if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker no está respondiendo."
    exit 1
fi

# 2. Limpieza (Opcional en servidores, pero incluida según tu flujo)
echo "Limpiando instalaciones previas..."
docker compose down -v --remove-orphans

# 3. Crear carpetas de datos con permisos correctos
echo "Creando directorios..."
folders=("data/postgres" "data/odoo" "extra-addons" "config" "backups")
for folder in "${folders[@]}"; do
    mkdir -p "$folder"
done
# Ajustar permisos para que Docker (usuario 101 en Odoo) pueda escribir
sudo chown -R 101:101 extra-addons data/odoo

# 4. Levantar el proyecto
echo "Levantando contenedores..."
docker compose up -d --build --force-recreate

# 5. Pausa de carga
echo "Esperando 25 segundos..."
sleep 25

# 6. Instalación de librerías
CONTAINER_NAME=$(docker ps --filter "name=web" --format "{{.Names}}" | head -n 1)

if [ -n "$CONTAINER_NAME" ]; then
    echo "Instalando librerías en $CONTAINER_NAME..."
    docker exec -u root -t "$CONTAINER_NAME" pip3 install qifparse num2words premailer lyra --break-system-packages
    echo "LISTO: Accede a http://tu-ip-servidor:8069"
else
    echo "ERROR: El contenedor web no se encuentra ejecutandose."
fi