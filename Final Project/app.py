import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the DataFrame
df = pd.read_csv('/content/merged_final_amazon.csv')  # Replace 'your_data.csv' with the path to your CSV file
df = df.drop('Unnamed: 0', axis=1)
st.set_page_config(layout="wide")
# Set column names
df.columns = ['url', 'ASIN', 'title', 'brand', 'fulfillment', 'category', 'BSR', 'subcategory',
              'price', 'price_trend_90days', 'monthly_sales', 'sales_trend_90days', 'monthly_revenue',
              'review_count', 'reviews_rating', 'seller', 'num_active_sellers', 'last_year_sales', 'sales_yoy',
              'size_tier', 'length', 'width', 'height', 'weight', 'storage_fee_jan_sep', 'storage_fee_oct_dec',
              'best_sales_period', 'age_months', 'num_images', 'variation_count', 'sales_to_reviews']







# Top 10 highest selling categories
category_sales = df.groupby('category')['monthly_sales'].sum().reset_index()
top_10_categories = category_sales.sort_values(by='monthly_sales', ascending=False).head(10)

# Top Selling Products
highest_selling_products = df.loc[df.groupby('category')['last_year_sales'].idxmax()]

# Number of products in each category with good BSR
df_filtered = df.dropna(subset=['BSR', 'category'])
bsr_desirable_range = df_filtered[(df_filtered['BSR'] >= 1) & (df_filtered['BSR'] <= 10000)]
products_in_desirable_bsr = bsr_desirable_range.groupby('category').size().reset_index(name='count')

# Average last year sales
average_last_year_sales = df.groupby('category')['last_year_sales'].mean().reset_index()

# Convert 'best_sales_period' to datetime format with errors='coerce'
df['best_sales_period'] = pd.to_datetime(df['best_sales_period'], errors='coerce')

# Drop rows with NaT values
temp = df.dropna(subset=['best_sales_period'])

# Extract month from 'best_sales_period'
temp['best_sales_month'] = temp['best_sales_period'].dt.month

# Group data by category and best sales month
category_month_sales = temp.groupby(['category', 'best_sales_month']).size().reset_index(name='total_sales')

# Find the best sales month for each category
best_sales_month_per_category = category_month_sales.loc[category_month_sales.groupby('category')['total_sales'].idxmax()]

# Review count by category
review_count_by_subcategory = df.groupby('category')['review_count'].sum().reset_index()
review_count_by_subcategory = review_count_by_subcategory.sort_values(by='review_count', ascending=False)

# Pie chart of distribution by fulfillment count
fulfillment_counts = df['fulfillment'].value_counts().reset_index()
fulfillment_counts.columns = ['Fulfillment Type', 'Count']

# Display the dashboard
st.markdown("<h1 style='text-align: center;'>Market Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center;'>Sidebar Content</h1>", unsafe_allow_html=True)

# Display the category selection dropdown in the sidebar
selected_category = st.sidebar.selectbox('Select a category', ['All'] + df['category'].unique().tolist())

# Filter data based on selected category
if selected_category != 'All':
    df = df[df['category'] == selected_category]

if selected_category == 'Beauty':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Beauty']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Beauty")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Lipstick")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Maybelline") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Beauty Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Beauty')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Beauty')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Car & Motorbike':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Car & Motorbike']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Car & Motorbike")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Open Face Helmet")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Vega") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Car & Motorbike Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Car & Motorbike')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Car & Motorbike')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)

