import sqlite3
import pandas as pd
import gradio as gr

# 顯示折線圖（lineplot）

connection = sqlite3.connect("data/covid_19.db")
time_series = pd.read_sql("""SELECT * FROM time_series;""", con=connection)
connection.close()
time_series = time_series[time_series["country"] == "Taiwan*"]
time_series["reported_on"] = pd.to_datetime(time_series["reported_on"])

with gr.Blocks() as demo:
    gr.Markdown("""# Covid 19 Country Time Series""")
    gr.LinePlot(time_series, x="reported_on", y="confirmed")
    gr.LinePlot(time_series, x="reported_on", y="deaths")
    gr.LinePlot(time_series, x="reported_on", y="doses_administered")

demo.launch()