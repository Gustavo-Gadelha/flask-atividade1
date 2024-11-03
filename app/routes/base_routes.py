from flask import Blueprint, url_for, redirect

base_bp = Blueprint('base', __name__)


@base_bp.route('/')
def index():
    return redirect(url_for('product.list_all'))
