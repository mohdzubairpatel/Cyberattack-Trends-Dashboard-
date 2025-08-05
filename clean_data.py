import pandas as pd

# Load the raw dataset
df = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")

# Rename columns to simplify names
df.rename(columns={
    'Attack Type': 'Threat_Type',
    'Number of Affected Users': 'Records_Affected'
}, inplace=True)

# Show basic info
print("Initial shape:", df.shape)
print("Columns:", df.columns.tolist())

# Drop rows with missing Year or Threat Type
df = df.dropna(subset=['Year', 'Threat_Type'])

# Clean up text entries
df['Threat_Type'] = df['Threat_Type'].str.strip().str.lower()
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

# Optional: clean Records_Affected column
if 'Records_Affected' in df.columns:
    df['Records_Affected'] = pd.to_numeric(df['Records_Affected'], errors='coerce')

# Remove rows with missing records 
df = df.dropna(subset=['Records_Affected'])

# Group by Year to get total number of attacks
attacks_by_year = df.groupby('Year').size().reset_index(name='Total_Attacks')

#  Save to cleaned CSV for dashboard
attacks_by_year.to_csv("data/cyberattacks_by_year.csv", index=False)

print("Cleaned data saved to 'data/cyberattacks_by_year.csv'")

# Breakdown of attacks by Year and Threat Type
threat_by_year = df.groupby(['Year', 'Threat_Type']).size().reset_index(name='Count')
threat_by_year.to_csv("data/threat_types_by_year.csv", index=False)

print("Threat type breakdown saved to 'data/threat_types_by_year.csv'")
