import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

# Load the dataset
file_path = 'World Energy Consumption.csv'
energy_data = pd.read_csv(file_path)

# Data Cleaning
# Drop duplicate rows if any
energy_data.drop_duplicates(inplace=True)

# Minimum Expected Statistics: Dataframe describe and correlation
numeric_data = energy_data.select_dtypes(include=['number'])
print(numeric_data.describe())

# Calculate skewness and kurtosis for each numeric column
skewness = numeric_data.apply(lambda x: skew(x.dropna()))
kurtosis_values = numeric_data.apply(lambda x: kurtosis(x.dropna()))

print("\nSkewness of numeric columns:\n", skewness)
print("\nKurtosis of numeric columns:\n", kurtosis_values)

# Reducing the number of numeric columns for a clearer heatmap
selected_numeric_columns = numeric_data[['year', 'wind_consumption', 'solar_consumption', 'gdp', 'biofuel_consumption']]
print(selected_numeric_columns.corr())

# Filtering data for specific analysis: Focusing on user-specified countries
selected_countries = ['United States', 'United Kingdom', 'Canada', 'India', 'Pakistan']
selected_countries_data = energy_data[energy_data['country'].isin(selected_countries)]
selected_data_filtered = selected_countries_data[(selected_countries_data['year'] >= 2015) & (selected_countries_data['year'] <= 2020)]

# Function to create Bar Chart: Distribution of wind consumption by year for selected countries
def plot_bar_chart():
    plt.figure(figsize=(10, 6))
    sns.barplot(data=selected_data_filtered, x='year', y='wind_consumption', hue='country', ci=None)
    plt.title('Distribution of Wind Consumption by Year for Selected Countries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Wind Consumption (TWh)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.legend(title='Country', fontsize='medium', title_fontsize='large', prop={'weight': 'bold'})
    plt.tight_layout()
    plt.show()

# Function to create Line Chart: Trends in Wind Consumption for Selected Countries (2015-2020)
def plot_line_chart():
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid") 
    sns.lineplot(data=selected_data_filtered, x='year', y='wind_consumption', hue='country', marker='o', linewidth=3, palette='Set1', alpha=1, legend='full')

    plt.title('Trends in Wind Consumption for Selected Countries (2015-2020)', fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel('Year', fontsize=14, fontweight='bold', color='darkblue')
    plt.ylabel('Wind Consumption (TWh)', fontsize=14, fontweight='bold', color='darkblue')
    plt.xticks(fontsize=12, fontweight='bold', color='black')
    plt.yticks(fontsize=12, fontweight='bold', color='black')

    plt.legend(title='Country', loc='upper left', fontsize='large', title_fontsize='x-large', fancybox=True, shadow=True, borderpad=1, frameon=False, prop={'weight': 'bold'})
    plt.grid(visible=True, linestyle='--', linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.show()

# Function to create Pie Chart: Distribution of Wind Energy Share in Electricity for 2020
def plot_pie_chart():
    plt.figure(figsize=(10, 10))
    energy_2020 = selected_data_filtered[selected_data_filtered['year'] == 2020]
    wind_share_distribution = energy_2020.groupby('country')['wind_share_elec'].sum()
    colors = sns.color_palette('pastel')[0:5]
    
    # Creating the pie chart with larger text for better readability
    plt.pie(
        wind_share_distribution, 
        labels=wind_share_distribution.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        explode=[0.1] * len(wind_share_distribution), 
        shadow=True, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
        textprops={'fontsize': 14, 'fontweight': 'bold'}  # Increasing the font size and making it bold
    )
    
    # Setting the title with bold font and larger size
    plt.title('Wind Energy Share in Electricity for Selected Countries (2020)', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Function to create Box Plot: Distribution of Wind Consumption by Country
def plot_box_wind_consumption():
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=selected_data_filtered, x='country', y='wind_consumption', palette='muted')
    plt.title('Distribution of Wind Consumption by Country (2015-2020)', fontsize=18, fontweight='bold')
    plt.xlabel('Country', fontsize=14, fontweight='bold')
    plt.ylabel('Wind Consumption (TWh)', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold', rotation=45)
    plt.yticks(fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Function to create Heatmap: Correlation between Selected Numeric Variables for Two Countries
def plot_heatmap_two_countries(country1, country2):
    filtered_two_countries = selected_data_filtered[selected_data_filtered['country'].isin([country1, country2])]
    numeric_two_countries = filtered_two_countries.select_dtypes(include=['number'])[['year', 'wind_consumption', 'solar_consumption', 'gdp', 'biofuel_consumption']]
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_two_countries.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title(f'Correlation Heatmap of Numeric Variables ({country1} & {country2})', fontsize=18, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold', rotation=45)
    plt.yticks(fontsize=12, fontweight='bold', rotation=0)
    plt.tight_layout()
    plt.show()

# Call the functions to create plots
plot_bar_chart()
plot_line_chart()
plot_pie_chart()
plot_heatmap_two_countries('United States', 'India')