from . import  models,fields 

class estate_property(models.Models):
    _name = "estate.property"
    _description= "estate property"

    name= fields.char(required=True)
    description= fields.char()
    postcode= fields.char()
    date_availability=fields.data()
    expected_price=fields.float( required=True)
    selling_price=fields.float()
    bedrooms=fields.Integer()
    living_area=fields.integer()
    facades=fields.integer()
    garage=fields.Boolean(bool,defauld=False)
    garden=fields.Boolean(bool,defauld=False)
    garden_area=fields.interger()
    garden_orientation=fields.selection(
        String='type',
        selection=[('Nord','Sud','Est','Ouest')]
    )
