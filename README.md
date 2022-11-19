# PM2.5 - visualization

## LINK: https://airvisualization.herokuapp.com/
- if the link does not work it means that my heroku license is paused, as when the app is not needed

## Project 
- Simple web app for visualising the level of particulate matter (PM2.5), which is the most prominent component of air pollution in Northern Thailand
- data were collected by monitoring stations in Northern Thailand and I accessed them at through my internship at the Environmental Science Research Center, Faculty of Science, Chiang Mai  (https://www.science.cmu.ac.th)

## Files & folders
**Data_prep.py** - definition of several useful functions and data preprocessing (yearly_data -> PM25_11_2020.xlsx)

**Dash_app.py** - the web application using Plotly & Dash. Meant for deployment on heroku.com

**Procfile** - file needed for connecting the Dash_app.py with Heroku server

**requirements.txt** - all libraries (versions) needed for the Dash_app.py

**List of AQM stations_PCD.docx** - list of air quality monitoring stations in Northern Thailand

**example1.png, example2.png** - two examples of the app functionality

## References:
- https://plotly.com/
- https://dash.plotly.com/
