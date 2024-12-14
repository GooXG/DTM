import plotly.graph_objects as go

def plot_progress(dtm_instance, dashboard_bg_color):
    """
    Cria um gráfico de linha comparando o progresso planejado e executado do projeto DTM.
    
    :param plan: Instância de DTM que contém o DataFrame processado.
    :param dashboard_bg_color: Cor de fundo do dashboard para aplicar no papel do gráfico.
    :return: Objeto Figure do Plotly.
    """
    # Reorganizar os dados para plottar múltiplas curvas no mesmo gráfico
    progress_data = dtm_instance.progress_df.melt(
        id_vars="Dia", 
        value_vars=["Planejado - % Completo", "Executado - % Completo"],
        var_name="Tipo",
        value_name="Porcentagem Concluída (%)"
    )
    
    # Configurar o gráfico de linha como Figura do Plotly
    fig = go.Figure()
    
    # Definir as cores RGB das curvas
    color_mapping = {
        "Planejado - % Completo": "rgb(246, 99, 59)",  # Cor para o planejado
        "Executado - % Completo": "rgb(121, 211, 84)"  # Cor para o executado
    }
    
    # Adicionar as curvas manualmente com nomes customizados
    for tipo, color in color_mapping.items():
        filtered_data = progress_data[progress_data["Tipo"] == tipo]
        fig.add_trace(
            go.Scatter(
                x=filtered_data["Dia"],
                y=filtered_data["Porcentagem Concluída (%)"],
                mode="lines",
                line=dict(color=color, width=5),  # Cor e espessura da linha
                name="Planejado" if tipo == "Planejado - % Completo" else "Executado"  # Nomes customizados na legenda
            )
        )
    
    # Ajustar layout do gráfico
    fig.update_layout(
        height=500,  # Altura do gráfico
        xaxis_title="Dias",
        yaxis_title="Porcentagem Concluída (%)",
        xaxis=dict(
            tickmode="linear",
            gridcolor="rgba(211, 211, 211, 0.5)",  # Linhas de grade verticais cinza muito claro
            zerolinecolor="rgba(211, 211, 211, 0.5)",  # Linha zero em cinza muito claro
            tickfont=dict(color="white"),  # Cor das labels do eixo X
            title_font=dict(size=18, color="white", family="Cantarell")  # Título do eixo X
        ),
        yaxis=dict(
            range=[0, 110],
            gridcolor="rgba(211, 211, 211, 0.5)",  # Linhas de grade horizontais cinza muito claro
            zerolinecolor="rgba(211, 211, 211, 0.5)",  # Linha zero em cinza muito claro
            tickfont=dict(color="white"),  # Cor das labels do eixo Y
            title_font=dict(size=18, color="white", family="Cantarell")  # Título do eixo Y
        ),
        font=dict(size=14, color="white"),  # Fonte geral branca
        plot_bgcolor="rgba(240, 240, 240, 1)",  # Fundo cinza claro do gráfico
        paper_bgcolor=dashboard_bg_color,  # Fundo do papel igual ao fundo do dashboard
        legend=dict(
            title="",  # Ocultar título da legenda
            font=dict(size=14, color="white"),  # Fonte branca na legenda
            x=0.04,  # Posição horizontal no gráfico
            y=0.83,  # Posição vertical próximo ao topo
            xanchor="center",  # Centraliza horizontalmente
            yanchor="bottom",  # Alinha verticalmente à base
            bgcolor="rgba(0, 0, 0, 0.5)",  # Fundo semitransparente para destaque
            bordercolor="white",  # Bordas brancas na legenda
            borderwidth=1  # Largura da borda
        )
    )
    
    return fig

