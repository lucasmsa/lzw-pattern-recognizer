import plotly.graph_objects as go


def generate_graphs(hit_rate_values: list, time_values: list, x_range: tuple):
    hit_rate_fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(x_range[0], x_range[1])],
                         y=hit_rate_values)],
        layout=go.Layout(title="Taxa de acerto por K",
                         yaxis=dict(
                             range=[0, 1]
                         ),
                         xaxis_title="K",
                         yaxis_title="Taxa de acerto"),
    )
    hit_rate_fig.write_image(
        f"results/hit_rate_x_k.png")

    time_fig = go.Figure(
        data=[go.Scatter(x=[i for i in range(x_range[0], x_range[1])], 
                         y=time_values)],
        layout=go.Layout(title="Tempo de processamento por K",
                         xaxis=dict(
                             title="K"
                         ),
                         yaxis_title="Tempo em segundos")
    )

    time_fig.write_image(f"results/time_x_k.png")