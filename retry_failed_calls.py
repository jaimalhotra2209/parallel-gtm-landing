#!/usr/bin/env python3
"""
Retry failed Parallel API calls for companies with missing data
"""

import pandas as pd
import time
import random
import threading
from parallel import Parallel
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

# Initialize client with API key
client = Parallel(api_key="fdtxy0y6gmOFPJ7476UmF5mW4OVrzSN7P34zV3Qr")

class ParallelUseCase(BaseModel):
    overview: str = Field(description="How the specific company can use Parallel's APIs to improve their business. Include specific examples of how the company can use the APIs based on their product.")

def safe_call(func, *args, retries=1, delay=2, timeout=180, **kwargs):
    """Wrapper to safely call a function with timeout and retries.
       Returns tuple (value, confidence, citations)."""
    
    def run_with_timeout():
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    
    for attempt in range(1, retries+1):
        try:
            # Set up timeout using threading
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = run_with_timeout()
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout=timeout)
            
            if thread.is_alive():
                print(f"⏰ Timeout after {timeout}s on attempt {attempt}")
                if attempt == retries:
                    print(f"❌ Skipping after {retries} attempts due to timeout")
                    return None, None, None
                sleep_time = delay * attempt + random.uniform(0, 1)
                print(f"⚠️ Retrying in {sleep_time:.1f}s")
                time.sleep(sleep_time)
                continue
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
            
        except Exception as e:
            if attempt == retries:
                print(f"❌ Failed after {retries} attempts: {e}")
                return None, None, None
            sleep_time = delay * attempt + random.uniform(0, 1)
            print(f"⚠️ Error: {e} (retrying in {sleep_time:.1f}s)")
            time.sleep(sleep_time)
    
    return None, None, None

def fetch_parallel_usecase(company):
    prompt = f"Suggest specific ways {company['Company']} ({company['Website']}) can use Parallel's APIs to improve their business, with concrete examples."
    res = client.task_run.execute(input=prompt, output=ParallelUseCase, processor="core")
    return res.output.parsed.overview, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

def retry_failed_calls():
    """Retry API calls for companies with missing Parallel use case data"""
    
    # Read the current CSV
    try:
        df = pd.read_csv('ceo_sourcing_results.csv')
        print(f"✅ Loaded {len(df)} companies from CSV")
    except FileNotFoundError:
        print("❌ CSV file not found! Please run the main script first.")
        return
    
    # Find companies with missing Parallel use case data
    missing_data = df[df['Parallel Use Case'].isin(['Not found', 'Error fetching data', 'Not available', '']) | df['Parallel Use Case'].isna()]
    
    if len(missing_data) == 0:
        print("✅ All companies have Parallel use case data!")
        return
    
    print(f"🔄 Found {len(missing_data)} companies with missing Parallel use case data:")
    for _, row in missing_data.iterrows():
        print(f"  - {row['Company']} ({row['Website']})")
    
    print(f"\n⏰ Starting retry with 180-second timeout per request...")
    
    # Retry API calls for missing data
    updated_count = 0
    for i, (idx, row) in enumerate(missing_data.iterrows()):
        print(f"\n[{i+1}/{len(missing_data)}] Retrying: {row['Company']} ({row['Website']})")
        
        start_time = time.time()
        result, conf, basis = safe_call(fetch_parallel_usecase, row, timeout=180, retries=1)
        elapsed = time.time() - start_time
        
        if result and result != "Not found":
            df.at[idx, 'Parallel Use Case'] = result
            df.at[idx, 'UseCase Confidence'] = conf
            df.at[idx, 'UseCase Sources'] = basis
            updated_count += 1
            print(f"  ✅ Success: {row['Company']} - Updated Parallel use case (took {elapsed:.1f}s)")
        else:
            print(f"  ❌ Failed: {row['Company']} - Still no data (took {elapsed:.1f}s)")
    
    # Save updated CSV
    df.to_csv('ceo_sourcing_results.csv', index=False)
    print(f"\n✅ Updated CSV with {updated_count} new Parallel use cases")
    print(f"📊 Total companies with Parallel use case data: {len(df[df['Parallel Use Case'].notna() & (df['Parallel Use Case'] != 'Not found') & (df['Parallel Use Case'] != 'Error fetching data') & (df['Parallel Use Case'] != 'Not available')])}")
    
    # Regenerate HTML table
    print("\n🔄 Regenerating HTML table...")
    try:
        from generate_html_table import generate_html_table
        generate_html_table()
        print("✅ HTML table regenerated successfully!")
    except ImportError:
        print("⚠️ Could not import generate_html_table module. Please run it manually.")

if __name__ == "__main__":
    retry_failed_calls()


