from datetime import timedelta
from odoo import models,fields,api
class propertyoffer (models.Model):
    _name="estate.property.offer"
    _description= "estate property offer"
    price=fields.Float(string="price")
    validity=fields.Integer("validity(day)",default=7)
    create_date = fields.Date(string="Creation Date", readonly=True,)
    date_deadline=fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline",
        store=True)
    status=fields.Selection(
        string="status",copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')]
    ) 
    partner_id=fields.Many2one('res.partner',string="partner",required=True)
    property_id=fields.Many2one('estate.property',string= "property id",required=True)

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

