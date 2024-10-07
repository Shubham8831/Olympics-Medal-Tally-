import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

athletes = pd.read_csv("data/athlete_events.csv")
regions = pd.read_csv("data/noc_regions.csv")



def data_preprocessor():
    global athletes,regions
    df = pd.merge(athletes,regions,on = "NOC")
    df.drop_duplicates(inplace = True)
    df["Medal"].fillna("No_Medal", inplace = True) 
    summer = df[df["Season"]=="Summer"]
    winter = df[df["Season"]=="Winter"]
    return summer,winter


def dublicate_rows_remover(df1,df2):
    df1 = df1.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event"])
    df2 = df2.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event"])
    return df1, df2

def medal_tally_calculator(df):
    medal_count = df.groupby(["NOC","Medal"]).size().reset_index(name="count")
    medal_pivot = medal_count.pivot_table(index = "NOC", columns="Medal",values = "count").fillna(0)
    medal_pivot = medal_pivot.astype(int)

    if "No_Medal" in medal_pivot.columns:
        medal_pivot.drop(columns = "No_Medal", inplace = True)
    medal_pivot["Total_Medal"]=medal_pivot[["Bronze", "Gold", "Silver"]].sum(axis = 1)
    return medal_pivot



def country_wise_search(noc,pivot_table):
    if noc in pivot_table.index:
        details={
            "Gold": pivot_table.loc[noc,"Gold"],
            "Silver": pivot_table.loc[noc,"Silver"],
            "Bronze": pivot_table.loc[noc,"Bronze"],
            "Total Medal": pivot_table.loc[noc,"Total_Medal"]
        }
        return details
    else:
        Print("No NOC Exists")

def plot_medals(year, country, df):
    medals_count = df.groupby(["region","Year","Medal"]).size().unstack(fill_value=0)
    medals_count = medals_count.reset_index()
    medals_count["Total_Medal"]= medals_count[["Bronze", "Gold", "Silver"]].sum(axis = 1)

    filtered_df = medals_count[(medals_count["Year"]==year) & (medals_count["region"]==country)]
    gold = filtered_df["Gold"].values[0]
    silver = filtered_df["Silver"].values[0]    
    bronze = filtered_df["Bronze"].values[0]    
    total_medal = filtered_df["Total_Medal"].values[0] 
    
    fig,ax = plt.subplots()
    medals = ["Gold", "Silver","Bronze","Total_Medals"]
    counts = [gold, silver, bronze, total_medal]
    ax.bar(medals, counts, color = ["gold","silver","brown","green"])
    st.pyplot(fig)


def year_analysis(country, df):
    medals_count = df.groupby(["region","Year","Medal"]).size().unstack(fill_value=0)
    medals_count = medals_count.reset_index()
    medals_count["Total_Medal"]= medals_count[["Bronze", "Gold", "Silver"]].sum(axis = 1)
    
    filtered_df = medals_count[medals_count["region"]==country]
    fig,ax = plt.subplots()
    ax.plot(filtered_df["Year"], filtered_df["Gold"], color="gold", label="GOLD", marker="o", linestyle="-")
    ax.plot(filtered_df["Year"], filtered_df["Silver"], color="silver", label="SILVER", marker="o", linestyle="-")
    ax.plot(filtered_df["Year"], filtered_df["Bronze"], color="brown", label="BRONZE", marker="o", linestyle="-")
    ax.plot(filtered_df["Year"], filtered_df["Total_Medal"], color="green", label="TOTAL MEDAL", marker="o", linestyle="-")
    ax.legend()
    st.pyplot(fig)


    