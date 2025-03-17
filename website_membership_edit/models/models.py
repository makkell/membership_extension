# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.http_routing.models.ir_http import slug

class MembershipCategory(models.Model):
    _name = 'membership.membership_category'
    name =  fields.Char(required=True, translate = True )
    company_id = fields.Many2one("res.company")
    view_id = fields.Char()
    url = fields.Char()

    def create_unique_xml_web(self):
        for web in self:
            page_result = self.env['website'].sudo().new_page(
                name=f'{self.name} {self.name}', template="website_membership_edit.page",
                add_menu=False, ispage=False)
            url = f"/members/{slug(self)}/page{page_result['url']}"
            web.view_id = page_result['view_id']
            web.url = url
    
    def create(self, vals_list):
        web_xml = super().create(vals_list)
        web_xml.create_unique_xml_web()
        return web_xml
    
