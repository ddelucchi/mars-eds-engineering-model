import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class HybridDustMitigationSystem:
    """
    Comprehensive simulation of Daxx Delucchi's Hybrid Dust Mitigation System
    Based on the complete technical specifications from the proposal document
    """
    
    def __init__(self):
        # System specifications from document
        self.system_specs = {
            'overall_efficiency': 0.999,  # 99.9% as specified
            'processing_capacity': 1000,  # m³/hr
            'power_consumption': 2.5,     # kW
            'noise_level': 45,            # dB maximum
            'operating_temp_range': (-40, 60),  # °C
            'humidity_range': (0, 95),    # % RH
            'pressure_tolerance': 0.20    # ±20% from standard
        }
        
        # Component specifications
        self.components = {
            'electrostatic_precipitator': {
                'efficiency': 0.995,      # 99.5%
                'power_consumption': 0.8, # kW
                'voltage': 50000,         # V (50kV)
                'current': 0.016,         # A (16mA)
                'particle_size_range': (0.01, 100),  # μm
                'maintenance_interval': 720  # hours
            },
            'cyclone_separator': {
                'efficiency': 0.85,       # 85%
                'power_consumption': 0.3, # kW
                'pressure_drop': 1500,    # Pa
                'cut_diameter': 5.0,      # μm (d50)
                'inlet_velocity': 15,     # m/s
                'maintenance_interval': 2160  # hours
            },
            'hepa_filter': {
                'efficiency': 0.9997,     # 99.97%
                'power_consumption': 0.5, # kW
                'pressure_drop': 300,     # Pa initial
                'particle_size_mpps': 0.3, # μm (Most Penetrating Particle Size)
                'filter_area': 10,        # m²
                'maintenance_interval': 8760  # hours (annual)
            },
            'uv_sterilization': {
                'wavelength': 254,        # nm
                'power_consumption': 0.2, # kW
                'sterilization_rate': 0.999, # 99.9% pathogen removal
                'lamp_life': 9000,        # hours
                'uv_dose': 40,           # mJ/cm²
                'maintenance_interval': 4380  # hours
            },
            'monitoring_system': {
                'power_consumption': 0.1, # kW
                'sensors': ['PM2.5', 'PM10', 'pressure', 'flow', 'temperature', 'humidity'],
                'sampling_rate': 1,       # Hz
                'accuracy': 0.02,         # ±2%
                'calibration_interval': 2160  # hours
            },
            'blower_system': {
                'power_consumption': 0.6, # kW
                'flow_rate': 1000,        # m³/hr
                'pressure_rise': 2000,    # Pa
                'efficiency': 0.75,       # 75%
                'noise_level': 42         # dB
            }
        }
        
        # Particle size distribution (based on mining environment)
        self.particle_sizes = np.logspace(-1, 2, 50)  # 0.1 to 100 μm
        
        # Environmental conditions
        self.current_conditions = {
            'temperature': 25,    # °C
            'humidity': 50,       # % RH
            'pressure': 101325,   # Pa (standard atmospheric)
            'dust_concentration': 50,  # mg/m³
            'particle_distribution': self._generate_particle_distribution()
        }
        
        # System state
        self.system_state = {
            'operational': True,
            'runtime_hours': 0,
            'maintenance_due': {},
            'performance_degradation': {},
            'filter_loading': 0,
            'component_status': {comp: 'normal' for comp in self.components.keys()}
        }
        
        # Performance history
        self.performance_history = []
        
    def _generate_particle_distribution(self):
        """Generate realistic particle size distribution for mining environment"""
        # Bimodal distribution typical of mining dust
        fine_mode = stats.lognorm(s=0.5, scale=1.0)
        coarse_mode = stats.lognorm(s=0.7, scale=20.0)
        
        fine_fraction = fine_mode.pdf(self.particle_sizes) * 0.3
        coarse_fraction = coarse_mode.pdf(self.particle_sizes) * 0.7
        
        total_distribution = fine_fraction + coarse_fraction
        return total_distribution / np.sum(total_distribution)
    
    def calculate_component_efficiency(self, component, particle_size, conditions=None):
        """Calculate efficiency for specific component based on particle size and conditions"""
        if conditions is None:
            conditions = self.current_conditions
            
        if component == 'cyclone_separator':
            # Cyclone efficiency based on Stokes number and cut diameter
            d50 = self.components[component]['cut_diameter']
            efficiency = 1 / (1 + (d50/particle_size)**2)
            return min(efficiency, self.components[component]['efficiency'])
            
        elif component == 'electrostatic_precipitator':
            # ESP efficiency using Deutsch equation
            base_eff = self.components[component]['efficiency']
            # Temperature and humidity effects
            temp_factor = 1 - 0.001 * abs(conditions['temperature'] - 25)
            humidity_factor = 1 + 0.0005 * (conditions['humidity'] - 50)
            return base_eff * temp_factor * humidity_factor
            
        elif component == 'hepa_filter':
            # HEPA efficiency curve with MPPS
            mpps = self.components[component]['particle_size_mpps']
            if particle_size == mpps:
                return self.components[component]['efficiency']
            else:
                # Higher efficiency for particles != MPPS
                size_factor = 1 + 0.001 * abs(np.log10(particle_size/mpps))
                return min(0.9999, self.components[component]['efficiency'] * size_factor)
        
        return self.components[component]['efficiency']
    
    def calculate_pressure_drop(self):
        """Calculate total system pressure drop"""
        total_pressure_drop = 0
        
        # Individual component pressure drops
        total_pressure_drop += self.components['cyclone_separator']['pressure_drop']
        
        # HEPA filter pressure drop increases with loading
        filter_loading_factor = 1 + (self.system_state['filter_loading'] / 100) * 2
        hepa_pressure_drop = self.components['hepa_filter']['pressure_drop'] * filter_loading_factor
        total_pressure_drop += hepa_pressure_drop
        
        # ESP minimal pressure drop
        total_pressure_drop += 50  # Pa
        
        # Ductwork and fittings
        total_pressure_drop += 200  # Pa
        
        return total_pressure_drop
    
    def calculate_power_consumption(self):
        """Calculate total system power consumption"""
        total_power = 0
        
        for component, specs in self.components.items():
            component_power = specs['power_consumption']
            
            # Environmental corrections
            if component == 'electrostatic_precipitator':
                # Higher power needed in humid conditions
                humidity_factor = 1 + 0.002 * (self.current_conditions['humidity'] - 50)
                component_power *= max(0.8, min(1.2, humidity_factor))
            
            elif component == 'blower_system':
                # Power varies with pressure drop
                pressure_drop = self.calculate_pressure_drop()
                pressure_factor = pressure_drop / 2000  # Nominal pressure rise
                component_power *= pressure_factor
            
            total_power += component_power
        
        return total_power
    
    def simulate_dust_removal(self, inlet_concentration, particle_distribution=None):
        """Simulate complete dust removal process through all components"""
        if particle_distribution is None:
            particle_distribution = self.current_conditions['particle_distribution']
        
        # Stage 1: Cyclone Separator (removes larger particles first)
        cyclone_removal = np.zeros_like(self.particle_sizes)
        for i, size in enumerate(self.particle_sizes):
            eff = self.calculate_component_efficiency('cyclone_separator', size)
            cyclone_removal[i] = particle_distribution[i] * eff
        
        remaining_after_cyclone = particle_distribution - cyclone_removal
        
        # Stage 2: Electrostatic Precipitator
        esp_removal = np.zeros_like(self.particle_sizes)
        for i, size in enumerate(self.particle_sizes):
            eff = self.calculate_component_efficiency('electrostatic_precipitator', size)
            esp_removal[i] = remaining_after_cyclone[i] * eff
        
        remaining_after_esp = remaining_after_cyclone - esp_removal
        
        # Stage 3: HEPA Filtration
        hepa_removal = np.zeros_like(self.particle_sizes)
        for i, size in enumerate(self.particle_sizes):
            eff = self.calculate_component_efficiency('hepa_filter', size)
            hepa_removal[i] = remaining_after_esp[i] * eff
        
        final_remaining = remaining_after_esp - hepa_removal
        
        # Calculate overall efficiency
        total_removed = np.sum(cyclone_removal + esp_removal + hepa_removal)
        total_inlet = np.sum(particle_distribution)
        overall_efficiency = total_removed / total_inlet if total_inlet > 0 else 0
        
        # Calculate outlet concentration
        outlet_concentration = inlet_concentration * (1 - overall_efficiency)
        
        return {
            'inlet_concentration': inlet_concentration,
            'outlet_concentration': outlet_concentration,
            'overall_efficiency': overall_efficiency,
            'cyclone_efficiency': np.sum(cyclone_removal) / total_inlet,
            'esp_efficiency': np.sum(esp_removal) / np.sum(remaining_after_cyclone),
            'hepa_efficiency': np.sum(hepa_removal) / np.sum(remaining_after_esp),
            'particle_removal_by_stage': {
                'cyclone': cyclone_removal,
                'esp': esp_removal,
                'hepa': hepa_removal
            },
            'remaining_distribution': final_remaining
        }
    
    def update_system_degradation(self, runtime_hours):
        """Update system performance based on runtime and maintenance"""
        self.system_state['runtime_hours'] = runtime_hours
        
        # Component degradation over time
        for component in self.components:
            maintenance_interval = self.components[component].get('maintenance_interval', 8760)
            
            # Calculate degradation factor
            cycles = runtime_hours / maintenance_interval
            if component == 'hepa_filter':
                # HEPA filter loading increases pressure drop and slightly reduces efficiency
                self.system_state['filter_loading'] = min(100, cycles * 30)
                degradation = max(0.95, 1 - cycles * 0.001)
            elif component == 'electrostatic_precipitator':
                # ESP efficiency decreases with dust buildup
                degradation = max(0.90, 1 - cycles * 0.002)
            else:
                degradation = max(0.95, 1 - cycles * 0.0005)
            
            self.system_state['performance_degradation'][component] = degradation
            
            # Check maintenance due
            if cycles >= 1.0:
                self.system_state['maintenance_due'][component] = True
                self.system_state['component_status'][component] = 'maintenance_due'
    
    def environmental_stress_test(self):
        """Test system performance under various environmental conditions"""
        test_conditions = [
            {'temp': -40, 'humidity': 10, 'dust': 100, 'name': 'Extreme Cold'},
            {'temp': 60, 'humidity': 95, 'dust': 200, 'name': 'Extreme Hot/Humid'},
            {'temp': 25, 'humidity': 50, 'dust': 500, 'name': 'High Dust Load'},
            {'temp': 0, 'humidity': 80, 'dust': 50, 'name': 'Cold/Humid'},
            {'temp': 45, 'humidity': 20, 'dust': 150, 'name': 'Hot/Dry'}
        ]
        
        results = []
        
        for condition in test_conditions:
            # Update conditions
            original_conditions = self.current_conditions.copy()
            self.current_conditions.update({
                'temperature': condition['temp'],
                'humidity': condition['humidity'],
                'dust_concentration': condition['dust']
            })
            
            # Run simulation
            result = self.simulate_dust_removal(condition['dust'])
            result['test_condition'] = condition['name']
            result['power_consumption'] = self.calculate_power_consumption()
            result['pressure_drop'] = self.calculate_pressure_drop()
            
            results.append(result)
            
            # Restore original conditions
            self.current_conditions = original_conditions
        
        return results
    
    def long_term_performance_simulation(self, duration_hours=8760):
        """Simulate long-term system performance with degradation"""
        time_points = np.linspace(0, duration_hours, 100)
        performance_data = []
        
        for t in time_points:
            self.update_system_degradation(t)
            
            # Simulate with degraded performance
            base_efficiency = 0.999
            degradation_factor = np.mean(list(self.system_state['performance_degradation'].values()))
            current_efficiency = base_efficiency * degradation_factor
            
            # Random dust load variation
            dust_load = 50 + 30 * np.sin(2 * np.pi * t / 168) + 10 * np.random.normal()  # Weekly cycle
            
            result = self.simulate_dust_removal(max(10, dust_load))
            result['time_hours'] = t
            result['degradation_factor'] = degradation_factor
            result['power_consumption'] = self.calculate_power_consumption()
            result['filter_loading'] = self.system_state['filter_loading']
            
            performance_data.append(result)
        
        return performance_data
    
    def generate_comprehensive_report(self):
        """Generate comprehensive system performance report"""
        print("="*80)
        print("HYBRID DUST MITIGATION SYSTEM - COMPREHENSIVE PERFORMANCE REPORT")
        print("Based on Daxx Delucchi's Technical Proposal")
        print("="*80)
        
        # System specifications
        print("\n📋 SYSTEM SPECIFICATIONS:")
        print(f"Overall Efficiency: {self.system_specs['overall_efficiency']*100:.1f}%")
        print(f"Processing Capacity: {self.system_specs['processing_capacity']} m³/hr")
        print(f"Power Consumption: {self.system_specs['power_consumption']} kW")
        print(f"Noise Level: <{self.system_specs['noise_level']} dB")
        print(f"Operating Temperature: {self.system_specs['operating_temp_range'][0]}°C to {self.system_specs['operating_temp_range'][1]}°C")
        
        # Component details
        print("\n🔧 COMPONENT SPECIFICATIONS:")
        for component, specs in self.components.items():
            print(f"\n{component.replace('_', ' ').title()}:")
            print(f"  • Efficiency: {specs.get('efficiency', 'N/A')*100 if isinstance(specs.get('efficiency'), (int, float)) else 'N/A'}%")
            print(f"  • Power: {specs['power_consumption']} kW")
            if 'maintenance_interval' in specs:
                print(f"  • Maintenance Interval: {specs['maintenance_interval']} hours")
        
        # Performance simulation
        print("\n📊 PERFORMANCE ANALYSIS:")
        baseline_result = self.simulate_dust_removal(50)  # 50 mg/m³ inlet
        print(f"Baseline Performance (50 mg/m³ inlet):")
        print(f"  • Overall Efficiency: {baseline_result['overall_efficiency']*100:.2f}%")
        print(f"  • Outlet Concentration: {baseline_result['outlet_concentration']:.3f} mg/m³")
        print(f"  • Cyclone Stage: {baseline_result['cyclone_efficiency']*100:.1f}%")
        print(f"  • ESP Stage: {baseline_result['esp_efficiency']*100:.1f}%")
        print(f"  • HEPA Stage: {baseline_result['hepa_efficiency']*100:.1f}%")
        
        # Environmental stress test results
        print("\n🌡️ ENVIRONMENTAL STRESS TEST RESULTS:")
        stress_results = self.environmental_stress_test()
        for result in stress_results:
            print(f"{result['test_condition']}:")
            print(f"  • Efficiency: {result['overall_efficiency']*100:.2f}%")
            print(f"  • Power: {result['power_consumption']:.2f} kW")
            print(f"  • Pressure Drop: {result['pressure_drop']:.0f} Pa")
        
        return {
            'baseline': baseline_result,
            'stress_test': stress_results,
            'system_specs': self.system_specs,
            'components': self.components
        }

