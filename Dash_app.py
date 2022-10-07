import pandas as pd
import numpy as np
import datetime as dt

from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go

import dash_daq as daq
import dash_bootstrap_components as dbc

from Data_prep import make_dataframe, nth_day_to_date

magma = px.colors.sequential.Magma


month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
    }

#CREATE A BASE DATAFRAME df
years = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
stations = ["35T","36T","37T"]

df = make_dataframe(stations = stations, years = years)

#COLOR DISCRETE MAP
color_discrete_map = dict(zip([2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021], [px.colors.qualitative.Vivid[n] for n in range(11)]))

#DASH APP
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

controls = html.Div([
    html.H3("Controls"),
    html.Div(
        dcc.Dropdown(id="station",
            options=[{"label": "35T", "value": "35T"},
                    {"label": "36T", "value": "36T"},
                    {"label": "37T", "value": "37T"}],
            multi=False,
            style={'color': 'black'},
            value="36T"),
        className="p-1 bg-light border"),
    html.Div(
        dcc.Checklist(id='checklist',
            options = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021],
            value = [2014,2020],
            inline=True),
        className="p-1 bg-dark border"),
    html.Div(
        daq.BooleanSwitch(id='show_standard',
            label='Show standard',
            on=True,
            color="#AEAEAE"),
        className="p-1 bg-dark border"),
    html.Div([
        html.Small("select standard"), 
        dcc.Slider(0, 60,
            value=50,
            marks={
                0: '0 ug/m3',
                20: '20 ug/m3',
                37.5: '37.5 ug/m3',
                50: '50 ug/m3'
            },
            id='standard')], 
        className="p-1 bg-light border")
], className="d-grid gap-3") #spread child elements evenly with gap 4

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Dashboard", className="text-center"), html.Br(), 
        html.Div(" Dashboard for displaying various data related to atmospheric pollution in Northern Thailand"),
        html.Br()],
        width=12)
    ]),
    dbc.Row([
        dbc.Col(controls, width=4),
        dbc.Col([dcc.Graph(id='graph')])
    ], className="d-flex align-items-center"), 
    dbc.Row([
        html.Div(id='update_standard', className="fs-6 "),
    ], align="end", style= {"height": "50px"}, ),
    dbc.Row([dash_table.DataTable(id='table', style_data={
        'whiteSpace': 'normal',
        'width': '160px'}, style_cell={'color': '#000C66'})
    ]),
    dbc.Row([dcc.Graph(id='graph2')])

])

@app.callback(
    Output("graph", "figure"), 
    Output("graph2", "figure"),
    Output("update_standard","children"),
    Output("table","data"),
    Input("station", "value"), 
    Input("checklist", "value"),
    Input("show_standard", "on"),
    Input("standard", "value")
)
def update_figure(station, years, show_standard, standard):
    station = station
    years = years
    show_standard = show_standard
    standard = standard
    tickvals = [0, 50 ,100, 150, 200, 250, 300, 350]
    colorscale = [[0, magma[1]],[0.2, magma[5]],[0.5, magma[9]],[0.7, magma[9]],[1., magma[9]]]
    show_marker = True
    
    print(years)
    print(show_standard)
    print(standard)
    print(station)
    print(show_marker)
    
    dff = df.copy()
    df_ = dff[['Year','Month','nth',station]] #df_ is going to be used for heatmap (displays all years)
    df_c = df_[df_['Year'].isin(years)] #df_c is used in line graph (displays only selected years)
    df_c['Date'] = df['Date'].apply(lambda x: x.strftime('%d-%m-%Y')) #I need this column for custom data

    #TABLE
    pivot_t = df_.groupby(["Year", "Month"])[station].apply(lambda x: x[x > standard].count()/x.count()).to_frame() #count only if the column value > stan
    pivot_t = pivot_t.unstack()
    pivot_t.columns = [c[1] for c in pivot_t.columns]
    pivot_t = pivot_t.applymap(lambda x: x*100)
    pivot_t = pivot_t.applymap(lambda x: round(x, 0))
    pivot_t = pivot_t.reset_index()
    pivot_t = pivot_t[pivot_t["Year"].isin(years)]
    pivot_t.columns = ["Year"]+[month_dict[x] for x in pivot_t.columns if (x!="Year")]

    #HEATMAP 
    fig2 = go.Figure() 
    fig2.add_trace(go.Heatmap(
        x = df_['nth'],
        y = df_['Year'],
        z = df_[station],
        text = [nth_day_to_date(int(df_.loc[i,'nth']),2018).strftime('%d/%m') for i in range(len(df_))],
        hovertemplate = 'day: %{text} <br> year: %{y} <br> PM2.5: %{z} ug/m3',
        colorscale = colorscale,
        showlegend=False,
        colorbar=dict(title="ug/m3"),
        name = '',
    ))
    
    fig2.update_layout(
        xaxis=dict(range=[0,366], title="Day", tickvals = tickvals, ticktext = [nth_day_to_date(x, 2018).strftime('%d/%m') for x in tickvals ]),
        yaxis=dict(title="Year", tickvals = list(range(2011,2022))),
        title=dict(text=F"PM2.5 at station {station} ",
                  x=0.5)
    ) 
    
    #if no years selected -> only heatmap displayed
    if years == []:
        fig = go.Figure()
        fig.update_layout(
        xaxis=dict(range=[0,366], title="Day in the year", tickvals = tickvals, ticktext = [nth_day_to_date(x, 2018).strftime('%d/%m') for x in tickvals ]),
        yaxis=dict(range=[0,270], title="ug/m3"),
        title=dict(text=F"PM2.5 at station {station} ", x=0.5))
        return fig, fig2, F"number of measurements > {standard} ug/m3 (%)", pivot_t.to_dict('records')
        
    #LINE GRAPH
    fig = px.line(df_c,
                  x='nth',
                  y=station,
                  color='Year',
                  color_discrete_map=color_discrete_map,
                  custom_data= ['Date'])

    fig.update_traces(hovertemplate = 'date: %{customdata[0]} <br> PM2.5 : %{y} ug/m3')
    
    if show_standard==True:
        #adding horizontal dashed line (the treshold)
        fig.add_shape(type='line',
                x0=0,
                y0=standard,
                x1=365,
                y1=standard,
                line=dict(color='black', dash="dot", width=2)
        )
        
        #adding annotation
        fig.add_annotation(
            xref="x",
            yref="y",
            x=330,
            y=standard+10,
            text='standard',
            showarrow=False
        )
        
        trace_list = []
        for year in years:
            df_cc = df_c[(df_c[station]>=standard) & (df_c['Year']==year)]
            trace = go.Scatter(x=df_cc['nth'], 
                               y=df_cc[station],
                               mode='markers', 
                               marker_color = color_discrete_map[year],
                               hovertemplate = 'date: %{text} <br> PM2.5: %{y} ug/m3',
                               text = df_cc['Date'],
                               showlegend=False,
                               name=year)
            trace_list.append(trace)
        fig.add_traces(trace_list)

    
    fig.update_layout(
        xaxis=dict(range=[0,366], title="Day in the year", tickvals = tickvals, ticktext = [nth_day_to_date(x, 2018).strftime('%d/%m') for x in tickvals ]),
        yaxis=dict(range=[0,270], title="ug/m3"),
        title=dict(text=F"PM2.5 at station {station} ",
                  x=0.5)
    )
        
    return fig, fig2, F"number of measurements > {standard} ug/m3 (%)", pivot_t.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)