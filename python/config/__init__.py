# --- Configuration ---
# It's recommended to use environment variables for sensitive data
# and host configuration for better security and flexibility.
import os
USERNAME = os.environ.get("SAP_PO_USER", "SUP.FRACASSG")
PASSWORD = os.environ.get("SAP_PO_PASSWORD", "ini00ini")
HOST = os.environ.get("SAP_PO_HOST", "http://sappod.menarini.net:54000")
DB_FILE = "sap_po_data.db"