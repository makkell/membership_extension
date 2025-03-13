# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import Warning
import random, urllib
import requests
from datetime import datetime, timedelta
from base64 import b64encode
import logging
_logger = logging.getLogger(__name__)

class WizardAuth(models.TransientModel):
    _name = 'rekassa.wizardauth'
    _description = 'Авторизация'
    address = fields.Char(string="URL-адрес кассы: ")
    apiKey = fields.Char(string="Ключ для доступа к API: ")
    login = fields.Char(string="Серийный номер кассы: ")
    password = fields.Char(string="Пароль: ")
    journal_id = fields.Many2one('account.journal')
    many_kassa_id = fields.Boolean()
    show_text = fields.Boolean()
    text_message = fields.Text(
        default='Журнал с таким Серийным номером ККТ уже существует. Во избежание ошибок доступа к сервису Rekassa выберите один из следующих вариантов:\n1. Использовать существующие данные для указанного uuid\n2. Запросить новые данные для доступа к сервису и обновить их для всех журналов с этим серийным номером\n',
        readonly=1)

    def get_auth(self):
        for s in self:
            apikey = s.apiKey
            address = s.address
            login = s.login
            password = s.password
            url = str(address)+"/api/auth/login?apiKey="+str(apikey)+"&format=json"
            headerst = {'Content-Type': 'application/json'}
            req = requests.post(url, headers=headerst, json={'number': login, 'password': password})
            if req.status_code in [200, 201]:
                res = req.json()
                message = self.env['account.payment'].search_error(res)
                if 'error' in res:
                    raise Warning(message)
                else:
                   if 'serialNumber' in res and 'id' in res and 'token' in res:
                        new_id = res['id']
                        new_token = res['token']
                        s.journal_id.kassa_uid = apikey
                        s.journal_id.kassa_address = address
                        s.journal_id.kassa_password = password
                        s.journal_id.kassa_token = new_token
                        s.journal_id.kassa_id = new_id

                   if s.many_kassa_id: s.update_journals()
            else:
                raise Warning('Ошибка подключения к сервису reKassa')

    def update_journals(self):
        for s in self:
          all_kassa = self.env['account.journal'].search([('kassa_login', '=', s.journal_id.kassa_login)])
          if all_kassa:
                for k in all_kassa:
                    k.kassa_token = s.journal_id.kassa_token
                    k.kassa_id = s.journal_id.kassa_id
                    k.kassa_address = s.journal_id.kassa_address
                    k.kassa_password = s.journal_id.kassa_password

    def update_auth_and_journals(self):
        for s in self:
            return {
                'name': ("Авторизация"),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'rekassa.wizardauth',
                'view_id': self.env.ref('rekassa.form').id,
                'target': 'new',
                'context': {'default_many_kassa_id': True,
                            'default_show_text': False,
                            'default_journal_id': s.journal_id.id,
                            }
            }
