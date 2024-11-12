import pandas as pd
import plotly.express as px
from flask import Blueprint, render_template
from sqlalchemy import func

from app import db
from app.models import Sales

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/chart', methods=['GET'])
def chart():
    sales_results = db.session.query(
        func.extract('year', Sales.date).label('year'),
        func.extract('month', Sales.date).label('month'),
        Sales.product_name,
        func.sum(Sales.quantity).label('total_quantity')
    ).group_by('year', 'month', Sales.product_name).order_by('year', 'month').all()

    data = pd.DataFrame(sales_results, columns=['year', 'month', 'product_name', 'total_quantity'])
    data['date'] = data.apply(lambda date: f"{date['year']}-{date['month']}", axis=1)

    figure = px.line(
        data,
        x='date',
        y='total_quantity',
        color='product_name',
        title='Vendas Mensais por Produto',
        labels={'date': 'Data', 'product_name': 'Produto', 'total_quantity': 'Quantidade Total Vendida'},
        markers=True
    )

    figure.update_xaxes(
        tickformat='%b %Y'
    )

    return render_template('sales/chart.html', figure=figure.to_html(full_html=False))
