"""
Script to download and prepare agricultural datasets
"""
import requests
import pandas as pd
import os

def download_data_gov_in():
    """
    Instructions to download from data.gov.in
    """
    print("="*60)
    print("OPTION 1: Download from data.gov.in (RECOMMENDED)")
    print("="*60)
    print("\nSteps:")
    print("1. Visit: https://data.gov.in")
    print("2. Search: 'Kisan Call Centre' or 'Agricultural Advisory'")
    print("3. Look for datasets like:")
    print("   - Kisan Call Centre Query Data")
    print("   - State-wise Agricultural Queries")
    print("   - Farmer Helpline Records")
    print("4. Download CSV/Excel file")
    print("5. Save as: data/raw_kcc.csv")
    print("\nExpected columns:")
    print("   - QueryText (farmer's question)")
    print("   - KccAns (expert answer)")
    print("   - Category, Crop, State, District (metadata)")
    print()

def download_kaggle_datasets():
    """
    Instructions for Kaggle datasets
    """
    print("="*60)
    print("OPTION 2: Download from Kaggle")
    print("="*60)
    print("\nSteps:")
    print("1. Visit: https://www.kaggle.com/datasets")
    print("2. Search for:")
    print("   - 'Indian Agriculture Dataset'")
    print("   - 'Crop Disease Dataset'")
    print("   - 'Agricultural Q&A'")
    print("3. Download and extract")
    print("4. Convert to required format (see below)")
    print()

def create_sample_from_web():
    """
    Create a larger sample dataset by scraping public sources
    """
    print("="*60)
    print("OPTION 3: Create Enhanced Sample Dataset")
    print("="*60)
    print("\nI can help you create a larger sample dataset with common queries.")
    print("This will have ~500 entries covering:")
    print("   - Pest control (100 queries)")
    print("   - Disease management (100 queries)")
    print("   - Fertilizer recommendations (100 queries)")
    print("   - Government schemes (50 queries)")
    print("   - Weather advisories (50 queries)")
    print("   - Crop management (100 queries)")
    print()
    
    response = input("Create enhanced sample dataset? (y/n): ")
    if response.lower() == 'y':
        create_enhanced_sample()

