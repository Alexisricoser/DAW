from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RepartidorEmpleado(models.Model):
    _name = 'repartidor.empleado'
    _description = 'Empleado Repartidor'
    _rec_name = 'dni'

    nombre = fields.Char(string="Nombre", required=True)
    apellido = fields.Char(string="Apellido", required=True)
    dni = fields.Char(string="DNI", required=True)
    telefono = fields.Char(string="Teléfono")
    foto = fields.Binary(string="Foto")

    tiene_carnet_ciclomotor = fields.Boolean(string="Carnet Ciclomotor")
    tiene_carnet_furgoneta = fields.Boolean(string="Carnet Furgoneta")

    reparto_ids = fields.One2many('repartidor.reparto', 'repartidor_id', string="Repartos Realizados")