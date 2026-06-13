import plotly.express as px

def create_bar_chart(df, x_col, y_col, title):

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title
    )

    return fig


def create_pie_chart(df, names, values, title):

    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title
    )

    return fig