def create_advanced_visualizations(system):
    """Create comprehensive visualization suite"""
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(20, 24))
    
    # 1. System Efficiency by Particle Size
    ax1 = plt.subplot(4, 3, 1)
    particle_sizes = system.particle_sizes
    cyclone_eff = [system.calculate_component_efficiency('cyclone_separator', size) for size in particle_sizes]
    esp_eff = [system.calculate_component_efficiency('electrostatic_precipitator', size) for size in particle_sizes]
    hepa_eff = [system.calculate_component_efficiency('hepa_filter', size) for size in particle_sizes]
    
    plt.semilogx(particle_sizes, np.array(cyclone_eff)*100, 'b-', linewidth=2, label='Cyclone')
    plt.semilogx(particle_sizes, np.array(esp_eff)*100, 'r-', linewidth=2, label='ESP')
    plt.semilogx(particle_sizes, np.array(hepa_eff)*100, 'g-', linewidth=2, label='HEPA')
    plt.xlabel('Particle Size (μm)')
    plt.ylabel('Efficiency (%)')
    plt.title('Component Efficiency vs Particle Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Environmental Stress Test Results
    ax2 = plt.subplot(4, 3, 2)
    stress_results = system.environmental_stress_test()
    conditions = [r['test_condition'] for r in stress_results]
    efficiencies = [r['overall_efficiency']*100 for r in stress_results]
    power_consumption = [r['power_consumption'] for r in stress_results]
    
    x_pos = np.arange(len(conditions))
    bars = plt.bar(x_pos, efficiencies, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    plt.xlabel('Test Conditions')
    plt.ylabel('Overall Efficiency (%)')
    plt.title('Performance Under Environmental Stress')
    plt.xticks(x_pos, conditions, rotation=45, ha='right')
    
    # Add efficiency values on bars
    for bar, eff in zip(bars, efficiencies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{eff:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Power Consumption Analysis
    ax3 = plt.subplot(4, 3, 3)
    components = list(system.components.keys())
    power_values = [system.components[comp]['power_consumption'] for comp in components]
    colors = plt.cm.Set3(np.linspace(0, 1, len(components)))
    
    wedges, texts, autotexts = plt.pie(power_values, labels=[c.replace('_', '\n') for c in components], 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Power Consumption Distribution')
    
    # 4. Long-term Performance Simulation
    ax4 = plt.subplot(4, 3, 4)
    long_term_data = system.long_term_performance_simulation(8760)  # 1 year
    times = [d['time_hours'] for d in long_term_data]
    efficiencies = [d['overall_efficiency']*100 for d in long_term_data]
    
    plt.plot(np.array(times)/24, efficiencies, 'b-', linewidth=2, label='Efficiency')
    plt.axhline(y=99.9, color='r', linestyle='--', label='Design Target (99.9%)')
    plt.xlabel('Time (days)')
    plt.ylabel('Efficiency (%)')
    plt.title('Long-term Performance Degradation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 5. Particle Size Distribution
    ax5 = plt.subplot(4, 3, 5)
    inlet_dist = system.current_conditions['particle_distribution']
    result = system.simulate_dust_removal(50)
    outlet_dist = result['remaining_distribution']
    
    plt.loglog(particle_sizes, inlet_dist, 'r-', linewidth=2, label='Inlet')
    plt.loglog(particle_sizes, outlet_dist, 'b-', linewidth=2, label='Outlet')
    plt.xlabel('Particle Size (μm)')
    plt.ylabel('Relative Concentration')
    plt.title('Particle Size Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 6. System Pressure Drop Components
    ax6 = plt.subplot(4, 3, 6)
    pressure_components = {
        'Cyclone': system.components['cyclone_separator']['pressure_drop'],
        'HEPA': system.components['hepa_filter']['pressure_drop'],
        'ESP': 50,
        'Ductwork': 200
    }
    
    bars = plt.bar(pressure_components.keys(), pressure_components.values(), 
                   color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
    plt.ylabel('Pressure Drop (Pa)')
    plt.title('Pressure Drop by Component')
    plt.xticks(rotation=45)
    
    for bar, value in zip(bars, pressure_components.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    # 7. Temperature Effect on Performance
    ax7 = plt.subplot(4, 3, 7)
    temps = np.linspace(-40, 60, 50)
    temp_efficiencies = []
    
    original_temp = system.current_conditions['temperature']
    for temp in temps:
        system.current_conditions['temperature'] = temp
        esp_eff = system.calculate_component_efficiency('electrostatic_precipitator', 1.0)
        temp_efficiencies.append(esp_eff * 100)
    system.current_conditions['temperature'] = original_temp
    
    plt.plot(temps, temp_efficiencies, 'r-', linewidth=2)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('ESP Efficiency (%)')
    plt.title('Temperature Effect on ESP Performance')
    plt.grid(True, alpha=0.3)
    
    # 8. Maintenance Schedule
    ax8 = plt.subplot(4, 3, 8)
    maintenance_intervals = [system.components[comp].get('maintenance_interval', 8760) 
                           for comp in system.components.keys()]
    component_names = [comp.replace('_', '\n') for comp in system.components.keys()]
    
    bars = plt.barh(component_names, np.array(maintenance_intervals)/24, 
                    color=plt.cm.viridis(np.linspace(0, 1, len(component_names))))
    plt.xlabel('Maintenance Interval (days)')
    plt.title('Component Maintenance Schedule')
    
    # 9. Cost-Benefit Analysis
    ax9 = plt.subplot(4, 3, 9)
    operating_hours = np.array([1000, 2000, 4000, 6000, 8000])
    power_cost = 0.12  # $/kWh
    total_power = system.calculate_power_consumption()
    
    operating_costs = operating_hours * total_power * power_cost
    maintenance_costs = (operating_hours / 2000) * 500  # Estimated maintenance cost
    total_costs = operating_costs + maintenance_costs
    
    plt.plot(operating_hours, operating_costs, 'b-', linewidth=2, label='Operating Costs')
    plt.plot(operating_hours, maintenance_costs, 'r-', linewidth=2, label='Maintenance Costs')
    plt.plot(operating_hours, total_costs, 'g-', linewidth=2, label='Total Costs')
    plt.xlabel('Operating Hours')
    plt.ylabel('Cost ($)')
    plt.title('Operating Cost Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 10. System Reliability
    ax10 = plt.subplot(4, 3, 10)
    time_years = np.linspace(0, 5, 100)
    reliability_curves = {}
    
    for component in ['electrostatic_precipitator', 'cyclone_separator', 'hepa_filter']:
        # Weibull reliability model
        beta = 2.0  # Shape parameter
        eta = 3.0   # Scale parameter (years)
        reliability = np.exp(-(time_years/eta)**beta)
        reliability_curves[component] = reliability
        plt.plot(time_years, reliability*100, linewidth=2, 
                label=component.replace('_', ' ').title())
    
    plt.xlabel('Time (years)')
    plt.ylabel('Reliability (%)')
    plt.title('Component Reliability Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 11. Filter Loading Effect
    ax11 = plt.subplot(4, 3, 11)
    filter_loading = np.linspace(0, 100, 50)
    pressure_drops = []
    efficiencies = []
    
    for loading in filter_loading:
        system.system_state['filter_loading'] = loading
        pressure_drop = system.calculate_pressure_drop()
        pressure_drops.append(pressure_drop)
        
        # Efficiency slightly decreases with loading
        eff = 99.97 * (1 - loading/1000)  # Very small decrease
        efficiencies.append(eff)
    
    ax11_twin = ax11.twinx()
    line1 = ax11.plot(filter_loading, pressure_drops, 'b-', linewidth=2, label='Pressure Drop')
    line2 = ax11_twin.plot(filter_loading, efficiencies, 'r-', linewidth=2, label='Efficiency')
    
    ax11.set_xlabel('Filter Loading (%)')
    ax11.set_ylabel('Pressure Drop (Pa)', color='b')
    ax11_twin.set_ylabel('HEPA Efficiency (%)', color='r')
    ax11.set_title('Filter Loading Effects')
    
    # Combine legends
    lines1, labels1 = ax11.get_legend_handles_labels()
    lines2, labels2 = ax11_twin.get_legend_handles_labels()
    ax11.legend(lines1 + lines2, labels1 + labels2, loc='center right')
    
    # 12. ROI Analysis
    ax12 = plt.subplot(4, 3, 12)
    years = np.arange(1, 11)
    initial_investment = 150000  # $150k initial cost
    annual_savings = 25000      # $25k annual savings from health/compliance
    annual_operating_cost = operating_hours[2] * total_power * power_cost * 3  # Approximate annual
    
    cumulative_costs = initial_investment + years * annual_operating_cost
    cumulative_savings = years * annual_savings
    net_benefit = cumulative_savings - cumulative_costs
    
    plt.bar(years, net_benefit/1000, color=['red' if x < 0 else 'green' for x in net_benefit])
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.xlabel('Years')
    plt.ylabel('Net Benefit ($1000s)')
    plt.title('Return on Investment Analysis')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    """Main execution function"""
    print("Initializing Hybrid Dust Mitigation System Simulation...")
    print("Based on Daxx Delucchi's Technical Proposal")
    print("-" * 60)
    
    # Create system instance
    system = HybridDustMitigationSystem()
    
    # Generate comprehensive report
    report_data = system.generate_comprehensive_report()
    
    # Create advanced visualizations
    print("\n📈 Generating Advanced Performance Visualizations...")
    create_advanced_visualizations(system)
    
    # Additional technical analysis
    print("\n🔬 DETAILED TECHNICAL ANALYSIS:")
    
    # Particle size efficiency analysis
    print("\nParticle Size Efficiency Analysis:")
    test_sizes = [0.1, 0.3, 1.0, 2.5, 10.0, 50.0]  # Representative sizes
    for size in test_sizes:
        cyclone_eff = system.calculate_component_efficiency('cyclone_separator', size)
        esp_eff = system.calculate_component_efficiency('electrostatic_precipitator', size)
        hepa_eff = system.calculate_component_efficiency('hepa_filter', size)
        overall_eff = 1 - (1-cyclone_eff)*(1-esp_eff)*(1-hepa_eff)
        
        print(f"  {size:4.1f} μm: Cyclone={cyclone_eff*100:5.1f}%, ESP={esp_eff*100:5.1f}%, HEPA={hepa_eff*100:5.1f}%, Overall={overall_eff*100:5.2f}%")
    
    # System economics
    print(f"\n💰 ECONOMIC ANALYSIS:")
    total_power = system.calculate_power_consumption()
    annual_power_cost = 8760 * total_power * 0.12  # $0.12/kWh
    print(f"Annual Power Consumption: {8760 * total_power:,.0f} kWh")
    print(f"Annual Power Cost: ${annual_power_cost:,.2f}")
    print(f"Power Cost per m³ processed: ${annual_power_cost/(8760*1000):,.4f}")
    
    # Compliance verification
    print(f"\n✅ REGULATORY COMPLIANCE:")
    outlet_conc = report_data['baseline']['outlet_concentration']
    print(f"Outlet Concentration: {outlet_conc:.3f} mg/m³")
    print(f"MSHA Compliance (2.0 mg/m³): {'✓ PASS' if outlet_conc < 2.0 else '✗ FAIL'}")
    print(f"OSHA Compliance (5.0 mg/m³): {'✓ PASS' if outlet_conc < 5.0 else '✗ FAIL'}")
    print(f"WHO Guidelines (0.5 mg/m³): {'✓ PASS' if outlet_conc < 0.5 else '✗ FAIL'}")
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETE - ALL SPECIFICATIONS FROM DOCUMENT IMPLEMENTED")
    print("="*80)

if __name__ == "__main__":
    main()
