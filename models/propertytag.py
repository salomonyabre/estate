from odoo import fields,models
class propertytag(models.Model):
    _name= "estate.property.tag"
    _description= "estate property tage"
    name= fields.Char("name")