
from odoo import api, models,fields
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError
class estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description= "estate property type"
    name=fields.Char('name',required=True) 
    _sql_constraints = [
        ('unique_property_type_name','unique(name)',"Le nom du type de propriete doit être unique.")
    ]
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            # Recherche d'autres enregistrements avec le même nom
            duplicates = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if duplicates:
                raise UserError("Le nom du type de propriété doit être unique.")

