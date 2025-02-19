from odoo import models,fields
class propertyoffer (models.Model):
    _name="estate.property.offer"
    _description= "estate property offer"
    price=fields.Float(string="price")
    status=fields.Selection(
        string="status",copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')]
    ) 
    partner_id=fields.Many2one('res.partner',string="partner",required=True)
    property_id=fields.Many2one('estate.property',string= "property id",required=True)