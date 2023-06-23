import streamlit as st
import pandas as pd
import requests
import html

st.set_page_config(layout="wide")

url = f"{st.secrets['BASE_URL']}&DOLAPIKEY={st.secrets['DOLAPIKEY']}"

response = requests.request("GET", url)

df = pd.DataFrame(response.json())
df = df[["ref", "type", "label", "duration", "description", "price_ttc"]]

# a bit a cleaning
df["type"] = df["type"].apply(lambda x: "Produit" if x == '0' else "Service")
df["price_ttc"] = df["price_ttc"].apply(lambda x: round(float(x), 2))
df["description"] = df["description"].apply(lambda x: html.unescape(x))

df.columns = ["Ref.", "Type", "Label", "Durée (si service)", "Description", "Prix € (TTC)"]
df.sort_values(by=["Type", "Label"], inplace=True)

df_produit = df[df["Type"] == "Produit"]
df_produit.reset_index(inplace=True)
df_service = df[df["Type"] == "Service"]
df_service.reset_index(inplace=True)


with col1:

    st.write("## Liste de mes produits")
    for i in range(len(df_produit)):
        with st.expander(f"## **{df_produit.iloc[i]['Label']}**"):
            st.markdown(f"- **Ref**: {df_produit.iloc[i]['Ref.']}")
            st.markdown(f"- **Prix € (TTC)**: {df_produit.iloc[i]['Prix € (TTC)']}")
            st.markdown(f"- **Description**:")
            st.markdown(df.iloc[i]['Description'])

with col2:

    st.write("## Liste de mes services")
    for i in range(len(df_service)):
        with st.expander(f"## **{df_service.iloc[i]['Label']}**"):
            st.markdown(f"- **Ref**: {df_service.iloc[i]['Ref.']}")
            st.markdown(f"- **Durée**: {df_service.iloc[i]['Durée (si service)']}")
            st.markdown(f"- **Prix € (TTC)**: {df_service.iloc[i]['Prix € (TTC)']}")
            st.markdown(f"- **Description**:")
            st.markdown(df.iloc[i]['Description'])