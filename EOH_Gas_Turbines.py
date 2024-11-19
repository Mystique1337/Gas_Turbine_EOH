import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import os
os.environ["BROWSER_PATH"] = "/usr/bin/chromium-browser"  # Replace with the actual path
 
# Sidebar header
st.sidebar.header("Gas Turbine EOH Input")

# Input number of Gas Turbines
num_gt = st.sidebar.number_input("Enter the number of Gas Turbines", min_value=1, max_value=20, value=15)

# Data entry as a table
st.write("### Enter EOH Data for Gas Turbines")
columns = ['GT', 'Current EOH', 'CI', 'HGPI', 'MI', 'RLE']
data = []

# Input table for user data
for i in range(num_gt):
    row = [
        st.text_input(f"GT {i+1} Name", f"GT{i+1}"),
        st.number_input(f"Current EOH for GT {i+1}", min_value=0, max_value=250000, value=5000),
        st.number_input(f"CI for GT {i+1}", min_value=0, max_value=250000, value=6000),
        st.number_input(f"HGPI for GT {i+1}", min_value=0, max_value=250000, value=8000),
        st.number_input(f"MI for GT {i+1}", min_value=0, max_value=250000, value=10000),
        st.number_input(f"RLE for GT {i+1}", min_value=0, max_value=250000, value=12000)
    ]
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Allow the user to add a new line plot
new_line_name = st.text_input("Enter new line plot name")
new_line_values = st.text_area("Enter values for the new line plot (comma-separated)")

if new_line_name and new_line_values:
    new_line_values = [float(val) for val in new_line_values.split(',')]
    df[new_line_name] = new_line_values

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
    marker=dict(
        color='grey',
    ),
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

if new_line_name and new_line_values:
    fig.add_trace(go.Scatter(
        x=new_line_values,
        y=df['GT'],
        mode='lines',
        name=new_line_name,
        line=dict(color='purple', dash='dashdot', width=2)
    ))

# Update layout for better readability
fig.update_layout(
    title=dict(
        text='Gas Turbine EOH Chart',
        font=dict(size=24, color='black', family='Arial', weight='bold')
    ),
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
        title='Legend',
        font=dict(size=14, color='black'),
        bordercolor='black',
    )
)

# Display the plot in the Streamlit app
st.plotly_chart(fig)

# Download options
st.download_button(
    label="Download chart as PNG",
    data = fig.write_image('fig1.png', engine='orca'),
    #data=fig.to_image(format="png"),
    file_name="gas_turbine_eoh_chart.png",
    mime="image/png"
)

st.download_button(
    label="Download chart as HTML",
    data=fig.to_html(),
    file_name="gas_turbine_eoh_chart.html",
    mime="text/html"
)
