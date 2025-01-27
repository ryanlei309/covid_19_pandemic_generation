import pandas as pd
import sqlite3

class CreateCovid19DB:
    def create_time_series(self):
        confirmed = pd.read_csv("data/time_series_covid19_confirmed_global.csv")
        deaths = pd.read_csv("data/time_series_covid19_deaths_global.csv")
        vaccine = pd.read_csv("data/time_series_covid19_vaccine_global.csv")

        id_variables = ["Province/State", "Country/Region", "Lat", "Long"]
        melted_confirmed = pd.melt(confirmed, id_vars=id_variables, var_name="Date", value_name="Confirmed")
        melted_deaths = pd.melt(deaths, id_vars=id_variables, var_name="Date", value_name="Deaths")
        melted_confirmed["Date"] = pd.to_datetime(melted_confirmed["Date"], format="%m/%d/%y")
        melted_deaths["Date"] = pd.to_datetime(melted_deaths["Date"], format="%m/%d/%y")

        # Adjust vaccine columns: Change province state data type and rename
        vaccine["Province_State"] = vaccine["Province_State"].astype(object)
        vaccine["Date"] = pd.to_datetime(vaccine["Date"])
        vaccine = vaccine.rename(columns={"Province_State": "Province/State", "Country_Region": "Country/Region"})
        melted_confirmed = melted_confirmed.drop(labels=["Lat", "Long"], axis=1)
        melted_deaths = melted_deaths.drop(labels=["Lat", "Long"], axis=1)
        vaccine = vaccine.drop(labels=["UID", "People_at_least_one_dose"], axis=1)

        # Connect dataframe
        join_keys = ["Province/State", "Country/Region", "Date"]
        time_series = pd.merge(melted_confirmed, melted_deaths, left_on=join_keys, right_on=join_keys, how="left")
        time_series = pd.merge(time_series, vaccine, left_on=join_keys, right_on=join_keys, how="left")
        time_series = time_series.drop(labels="Province/State", axis=1)
        time_series = time_series.groupby(["Country/Region", "Date"])[["Confirmed", "Deaths", "Doses_admin"]].sum().reset_index()

        # Rename and change type columns in time_series
        time_series.columns = ["country", "reported_on", "confirmed", "deaths", "doses_administered"]
        time_series["doses_administered"] = time_series["doses_administered"].astype(int)
        
        return time_series

    def create_daily_report(self):
        daily_report = pd.read_csv("data/03-09-2023.csv")

        # Select the fields that we only need.
        daily_report = daily_report[["Country_Region", "Province_State", "Admin2", "Confirmed", "Deaths", "Lat", "Long_"]]

        # Rename the columns in daily_report. 
        daily_report.columns = ["country", "province", "county", "confirmed", "deaths", "latitude", "longitude"]

        return daily_report

    def create_database(self):
        time_series = self.create_time_series()
        time_series["reported_on"] = time_series["reported_on"].map(lambda x: x.strftime("%Y-%m-%d"))
        daily_report = self.create_daily_report()
        connection = sqlite3.connect("data/covid_19.db")
        time_series.to_sql("time_series", con=connection, if_exists="replace", index=False)
        daily_report.to_sql("daily_report", con=connection, if_exists="replace", index=False)
        connection.close()

create_covid_19_db = CreateCovid19DB()
create_covid_19_db.create_database()



