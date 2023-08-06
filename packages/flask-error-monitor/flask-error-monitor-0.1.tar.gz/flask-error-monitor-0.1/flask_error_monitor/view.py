# -*- coding: utf-8 -*-
#     Exception formatter defaults view
#
#     :copyright: 2018 Sonu Kumar
#     :license: BSD-3-Clause
#

import os

from flask import url_for, render_template, abort, redirect, request, blueprints

root_path = os.path.abspath(os.path.dirname(__file__))


class Views(object):
    def __init__(self, app, model, url_prefix):
        model = model
        blueprint = blueprints.Blueprint("app_error", 'app_error',
                                         root_path=root_path,
                                         template_folder="templates", url_prefix=url_prefix)

        @blueprint.route('/')
        def view_list():
            title = "App Error"
            page = request.args.get('page', 1, type=int)
            error = False
            errors = model.get_exceptions_per_page(page_number=page)
            next_url = url_for('app_error.view_list', page=errors.next_num) \
                if errors.has_next else None
            prev_url = url_for('app_error.view_list', page=errors.prev_num) \
                if errors.has_prev else None
            return render_template('list.html', error=error, title=title, errors=errors,
                                   next_url=next_url, prev_url=prev_url)

        @blueprint.route('/<string:rhash>')
        def view_detail(rhash):
            obj = model.get(rhash)
            error = False
            if obj is None:
                abort(404)
            title = "%s : %s" % (obj.method, obj.path)

            return render_template('detail.html', error=error, title=title, obj=obj)

        @blueprint.route('/delete/<string:rhash>')
        def view_delete(rhash):
            model.delete(rhash)
            return redirect(url_for('app_error.view_list'))

        app.register_blueprint(blueprint)
