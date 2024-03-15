#!/usr/bin/python3
"""init Blueprint and imports index func"""

from flask import Blueprint, render_template


app_views = Blueprint('app_view', __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
