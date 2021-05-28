import plotly.graph_objects as go


def generate_graphs(compressed_ratio_values, time_values, indices_values, is_txt):
    result_type = 'corpus' if is_txt else 'video'
    compression_ratio_fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(9, 17)],
                         y=compressed_ratio_values)],
        layout=go.Layout(title="Razão de compressão por K",
                         xaxis_title="K",
                         yaxis_title="Razão de compressão"),
    )
    compression_ratio_fig.write_image(
        f"results/{result_type}/compression_rate_x_k.png")

    time_fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(9, 17)], y=time_values)],
        layout=go.Layout(title="Tempo de processamento por K",
                         xaxis=dict(
                             title="K"
                         ),
                         yaxis_title="Tempo em segundos")
    )

    time_fig.write_image(f"results/{result_type}/time_x_k.png")

    indices_fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(9, 17)], y=indices_values)],
        layout=go.Layout(title="Índices por K",
                         xaxis=dict(
                             title="K",
                             tickmode='linear'
                         ),
                         yaxis_title="Índices usados para codificação")
    )

    indices_fig.write_image(f"results/{result_type}/indices_x_k.png")
