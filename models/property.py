from odoo import models, fields # type: ignore

class estateproperty(models.Model):
    _name = "estate.property"
    _description= "estate property"

    
    name = fields.Char() 

    description= fields.Char()
    postcode= fields.Char()
    #date_availability=fields.data()
    expected_price=fields.Float( )
    selling_price=fields.Float()
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean(bool,defauld=False)
    garden=fields.Boolean(bool,defauld=False)
    garden_area=fields.Integer()
    #garden_orientation=fields.Selection(
        #String='type',
        #Selection=[('Nord','Sud','Est','Ouest')]
    #)
