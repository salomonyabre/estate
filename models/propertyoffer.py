from datetime import timedelta
from odoo import models,fields,api
from odoo.exceptions import UserError
class propertyoffer (models.Model):
    _name="estate.property.offer"
    _description= "estate property offer"
    price=fields.Float(string="price")
    validity=fields.Integer("validity(day)",default=7)
    #create_date = fields.Date(string="Creation Date", readonly=True,)
    date_deadline=fields.Datetime(compute="_compute_date_deadline", inverse="_inverse_date_deadline",
        store=True)
    status=fields.Selection(
        string="status",copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')]
    ) 
    partner_id=fields.Many2one('res.partner',string="partner",required=True)
    property_id=fields.Many2one('estate.property',string= "property id",required=True)
    _sql_constraints = [
        ('check_offer_price_positive',
         'CHECK(price >= 0)',
         "Le prix d'offre doit être strictement positif.")
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
            if offer.property_id.buyer_id:
                # Option 1 : lever une erreur (comportement actuel)
                # raise UserError("Une offre a déjà été acceptée pour ce bien.")
                
                # Option 2 : remplacer l'offre existante par la nouvelle
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer_accepted'
                offer.status = 'accepted'
            else:
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer_accepted'

    def action_refuse(self):
        """ Refuser l'offre """
        self.status = 'refused'