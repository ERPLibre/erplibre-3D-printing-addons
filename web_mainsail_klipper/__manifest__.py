{
    "name": "Mainsail (Klipper) into ERPLibre",
    "category": "Manufacturing",
    "summary": "Module for embedding Mainsail in ERPLibre",
    "description": """
    This module bring Mainsail (Klipper) into ERPLibre.
    """,
    "version": "12.0.1.0",
    "author": "Jose Normil",
    "license": "AGPL-3",
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/web_mainsail_klipper.xml",
        "views/web_klipper_instances.xml",
        "views/menus.xml",
    ],
    "depends": [],
    "installable": True,
}