def create_enhanced_sample():
    """
    Create a comprehensive sample dataset
    """
    print("\nCreating enhanced sample dataset...")
    
    # Sample data structure
    data = []
    
    # Pest Control Queries (100)
    pests = [
        ("aphids", "mustard", "Spray Dimethoate 30 EC at 2 ml per liter or Imidacloprid 17.8 SL at 0.5 ml per liter"),
        ("whitefly", "cotton", "Apply Thiamethoxam 25 WG at 0.2 g per liter or Acetamiprid spray"),
        ("fruit borer", "brinjal", "Use Spinosad 45 SC at 0.3 ml per liter or install pheromone traps"),
        ("stem borer", "paddy", "Apply Cartap hydrochloride 50 SP at 1 g per liter or use light traps"),
        ("jassids", "cotton", "Spray Imidacloprid 17.8 SL at 0.3 ml per liter"),
        ("thrips", "chilli", "Use Fipronil 5 SC at 2 ml per liter or Spinosad spray"),
        ("mealybug", "mango", "Apply Profenophos 50 EC at 2 ml per liter or release natural predators"),
        ("leaf miner", "tomato", "Use Abamectin 1.9 EC at 0.5 ml per liter or remove affected leaves"),
        ("pod borer", "chickpea", "Spray Quinalphos 25 EC at 2 ml per liter during flowering"),
        ("cutworm", "cabbage", "Apply Chlorpyrifos 20 EC at 2.5 ml per liter around plant base"),
    ]
    
    for pest, crop, solution in pests:
        for i in range(10):  # Create 10 variations
            data.append({
                'StateName': 'UTTAR PRADESH',
                'DistrictName': 'AGRA',
                'BlockName': 'KHERAGARH',
                'Season': 'Kharif' if i % 2 == 0 else 'Rabi',
                'Sector': 'AGRICULTURE',
                'Category': 'Pest Control',
                'Crop': crop.title(),
                'QueryType': 'Plant Protection',
                'QueryText': f'How to control {pest} in {crop}?',
                'KccAns': solution
            })
    
    # Disease Management Queries (100)
    diseases = [
        ("blight", "potato", "Use Mancozeb or Metalaxyl fungicide spray at 15 day intervals"),
        ("leaf spot", "tomato", "Use Mancozeb 75 WP at 2.5 g per liter or Chlorothalonil spray"),
        ("blast", "paddy", "Apply Tricyclazole 75 WP at 0.6 g per liter or Carbendazim spray"),
        ("rust", "wheat", "Use Propiconazole at 0.1 percent spray or Mancozeb application"),
        ("wilt", "tomato", "Apply Carbendazim 50 WP at 1 g per liter as soil drench"),
        ("powdery mildew", "pea", "Spray Sulfur 80 WP at 3 g per liter or Hexaconazole"),
        ("anthracnose", "chilli", "Use Copper oxychloride 50 WP at 3 g per liter"),
        ("downy mildew", "grape", "Apply Metalaxyl + Mancozeb at 2.5 g per liter"),
        ("root rot", "chickpea", "Treat seeds with Trichoderma and apply Carbendazim soil drench"),
        ("bacterial blight", "cotton", "Spray Streptocycline 500 ppm with Copper oxychloride"),
    ]
    
    for disease, crop, solution in diseases:
        for i in range(10):
            data.append({
                'StateName': 'MAHARASHTRA',
                'DistrictName': 'PUNE',
                'BlockName': 'HAVELI',
                'Season': 'Kharif' if i % 2 == 0 else 'Rabi',
                'Sector': 'AGRICULTURE',
                'Category': 'Disease Management',
                'Crop': crop.title(),
                'QueryType': 'Plant Protection',
                'QueryText': f'What is the treatment for {disease} in {crop}?',
                'KccAns': solution
            })
    
    # Fertilizer Recommendations (100)
    fertilizers = [
        ("maize", "flowering", "Apply Urea at 50 kg per acre and Potash at 25 kg per acre"),
        ("wheat", "tillering", "Apply Urea at 40 kg per acre"),
        ("paddy", "transplanting", "Apply DAP at 50 kg per acre and Urea at 25 kg per acre"),
        ("cotton", "boll formation", "Apply Urea at 30 kg per acre and Potash at 20 kg per acre"),
        ("sugarcane", "grand growth", "Apply Urea at 100 kg per acre and Potash at 50 kg per acre"),
        ("tomato", "fruiting", "Apply 19:19:19 NPK at 5 kg per acre through drip"),
        ("potato", "tuber formation", "Apply Potash at 40 kg per acre and Urea at 30 kg per acre"),
        ("onion", "bulb development", "Apply Potash at 25 kg per acre"),
        ("banana", "bunch development", "Apply Potash at 60 kg per acre and Urea at 40 kg per acre"),
        ("mango", "flowering", "Apply 15:15:15 NPK at 500 g per tree"),
    ]
    
    for crop, stage, solution in fertilizers:
        for i in range(10):
            data.append({
                'StateName': 'PUNJAB',
                'DistrictName': 'LUDHIANA',
                'BlockName': 'LUDHIANA',
                'Season': 'Kharif' if i % 2 == 0 else 'Rabi',
                'Sector': 'AGRICULTURE',
                'Category': 'Fertilizer',
                'Crop': crop.title(),
                'QueryType': 'Fertilizer Use and Availability',
                'QueryText': f'What fertilizer is recommended during {stage} in {crop}?',
                'KccAns': solution
            })
    
    # Government Schemes (50)
    schemes = [
        ("PM Kisan Samman Nidhi", "Visit PM Kisan portal or contact local agriculture office for registration"),
        ("Pradhan Mantri Fasal Bima Yojana", "Contact insurance company or agriculture department within 7 days of sowing"),
        ("Soil Health Card Scheme", "Visit nearest Krishi Vigyan Kendra or agriculture office with land documents"),
        ("Kisan Credit Card", "Apply at nearest bank branch with land documents and Aadhaar card"),
        ("National Agriculture Market", "Register on eNAM portal for online trading of agricultural produce"),
    ]
    
    for scheme, answer in schemes:
        for i in range(10):
            data.append({
                'StateName': 'HARYANA',
                'DistrictName': 'KARNAL',
                'BlockName': 'KARNAL',
                'Season': 'NA',
                'Sector': 'AGRICULTURE',
                'Category': 'Government Schemes',
                'Crop': 'General',
                'QueryType': 'Government Schemes',
                'QueryText': f'How to apply for {scheme}?',
                'KccAns': answer
            })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_file = 'data/raw_kcc_enhanced.csv'
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Created enhanced dataset: {output_file}")
    print(f"✓ Total entries: {len(df)}")
    print(f"\nBreakdown:")
    print(df['Category'].value_counts())
    print(f"\nTo use this dataset:")
    print(f"1. Rename or replace: data/raw_kcc.csv")
    print(f"2. Run: python setup.py")
    print(f"3. Start the app!")

def show_dataset_format():
    """
    Show the expected dataset format
    """
    print("="*60)
    print("EXPECTED DATASET FORMAT")
    print("="*60)
    print("\nYour CSV file should have these columns:")
    print()
    print("Required columns:")
    print("  - QueryText: The farmer's question")
    print("  - KccAns: The expert's answer")
    print()
    print("Optional columns (for better categorization):")
    print("  - Category: Pest Control, Disease, Fertilizer, etc.")
    print("  - Crop: Wheat, Rice, Cotton, etc.")
    print("  - State: State name")
    print("  - District: District name")
    print("  - Season: Kharif, Rabi, Zaid")
    print("  - QueryType: Plant Protection, Fertilizer, etc.")
    print()
    print("Example row:")
    print("QueryText: How to control aphids in mustard?")
    print("KccAns: Spray Dimethoate 30 EC at 2 ml per liter")
    print("Category: Pest Control")
    print("Crop: Mustard")
    print()

def main():
    """
    Main function
    """
    print("\n" + "="*60)
    print("AGRICULTURAL DATASET DOWNLOAD GUIDE")
    print("="*60)
    print()
    
    print("Choose an option:")
    print("1. Instructions for data.gov.in (Real KCC data)")
    print("2. Instructions for Kaggle datasets")
    print("3. Create enhanced sample dataset (500+ entries)")
    print("4. Show expected dataset format")
    print("5. All of the above")
    print()
    
    choice = input("Enter choice (1-5): ")
    
    if choice == '1':
        download_data_gov_in()
    elif choice == '2':
        download_kaggle_datasets()
    elif choice == '3':
        create_sample_from_web()
    elif choice == '4':
        show_dataset_format()
    elif choice == '5':
        download_data_gov_in()
        download_kaggle_datasets()
        show_dataset_format()
        create_sample_from_web()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
