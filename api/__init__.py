from flask import Blueprint
from .auth import auth
from .guilds import guilds

api = Blueprint('api', __name__, url_prefix='/api')
subdomains = (auth, guilds)

for subdomain in subdomains:
    api.register_blueprint(subdomain)
