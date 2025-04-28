import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from dash.dash_table import DataTable

# Initialize app
app = dash.Dash(__name__)

# Sample data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=30)
sales = np.random.randint(100, 500, size=(30,))
df = pd.DataFrame({'Date': dates, 'Sales': sales})
df['Category'] = np.random.choice(['A', 'B', 'C'], size=30)

# Plot
fig = px.bar(df, x='Date', y='Sales', title='Sales Over Time')
fig2 = px.bar(df, x='Category', y='Sales', title='Sales by Category')
fig3 = px.line(df, x='Date', y='Sales', color='Category', title='Sales Trend by Category')
fig4 = px.pie(df, names='Category', values='Sales', title='Sales Distribution by Category')

# Layout
app.layout = html.Div(children=[
    html.H1(children='📈 Sales Dashboard', style={'textAlign': 'center'}),
    
    # Filtro de fecha
    html.Div(children=[
        html.Label('Select Date Range:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['Date'].min(),
            end_date=df['Date'].max(),
            display_format='YYYY-MM-DD'
        ),
    ], style={'textAlign': 'center'}),
    
    # Gráficos
    dcc.Graph(id='sales-graph', figure=fig),
    dcc.Graph(id='category-sales', figure=fig2),
    dcc.Graph(id='sales-trend', figure=fig3),
    dcc.Graph(id='category-pie', figure=fig4),
    
    # Información
    html.Div(children=[
        html.P(f"Total Sales: ${df['Sales'].sum():,}"),
        html.P(f"Average Daily Sales: ${df['Sales'].mean():.2f}")
    ], style={'textAlign': 'center', 'fontSize': '18px'}),
    
    # Tabla con datos
    DataTable(
        id='sales-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records')
    ),
])

# Callbacks para actualizar gráficos
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    fig = px.bar(filtered_df, x='Date', y='Sales', title='Sales Over Time')
    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
