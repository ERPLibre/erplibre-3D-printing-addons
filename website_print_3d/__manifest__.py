{
    "name": "Print3D Order",
    "category": "Manufacturing",
    "summary": "Module for ordering 3D printing",
    "description": """
    This module allow to sell Slicing Profile as 3D Product in the e-commerce. It depends on
    those modules : 'Web Slicing Profiles', 'Web Slicing Server', 'Mail' and 'Website Sale'. It extends the 'Product'
    model from ERPLibre.
    """,
    "version": "12.0.1.0",
    "author": "Jose Normil",
    "license": "AGPL-3",
    "application": True,
    "data": [
        "views/template_product_sale.xml",
        "views/p3d_product_form.xml",
        "views/assets.xml",
    ],
    "depends": [
        "web_slicing_profile",
        "web_slicing_server",
        "mail", "website_sale",
    ],
    "external_dependencies": {
        "python": [
            "requests", "os", "orjson", "re", "math", "datetime"
        ]
    },
    "installable": True,
}
