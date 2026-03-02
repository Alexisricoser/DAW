from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Reparto(models.Model):
    _name = 'repartidor.reparto'
    _description = 'Gestión de Repartos'
    _rec_name = 'codigo'

    codigo = fields.Char(string="Código de Reparto", required=True)

    fecha_recepcion = fields.Datetime(string="Fecha Recepción", default=fields.Datetime.now)
    fecha_inicio = fields.Datetime(string="Fecha Inicio", default=fields.Datetime.now)
    fecha_retorno = fields.Datetime(string="Fecha Retorno")

    repartidor_id = fields.Many2one('repartidor.empleado', string="Repartidor", required=True)
    vehiculo_id = fields.Many2one('repartidor.vehiculo', string="Vehículo", required=True)

    kilometros = fields.Float(string="Kilómetros")
    peso = fields.Float(string="Peso (kg)")
    volumen = fields.Float(string="Volumen")
    observaciones = fields.Text(string="Observaciones")

    urgencia = fields.Selection([
        ('0', 'Órganos humanos'),
        ('1', 'Alimentos refrigerados'),
        ('2', 'Alimentos'),
        ('3', 'Alta prioridad'),
        ('4', 'Baja prioridad'),
    ], string="Urgencia", default='4')

    state = fields.Selection([
        ('no_salido', 'No ha salido'),
        ('en_camino', 'De camino'),
        ('entregado', 'Entregada')
    ], string="Estado", default='no_salido', required=True)

    cliente_emisor_id = fields.Many2one('res.partner', string="Cliente Emisor")
    receptor_nombre = fields.Char(string="Nombre Receptor")

    @api.constrains('repartidor_id', 'vehiculo_id')
    def _check_carnet_conducir(self):
        for record in self:

            if record.repartidor_id and record.vehiculo_id and record.vehiculo_id.tipo == 'ciclomotor' and not record.repartidor_id.tiene_carnet_ciclomotor:
                raise ValidationError("El empleado no tiene carnet de ciclomotor.")

            if record.repartidor_id and record.vehiculo_id and record.vehiculo_id.tipo == 'furgoneta' and not record.repartidor_id.tiene_carnet_furgoneta:
                raise ValidationError("El empleado no tiene carnet de furgoneta.")

    @api.constrains('kilometros', 'vehiculo_id')
    def _check_distancia_vehiculo(self):
        for record in self:
            if record.vehiculo_id.tipo == 'bicicleta' and record.kilometros > 10:
                raise ValidationError("No se pueden recorrer más de 10km en bicicleta.")

            if record.vehiculo_id.tipo == 'furgoneta' and record.kilometros < 1:
                raise ValidationError("No se pueden recorrer menos de 1km en furgoneta.")

    @api.constrains('repartidor_id', 'vehiculo_id', 'state')
    def _check_disponibilidad_reparto(self):
        for record in self:
            if record.state == 'en_camino':
                otros_repartos = self.search([
                    ('id', '!=', record.id),
                    ('state', '=', 'en_camino')
                ])

                for reparto in otros_repartos:
                    if reparto.repartidor_id == record.repartidor_id:
                        raise ValidationError(f"El repartidor ya tiene un viaje.")

                    if reparto.vehiculo_id == record.vehiculo_id:
                        raise ValidationError(f"El vehículo ya está en uso.")