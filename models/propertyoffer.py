from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo import models,fields,api
from odoo.exceptions import UserError

class propertyoffer (models.Model):
    _name="estate.property.offer"
    _description= "estate property offer"
    _order=" price desc"
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status",)

    price=fields.Float(string="price")
    validity=fields.Integer("validity(day)",default=7)
    #create_date = fields.Date(string="Creation Date", readonly=True,)
    date_deadline=fields.Datetime(compute="_compute_date_deadline", inverse="_inverse_date_deadline",
        store=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)
    partner_id=fields.Many2one('res.partner',string="partner",required=True)
    property_id=fields.Many2one('estate.property',string= "property id",required=True,ondelete='cascade')
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)',"le prix doit est positive" ),
    ]
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Calcule la date de fin de validité (deadline) en ajoutant validity à create_date."""
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Permet de modifier soit la date_deadline, soit validity."""
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.create_date = record.date_deadline - timedelta(days=record.validity)
                
    def action_accept(self):
        """ Accepter l'offre et mettre à jour l'acheteur et le prix de vente """
        for offer in self:
            #expected_price = offer.property_id.expected_price
            #if expected_price and offer.price < 0.9 * expected_price:
            #    raise UserError("L'offre doit être au moins de 90 % du prix attendu.")
            if offer.property_id.buyer_id:
                # Option 1 : lever une erreur (comportement actuel)
                # raise UserError("Une offre a déjà été acceptée pour ce bien.")    
                # Option 2 : remplacer l'offre existante par la nouvelle
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.expected_price = offer.price
                offer.property_id.selling_price = offer.price
                
                offer.status = 'accepted'
            else:
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
    
    def action_refuse(self):
        """ Refuser l'offre """
        self.status = 'refused'
        

    @api.constrains('price')
    def _check_price_positive(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Le prix  dans l'offre doit être strictement positif.")
    
    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals.get('property_id'))

        # Vérifier si l'offre est inférieure à une offre existante
        existing_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', property_id.id)
        ])
        if existing_offers and vals.get('price') < max(existing_offers.mapped('price')):
        
            max_offer_price = max(existing_offers.mapped('price')) if existing_offers else 0.0
            raise ValidationError(f"L'offre doit être supérieure à {max_offer_price}.")
            #raise ValidationError("L'offre doit être supérieure  à la meilleure offre existante qui est ." )

        # Mettre à jour l'état de la propriété à "Offre reçue"
        property_id.state = 'offer_received'

        return super().create(vals)
    