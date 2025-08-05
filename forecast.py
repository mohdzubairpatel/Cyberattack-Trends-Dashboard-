import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import plotly.express as px

# Load cleaned dataset
df = pd.read_csv("data/cyberattacks_by_year.csv")
# print(df.head())

# Prepare data for Prophet
df_prophet = df.rename(columns={'Year': 'ds', 'Total_Attacks': 'y'})
df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], format='%Y')

# Initialize and train model
model = Prophet()
model.fit(df_prophet)

# Make future dataframe for next 5 years
future = model.make_future_dataframe(periods=5, freq='Y')

# Predict
forecast = model.predict(future)

# Round forecast values to whole numbers
forecast['yhat'] = forecast['yhat'].round()
forecast['yhat_lower'] = forecast['yhat_lower'].round()
forecast['yhat_upper'] = forecast['yhat_upper'].round()

# Save forecast to CSV 
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv("data/forecast_attacks.csv", index=False)

# 📊 Interactive forecast plot
fig = px.line(forecast, x='ds', y='yhat', title='🔮 Forecasted Cyberattacks ',
              labels={'ds': 'Year', 'yhat': 'Predicted Attacks'})

# Add confidence intervals
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot'))
fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot'))

fig.update_traces(hovertemplate='Year: %{x|%Y}<br>Attacks: %{y}')
fig.show()