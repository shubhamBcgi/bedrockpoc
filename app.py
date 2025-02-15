from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.utils
import json

app = Flask(__name__)

# Read the Excel file
df = pd.read_excel('community.xlsx', sheet_name='Sheet2')

@app.route('/')
def index():
    # Basic statistics about car brands
    # Add error handling for car brands
    def get_brand(x):
        if pd.isna(x):  # Check if the value is NaN
            return 'Unknown'
        try:
            return str(x).split()[0]  # Convert to string and get first word
        except:
            return 'Unknown'

    car_brands = df['Car_Model'].apply(get_brand)
    brand_counts = car_brands.value_counts()
    
    # Create a pie chart for car brands
    fig_brands = px.pie(values=brand_counts.values, 
                       names=brand_counts.index, 
                       title='Distribution of Car Brands')
    brand_chart = json.dumps(fig_brands, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Average car age by brand
    df['Car_Age'] = 2023 - pd.to_numeric(df['Car_Year'], errors='coerce')
    avg_age_by_brand = df.groupby(car_brands)['Car_Age'].mean().round(1)
    
    # Create a bar chart for average car age
    fig_age = px.bar(x=avg_age_by_brand.index, 
                     y=avg_age_by_brand.values,
                     title='Average Car Age by Brand',
                     labels={'x': 'Brand', 'y': 'Average Age (years)'})
    age_chart = json.dumps(fig_age, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html',
                         tables=[df.to_html(classes='data', index=False)],
                         brand_chart=brand_chart,
                         age_chart=age_chart,
                         brand_counts=brand_counts.to_dict())

if __name__ == '__main__':
    app.run(debug=True)