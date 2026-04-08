"""
Visualization module for Artemis mission tracking data.
Creates interactive HTML dashboards with mission data.
"""

import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
from datetime import datetime, timedelta
import requests


def fetch_all_artemis_data():
    """
    Fetch all Artemis tracking data from the APIs.
    """
    try:
        response = requests.get('https://artemis.cdnspace.ca/api/all', timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def create_3d_trajectory_plot(arw_data, state_data, all_data):
    """
    Create an interactive 3D plot of the spacecraft trajectory.
    """
    # Extract position data
    arw_pos = arw_data.get('positionKm', {})
    state_pos = state_data.get('stateVector', {}).get('position', {})
    moon_pos = all_data.get('moonPosition', {})
    
    spacecraft_x = [arw_pos.get('x', 0), state_pos.get('x', 0)]
    spacecraft_y = [arw_pos.get('y', 0), state_pos.get('y', 0)]
    spacecraft_z = [arw_pos.get('z', 0), state_pos.get('z', 0)]
    
    fig = go.Figure()
    
    # Add Earth at origin
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=15, color='blue'),
        name='Earth'
    ))
    
    # Add Moon
    fig.add_trace(go.Scatter3d(
        x=[moon_pos.get('x', 0)],
        y=[moon_pos.get('y', 0)],
        z=[moon_pos.get('z', 0)],
        mode='markers',
        marker=dict(size=8, color='gray'),
        name='Moon'
    ))
    
    # Add spacecraft trajectory
    fig.add_trace(go.Scatter3d(
        x=spacecraft_x,
        y=spacecraft_y,
        z=spacecraft_z,
        mode='lines+markers',
        marker=dict(size=6, color='red'),
        line=dict(color='red', width=2),
        name='Artemis Trajectory'
    ))
    
    fig.update_layout(
        title='Artemis Spacecraft 3D Trajectory',
        scene=dict(
            xaxis_title='X Position (km)',
            yaxis_title='Y Position (km)',
            zaxis_title='Z Position (km)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        hovermode='closest',
        height=700,
        width=900
    )
    
    return fig


def create_orbital_metrics_plot(orbit_data):
    """
    Create a dashboard of orbital metrics.
    """
    fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=('Speed Profile', 'Distance Metrics', 'Orbital Parameters', 'Performance')
    )
    
    # Speed data
    speeds = [
        orbit_data.get('speedKmS', 0),
        orbit_data.get('moonRelSpeedKmH', 0) / 3600
    ]
    speed_labels = ['vs Earth', 'vs Moon']
    
    fig.add_trace(
        go.Bar(x=speed_labels, y=speeds, name='Speed (km/s)', marker_color='steelblue'),
        row=1, col=1
    )
    
    # Distance comparison
    distances = {
        'Altitude': orbit_data.get('altitudeKm', 0),
        'Earth': orbit_data.get('earthDistKm', 0),
        'Moon': orbit_data.get('moonDistKm', 0)
    }
    
    fig.add_trace(
        go.Bar(x=list(distances.keys()), y=list(distances.values()), 
               name='Distance (km)', marker_color='darkgreen'),
        row=1, col=2
    )
    
    # Orbital parameters
    orbital_params = {
        'Periapsis': orbit_data.get('periapsisKm', 0),
        'Apoapsis': orbit_data.get('apoapsisKm', 0)
    }
    
    fig.add_trace(
        go.Bar(x=list(orbital_params.keys()), y=list(orbital_params.values()), 
               name='Distance (km)', marker_color='darkred'),
        row=2, col=1
    )
    
    # G-Force and related metrics
    metrics_labels = ['G-Force (μg)', 'Speed (km/s)']
    metrics_values = [
        orbit_data.get('gForce', 0) * 1e6,
        orbit_data.get('speedKmS', 0) * 100
    ]
    
    fig.add_trace(
        go.Bar(x=metrics_labels, y=metrics_values, name='Value', marker_color='orange'),
        row=2, col=2
    )
    
    fig.update_yaxes(title_text="Speed (km/s)", row=1, col=1)
    fig.update_yaxes(title_text="Distance (km)", row=1, col=2)
    fig.update_yaxes(title_text="Distance (km)", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=2)
    
    fig.update_layout(height=700, width=1000, title_text="Artemis Orbital Metrics Dashboard", showlegend=False)
    return fig


