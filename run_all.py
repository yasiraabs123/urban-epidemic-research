"""
Master script to run complete analysis
Student: Yasir Abbas 
Group: J4133
"""

import subprocess
import sys
import time
import os

def run_script(script_name, description):
    """Run a Python script"""
    print(f"\n{'='*60}")
    print(f"STARTING: {description}")
    print(f"{'='*60}")
    
    start = time.time()
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            # Print last few lines of output
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:  # Last 5 lines
                    if line.strip():
                        print(f"   {line}")
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    elapsed = time.time() - start
    print(f"⏱️  Time: {elapsed:.1f} seconds")
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    
    required = ['networkx', 'numpy', 'matplotlib', 'pandas', 'scipy', 'seaborn', 'tqdm']
    
    for package in required:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} is missing")
            print(f"   Install with: pip install {package}")
            return False
    
    return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("URBAN NETWORK EPIDEMICS - COMPLETE ANALYSIS")
    print("Student: Yasir Abbas, Group J4133")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first.")
        return
    
    # Create directories
    os.makedirs('data/networks', exist_ok=True)
    os.makedirs('data/simulation_results', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    
    print("\n🚀 Starting analysis pipeline...")
    
    # Step 1: Network Generation
    if not run_script("network_generation.py", "Task 2: Network Generation"):
        print("\nStopping due to error in network generation.")
        return
    
    # Step 2: Epidemic Simulation
    if not run_script("epidemic_simulation.py", "Task 3: Epidemic Simulation"):
        print("\nStopping due to error in simulation.")
        return
    
    # Step 3: Analysis and Visualization
    if not run_script("analysis_plots.py", "Tasks 4-5: Analysis & Visualization"):
        print("\nStopping due to error in analysis.")
        return
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📊 RESEARCH SUMMARY:")
    print("• Generated 3 synthetic city networks")
    print("• Ran 90 epidemic simulations (30 per city)")
    print("• Performed statistical analysis (ANOVA, correlation)")
    print("• Created 3 publication-quality figures")
    print("• All results are reproducible")
    
    print("\n📁 OUTPUT FILES:")
    print("data/networks/")
    print("  ├── dense_city.pkl")
    print("  ├── sparse_city.pkl")
    print("  └── polycentric_city.pkl")
    print("")
    print("data/simulation_results/")
    print("  ├── *_summary.pkl (summary files)")
    print("  ├── *_results.csv (detailed results)")
    print("  └── statistics.pkl (statistical tests)")
    print("")
    print("figures/")
    print("  ├── network_structures.png")
    print("  ├── outbreak_curves.png")
    print("  ├── intervention_analysis.png")
    print("  └── summary_table.csv")
    
    print("\n✅ All research objectives completed!")
    print("Ready for presentation and defense.")

if __name__ == "__main__":
    main()
