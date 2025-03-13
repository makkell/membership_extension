# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug.urls

from odoo.addons.website_membership.controllers.main import WebsiteMembership
from odoo import http, fields
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import unslug, slug
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class WebMembmerShipFilterTags(WebsiteMembership):
    tags_arr = set()

    @http.route([
        '/members',
        '/members/page/<int:page>',
        '/members/association/<membership_id>',
        '/members/association/<membership_id>/page/<int:page>',

        '/members/country/<int:country_id>',
        '/members/country/<country_name>-<int:country_id>',
        '/members/country/<int:country_id>/page/<int:page>',
        '/members/country/<country_name>-<int:country_id>/page/<int:page>',

        '/members/association/<membership_id>/country/<country_name>-<int:country_id>',
        '/members/association/<membership_id>/country/<int:country_id>',
        '/members/association/<membership_id>/country/<country_name>-<int:country_id>/page/<int:page>',
        '/members/association/<membership_id>/country/<int:country_id>/page/<int:page>',
        '/members/memberships/<membership_id>/tags/<int:tag_id>'
    ], type='http', auth="public", website=True, sitemap=True)
    def members(self, membership_id=None, country_name=None, country_id=0, page=1, **post):
        response = super().members(membership_id, country_name, country_id, page=1)
        tag_id = post.get('tag_id')
        tag_arr = self.tags_arr
        for tag_id in tag_arr:
            if tag_id:
                partner_values = response.qcontext.get('partners').values()


                partner_final = {record_id.id: record_id for record_id in partner_values if tag_id in record_id.category_id.ids}

                membership_partner_ids = response.qcontext.get("memberships_partner_ids")

                set_partners = set(partner_final.keys())
                membership_partner_ids = {key: list(set(value).intersection(set_partners)) for key, value in membership_partner_ids.items()}


                response.qcontext['partners'] = partner_final
                response.qcontext['memberships_partner_ids'] = membership_partner_ids

        print(response.qcontext)
        return response

    @http.route([
        '/members/tags/add/<int:tag_id>/<int:membership_id>',
        '/members/tags/add/<int:tag_id>'
    ], type='http', auth="public", website=False, sitemap=True)
    def AddTagsInArr(self, **post):
        self.tags_arr.add(post.get('tag_id'))
        membership_id = post.get('membership_id') or None
        if membership_id:
            return request.redirect(f'/members/association/{membership_id}')
        else:
            return request.redirect('/members')
    
    @http.route([
        '/members/tags/del'
    ], type='http', auth="public", website=False, sitemap=True)
    def DelTagsInArr(self, **post):
        self.tags_arr.clear()
        return request.redirect('/members')
        



            