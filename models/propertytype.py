
from odoo import api, models,fields
from datetime import date, datetime, time, timedelta

class estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description= "estate property type"
    name=fields.Char('name',required=True) 