import streamlit as st
import pdfplumber
import pandas as pd
import tempfile

st.set_page_config(page_title="Detector de Tabelas em PDF")

st.title("📄 Detector de Tabelas em PDF")

uploaded_file = st.file_uploader("Faça upload de um arquivo PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    tables_found = []
    full_text = ""

    with pdfplumber.open(tmp_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extrair tabelas
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                if table:
                    df = pd.DataFrame(table)
                    tables_found.append((page_num, table_idx + 1, df))
            # Extrair texto
            text = page.extract_text()
            if text:
                full_text += f"\n--- Página {page_num} ---\n{text}"

    # Exibir tabelas
    if tables_found:
        st.success(f"{len(tables_found)} tabela(s) encontrada(s) no PDF:")
        for page_num, table_idx, df in tables_found:
            st.markdown(f"**Página {page_num} - Tabela {table_idx}**")
            st.dataframe(df)
    else:
        st.warning("Nenhuma tabela encontrada no PDF.")

    # Exibir texto completo
    st.markdown("### 📝 Texto extraído do PDF")
    if full_text.strip():
        st.text_area("Conteúdo textual do PDF", full_text, height=400)
    else:
        st.info("Nenhum texto extraído do PDF.")