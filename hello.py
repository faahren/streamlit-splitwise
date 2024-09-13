import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
from services.splitwise import SplitwiseService

def main():
    st.title("Splitwise")
    st.write("This is a simple app to send your expenses to Splitwise")
    try:
        st.write("Logged in with the user: " + SplitwiseService().getUser().getEmail())
        show_file_uploader()

    except:
        st.write("Splitwise credentials non functional")


def show_file_uploader():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:

        # Can be used wherever a "file-like" object is accepted:
        global data_df
        data_df = pd.read_csv(uploaded_file, sep=";")
        global uploaded_file_name
        uploaded_file_name = uploaded_file.name

        show_table()

def show_table():

    if "df_value" not in st.session_state:
        st.session_state.df_value = data_df

    data_df["send_to_splitwise"] = False
    try:
        data_df.drop(columns=["Credit"], inplace=True)
    except:
        pass
    try:
        data_df.drop(columns=["Numero de Carte"], inplace=True)
    except:
        pass
    try:
        data_df.drop(columns=["Solde"], inplace=True)
    except:
        pass



    global edited_df
    edited_df = st.data_editor(
        data_df,
        use_container_width=True,
        column_config={
            "send_to_splitwise": st.column_config.CheckboxColumn(
                "Send to Splitwise",
                help="Select",
                default=False,
            )
        },
        on_change=changed,
        disabled=["widgets"],
        hide_index=True,
    )


    btn = st.button("Send", type="primary")

    if btn:
        to_send = edited_df[edited_df['send_to_splitwise'] == True]
        splitwise = SplitwiseService()
        for index, row in to_send.iterrows():
            try:
                expense_id = splitwise.send_to_sw(row)
                st.write("Expense sent with id: " + str(expense_id))
            except:
                st.write("Error sending to splitwise")


    if edited_df is not None and not edited_df.equals(st.session_state["df_value"]):
        # This will only run if
        # 1. Some widget has been changed (including the dataframe editor), triggering a
        # script rerun, and
        # 2. The new dataframe value is different from the old value
        changed()
        st.session_state["df_value"] = edited_df



def changed():
    edited_df.to_csv('data/' + uploaded_file_name + "_modified")
    st.write("Changed!")

if __name__ == "__main__":
    main()