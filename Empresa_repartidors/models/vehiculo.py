from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RepartidorVehiculo(models.Model):
    _name = 'repartidor.vehiculo'
    _description = 'Vehículo de Reparto'
    _rec_name = 'matricula'


    tipo = fields.Selection([
        ('bicicleta', 'Bicicleta'),
        ('ciclomotor', 'Ciclomotor'),
        ('furgoneta', 'Furgoneta')
    ], string="Tipo de Vehículo", required=True)
    matricula = fields.Char(string="Matrícula", required=True)
    descripcion = fields.Char(string="Descripción")
    foto = fields.Binary(string="Foto")