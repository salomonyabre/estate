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
    date_availability=fields.Date('date availability',copy=False)
    expected_price=fields.Float('expected price',required=True)
    selling_price=fields.Float('selling price',readonly=True,copy=False)
    bedrooms = fields.Integer('bedrooms',default=2)
    living_area=fields.Integer('liveving area')
    facades=fields.Integer('facades')
    garage=fields.Boolean('garage',default=False)
    garden=fields.Boolean('garden',)
    garden_area=fields.Integer('garden area')
    total_areas=fields.Float(compute="_calcule_total")
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True
    )
    garden_orientation=fields.Selection(
        string='garden orientation',
        selection=[('nord','Nord'),('sud','Sud'),('est','Est'),('ouest','Ouest')]
    )
    state=fields.Boolean("active",default=False)
   
    status=fields.Selection(
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
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    
    Salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner",string="Acheteur", copy=False)
    tag_ids=fields.Many2many("estate.property.tag",string="property tag", required= True)
    offer_ids=fields.One2many('estate.property.offer',"property_id",string="offer")

    @api.depends('living_area',"garden_area")
    def _calcule_total(self):
        for record in self:
            record.total_areas=record.living_area + record.garden_area
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price=max(record.offer_ids.mapped('price'),default=0)
            
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation='nord'
        else:
            self.garden_area=0
            self.garden_orientation=False

            
