# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class mklab_web_addit_fields(models.Model):
    _inherit = 'res.partner'
    people_spec = fields.Many2one(string='Специальность', comodel_name='res.partner.speciality')
    people_custom_spec = fields.Char('Специализация')
    education = fields.Char('Образование')
    telegram = fields.Char('Телеграмм')
    citizenship = fields.Selection(string='Я гражданин РФ?', selection=[
        ('0', 'Нет'),
        ('1', 'Да'),
    ], ondelete='cascade')


class mklab_web_citizen(models.Model):
    _name = 'res.partner.citizenship'

    name = fields.Char('Вариант ответа')

class mklab_web_speciality(models.Model):
    _name = 'res.partner.speciality'

    name = fields.Char('Специальность')


class Contact(models.AbstractModel):
    _inherit = 'ir.qweb.field.contact'
