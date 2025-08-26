# Import the Parallel SDK
from parallel import Parallel
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import pandas as pd
import time
import random
import signal
import threading

# Initialize client with API key
client = Parallel(api_key="fdtxy0y6gmOFPJ7476UmF5mW4OVrzSN7P34zV3Qr")

class CEOName(BaseModel):
    name: str = Field(description="Full name of the current CEO of the company.")

class CEOLinkedIn(BaseModel):
    url: str = Field(description="LinkedIn URL of the current CEO of the company.")

class CompanyInfo(BaseModel):
    description: str = Field(description="Company description summary including what they do, their products/services, and key business focus. Keep to maximum 5 sentences.")

class MarketInfo(BaseModel):
    overview: str = Field(description="Overview of company's market: sector, size, growth, competitors.")

class ParallelUseCase(BaseModel):
    overview: str = Field(description="How the specific company can use Parallel's APIs to improve their business. Include specific examples of how the company can use the APIs based on their product.")

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

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

def fetch_ceo_name(company):
    prompt = f"Who is the CEO of {company['name']} ({company['website']})?"
    res = client.task_run.execute(input=prompt, output=CEOName, processor="core")
    return res.output.parsed.name, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

def fetch_ceo_linkedin(company):
    prompt = f"Provide the LinkedIn URL of the CEO of {company['name']} ({company['website']})."
    res = client.task_run.execute(input=prompt, output=CEOLinkedIn, processor="core")
    return res.output.parsed.url, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

def fetch_company_description(company):
    prompt = f"Provide a concise company description of {company['name']} ({company['website']}). Include what they do, their products/services, and key business focus. Keep to maximum 5 sentences."
    res = client.task_run.execute(input=prompt, output=CompanyInfo, processor="core")
    return res.output.parsed.description, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

def fetch_market_research(company):
    prompt = f"Provide a market overview of {company['name']} ({company['website']}), including sector, size, growth, competitors."
    res = client.task_run.execute(input=prompt, output=MarketInfo, processor="core")
    return res.output.parsed.overview, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

def fetch_parallel_usecase(company):
    prompt = f"Suggest specific ways {company['name']} ({company['website']}) can use Parallel's APIs to improve their business, with concrete examples."
    res = client.task_run.execute(input=prompt, output=ParallelUseCase, processor="core")
    return res.output.parsed.overview, getattr(res.output, 'confidence', None), getattr(res.output, 'basis', None)

if __name__ == "__main__":
    print("✅ Parallel SDK imported successfully")
    print("✅ Pydantic models defined successfully")
    print("✅ Client initialized with API key")
    
    # Test creating a model instance
    company_info = CompanyInfo(description="Tech company focused on AI solutions")
    print(f"✅ CompanyInfo model test: {company_info.description}")

    startups = [
        {"name": "Greptile", "website": "https://www.greptile.com/"},
        {"name": "Qodo", "website": "https://www.qodo.ai/"},
        {"name": "Coworker", "website": "https://coworker.ai/"},
        {"name": "Bitloops", "website": "https://bitloops.com/"},
        {"name": "Cline", "website": "https://cline.bot/"},
        {"name": "CodeAnt", "website": "https://www.codeant.ai/"},
        {"name": "Augment", "website": "https://www.augmentcode.com/"},
        {"name": "Reflection AI", "website": "https://reflection.ai/"},
        {"name": "Scrunch AI", "website": "https://scrunchai.com/"},
        {"name": "BackOps AI", "website": "https://backops.ai/"},
    ]

    print(f"✅ Starting CEO sourcing for {len(startups)} companies...")
    print(f"⏰ Timeout set to 180 seconds per request")

    # Step 1: Fetch CEO names first
    print("\nStep 1: Fetching CEO names...")
    for i, c in enumerate(startups):
        start_time = time.time()
        print(f"  [{i+1}/{len(startups)}] Processing: {c['name']} ({c['website']})")
        name, conf, basis = safe_call(fetch_ceo_name, c, timeout=180, retries=1)
        elapsed = time.time() - start_time
        c["ceo"] = name or "Unknown"
        c["ceo_confidence"] = conf
        c["ceo_sources"] = basis
        print(f"  [{i+1}/{len(startups)}] Completed: {c['name']} - CEO: {c['ceo']} (took {elapsed:.1f}s)")

    # Step 2: Run LinkedIn + background + market + use case concurrently
    print("\nStep 2: Fetching additional information in parallel...")
    with ThreadPoolExecutor(max_workers=2) as executor:  # Reduced workers to avoid overwhelming the API
        future_to_company = {}
        for c in startups:
            future_to_company[executor.submit(safe_call, fetch_ceo_linkedin, c, timeout=180, retries=1)] = (c, "ceo_linkedin")
            future_to_company[executor.submit(safe_call, fetch_company_description, c, timeout=180, retries=1)] = (c, "company_info")
            future_to_company[executor.submit(safe_call, fetch_market_research, c, timeout=180, retries=1)] = (c, "market_info")
            future_to_company[executor.submit(safe_call, fetch_parallel_usecase, c, timeout=180, retries=1)] = (c, "parallel_usecase")

        completed = 0
        total_tasks = len(future_to_company)
        for future in as_completed(future_to_company):
            company, field = future_to_company[future]
            completed += 1
            try:
                result, conf, basis = future.result()
                company[field] = result if result else "Not found"
                company[f"{field}_confidence"] = conf
                company[f"{field}_sources"] = basis
                print(f"  [{completed}/{total_tasks}] ✅ {company['name']} - {field} completed")
            except Exception as e:
                print(f"  [{completed}/{total_tasks}] ❌ {company['name']} - {field} failed: {e}")
                company[field] = "Error fetching data"
                company[f"{field}_confidence"] = None
                company[f"{field}_sources"] = None

    # Create DataFrame
    print("\nStep 3: Creating results DataFrame...")
    df = pd.DataFrame([
        {
            "Company": c["name"],
            "Website": c["website"],
            "CEO": c.get("ceo", ""),
            "CEO Confidence": c.get("ceo_confidence", ""),
            "CEO Sources": c.get("ceo_sources", ""),
            "CEO LinkedIn": c.get("ceo_linkedin", ""),
            "LinkedIn Confidence": c.get("ceo_linkedin_confidence", ""),
            "LinkedIn Sources": c.get("ceo_linkedin_sources", ""),
            "Company Description": c.get("company_info", ""),
            "Description Confidence": c.get("company_info_confidence", ""),
            "Description Sources": c.get("company_info_sources", ""),
            "Market Research": c.get("market_info", ""),
            "Market Confidence": c.get("market_info_confidence", ""),
            "Market Sources": c.get("market_info_sources", ""),
            "Parallel Use Case": c.get("parallel_usecase", ""),
            "UseCase Confidence": c.get("parallel_usecase_confidence", ""),
            "UseCase Sources": c.get("parallel_usecase_sources", ""),
        }
        for c in startups
    ])

    print("✅ Results DataFrame created successfully!")
    print("\n📊 Results Summary:")
    print(df.head())
    
    # Save to CSV
    df.to_csv("ceo_sourcing_results.csv", index=False)
    print("✅ Results saved to ceo_sourcing_results.csv")
    
    # Display the full DataFrame
    print("\n📋 Full Results Table:")
    print(df)





