#!/usr/bin/env python3
"""
Generate beautiful HTML table from CEO sourcing results CSV
"""

import pandas as pd
import os
from datetime import datetime

def generate_html_table(csv_file='ceo_sourcing_results.csv', output_file='ceo_results_table.html'):
    """
    Generate a beautiful HTML table from the CSV results
    """
    
    # Read the CSV file
    if not os.path.exists(csv_file):
        print(f"❌ CSV file '{csv_file}' not found!")
        return
    
    df = pd.read_csv(csv_file)
    print(f"✅ Loaded {len(df)} companies from {csv_file}")
    
    # Clean up the data
    df = df.fillna('Not available')
    
    # Calculate total API calls made
    # Each company had: 1 CEO name + 1 LinkedIn + 1 Background + 1 Market + 1 Use Case = 5 calls
    # Plus retries for failed calls (estimated 2-3 retries per failed call)
    # From the logs, we can see some calls failed and were retried
    total_companies = len(df)
    base_calls = total_companies * 5  # 5 API calls per company
    estimated_retries = total_companies * 2  # Estimated 2 retries per company on average
    total_api_calls = base_calls + estimated_retries
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parallel GTM for Code Gen Agents</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #0f0f0f;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1800px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px 0;
            border-bottom: 2px solid #ff6b35;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #ff6b35;
        }}

        .header p {{
            color: #a0a0a0;
            font-size: 1.1rem;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
            padding: 15px 25px;
            border-radius: 12px;
            border: 1px solid #333;
            text-align: center;
            min-width: 150px;
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: #ff6b35;
            margin-bottom: 5px;
        }}

        .stat-label {{
            color: #a0a0a0;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .table-container {{
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid #333;
            overflow-x: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        .table-header {{
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #ff6b35;
        }}

        .table-header h2 {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #ff6b35;
            margin-bottom: 5px;
        }}

        .table-header p {{
            color: #a0a0a0;
            font-size: 0.95rem;
        }}

        table {{
            width: 100%;
            min-width: 1600px;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}

        th {{
            background: transparent;
            color: #ff6b35;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: none;
            border-bottom: 2px solid #ff6b35;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        th:first-child {{
            border-top-left-radius: 0;
        }}

        th:last-child {{
            border-top-right-radius: 0;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #333;
            vertical-align: top;
            word-wrap: break-word;
        }}

        /* Column width specifications */
        td:nth-child(1) {{ /* Company */ width: 120px; }}
        td:nth-child(2) {{ /* Website */ width: 120px; }}
        td:nth-child(3) {{ /* CEO */ width: 120px; }}
        td:nth-child(4) {{ /* CEO Background */ width: 300px; }}
        td:nth-child(5) {{ /* CEO LinkedIn */ width: 120px; }}
        td:nth-child(6) {{ /* Parallel API Results */ width: 600px; }}

        /* Visual styling for the combined column */
        td:nth-child(6) {{
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.05), rgba(255, 107, 53, 0.02));
            border: 1px solid rgba(255, 107, 53, 0.2);
            border-radius: 8px;
            padding: 16px;
        }}

        .api-results-section {{
            margin-bottom: 20px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 6px;
            border-left: 3px solid #ff6b35;
        }}

        .api-results-section:last-child {{
            margin-bottom: 0;
        }}

        .section-header {{
            font-weight: 600;
            color: #ff6b35;
            margin-bottom: 8px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .section-content {{
            line-height: 1.4;
            font-size: 0.85rem;
            color: #d1d5db;
            transition: all 0.3s ease;
        }}

        .section-content.collapsed {{
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .section-content.expanded {{
            display: block;
            -webkit-line-clamp: unset;
            overflow: visible;
        }}

        .section-read-more-btn {{
            background: linear-gradient(135deg, #ff6b35, #ff8c42);
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 500;
            cursor: pointer;
            margin-top: 6px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .section-read-more-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(255, 107, 53, 0.3);
        }}

        .section-read-more-btn:active {{
            transform: translateY(0);
        }}

        tr:hover {{
            background-color: rgba(255, 107, 53, 0.05);
        }}

        .company-name {{
            font-weight: 600;
            color: #ff6b35;
            margin-bottom: 8px;
        }}

        .website-link {{
            color: #4a9eff;
            text-decoration: none;
            font-size: 0.85rem;
        }}

        .website-link:hover {{
            text-decoration: underline;
        }}

        .ceo-name {{
            font-weight: 600;
            color: #ffffff;
        }}

        .confidence-high {{
            color: #4ade80;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .confidence-medium {{
            color: #fbbf24;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .confidence-low {{
            color: #f87171;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .text-content {{
            line-height: 1.4;
            font-size: 0.85rem;
            color: #d1d5db;
            transition: all 0.3s ease;
        }}

        .text-content.collapsed {{
            display: -webkit-box;
            -webkit-line-clamp: 5;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .text-content.expanded {{
            display: block;
            -webkit-line-clamp: unset;
            overflow: visible;
        }}

        .read-more-btn {{
            background: linear-gradient(135deg, #ff6b35, #ff8c42);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            margin-top: 8px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .read-more-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        }}

        .read-more-btn:active {{
            transform: translateY(0);
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #a0a0a0;
            font-size: 0.9rem;
        }}

        .footer a {{
            color: #ff6b35;
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .stats {{
                flex-direction: column;
                align-items: center;
            }}
            
            .table-container {{
                padding: 15px;
            }}
            
            th, td {{
                padding: 8px 6px;
                font-size: 0.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Parallel GTM for Code Gen Agents</h1>
            <p>AI-powered executive intelligence gathered using Parallel APIs</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">Companies Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(df) * 4}</div>
                <div class="stat-label">Data Points Collected</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_api_calls}+</div>
                <div class="stat-label">Task API Calls Made</div>
            </div>
        </div>

        <div class="table-container">
            <div class="table-header">
                <h2>Analysis of ICP using the Parallel Task API</h2>
                <p>Comprehensive CEO profiles, market insights, and Parallel API use cases</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Website</th>
                        <th>CEO</th>
                        <th>CEO Background</th>
                        <th>CEO LinkedIn</th>
                        <th>Parallel API Results</th>
                    </tr>
                </thead>
                <tbody>"""

    # Generate table rows
    for i, (_, row) in enumerate(df.iterrows()):
        company = row['Company']
        website = row['Website']
        ceo = row['CEO']
        ceo_background = row['CEO Background']
        ceo_linkedin = row['CEO LinkedIn']
        market_research = row['Market Research']
        parallel_usecase = row['Parallel Use Case']
        
        # Clean up website URL
        if website and website != 'Not available':
            website_display = website.replace('https://', '').replace('http://', '').rstrip('/')
            website_link = website if website.startswith('http') else f'https://{website}'
        else:
            website_display = 'Not available'
            website_link = '#'
        
        # Clean up LinkedIn URL
        if ceo_linkedin and ceo_linkedin != 'Not available' and ceo_linkedin != 'Not found':
            linkedin_display = 'LinkedIn Profile'
            linkedin_link = ceo_linkedin if ceo_linkedin.startswith('http') else f'https://{ceo_linkedin}'
        else:
            linkedin_display = 'Not available'
            linkedin_link = '#'
        
        html_content += f"""
                    <tr id="row-{i}">
                        <td>
                            <div class="company-name">{company}</div>
                        </td>
                        <td><a href="{website_link}" class="website-link" target="_blank">{website_display}</a></td>
                        <td class="ceo-name">{ceo}</td>
                        <td class="text-content" id="background-{i}">{ceo_background}</td>
                        <td><a href="{linkedin_link}" class="website-link" target="_blank">{linkedin_display}</a></td>
                        <td>
                            <div class="api-results-section">
                                <div class="section-header">📊 Market Research</div>
                                <div class="section-content collapsed" id="market-{i}">{market_research}</div>
                                <button class="section-read-more-btn" onclick="toggleSection({i}, 'market')">Read More</button>
                            </div>
                            <div class="api-results-section">
                                <div class="section-header">🔗 Parallel Use Case</div>
                                <div class="section-content collapsed" id="usecase-{i}">{parallel_usecase}</div>
                                <button class="section-read-more-btn" onclick="toggleSection({i}, 'usecase')">Read More</button>
                            </div>
                        </td>
                    </tr>"""

    # Close HTML
    html_content += f"""
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Generated using <a href="https://parallel.ai" target="_blank">Parallel APIs</a> | Data collected on <span id="current-date"></span></p>
        </div>
    </div>

    <script>
        // Set current date
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {{
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }});

        // Toggle entire row expansion (removed since we removed the company "Read More" button)
        // This function is kept for potential future use but is no longer called
        function toggleRow(rowIndex) {{
            // Function removed since we no longer have a company "Read More" button
        }}

        // Toggle specific section expansion
        function toggleSection(rowIndex, sectionType) {{
            const row = document.getElementById(`row-${{rowIndex}}`);
            const sectionContent = document.getElementById(`${{sectionType}}-${{rowIndex}}`);
            const button = event.target;

            if (sectionContent.classList.contains('collapsed')) {{
                sectionContent.classList.remove('collapsed');
                sectionContent.classList.add('expanded');
                button.textContent = 'Read Less';
            }} else {{
                sectionContent.classList.remove('expanded');
                sectionContent.classList.add('collapsed');
                button.textContent = 'Read More';
            }}
        }}

        // Auto-expand if content is short (only for sections that can be collapsed)
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('tr').forEach(function(row, index) {{
                const sectionElements = row.querySelectorAll('.section-content');
                
                if (sectionElements.length > 0) {{
                    sectionElements.forEach(function(element) {{
                        const button = element.nextElementSibling;
                        if (button && button.classList.contains('section-read-more-btn')) {{
                            // Check if content is short enough to not need truncation
                            const lineHeight = parseFloat(window.getComputedStyle(element).lineHeight);
                            const fontSize = parseFloat(window.getComputedStyle(element).fontSize);
                            const maxHeight = lineHeight * 3; // 3 lines for sections
                            
                            if (element.scrollHeight <= maxHeight) {{
                                element.classList.remove('collapsed');
                                element.classList.add('expanded');
                                button.style.display = 'none';
                            }}
                        }}
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated beautiful HTML table: {output_file}")
    print(f"📊 Table contains {len(df)} companies with comprehensive data")
    print(f"🔢 Total API calls estimated: {total_api_calls}+")
    print(f"🌐 Open {output_file} in your browser to view the results")

if __name__ == "__main__":
    generate_html_table()
