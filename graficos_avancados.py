from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


def criar_grafico(df):
    # Histograma - Parâmetros
    fig1 = px.histogram(df, x='Nota', nbins=30)
    fig1.update_layout(
        title='Histograma - Produto e Nota',
        xaxis_title='Nota',
        yaxis_title='Frequência'
    )

    # Gráficos de Dispersão
    fig2 = px.scatter(df, x='Preço', y='N_Avaliações', color='Qtd_Vendidos_Cod', hover_data=['Nota'])
    fig2.update_layout(
        title='Dispersão de Preço e Número de Avaliações',
        xaxis_title='Preço',
        yaxis_title='Número de Avaliações'
    )

    # Mapa de Calor
    # Verificando correlações
    df_corr = df[['N_Avaliações', 'Qtd_Vendidos_Cod', 'Desconto', 'Nota', 'Preço', 'Material_Cod', 'Temporada_Cod',
                  'Marca_Cod']].corr()
    fig3 = px.imshow(
        df_corr,
        text_auto=True,  # Mostra os valores de correlação no heatmap
        aspect="auto",  # Ajusta automaticamente a proporção
        color_continuous_scale='RdBu',  # Escala de cores (vermelho-azul)
        range_color=[0, 1],  # Define o range para correlação (0 a 1)
        title='Mapa de Calor de Correlação entre Variáveis'
    )

    # Gráficos de barras
    top_n = 10
    contagem_marcas = df['Marca'].value_counts().reset_index()
    contagem_marcas.columns = ['Marca', 'Quantidade']

    # Separar as top N marcas
    top_marcas = contagem_marcas.head(top_n)
    outras = pd.DataFrame({
        'Marca': ['Outras'],
        'Quantidade': [contagem_marcas['Quantidade'].iloc[top_n:].sum()]
    })

    contagem_agrupada = pd.concat([top_marcas])

    # Criar o gráfico com Plotly Express
    fig4 = px.bar(contagem_agrupada,
                  x='Marca',
                  y='Quantidade',
                  title=f'Top {top_n} Marcas',
                  labels={'Quantidade': 'Quantidade de Produtos', 'Marca': 'Marca'},
                  color='Marca',
                  color_discrete_sequence=['#90ee70'] * len(contagem_agrupada))

    # Personalizar o layout
    fig4.update_layout(
        xaxis_title='Marca',
        yaxis_title='Quantidade',
        title_x=0.5,  # Centralizar o título
        showlegend=False,  # Remover legenda desnecessária
        hovermode='x',  # Melhorar interação ao passar o mouse
        xaxis={'categoryorder': 'total descending'}  # Ordenar por quantidade
    )

    # Gráfico de pizza
    fig5 = px.pie(df, names='Gênero', color='Gênero', hole=0.2,
                  color_discrete_sequence=px.colors.sequential.RdBu,
                  title='Distribuição de Vendas por Gênero')

    # Gráfico de Densidade
    fig6 = px.histogram(df,
                        x='Preço',
                        nbins=50,
                        marginal='rug',  # Adiciona marcadores de distribuição
                        title='Densidade de Preço',
                        color_discrete_sequence=['#863e9c'],
                        opacity=0.7)

    # Adicionar curva KDE
    fig6.update_traces(xbins=dict(size=10),  # Ajuste o tamanho dos bins conforme necessário
                       marker=dict(line=dict(width=1, color='#863e9c')),
                       selector=dict(type='histogram'))

    # Personalizar layout
    fig6.update_layout(
        xaxis_title='Preço',
        yaxis_title='Densidade',
        showlegend=False,
        plot_bgcolor='white',
        title_x=0.5
    )

    # Gráfico de Regressão
    fig7 = px.scatter(df,
                      x='Desconto',
                      y='Qtd_Vendidos_Cod',
                      trendline='lowess',  # 'ols' para regressão linear simples
                      title='Regressão de Desconto por Quantidade Vendida',
                      color_discrete_sequence=['#34c289'],
                      opacity=0.5)

    # Personalizar a linha de regressão
    fig7.update_traces(
        line=dict(color='#278f65', width=3),
        selector=dict(type='scatter', mode='lines')
    )

    # Personalizar marcadores
    fig7.update_traces(
        marker=dict(size=8, opacity=0.5),
        selector=dict(mode='markers')
    )

    # Personalizar layout
    fig7.update_layout(
        xaxis_title='Desconto',
        yaxis_title='Quantidade Vendida',
        plot_bgcolor='white',
        title_x=0.5,
        hovermode='closest'
    )
    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


def criar_app(df):
    # Cria App
    app = Dash(__name__)

    fig1, fig2, fig3, fig4, fig5, fig6, fig7 = criar_grafico(df)

    app.layout = html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6),
        dcc.Graph(figure=fig7)
    ])
    return app


df = pd.read_csv('ecommerce_estatistica.csv')

print(df.head().to_string())

# Executa o app
if __name__ == '__main__':
    app = criar_app(df)
    app.run(debug=True, port=8050)  # Default 8050
