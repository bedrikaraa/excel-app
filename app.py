
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel Duplicate & Filter App")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded Data:")
    st.dataframe(df)

    col_to_check = st.selectbox("Select column to check duplicates:", df.columns)

    # Show duplicates
    duplicates = df[df[col_to_check].duplicated(keep=False)]
    st.write("### 🔁 Duplicate Rows")
    st.dataframe(duplicates)

    if st.button("🗑️ Drop Duplicates"):
        df = df.drop_duplicates(subset=col_to_check, keep='first')
        st.success("Duplicates removed.")

    # Filtering
    st.write("### 🔍 Filter Data")
    filter_col = st.selectbox("Select column to filter:", df.columns)
    filter_vals = df[filter_col].unique()
    selected_val = st.selectbox("Select value:", filter_vals)
    filtered_df = df[df[filter_col] == selected_val]
    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    if st.button("🗑️ Delete Filtered Rows"):
        df = df[df[filter_col] != selected_val]
        st.success(f"Rows with `{selected_val}` in `{filter_col}` deleted.")

    # Export to Excel
    st.write("### 📥 Download Updated Excel")

    def to_excel(data):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    excel_data = to_excel(df)
    st.download_button("Download Excel", data=excel_data, file_name="cleaned_data.xlsx")

    # Action log
    st.info("✅ Actions Summary:")
    st.write(f"- Checked duplicates in `{col_to_check}`")
    st.write(f"- Filtered by `{filter_col}` = `{selected_val}`")
