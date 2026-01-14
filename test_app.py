"""
Quick test script to verify the dashboard is working
"""
import os
import sys

print("=" * 60)
print("CSR Dashboard - Quick Test")
print("=" * 60)

# Check if files exist
print("\n1. Checking Excel files...")
csr_file = "CSR MIS.xlsx"
jspl_file = "JSPL CSR Data Input.xlsx"

if os.path.exists(csr_file):
    print(f"   ✅ Found: {csr_file}")
else:
    print(f"   ❌ Missing: {csr_file}")
    print(f"   Current directory: {os.getcwd()}")

if os.path.exists(jspl_file):
    print(f"   ✅ Found: {jspl_file}")
else:
    print(f"   ❌ Missing: {jspl_file}")

# Check Python packages
print("\n2. Checking Python packages...")
packages = ['streamlit', 'pandas', 'openpyxl', 'plotly', 'numpy']
missing = []

for pkg in packages:
    try:
        __import__(pkg)
        print(f"   ✅ {pkg}")
    except ImportError:
        print(f"   ❌ {pkg} - NOT INSTALLED")
        missing.append(pkg)

if missing:
    print(f"\n   Install missing packages: pip install {' '.join(missing)}")

# Test data loader
print("\n3. Testing data loader...")
try:
    from data_loader import DataLoader
    
    if os.path.exists(csr_file) and os.path.exists(jspl_file):
        loader = DataLoader(csr_file, jspl_file)
        keys = loader.get_all_keys()
        print(f"   ✅ Data loader works!")
        print(f"   ✅ Loaded {len(keys)} sheets")
        print(f"   Sample sheets: {keys[:3] if len(keys) > 3 else keys}")
    else:
        print("   ⚠️  Cannot test - Excel files missing")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
print("\nTo run the dashboard:")
print("  streamlit run app.py")
