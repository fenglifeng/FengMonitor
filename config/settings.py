#!/usr/bin/env python
# coding: utf-8
import web

render = web.template.render('templates/', cache=False)

web.config.debug = True


config = web.storage(
    email='fenglifeng1987@163.com',
    site_name = 'ys',
    site_desc = '',
    static = '/static',
)

web.template.Template.globals['render'] = render
web.template.Template.globals['config'] = config

