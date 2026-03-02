from odoo import models, fields, api

class CrearRepartoWizard(models.TransientModel):
    _name = 'repartidor.crear.reparto.wizard'
    _description = 'Asistente para crear repartos'

    codigo = fields.Char(string="Código de Reparto", required=True)
    repartidor_id = fields.Many2one('repartidor.empleado', string="Repartidor", required=True)
    vehiculo_id = fields.Many2one('repartidor.vehiculo', string="Vehículo", required=True)
    cliente_emisor_id = fields.Many2one('res.partner', string="Cliente Emisor", required=True)
    receptor_nombre = fields.Char(string="Nombre del Receptor")
    urgencia = fields.Selection([
        ('0', 'Órganos humanos'),
        ('1', 'Alimentos refrigerados'),
        ('2', 'Alimentos'),
        ('3', 'Alta prioridad'),
        ('4', 'Baja prioridad'),
    ], string="Urgencia", default='4')
    fecha_recepcion = fields.Datetime(string="Fecha Recepción", default=fields.Datetime.now)
    fecha_inicio = fields.Datetime(string="Fecha Inicio", default=fields.Datetime.now)
    fecha_retorno = fields.Datetime(string="Fecha Retorno")
    kilometros = fields.Float(string="Kilómetros Previstos")
    volumen = fields.Float(string="Volumen Previsto")
    peso = fields.Float(string="Peso (kg) Previsto")
    observaciones = fields.Text(string="Observaciones")

    def action_crear(self):
        self.env['repartidor.reparto'].create({
            'codigo': self.codigo,
            'repartidor_id': self.repartidor_id.id,
            'vehiculo_id': self.vehiculo_id.id,
            'urgencia': self.urgencia,
            'cliente_emisor_id': self.cliente_emisor_id.id,
            'receptor_nombre': self.receptor_nombre,
            'fecha_recepcion': self.fecha_recepcion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_retorno': self.fecha_retorno,
            'kilometros': self.kilometros,
            'volumen': self.volumen,
            'peso': self.peso,
            'observaciones': self.observaciones,
            'state': 'no_salido',
        })