from odoo import fields,models,api
from odoo.exceptions import UserError
class propertytag(models.Model):
    _name= "estate.property.tag"
    _description= "estate property tage"
    name= fields.Char("name", required=True)
    _sql_constraints=[
        ('unique_property_tag_name','unique(name)',"Le nom de l'étiquette doit être unique.")
    ]
    @api.constrains('name')
    def _unique_property_tag_name(self):
        for record in self:
            duplicates= self.search([('name','=',record.name),('id','!=',record.id)])
            if duplicates:
                raise UserError("le nom de l'ettiquette exite ")