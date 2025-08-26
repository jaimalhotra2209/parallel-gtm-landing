#!/usr/bin/env python3
"""
Check the actual content of Market Research and Parallel Use Case columns
"""

import pandas as pd

def check_content():
    """
    Check the actual content of the columns to verify separation
    """
    
    df = pd.read_csv('ceo_sourcing_results.csv')
    
    print("🔍 Checking content separation...")
    
    # Check first company (Greptile)
    print("\n" + "="*80)
    print("GREPTILE - MARKET RESEARCH:")
    print("="*80)
    market_research = df[df['Company'] == 'Greptile']['Market Research'].iloc[0]
    print(market_research[:500] + "..." if len(market_research) > 500 else market_research)
    
    print("\n" + "="*80)
    print("GREPTILE - PARALLEL USE CASE:")
    print("="*80)
    parallel_usecase = df[df['Company'] == 'Greptile']['Parallel Use Case'].iloc[0]
    print(parallel_usecase[:500] + "..." if len(parallel_usecase) > 500 else parallel_usecase)
    
    # Check if there's overlap
    print("\n" + "="*80)
    print("CHECKING FOR OVERLAP:")
    print("="*80)
    
    market_lower = market_research.lower()
    parallel_lower = parallel_usecase.lower()
    
    # Check if Market Research contains Parallel API content
    if 'parallel' in market_lower and 'api' in market_lower:
        print("⚠️  Market Research contains 'parallel' and 'api' keywords")
        # Find the context
        market_words = market_lower.split()
        for i, word in enumerate(market_words):
            if word == 'parallel' and i < len(market_words) - 1:
                if market_words[i+1] == 'api' or 'api' in market_words[i+1]:
                    print(f"   Found 'parallel api' in Market Research around word {i}")
    else:
        print("✅ Market Research does NOT contain Parallel API content")
    
    # Check if Parallel Use Case contains market research content
    market_keywords = ['market', 'sector', 'competitor', 'funding', 'revenue', 'growth']
    market_matches = [kw for kw in market_keywords if kw in parallel_lower]
    if market_matches:
        print(f"⚠️  Parallel Use Case contains market keywords: {market_matches}")
    else:
        print("✅ Parallel Use Case does NOT contain market research keywords")
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print(f"Market Research length: {len(market_research)} characters")
    print(f"Parallel Use Case length: {len(parallel_usecase)} characters")
    print(f"Market Research starts with: {market_research[:100]}...")
    print(f"Parallel Use Case starts with: {parallel_usecase[:100]}...")

if __name__ == "__main__":
    check_content()


