
from odoo import api, models,fields
from datetime import date, datetime, time, timedelta
from odoo.exceptions import UserError
class estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description= "estate property type"
    _order="name"
    name=fields.Char('name',required=True) 
    
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    property_ids = fields.One2many('estate.property','property_type_id',string="Propriétés")

    sequence=fields.Integer("sequence",default=10)
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
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

