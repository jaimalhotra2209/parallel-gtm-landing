import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('ceo_sourcing_results.csv')

# Read the HTML file
with open('parallel_gtm_landing.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update each company's data
for index, row in df.iterrows():
    company_name = row['Company']
    
    # Update company background
    company_desc = row['Company Description'] if pd.notna(row['Company Description']) and row['Company Description'] != 'Not found' else 'Not available'
    background_pattern = rf'id="background-{index}">[^<]*</td>'
    background_replacement = f'id="background-{index}">{company_desc}</td>'
    html_content = re.sub(background_pattern, background_replacement, html_content)
    
    # Update market research
    market_research = row['Market Research'] if pd.notna(row['Market Research']) and row['Market Research'] != 'Not found' else 'Not available'
    market_pattern = rf'id="market-{index}">[^<]*</div>'
    market_replacement = f'id="market-{index}">{market_research}</div>'
    html_content = re.sub(market_pattern, market_replacement, html_content)
    
    # Update parallel use case
    parallel_usecase = row['Parallel Use Case'] if pd.notna(row['Parallel Use Case']) and row['Parallel Use Case'] != 'Not found' else 'Not available'
    usecase_pattern = rf'id="usecase-{index}">[^<]*</div>'
    usecase_replacement = f'id="usecase-{index}">{parallel_usecase}</div>'
    html_content = re.sub(usecase_pattern, usecase_replacement, html_content)

# Write the updated HTML back to the file
with open('parallel_gtm_landing.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Landing page updated with fresh data from CSV!")