def create_dsn_tracking_plot(all_data):
    """
    Create visualization of DSN dish tracking status.
    """
    dsn_data = all_data.get('dsn', {})
    dishes = dsn_data.get('dishes', [])
    
    dish_names = []
    azimuths = []
    elevations = []
    colors = []
    
    for dish in dishes:
        dish_names.append(f"{dish.get('dish')} ({dish.get('stationName')})")
        azimuths.append(dish.get('azimuth', 0))
        elevations.append(dish.get('elevation', 0))
        
        # Color based on activity
        if dish.get('downlinkActive') or dish.get('uplinkActive'):
            colors.append('green')
        else:
            colors.append('lightgray')
    
    fig = go.Figure()
    
    # Create scatter plot with antenna positions
    fig.add_trace(go.Scatterpolar(
        r=elevations,
        theta=azimuths,
        mode='markers+text',
        marker=dict(
            size=15,
            color=colors,
            line=dict(width=2, color='black')
        ),
        text=dish_names,
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Azimuth: %{theta}°<br>Elevation: %{r}°<extra></extra>'
    ))
    
    fig.update_layout(
        title='DSN Dish Tracking Positions<br><sub>Green = Active, Gray = Idle</sub>',
        showlegend=False,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 90]
            )
        ),
        height=600,
        width=800
    )
    
    return fig


def create_status_summary(all_data, state_data, orbit_data):
    """
    Create a comprehensive status summary visualization.
    """
    state_vector = all_data.get('stateVector', {})
    position = state_vector.get('position', {})
    velocity = state_vector.get('velocity', {})
    
    fig = go.Figure()
    
    # Create a custom text-based summary
    summary_text = f"""
    <b>ARTEMIS 2 REAL-TIME STATUS</b><br><br>
    <b>Position:</b><br>
    X: {position.get('x', 0):.1f} km<br>
    Y: {position.get('y', 0):.1f} km<br>
    Z: {position.get('z', 0):.1f} km<br><br>
    <b>Velocity:</b><br>
    X: {velocity.get('x', 0):.3f} km/s<br>
    Y: {velocity.get('y', 0):.3f} km/s<br>
    Z: {velocity.get('z', 0):.3f} km/s<br><br>
    <b>Orbital Data:</b><br>
    Speed: {orbit_data.get('speedKmS', 0):.3f} km/s<br>
    Altitude: {orbit_data.get('altitudeKm', 0):.0f} km<br>
    Distance to Earth: {orbit_data.get('earthDistKm', 0):.0f} km<br>
    Distance to Moon: {orbit_data.get('moonDistKm', 0):.0f} km<br>
    """
    
    fig.add_annotation(
        text=summary_text,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, family="monospace"),
        align="left"
    )
    
    fig.update_layout(
        title="Current Mission Status",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode=False,
        height=500,
        width=800
    )
    
    return fig


def generate_dashboard():
    """
    Generate all visualizations and save as HTML dashboard.
    """
    print("Fetching Artemis data...")
    all_data = fetch_all_artemis_data()
    
    if not all_data:
        print("Failed to fetch data")
        return
    
    # Extract individual data components
    arw_data = all_data.get('arow', {})
    state_data = all_data
    orbit_data = all_data.get('telemetry', {})
    
    print("Creating visualizations...")
    
    # Create individual plots
    trajectory_fig = create_3d_trajectory_plot(arw_data, all_data, all_data)
    metrics_fig = create_orbital_metrics_plot(orbit_data)
    dsn_fig = create_dsn_tracking_plot(all_data)
    status_fig = create_status_summary(all_data, all_data, orbit_data)
    
    # Create HTML file with all plots
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Artemis 2 Mission Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { color: #333; text-align: center; }
            .timestamp { text-align: center; color: #666; margin-bottom: 20px; }
            .plot-container { background-color: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .plot { width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛸 NASA Artemis 2 Real-Time Mission Dashboard</h1>
            <div class="timestamp">Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """</div>
            
            <div class="plot-container">
                <div id="status-plot" class="plot"></div>
            </div>
            
            <div class="plot-container">
                <div id="trajectory-plot" class="plot"></div>
            </div>
            
            <div class="plot-container">
                <div id="metrics-plot" class="plot"></div>
            </div>
            
            <div class="plot-container">
                <div id="dsn-plot" class="plot"></div>
            </div>
        </div>
        
        <script>
            """ + f"Plotly.newPlot('status-plot', {status_fig.to_json()});" + """
            """ + f"Plotly.newPlot('trajectory-plot', {trajectory_fig.to_json()});" + """
            """ + f"Plotly.newPlot('metrics-plot', {metrics_fig.to_json()});" + """
            """ + f"Plotly.newPlot('dsn-plot', {dsn_fig.to_json()});" + """
        </script>
    </body>
    </html>
    """
    
    # Save to file
    output_file = 'artemis_dashboard.html'
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✓ Dashboard generated successfully: {output_file}")
    print("Open this file in your web browser to view the interactive visualizations.")


if __name__ == "__main__":
    generate_dashboard()
