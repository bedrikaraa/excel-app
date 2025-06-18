
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel Üzerinde Çift Kayıt ve Filtreleme Uygulaması")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### 📄 Yüklenen Verinin Önizlemesi:")
    st.dataframe(df)

    col_to_check = st.selectbox("Çift kayıtları kontrol etmek istediğiniz kolonu seçin:", df.columns)

    # Çift kayıtları göster
    duplicates = df[df[col_to_check].duplicated(keep=False)]
    st.write("### 🔁 Çift (Duplicate) Satırlar")
    st.dataframe(duplicates)

    if st.button("🗑️ Çift Satırları Sil"):
        df = df.drop_duplicates(subset=col_to_check, keep='first')
        st.success("Çift satırlar kaldırıldı.")

    # Filtreleme
    st.write("### 🔍 Veri Filtreleme")
    filter_col = st.selectbox("Filtrelemek istediğiniz kolonu seçin:", df.columns)
    filter_vals = df[filter_col].unique()
    selected_val = st.selectbox("Filtrelenecek değeri seçin:", filter_vals)
    filtered_df = df[df[filter_col] == selected_val]
    st.write("### Filtrelenmiş Veri")
    st.dataframe(filtered_df)

    if st.button("🗑️ Filtrelenen Satırları Sil"):
        df = df[df[filter_col] != selected_val]
        st.success(f"`{filter_col}` sütununda `{selected_val}` olan satırlar silindi.")

    # Excel'e Aktar
    st.write("### 📥 Güncellenmiş Excel Dosyasını İndir")

    def to_excel(data):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sayfa1')
        return output.getvalue()

    excel_data = to_excel(df)
    st.download_button("Excel Olarak İndir", data=excel_data, file_name="duzenlenmis_veri.xlsx")

    # İşlem özeti
    st.info("✅ Yapılan İşlemler:")
    st.write(f"- `{col_to_check}` sütununda çift kayıt kontrolü yapıldı.")
    st.write(f"- `{filter_col}` sütununda `{selected_val}` değerine göre filtreleme yapıldı.")