elif selected_category == 'Clothing & Accessories':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Clothing & Accessories']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Clothing & Accessories")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Pyjama Set")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Ariel") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Clothing & Accessories Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Clothing & Accessories')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Clothing & Accessories')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Computers & Accessories':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Computers & Accessories']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Computers & Accessories")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Pen Drive")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("TP-Link") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Computers & Accessories Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Computers & Accessories')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Computers & Accessories')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Electronics':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Electronics']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Electronics")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("In-Ear")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Boat") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Electronics Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Electronics')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Electronics')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Health & Personal Care':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Health & Personal Care']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Health & Personal Care")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Sanitary Napkins")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Whisper") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Health & Personal Care Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Health & Personal Care')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Health & Personal Care')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Home & Kitchen':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Home & Kitchen']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Home & Kitchen")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Clothes Cover")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Global Grabbers") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Home & Kitchen Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Home & Kitchen')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Home & Kitchen')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Industrial & Scientific':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Industrial & Scientific']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Industrial & Scientific")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Water Quality and Instrumentation")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("3M") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Industrial & Scientific Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Industrial & Scientific')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Industrial & Scientific')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Musical Instruments':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Musical Instruments']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Musical Instruments")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Wireless")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Audio Array") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Musical Instruments Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Musical Instruments')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Musical Instruments')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Office Products':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Office Products']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Office Products")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Appoinment Book and Planners")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Reynolds") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Office Products Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Office Products')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Office Products')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Shoes & Handbags':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Shoes & Handbags']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Shoes & Handbags")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Flip-flop & Slipper")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Doctor Extra Soft") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Shoes & Handbags Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Shoes & Handbags')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Shoes & Handbags')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Sports, Fitness & Outdoors':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Sports, Fitness & Outdoors']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Sports, Fitness & Outdoors")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Racquets")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Li-Ning") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Sports, Fitness & Outdoors Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Sports, Fitness & Outdoors')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Sports, Fitness & Outdoors')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Toys & Games':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Toys & Games']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Toys & Games")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Car & Race Car")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Pikipo") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Toys & Games Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Toys & Games')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Toys & Games')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)


elif selected_category == 'Watches':
    col1, col2 = st.columns(2)
    df_temp = df[df['category'] == 'Watches']

    with col1:
      st.subheader("Top 10 Subcategories by Sales in Watches")
      # Aggregate sales by subcategory
      subcategory_sales = df_temp.groupby('subcategory')['monthly_sales'].sum().reset_index()

      # Sort subcategories by sales in descending order
      top_10_subcategories = subcategory_sales.sort_values(by='monthly_sales', ascending=False).head(10)

      # Create plot
      fig = px.bar(top_10_subcategories, x='subcategory', y='monthly_sales',
                  labels={'monthly_sales': 'Monthly Sales', 'subcategory': 'Subcategory'})

      # Show plot
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      st.subheader("Highest Selling Product")
      with st.container():
        st.write("Wrist Watches")
        st.write('---')
        st.subheader("Highest Selling Brand")  
        st.write("Fire-Boltt") 

    st.write('---') 
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("Watches Category and Subcategory Distribution")
      fig_sunburst = px.sunburst(df_temp, path=['category', 'subcategory'])

      # Show sunburst chart
      st.plotly_chart(fig_sunburst, use_container_width=True)

    with col4:
      st.subheader('Top Selling Brands in Watches')
      top_selling_brands = df_temp.groupby('brand')['last_year_sales'].sum().nlargest(10)

      # Plotting
      plt.figure(figsize=(10, 6))
      top_selling_brands.plot(kind='bar', color='skyblue')
      plt.title('Top Selling Brands in Watches')
      plt.xlabel('Brand')
      plt.ylabel('Total Last year Sales')
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()
      st.pyplot(plt)

