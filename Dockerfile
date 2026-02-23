# Usamos la imagen oficial de Odoo como base
FROM odoo:19.0

# Cambiamos a usuario root para instalar dependencias del sistema
USER root

# Instalamos las librerías que MuK necesita
# 'pip install' instala las herramientas de Python
RUN pip3 install --no-cache-dir \
    num2words \
    premailer \
    lyra

# Volvemos al usuario odoo por seguridad
USER odoo