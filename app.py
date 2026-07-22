import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="WSAN Edge-Cloud Engine", layout="wide")

st.title("Serverless WSAN Smart Farming Pipeline")
st.caption("Edge-Based Cyber-Physical Actuation vs Cloud Synchronization Engine")

st.sidebar.header("Cyber-Physical Configuration")
selected_node = st.sidebar.selectbox("Target Agricultural Node", ["Vineyard Sector A (Soil/Irrigation)", "Maize Sector B (Thermal/Pesticide)", "Greenhouse C (Climate/Ventilation)"])
network_state = st.sidebar.radio("Simulate Cloud Connectivity", ["Connected (Stable)", "Disconnected (Network Blackout)"])
run_simulation = st.sidebar.button("Initialize WSAN Edge Node")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Sensor Ingestion -> Edge ML Reflex -> AWS Cloud Sync")

if run_simulation:
    st.subheader(f"Active WSAN Edge Node: {selected_node}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_moisture = col1.empty()
    metric_actuation = col2.empty()
    metric_latency = col3.empty()
    metric_sync = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(505)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    moisture_values = []
    actuation_states = []
    
    base_moisture = 60.0 
    sync_queue = 0
    
    for i in range(100):
        if i < 30:
            current_moisture = base_moisture + np.random.uniform(-2.0, 2.0)
            actuation_active = 0
        elif i >= 30 and i < 70:
            current_moisture = base_moisture - (i - 30) * 1.5 + np.random.uniform(-1.0, 1.0)
            actuation_active = 1 if current_moisture < 45.0 else 0
        else:
            current_moisture = current_moisture + 2.0 + np.random.uniform(-1.0, 1.0)
            actuation_active = 1 if current_moisture < 55.0 else 0
            
        moisture_values.append(current_moisture)
        actuation_states.append(actuation_active * 100) 
        
        edge_latency = np.random.uniform(2.0, 5.0) 
        
        if network_state == "Disconnected (Network Blackout)":
            sync_queue += 1
            sync_status = f"{sync_queue} payloads queued"
        else:
            sync_queue = 0
            sync_status = "AWS Synced"
        
        metric_moisture.metric("Soil Moisture Index (%)", f"{current_moisture:.1f}%")
        
        if actuation_active == 1:
            metric_actuation.metric("Actuator Status", "DEPLOYED", "- Critical Desiccation")
        else:
            metric_actuation.metric("Actuator Status", "STANDBY", "Optimal Levels")
            
        metric_latency.metric("Edge Reflex Latency", f"{edge_latency:.1f} ms")
        metric_status = "CACHING LOCALLY" if network_state == "Disconnected (Network Blackout)" else "CLOUD CONNECTED"
        metric_sync.metric("Cloud Database Sync", sync_status, metric_status)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=moisture_values, mode='lines', name='Soil Moisture (%)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=actuation_states, mode='none', fill='tozeroy', name='Actuation Triggered', fillcolor='rgba(255, 0, 0, 0.2)'))
        
        fig.update_layout(
            title="Real-Time Cyber-Physical System: Environmental Demand vs Actuator Response",
            xaxis=dict(title="High-Frequency Timeline"),
            yaxis=dict(title="Moisture % / Actuation State", range=[0, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if actuation_active == 1:
            log_placeholder.error(f"EDGE REFLEX ALERT: Critical environmental threshold breached at {time_steps[i].strftime('%H:%M:%S')}. Mechanical actuators deployed locally at {edge_latency:.1f}ms latency.")
        else:
            if network_state == "Disconnected (Network Blackout)":
                log_placeholder.warning(f"Log: Tick {i} processed via Edge Computing. Network disconnected. Data cached in local queue.")
            else:
                log_placeholder.success(f"Log: Tick {i} processed via Edge Computing. Background telemetry synced to AWS Cloud successfully.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The hybrid edge-cloud framework successfully maintained cyber-physical actuation regardless of cloud connectivity states.")
else:
    st.info("Click 'Initialize WSAN Edge Node' in the sidebar to simulate the cyber-physical agricultural environment.")