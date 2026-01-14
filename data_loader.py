"""
Data Loader Module for CSR Dashboard
Loads and processes data from Excel files
"""
import pandas as pd
import os
from typing import Dict, List, Optional

class DataLoader:
    def __init__(self, csr_mis_path: str, jspl_input_path: str):
        self.csr_mis_path = csr_mis_path
        self.jspl_input_path = jspl_input_path
        self.data: Dict[str, pd.DataFrame] = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all sheets from both Excel files"""
        try:
            # Load CSR MIS.xlsx
            if not os.path.exists(self.csr_mis_path):
                raise FileNotFoundError(f"CSR MIS file not found: {self.csr_mis_path}")
            
            csr_mis = pd.ExcelFile(self.csr_mis_path)
            for sheet_name in csr_mis.sheet_names:
                try:
                    df = pd.read_excel(self.csr_mis_path, sheet_name=sheet_name)
                    # Skip empty sheets
                    if df.empty:
                        continue
                    # Clean column names
                    df.columns = df.columns.str.strip()
                    self.data[f"CSR_MIS_{sheet_name}"] = df
                except Exception as e:
                    print(f"Warning: Error loading sheet '{sheet_name}' from CSR MIS: {e}")
            
            # Load JSPL CSR Data Input.xlsx
            if not os.path.exists(self.jspl_input_path):
                raise FileNotFoundError(f"JSPL Input file not found: {self.jspl_input_path}")
            
            jspl_input = pd.ExcelFile(self.jspl_input_path)
            for sheet_name in jspl_input.sheet_names:
                try:
                    df = pd.read_excel(self.jspl_input_path, sheet_name=sheet_name)
                    # Skip empty sheets
                    if df.empty:
                        continue
                    # Clean column names
                    df.columns = df.columns.str.strip()
                    self.data[f"JSPL_{sheet_name}"] = df
                except Exception as e:
                    print(f"Warning: Error loading sheet '{sheet_name}' from JSPL Input: {e}")
        
        except Exception as e:
            raise Exception(f"Error loading Excel files: {e}")
    
    def get_data(self, key: str) -> Optional[pd.DataFrame]:
        """Get data by key"""
        return self.data.get(key)
    
    def get_all_keys(self) -> List[str]:
        """Get all data keys"""
        return list(self.data.keys())
    
    def get_program_data(self, program_name: str) -> Optional[pd.DataFrame]:
        """Get data for a specific program"""
        # Try different naming conventions
        possible_keys = [
            f"CSR_MIS_{program_name}",
            f"JSPL_{program_name}",
            f"CSR_MIS_{program_name.replace('_', ' ')}",
            f"JSPL_{program_name.replace('_', ' ')}",
        ]
        
        for key in possible_keys:
            if key in self.data:
                return self.data[key]
        
        # Try partial match
        for key in self.data.keys():
            if program_name.lower() in key.lower():
                return self.data[key]
        
        return None
    
    def get_master_data(self) -> Dict[str, pd.DataFrame]:
        """Get all master data sheets"""
        masters = {}
        for key, df in self.data.items():
            if 'Master' in key or 'master' in key:
                masters[key] = df
        return masters
