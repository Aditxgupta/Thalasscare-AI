# app.py (CORRECTED Version with Shading and Filtering)
import streamlit as st
import pandas as pd
import joblib
from prophet import Prophet
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Blood Forecaster 360°",
    page_icon="🩸",
    layout="wide"
)

# --- Model Loading ---
@st.cache_resource
def load_all_models():
    """Loads supply, demand, and availability models from disk."""
    try:
        supply_models = joblib.load('blood_supply_forecast_models.joblib')
        demand_models = joblib.load('demand_forecast_models.joblib')
        availability_models = joblib.load('availability_forecast_models.joblib')
        return supply_models, demand_models, availability_models
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}. Please ensure all .joblib files are in the root directory.")
        return None, None, None

supply_models, demand_models, availability_models = load_all_models()

# --- App Header ---
st.title("🩸 Blood Inventory & Demand Dashboard")
st.markdown("A complete forecasting tool for daily inventory and long-term supply vs. demand planning.")

# --- Main Application ---
if all([supply_models, demand_models, availability_models]):
    # ==============================================================================
    # SECTION 1: DAILY INVENTORY FORECAST
    # ==============================================================================
    st.header("📊 Daily Inventory Snapshot")
    target_date = st.date_input("Select a Future Date for the Snapshot", value=datetime.now().date() + pd.Timedelta(days=7))
    future_df_daily = pd.DataFrame({'ds': [target_date]})

    def get_prediction(models_dict, blood_group, df):
        model = models_dict.get(blood_group)
        if model:
            forecast = model.predict(df)
            prediction = int(round(forecast['yhat'].iloc[0]))
            return max(0, prediction)
        return 0

    predictions_daily = []
    blood_groups_sorted = sorted(supply_models.keys())
    for bg in blood_groups_sorted:
        availability_pred = get_prediction(availability_models, bg, future_df_daily)
        supply_pred = get_prediction(supply_models, bg, future_df_daily)
        demand_pred = get_prediction(demand_models, bg, future_df_daily)
        predictions_daily.append({
            'Blood Group': bg, 'Starting Inventory (Availability)': availability_pred,
            'Total Available Supply': availability_pred + supply_pred,
            'Predicted Demand': demand_pred
        })
    
    plot_df_daily = pd.DataFrame(predictions_daily)
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=plot_df_daily['Blood Group'], y=plot_df_daily['Starting Inventory (Availability)'], name='Starting Inventory', mode='lines+markers', line=dict(color='royalblue')))
    fig_daily.add_trace(go.Scatter(x=plot_df_daily['Blood Group'], y=plot_df_daily['Total Available Supply'], name='Total Available Supply', mode='lines+markers', line=dict(color='green', width=4)))
    fig_daily.add_trace(go.Scatter(x=plot_df_daily['Blood Group'], y=plot_df_daily['Predicted Demand'], name='Predicted Demand', mode='lines+markers', line=dict(color='red', width=2, dash='dash')))

    ## FIX 1: ADDED THE SHADED AREAS BACK TO THE DAILY GRAPH ##
    fig_daily.add_trace(go.Scatter(
        x=plot_df_daily['Blood Group'], y=np.maximum(plot_df_daily['Total Available Supply'], plot_df_daily['Predicted Demand']),
        fill='tonexty', fillcolor='rgba(0,255,0,0.2)', line=dict(width=0), name='Surplus', showlegend=True))
    fig_daily.add_trace(go.Scatter(
        x=plot_df_daily['Blood Group'], y=np.minimum(plot_df_daily['Total Available Supply'], plot_df_daily['Predicted Demand']),
        fill='tonexty', fillcolor='rgba(255,0,0,0.2)', line=dict(width=0), name='Deficit', showlegend=True))

    fig_daily.update_layout(title_text=f'Daily Inventory Forecast for {target_date.strftime("%Y-%m-%d")}', xaxis_title='Blood Group', yaxis_title='Number of Units', height=500, template='plotly_white')
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("---") 

    # ==============================================================================
    # SECTION 2: MULTI-WEEK SUPPLY VS. DEMAND FORECAST
    # ==============================================================================
    st.header("🗓️ 4-Week Supply vs. Demand Forecast")
    
    selected_blood_group = st.selectbox(
        "Select a Blood Group to Forecast",
        options=blood_groups_sorted
    )

    if selected_blood_group:
        supply_model = supply_models.get(selected_blood_group)
        demand_model = demand_models.get(selected_blood_group)
        
        future_df_weekly = supply_model.make_future_dataframe(periods=28)
        supply_forecast = supply_model.predict(future_df_weekly)
        demand_forecast = demand_model.predict(future_df_weekly)
        
        forecast_df = pd.DataFrame({
            'Date': supply_forecast['ds'],
            'Predicted Supply': supply_forecast['yhat'].apply(lambda x: max(0, x)),
            'Predicted Demand': demand_forecast['yhat'].apply(lambda x: max(0, x))
        })
        
        ## FIX 2: FILTER THE DATAFRAME TO SHOW ONLY FUTURE DATES ##
        forecast_df = forecast_df[forecast_df['Date'] >= pd.to_datetime('today').normalize()]

        fig_weekly = go.Figure()
        fig_weekly.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Predicted Supply'], name='Predicted Supply (New Donors)', mode='lines', line=dict(color='green', width=3)))
        fig_weekly.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Predicted Demand'], name='Predicted Demand (Requests)', mode='lines', line=dict(color='red', width=2, dash='dash')))
        fig_weekly.add_trace(go.Scatter(x=forecast_df['Date'], y=np.maximum(forecast_df['Predicted Supply'], forecast_df['Predicted Demand']), fill='tonexty', fillcolor='rgba(0,255,0,0.2)', line=dict(width=0), name='Surplus', showlegend=True))
        fig_weekly.add_trace(go.Scatter(x=forecast_df['Date'], y=np.minimum(forecast_df['Predicted Supply'], forecast_df['Predicted Demand']), fill='tonexty', fillcolor='rgba(255,0,0,0.2)', line=dict(width=0), name='Deficit', showlegend=True))
        
        fig_weekly.update_layout(
            title_text=f'4-Week Supply vs. Demand Forecast for {selected_blood_group}',
            xaxis_title='Date', yaxis_title='Number of Units', height=500, template='plotly_white', legend_title='Forecast')
        
        st.plotly_chart(fig_weekly, use_container_width=True)

else:
    st.warning("Models could not be loaded. Please check the file paths and try again.")