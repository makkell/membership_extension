# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import Warning
import random, urllib
import requests
from datetime import datetime, timedelta
from base64 import b64encode

class WizardMes(models.TransientModel):
    _name='rekassa.wizardmessages'
    _description='Авторизация'

    message_text = fields.Text(readonly=1)
