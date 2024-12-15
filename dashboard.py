import streamlit as st
from dtm_dataframe_from_excel import DTM  # Importa a classe DTM para processar os dados
from dtm_plots import plot_progress, plot_class_task_percentage  # Importa as funções para criar os gráficos

# Cor de fundo do dashboard
dashboard_bg_color = 'rgba(14, 17, 23, 1)'  # Fundo escuro do dashboard

# Configuração do layout da página
st.set_page_config(layout='wide', page_title="DTM Dashboard", page_icon="📊")

# Layout do título com a logo
col1, col2 = st.columns([1, 16])  # Coluna para logo (1 parte) e título (16 partes)

with col1:
    st.image("logo_mapa-removebg-preview.png", width=120)  # Ajuste o tamanho conforme necessário

title = 'DTM - PR-14'
with col2:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; height: 100%;">
            <h1 style="text-align: left; margin: 0;">{title}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Criar abas
tab1, tab2 = st.tabs(["Upload de Dados", "Gráficos de Progresso"])

# Aba 1: Upload de Dados
with tab1:
    st.header("Upload do Arquivo Excel")
    uploaded_file = st.file_uploader("Faça o upload do arquivo Excel contendo os dados do DTM:", type=["xlsx"])

    if uploaded_file is not None:
        # Processar o arquivo com a classe DTM
        try:
            # Ler o arquivo Excel com pandas e criar uma instância da classe DTM
            dtm_instance = DTM(uploaded_file)  # Passa os dados para a classe DTM
            st.success("Arquivo processado com sucesso!")
            
            # Exibir os dados carregados
            st.subheader("Visualização dos Dados Processados")
            st.dataframe(dtm_instance.progress_df)
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

# Aba 2: Gráficos de Progresso
with tab2:
    st.header("Análise de Progresso")

    # Dividir a linha em colunas com proporção 1:4
    col1, col2 = st.columns([1, 1.5])

    # Gráfico de Progresso na primeira coluna (menor)
    with col2:
        #st.subheader("Progresso Diário")
        try:
            if 'dtm_instance' in locals() or 'dtm_instance' in globals():
                fig_progress = plot_progress(dtm_instance, dashboard_bg_color)
                st.plotly_chart(fig_progress, use_container_width=True)
            else:
                st.warning("Carregue os dados na aba 'Upload de Dados' antes de acessar o gráfico.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o gráfico de progresso: {e}")

    # Gráfico de Percentual por Classe na segunda coluna (maior)
    with col1:
        #st.subheader("Percentual por Classe de Tarefa")
        try:
            if 'dtm_instance' in locals() or 'dtm_instance' in globals():
                fig_class = plot_class_task_percentage(dtm_instance, dashboard_bg_color)
                st.plotly_chart(fig_class, use_container_width=True)
            else:
                st.warning("Carregue os dados na aba 'Upload de Dados' antes de acessar o gráfico.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o gráfico de classes: {e}")

