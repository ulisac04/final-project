# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = []
sites.append({'label': 'All Sites', 'value': 'ALL'})

for item in spacex_df["Launch Site"].unique():
    sites.append({'label': item, 'value': item})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection

                                dcc.Dropdown(id='site-dropdown',
                                             placeholder="Select a Launch Site here",
                                             searchable=True,
                                             value='ALL',
                                             options=sites),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       1000: '1000',
                                                        2000: '2000',
                                                        3000: '3000',
                                                        4000: '4000',
                                                        5000: '5000',
                                                        6000: '6000',
                                                        7000: '7000',
                                                        8000: '8000',9000: '9000',10000: '10000',
                                                       },
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
         ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, rangevalues):
    if entered_site == 'ALL':
        dd = spacex_df[(spacex_df["Payload Mass (kg)"] >= rangevalues[0]) & (spacex_df["Payload Mass (kg)"] <= rangevalues[1])]
        fig = px.scatter(dd, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    else:
        dd = spacex_df[(spacex_df["Launch Site"] == entered_site) & (spacex_df["Payload Mass (kg)"] >= rangevalues[0]) & (spacex_df["Payload Mass (kg)"] <= rangevalues[1])]
        fig = px.scatter(dd, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    return fig


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        proporcion_por_sitio = spacex_df['Launch Site'].value_counts(normalize=True).reset_index()
        proporcion_por_sitio.columns = ['Launch Site', 'Proporción']

        # Crear un gráfico de pastel con plotly.express
        fig = px.pie(proporcion_por_sitio, values='Proporción', names='Launch Site',
                     title='Proporción de lanzamientos por sitio')
        return fig
    else:
        df_filtrado = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Contar la cantidad de ocurrencias de cada clase en el sitio de lanzamiento seleccionado
        conteo_clases = df_filtrado['class'].value_counts().reset_index()
        conteo_clases.columns = ['class', 'conteo']

        # Crear un gráfico de pastel con plotly.express
        fig = px.pie(conteo_clases, values='conteo', names='class')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()