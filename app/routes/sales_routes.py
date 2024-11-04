import pandas as pd
import plotly.express as px
from flask import Blueprint, render_template
from sqlalchemy import func

from app import db
from app.models import Sales

sales_bp = Blueprint('sales', __name__)

months_translation = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}


@sales_bp.route('/chart', methods=['GET'])
def chart():
    sales_results = db.session.query(
        func.extract('month', Sales.date).label('month'),
        Sales.product_name,
        func.sum(Sales.quantity).label('total_quantity')
    ).group_by('month', Sales.product_name).order_by('month').all()

    data = pd.DataFrame(sales_results, columns=['month', 'product_name', 'total_quantity'])
    data['month'] = data['month'].apply(lambda month: months_translation[month])

    figure = px.line(
        data,
        x='month',
        y='total_quantity',
        color='product_name',
        title='Vendas Mensais por Produto',
        labels={'month': 'Mês', 'product_name': 'Produto', 'total_quantity': 'Quantidade Total Vendida'},
        markers=True
    )

    return render_template('sales/chart.html', figure=figure.to_html())
