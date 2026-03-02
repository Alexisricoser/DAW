from odoo import http
from odoo.http import request


class RepartoController(http.Controller):

    @http.route('/reparto/status/<codigo>', auth='none', type='http')
    def consultar_estado(self, codigo):
        reparto = request.env['repartidor.reparto'].sudo().search([('codigo', '=', codigo)])

        if reparto:
            return f"Estado de {codigo}: {reparto.state}"
        return "No encontrado"