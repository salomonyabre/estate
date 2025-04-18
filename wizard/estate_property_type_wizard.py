from odoo import models, fields

class EstatePropertyTypeWizard(models.TransientModel):
    _name = 'estate.property.type.wizard'
    _description = 'Wizard to create a new property type'

    name = fields.Char(string="Name", required=True)

    def action_confirm(self):
        self.env['estate.property.type'].create({'name': self.name})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'estate.property',
            'view_mode': 'tree,form',
            'target': 'current',
        }
