FROM odoo:17.0
USER root
# Instala dependencias necesarias para tu ERP
RUN pip3 install pandas
COPY ./extra-addons /mnt/extra-addons
USER odoo