else:
  # Display Top Categories by Sales and Top Selling Products side by side in one row
  st.subheader('Top Categories by Sales')

  # Split the layout into two columns
  col1, col2 = st.columns(2)

  # Display Top Categories by Sales (Bar Chart) in the first column
  with col1:
      fig1 = px.bar(top_10_categories, x='category', y='monthly_sales',
                    labels={'monthly_sales': 'Monthly Sales', 'category': 'Category'})
      fig1.update_layout(height=400, width=500)  # Adjust the height and width of the plot
      st.plotly_chart(fig1, use_container_width=True)  # Use container to fit the plot

  # Display Top Categories by Sales (Pie Chart) in the second column
  with col2:
      fig2 = px.pie(top_10_categories, values='monthly_sales', names='category')
      fig2.update_layout(height=400, width=500)  # Adjust the height and width of the plot
      st.plotly_chart(fig2, use_container_width=True)  # Use container to fit the plot

  st.write('---')
  col7, col8 = st.columns(2)
  # Display Top Selling Products in the second row
  with col7:
    st.subheader('Top Selling Products')
    highest_selling_products_reset_index = highest_selling_products.reset_index(drop=True)
    highest_selling_products_reset_index.index += 1
    highest_selling_products_reset_index = highest_selling_products_reset_index.rename(columns={'category': 'Category','title': 'Title','last_year_sales': 'Last Year Sale'})
    highest_selling_products_reset_index['Last Year Sale'] = highest_selling_products_reset_index['Last Year Sale'].astype(int)
    st.write(highest_selling_products_reset_index[['Category', 'Title', 'Last Year Sale']])

  with col8:
    st.subheader('Number of Products with Desirable BSR by Category')
    fig3 = px.bar(products_in_desirable_bsr, x='category', y='count',
                  labels={'category': 'Category', 'count': 'Number of Products'})
    fig3.update_layout(xaxis={'tickangle': 45})
    fig3.update_layout(height=400, width=800)  # Adjust the height and width of the plot
    st.plotly_chart(fig3, use_container_width=True)  # Use container to fit the plot

  # Display Average Last Year Sales and Best Sales Month side by side in a new row
  st.write('---')  
  col9, col10 = st.columns(2)
  with col9:
    st.subheader("Top selling brand")
    top_selling_brands = df.groupby('brand')['last_year_sales'].sum().nlargest(10)
    fig, ax = plt.subplots()
    top_selling_brands.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Top Selling Brands')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Total Last year Sales')
    ax.set_xticklabels(top_selling_brands.index, rotation=45, ha='right')
    st.pyplot(fig)

  with col10:
    st.subheader("Top Reviewed Brands")
    average_review_ratings = df.groupby('brand')['review_count'].mean()
    sorted_brands = average_review_ratings.sort_values(ascending=False)
    top_n = 10
    top_reviewed_brands = sorted_brands.head(top_n)
    fig, ax = plt.subplots()
    top_reviewed_brands.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Top Reviewed Brands')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Total Number of Reviews')
    ax.set_xticklabels(top_reviewed_brands.index, rotation=45, ha='right')
    st.pyplot(fig)

  st.write('---')
  col3, col4 = st.columns(2)
  with col3:
      st.subheader('Average Last Year Sales')
      average_last_year_sales_reset_index = average_last_year_sales.reset_index(drop=True)
      average_last_year_sales_reset_index.index += 1
      average_last_year_sales_reset_index = average_last_year_sales_reset_index.rename(columns={'category': 'Category','last_year_sales': 'Last Year Sale'})
      average_last_year_sales_reset_index['Last Year Sale'] = average_last_year_sales_reset_index['Last Year Sale'].astype(int)
      st.table(average_last_year_sales_reset_index)

  # Display Best Sales Month in the second sub-column
  with col4:
      st.subheader('Best Sales Month')
      fig4 = px.bar(best_sales_month_per_category, x='category', y='best_sales_month',
                    color='best_sales_month',
                    labels={'category': 'Category', 'best_sales_month': 'Best Sales Month'})
      fig4.update_layout(height=500, width=400)
      fig4.update_layout(xaxis={'tickangle': 45})
      st.plotly_chart(fig4, use_container_width=True)  # Use container to fit the plot

  # Display Reviews Count and Fulfillment Type Distribution side by side in a new row
  st.write('---')  # Add a horizontal line to visually separate the rows
  col5, col6 = st.columns(2)

  # Display Reviews Count in the first sub-column
  with col5:
      st.subheader('Reviews Count')
      fig5 = px.bar(review_count_by_subcategory, x='category', y='review_count',
                    labels={'category': 'Category', 'review_count': 'Review Count'})
      fig5.update_layout(height=400, width=400)  
      fig5.update_layout(xaxis={'tickangle': 45})
      st.plotly_chart(fig5, use_container_width=True)  # Use container to fit the plot

  # Display Fulfillment Type Distribution in the second sub-column
  with col6:
      st.subheader('Fulfillment Type Distribution')
      fig6 = px.pie(fulfillment_counts, values='Count', names='Fulfillment Type')
      fig6.update_layout(height=400, width=400)  # Adjust the height and width of the plot
      st.plotly_chart(fig6, use_container_width=True)