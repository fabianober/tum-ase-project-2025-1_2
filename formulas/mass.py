import csv
import os

def total_mass(name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data', name, 'properties', 'element_masses.csv')
    total_mass = 0.0
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_mass += float(row['mass'])
    return total_mass * 1000  # Convert tonns to kg

if __name__ == "__main__":
    mass = total_mass('fabian')
    print(f"Total mass: {mass}")