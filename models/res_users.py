from odoo import models, fields
class ResUsers(models.Model):
        _inherit = "res.users"

        property_ids = fields.One2many(
        "estate.property",  # Modèle cible
        "salesperson_id",        # Champ Many2one dans estate.property
        string="Identifiants de propriété",
        domain=[("state", "=", "nouveau")]  # Filtrer uniquement les propriétés disponibles
    )