# Cambia a 19.0 si la 19.0 te da error de "manifest not found"
FROM odoo:19.0

USER root

# Actualizamos repositorios e instalamos dependencias de sistema que suelen pedir estas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalamos las librerías con el flag necesario para Debian moderno
RUN pip3 install --no-cache-dir \
    num2words \
    premailer \
    qifparse \
    lyra \
    --break-system-packages

USER odoo