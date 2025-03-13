import base64

from odoo import _, http
from odoo.http import content_disposition, Controller, request, route
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import logging
_logger = logging.getLogger(__name__)

class PartnerCustomerPortal(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "phone", "email"]
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("city")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("street")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("country_id")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("people_spec")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("people_custom_spec")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("education")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("telegram")
    CustomerPortal.OPTIONAL_BILLING_FIELDS.append("image_1920")

    def _prepare_portal_layout_values(self):
        values = super(PartnerCustomerPortal, self)._prepare_portal_layout_values()
        _logger.warning(str(values))
        partner = request.env.user.partner_id
        people_custom_spec = partner.people_custom_spec
        education = partner.education
        telegram = partner.telegram
        specialityVals = request.env['res.partner.speciality'].sudo().search([])
        values.update({
            'people_spec_vals': specialityVals,
            'people_custom_spec': people_custom_spec,
            'education': education,
            'telegram': telegram,
        })
        _logger.warning(str(partner))
        _logger.warning(str(values))
        return values

    @route()
    def account(self, redirect=None, **post):
        if 'image_1920' in post:
            image_1920 = post.get('image_1920')
            if image_1920:
                image_1920 = image_1920.read()
                image_1920 = base64.b64encode(image_1920)
                request.env.user.partner_id.sudo().write({
                    'image_1920': image_1920
                })
            post.pop('image_1920')
        if 'clear_avatar' in post:
            request.env.user.partner_id.sudo().write({
                'image_1920': False
            })
            post.pop('clear_avatar')
        return super(PartnerCustomerPortal, self).account(redirect=redirect, **post)

