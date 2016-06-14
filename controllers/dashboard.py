# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    return dict(message="hello from dashboard.py")
