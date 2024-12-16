import plotly.graph_objects as go
from dtm_dataframe_from_excel import DTM

# Função auxiliar para configurar layout padrão
def apply_layout(fig, dashboard_bg_color, xaxis_title, yaxis_title, invert_yaxis=False, x_range=None):
    """
    Aplica configurações de layout padrão ao gráfico.

    :param fig: Objeto Figure do Plotly a ser configurado.
    :param dashboard_bg_color: Cor de fundo do dashboard para aplicar no papel do gráfico.
    :param xaxis_title: Título do eixo X.
    :param yaxis_title: Título do eixo Y.
    :param invert_yaxis: Se True, inverte o eixo Y.
    :param x_range: Define o limite do eixo X (ex: [0, 100]).
    """
    fig.update_layout(
        height=500,  # Altura padrão
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(
            range=x_range,  # Limita o eixo X, se especificado
            gridcolor="rgba(211, 211, 211, 0.5)",  # Grade cinza claro
            zerolinecolor="rgba(211, 211, 211, 0.5)",  # Linha zero cinza claro
            tickfont=dict(color="white"),  # Fonte branca no eixo X
            title_font=dict(size=18, color="white", family="Cantarell")  # Título do eixo X
        ),
        yaxis=dict(
            autorange="reversed" if invert_yaxis else True,  # Inverte o eixo Y se necessário
            gridcolor="rgba(211, 211, 211, 0.5)",  # Grade cinza claro
            tickfont=dict(color="white"),  # Fonte branca no eixo Y
            title_font=dict(size=18, color="white", family="Cantarell")  # Título do eixo Y
        ),
        font=dict(size=14, color="white"),  # Fonte geral branca
        plot_bgcolor="rgba(240, 240, 240, 1)",  # Fundo cinza claro do gráfico
        paper_bgcolor=dashboard_bg_color,  # Fundo do papel igual ao fundo do dashboard
    )


def plot_progress(dtm_instance, dashboard_bg_color):
    """
    Cria um gráfico de linha comparando o progresso planejado e executado do projeto DTM, com marcadores.
    """
    # Reorganizar os dados
    progress_data = dtm_instance.progress_df.melt(
        id_vars="Dia", 
        value_vars=["Planejado - % Completo", "Executado - % Completo"],
        var_name="Tipo",
        value_name="Porcentagem Concluída (%)"
    )

    # Criar o gráfico
    fig = go.Figure()
    color_mapping = {
        "Planejado - % Completo": "rgb(246, 99, 59)",  # Laranja
        "Executado - % Completo": "rgb(121, 211, 84)"  # Verde
    }

    # Adicionar linhas com marcadores
    for tipo, color in color_mapping.items():
        filtered_data = progress_data[progress_data["Tipo"] == tipo]
        fig.add_trace(
            go.Scatter(
                x=filtered_data["Dia"],
                y=filtered_data["Porcentagem Concluída (%)"],
                mode="lines+markers",  # Adiciona linhas e marcadores
                line=dict(color=color, width=5),
                marker=dict(size=8, symbol="circle", color=color, line=dict(width=1, color="white")),  # Personaliza marcadores
                name="Planejado" if tipo == "Planejado - % Completo" else "Executado"  # Nomes customizados
            )
        )

    # Aplicar layout padrão
    apply_layout(fig, dashboard_bg_color, "Dias", "Porcentagem Concluída (%)")

    return fig

def plot_class_task_percentage(dtm_instance, dashboard_bg_color):
    """
    Cria um gráfico de barras horizontais para exibir o percentual de execução por classe de tarefa.
    """
    class_tasks = list(dtm_instance.class_task_percentage.keys())
    percentages = list(dtm_instance.class_task_percentage.values())

    # Criar o gráfico de barras horizontais
    fig = go.Figure(
        go.Bar(
            y=class_tasks,
            x=percentages,
            orientation='h',
            marker=dict(color='rgb(121, 211, 84)',  # Verde
                        line=dict(color='rgb(41, 78, 26)', width=2))  # Contorno mais escuro
        )
    )

    # Aplicar layout padrão sem label no eixo Y
    apply_layout(fig, dashboard_bg_color, "Percentual Executado (%)", None, invert_yaxis=True, x_range=[0, 100])

    return fig

# Testando os gráficos
if __name__ == "__main__":
    dtm = DTM('DTM_PR-14.xlsx')  # Carregar os dados do Excel
    dashboard_bg_color = 'rgba(14, 17, 23, 1)'  # Fundo escuro do dashboard

    # Plotar os gráficos
    fig_progress = plot_progress(dtm, dashboard_bg_color)
    fig_progress.show()

    fig_class_task = plot_class_task_percentage(dtm, dashboard_bg_color)
    fig_class_task.show()