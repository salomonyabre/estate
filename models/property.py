from venv import logger
import pytz
from odoo import api, models,fields
from datetime import date, datetime, time, timedelta

class estateproperty(models.Model):
    _name = "estate.property"
    _description= "estate property"
    name=fields.Char('name',required=True) 
    description= fields.Char('description')
    postcode= fields.Char('code postal')
    date_availability=fields.Date('date availability')
    expected_price=fields.Float('expected price',)
    selling_price=fields.Float('selling price',readonly=True)
    bedrooms = fields.Integer('bedrooms',default=2)
    living_area=fields.Integer('liveving area')
    facades=fields.Integer('facades')
    garage=fields.Boolean('garage',default=False)
    garden=fields.Boolean('garden',default=False)
    garden_area=fields.Integer('garden area')
    garden_orientation=fields.Selection(
        string='garden orientation',
        selection=[('nord','Nord'),('sud','Sud'),('est','Est'),('ouest','Ouest')]
    )
    active=fields.Boolean("active",default=True)
  
    statu=fields.Selection(
        string='status',
        selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold and canceled',' Sold and Canceled')]
    )
   
    @api.model
    def default_get(self, fields_list):
        #Définit les valeurs par défaut pour les champs spécifiés ici ces le nom du model qui doit etre ajoute dans le supert.
        defaults = super().default_get(fields_list)

        # Ajout de la date de disponibilité par défaut (+90 jours)
        if 'date_availability' in fields_list:
            defaults['date_availability'] = date.today() + timedelta(days=90)

        return defaults
    