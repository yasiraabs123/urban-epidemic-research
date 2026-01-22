"""
Epidemic Simulation on Urban Networks
SEIR model implementation
Student: Yasir Abbas
Group: J4133
"""

import numpy as np
import pandas as pd
import pickle
import os
import time
from tqdm import tqdm

print("=" * 60)
print("EPIDEMIC SIMULATION - SEIR MODEL")
print("Student: Yasir Abbas, Group J4133")
print("=" * 60)

# Create directories
os.makedirs('data/simulation_results', exist_ok=True)

class SEIRSimulator:
    """Simple SEIR model simulator"""
    
    def __init__(self, network_size, avg_degree):
        self.N = network_size
        self.avg_degree = avg_degree
        
        # SEIR parameters (COVID-19 like)
        self.beta = 0.28  # transmission rate
        self.sigma = 1/5.2  # incubation rate
        self.gamma = 1/7.0  # recovery rate
        self.R0 = 2.5
        
        # Simulation parameters
        self.days = 120
        self.init_infected = max(1, int(network_size * 0.001))  # 0.1%
    
    def simulate(self, seed=None):
        """Run single simulation"""
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize compartments
        S = self.N - self.init_infected
        E = 0
        I = self.init_infected
        R = 0
        
        # Track results
        S_hist = [S]
        E_hist = [E]
        I_hist = [I]
        R_hist = [R]
        new_cases = [I]
        
        peak_infected = I
        peak_day = 0
        
        # Daily simulation
        for day in range(1, self.days):
            # Calculate new infections
            # Simplified: based on avg degree and current infected
            effective_contacts = self.avg_degree * I
            new_infections = np.random.binomial(S, 
                                              1 - np.exp(-self.beta * effective_contacts / self.N))
            
            # New exposures
            new_exposed = np.random.binomial(E, self.sigma)
            
            # New recoveries
            new_recoveries = np.random.binomial(I, self.gamma)
            
            # Update compartments
            S -= new_infections
            E += new_infections - new_exposed
            I += new_exposed - new_recoveries
            R += new_recoveries
            
            # Ensure non-negative
            S = max(0, S)
            E = max(0, E)
            I = max(0, I)
            R = max(0, R)
            
            # Track
            S_hist.append(S)
            E_hist.append(E)
            I_hist.append(I)
            R_hist.append(R)
            new_cases.append(new_infections)
            
            # Update peak
            if I > peak_infected:
                peak_infected = I
                peak_day = day
        
        # Calculate metrics
        attack_rate = (R / self.N) * 100
        peak_percentage = (peak_infected / self.N) * 100
        
        return {
            'S': S_hist, 'E': E_hist, 'I': I_hist, 'R': R_hist,
            'new_cases': new_cases,
            'peak_day': peak_day,
            'peak_infected': peak_infected,
            'peak_percentage': peak_percentage,
            'attack_rate': attack_rate,
            'final_S': S, 'final_R': R
        }

def run_simulations_for_city(city_name, network_size, avg_degree, num_simulations=30):
    """Run multiple simulations for a city type"""
    print(f"\nSimulating: {city_name}")
    
    simulator = SEIRSimulator(network_size, avg_degree)
    results = []
    
    # Run simulations
    for sim in tqdm(range(num_simulations), desc=f"{city_name} simulations"):
        result = simulator.simulate(seed=sim)
        results.append(result)
    
    # Calculate statistics
    peak_days = [r['peak_day'] for r in results]
    attack_rates = [r['attack_rate'] for r in results]
    peak_percentages = [r['peak_percentage'] for r in results]
    
    summary = {
        'city_name': city_name,
        'network_size': network_size,
        'avg_degree': avg_degree,
        'num_simulations': num_simulations,
        'peak_day_mean': np.mean(peak_days),
        'peak_day_std': np.std(peak_days),
        'attack_rate_mean': np.mean(attack_rates),
        'attack_rate_std': np.std(attack_rates),
        'peak_percentage_mean': np.mean(peak_percentages),
        'peak_percentage_std': np.std(peak_percentages),
        'all_results': results
    }
    
    return summary

def save_simulation_results(summary):
    """Save simulation results to file"""
    city = summary['city_name']
    
    # Save summary
    with open(f"data/simulation_results/{city}_summary.pkl", 'wb') as f:
        pickle.dump(summary, f)
    
    # Save CSV with main results
    data = []
    for i, result in enumerate(summary['all_results']):
        data.append({
            'simulation': i,
            'peak_day': result['peak_day'],
            'attack_rate': result['attack_rate'],
            'peak_percentage': result['peak_percentage']
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"data/simulation_results/{city}_results.csv", index=False)
    
    print(f"   ✓ Saved: {city}_summary.pkl")
    print(f"   ✓ Saved: {city}_results.csv")
    
    return df

if __name__ == "__main__":
    print("\nStarting epidemic simulations...")
    start_time = time.time()
    
    # City parameters (from network generation)
    cities = {
        'dense_city': {'size': 5000, 'avg_degree': 5.8},
        'sparse_city': {'size': 5000, 'avg_degree': 20.3},
        'polycentric_city': {'size': 5000, 'avg_degree': 10.1}
    }
    
    all_summaries = {}
    
    # Run simulations for each city
    for city_name, params in cities.items():
        print(f"\n{'='*40}")
        print(f"CITY: {city_name.upper()}")
        print(f"{'='*40}")
        
        summary = run_simulations_for_city(
            city_name=city_name,
            network_size=params['size'],
            avg_degree=params['avg_degree'],
            num_simulations=30  # 30 per city = 90 total
        )
        
        save_simulation_results(summary)
        all_summaries[city_name] = summary
        
        # Print quick results
        print(f"   • Peak Day: {summary['peak_day_mean']:.1f} ± {summary['peak_day_std']:.1f}")
        print(f"   • Attack Rate: {summary['attack_rate_mean']:.1f}% ± {summary['attack_rate_std']:.1f}%")
    
    # Print final summary
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"\n{'City Type':<15} {'Peak Day':<12} {'Attack Rate':<12} {'Simulations':<12}")
    print("-" * 60)
    
    total_simulations = 0
    for city_name, summary in all_summaries.items():
        print(f"{city_name:<15} "
              f"{summary['peak_day_mean']:.1f}±{summary['peak_day_std']:.1f}  "
              f"{summary['attack_rate_mean']:.1f}%±{summary['attack_rate_std']:.1f}%  "
              f"{summary['num_simulations']}")
        total_simulations += summary['num_simulations']
    
    elapsed = time.time() - start_time
    print(f"\nTotal simulations: {total_simulations}")
    print(f"Total time: {elapsed:.1f} seconds")
    print(f"Time per simulation: {elapsed/total_simulations:.2f} seconds")
    
    print("\n✅ Task 3 COMPLETED: All simulations finished!")
    print("Results saved in: data/simulation_results/")
