import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Sidebar header
st.sidebar.header("Gas Turbine EOH Input")

# Input number of Gas Turbines
num_gt = st.sidebar.number_input("Enter the number of Gas Turbines", min_value=6, max_value=20, value=15)

# Data entry as a table
st.write("### Enter EOH Data for Gas Turbines")
columns = ['GT', 'Current EOH', 'CI', 'HGPI', 'MI', 'RLE']

# Prepopulate data
data = [
    {
        'GT': f"GT{i+1}",
        'Current EOH': 5000,
        'CI': 12000,
        'HGPI': 32000,
        'MI': 64000,
        'RLE': 200000
    } for i in range(num_gt)
]

# Use Streamlit's experimental data editor
df = st.data_editor(pd.DataFrame(data), key="data_editor")

# Allow the user to add a new line plot
st.write("### Add a New Line Plot")
new_line_name = st.text_input("Enter new line plot name")
new_line_values = st.text_area("Enter values for the new line plot (comma-separated)")

if new_line_name and new_line_values:
    try:
        new_line_values = [float(val) for val in new_line_values.split(',')]
        if len(new_line_values) == len(df):
            df[new_line_name] = new_line_values
        else:
            st.warning(f"Number of values must match the number of rows ({len(df)}).")
    except ValueError:
        st.error("Ensure all entered values are numeric.")

# Display the data table
st.write("### Data Table")
st.dataframe(df)

# Create the Plotly figure
fig = go.Figure()

# Add the bar chart for Current EOH
fig.add_trace(go.Bar(
    y=df['GT'],
    x=df['Current EOH'],
    orientation='h',
    name='Current EOH',
    marker=dict(color='grey'),
    text=df['Current EOH'],
    textposition='outside',
    texttemplate='%{text:.0f}',
    textfont=dict(size=14, color='black')
))

# Add target lines for CI, HGPI, MI, RLE, and new line plots
for col, color, dash in zip(['CI', 'HGPI', 'MI', 'RLE'], ['green', 'orange', 'red', 'blue'], ['dash', 'dot', 'solid', 'dash']):
    fig.add_trace(go.Scatter(
        x=df[col],
        y=df['GT'],
        mode='lines',
        name=col,
        line=dict(color=color, dash=dash, width=2)
    ))

if new_line_name and new_line_name in df.columns:
    fig.add_trace(go.Scatter(
        x=df[new_line_name],
        y=df['GT'],
        mode='lines',
        name=new_line_name,
        line=dict(color='purple', dash='dashdot', width=2)
    ))

# Update layout for better readability
fig.update_layout(
    title="Gas Turbine EOH Chart",
    xaxis_title=dict(
        text='Hours',
        font=dict(size=18, color='black', family='Arial', weight='bold')
    ),
    yaxis_title=dict(
        text='Gas Turbine (GT)',
        font=dict(size=18, color='black', family='Arial', weight='bold')
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        color='black',
        title_font=dict(size=16),
        tickfont=dict(size=14, color='black')
    ),
    yaxis=dict(
        showgrid=False,
        color='black',
        title_font=dict(size=16),
        tickfont=dict(size=14, color='black')
    ),
    barmode='group',
    bargap=0.1,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    legend=dict(
        title="Legend",
        font=dict(size=14, color='black'),
        bordercolor='black'
    )
)

# Display the plot in the Streamlit app
st.plotly_chart(fig)

# Download options
import io

# Generate PNG
png_buffer = io.BytesIO()
fig.write_image(png_buffer, format="png")
png_buffer.seek(0)

# Generate HTML
html_buffer = fig.to_html(full_html=False)

st.download_button(
    label="Download chart as PNG",
    data=png_buffer,
    file_name="gas_turbine_eoh_chart.png",
    mime="image/png"
)

st.download_button(
    label="Download chart as HTML",
    data=html_buffer,
    file_name="gas_turbine_eoh_chart.html",
    mime="text/html"
)
