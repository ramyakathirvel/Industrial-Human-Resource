import streamlit as st
import pandas as pd
import plotly.express as px
import csv

# Load data
@st.cache_data
def load_data():
         df=pd.read_csv("data.csv", encoding='ISO-8859-1')
         df = df.applymap(lambda x: x.strip('`').strip() if isinstance(x, str) else x)
         worker_columns = [col for col in df.columns if 'Workers' in col]
         df[worker_columns] = df[worker_columns].apply(pd.to_numeric, errors='coerce')
         return df

df = load_data()

# Static filter values for demo/testing purposes
selected_state = "STATE - NCT OF DELHI"
selected_division = "01"
selected_industry = "Growing of rice"

filtered_df = df[(df["India/States"] == selected_state) &
                 (df["Division"] == selected_division) &
                 (df["NIC Name"] == selected_industry)]

main_total = filtered_df[[
    "Main Workers - Total - Males", "Main Workers - Total - Females"
]].sum()
marginal_total = filtered_df[[
    "Marginal Workers - Total - Males", "Marginal Workers - Total - Females"
]].sum()

fig_main = px.pie(names=main_total.index, values=main_total.values, 
                  title="Main Workers by Gender")
fig_marginal = px.pie(names=marginal_total.index, values=marginal_total.values, 
                      title="Marginal Workers by Gender")

rural_urban = filtered_df[[
    "Main Workers - Rural -  Persons", "Main Workers - Urban -  Persons",
    "Marginal Workers - Rural -  Persons", "Marginal Workers - Urban -  Persons"
]].sum().reset_index()
rural_urban.columns = ["Category", "Count"]
fig_scatter = px.scatter(rural_urban, x="Category", y="Count", color="Category",
                 title="Distribution of Workers by Area and Type")
fig_line = px.line(rural_urban, x="Category", y="Count", color="Category",
                 title="Distribution of Workers by Area and Type")
fig_bar = px.bar(rural_urban, x="Category", y="Count", color="Category",
                 title="Distribution of Workers by Area and Type")
a=px.bar(rural_urban, x="Category", y="Count", color="Category",title="Distribution of Workers by Area and Type",
 barmode='group', log_y=True, text_auto=True)


# Display figures
fig_main.show()
fig_marginal.show()
fig_bar.show()
fig_line.show()
fig_scatter.show()
a.show()

# Output textual insights
print("\n🔍 Key Facts & Insights")
print(f"Industry: {selected_industry} in {selected_state} under Division {selected_division}")
print(f"Total Main Workers: {int(filtered_df['Main Workers - Total -  Persons'].sum()):,}")
print(f"Total Marginal Workers: {int(filtered_df['Marginal Workers - Total -  Persons'].sum()):,}")
print(f"Main Workers Gender Split: {int(main_total['Main Workers - Total - Males']):,} Males vs {int(main_total['Main Workers - Total - Females']):,} Females")
ur = int(rural_urban[rural_urban['Category'].str.contains('Urban')]['Count'].sum())
rr = int(rural_urban[rural_urban['Category'].str.contains('Rural')]['Count'].sum())
print(f"Urban vs Rural: {ur:,} Urban vs {rr:,} Rural")
