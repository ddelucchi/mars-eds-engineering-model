import numpy as np
import pandas as pd
import scipy.integrate as integrate
import scipy.constants as const
import scipy.optimize as optimize
import scipy.interpolate as interp
import scipy.ndimage as ndimage
import scipy.signal as signal
import matplotlib.pyplot as plt
import sympy as sp
import mpmath as mp

# Platform-specific imports with fallbacks
try:
    from astropy import units as u
    from astropy import constants as ast_const
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False

try:
    import qutip as qt
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False

import networkx as nx

try:
    import chess
    CHESS_AVAILABLE = True
except ImportError:
    CHESS_AVAILABLE = False

try:
    from Bio import SeqIO
    from Bio.Seq import Seq
    BIO_AVAILABLE = True
except ImportError:
    BIO_AVAILABLE = False

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

try:
    from pyscf import gto, scf, dft, mcscf, lo, tdscf, solvent
    PYSCF_AVAILABLE = True
except ImportError:
    PYSCF_AVAILABLE = False

try:
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

try:
    import pulp
    PULP_AVAILABLE = True
except ImportError:
    PULP_AVAILABLE = False

try:
    import snappy
    SNAPPY_AVAILABLE = True
except ImportError:
    SNAPPY_AVAILABLE = False

try:
    from mido import MidiFile, MidiTrack, Message
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False

try:
    import control
    CONTROL_AVAILABLE = True
except ImportError:
    CONTROL_AVAILABLE = False

try:
    from dendropy import Tree
    DENDROPY_AVAILABLE = True
except ImportError:
    DENDROPY_AVAILABLE = False

try:
    import pubchempy as pcp
    PUBCHEM_AVAILABLE = True
except ImportError:
    PUBCHEM_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from torch_geometric.data import Data
    from torch_geometric.nn import GCNConv
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    TORCH_GEOMETRIC_AVAILABLE = False
# Core Python imports
import os
import sys
import time
import random
import math
import cmath
import concurrent.futures
from multiprocessing import Pool, cpu_count, freeze_support
import functools
import itertools
import collections
import bisect
import heapq
import queue
import threading
import asyncio
import logging
import warnings
import traceback
import gc
import psutil
import h5py
import json
import xml.etree.ElementTree as ET
import csv
import pickle
import bz2
import lzma
import zlib
import tarfile
import zipfile
import shutil
import subprocess
import re
import glob
import fnmatch
import pathlib
import datetime
import calendar
import zoneinfo
import email
import http.client
import urllib.request
import socket
import ssl
import hashlib
import base64
import secrets
from cryptography.fernet import Fernet
import getpass
import array
import struct
import signal
import atexit
import errno
import ctypes
import ctypes.util
import tempfile
import uuid
import mimetypes
import configparser
import argparse
import logging.handlers

# Platform-specific imports for Windows compatibility
try:
    import pwd
    import grp
    import syslog
    import termios
    import select
    import fcntl
    import pty
    import tty
    import resource
    UNIX_AVAILABLE = True
except ImportError:
    UNIX_AVAILABLE = False

# Asyncio submodule imports
import asyncio.base_events
import asyncio.coroutines
import asyncio.events
import asyncio.exceptions
import asyncio.format_helpers
import asyncio.futures
import asyncio.locks
import asyncio.log
import asyncio.mixins
import asyncio.protocols
import asyncio.queues
import asyncio.runners
import asyncio.selector_events
import asyncio.streams
import asyncio.subprocess
import asyncio.tasks
import asyncio.threads
import asyncio.transports

# Windows-specific asyncio imports only on Windows
if sys.platform == "win32":
    import asyncio.proactor_events
    import asyncio.windows_events
    import asyncio.windows_utils
else:
    import asyncio.unix_events


# Updated constants from 2025 data with proper mpmath usage
MARS_GRAVITY = mp.mpf('3.72076')
MARS_ATM_PRESSURE = mp.mpf('636')  # Average from recent measurements
MARS_TEMP = mp.mpf('210')  # Global average
MARS_ATM_DENSITY = mp.mpf('0.016')  # CO2 dominated
CO2_DIELECTRIC = mp.mpf('1.00092')  # More accurate for CO2 gas
DUST_DENSITY = mp.mpf('2900')  # Basaltic with iron oxides
DUST_PARTICLE_RADIUS_MEAN = mp.mpf('1.6e-6')  # From recent simulant studies ~1.6 um
DUST_PARTICLE_RADIUS_STD = mp.mpf('0.8e-6')
DUST_HAMAKER_CONSTANT = mp.mpf('6.5e-20')  # Updated from QM calculations for silicates/oxides
DUST_DIELECTRIC_CONSTANT = mp.mpf('5.5')  # For Martian dust
DUST_CHARGE_MEAN_SMALL = mp.mpf('-1e-15')  # Bipolar: small negative
DUST_CHARGE_MEAN_LARGE = mp.mpf('1e-15')  # Large positive
DUST_CHARGE_STD = mp.mpf('5e-16')
PERCHLORATE_CONC = mp.mpf('0.005')  # 0.5% by mass
BRINE_SURFACE_TENSION = mp.mpf('0.08')  # Higher due to salts
CONTACT_ANGLE = mp.mpf('20')  # Degrees for brine on silicates
HUMIDITY_MARS = mp.mpf('0.0003')  # Very low, but perchlorates deliquesce
WIND_SPEED_MEAN = mp.mpf('7')  # m/s
WIND_SPEED_STD = mp.mpf('3')
DUST_FLUX = mp.mpf('1e-9')  # kg/m²/s during storms
DEPOSITION_RATE = mp.mpf('0.002')  # Fraction per sol

# HDMS updated
EDS_ELECTRODE_SPACING = mp.mpf('5e-4')  # 0.5 mm from recent NASA tests
EDS_VOLTAGE_AMPLITUDE = mp.mpf('1200')  # Higher for Mars
EDS_FREQUENCY = mp.mpf('50')  # Optimized
EDS_PHASE_COUNT = 4  # Quad-phase for better wave
DIELECTRIC_THICKNESS = mp.mpf('5e-5')  # 50 um
DIELECTRIC_CONSTANT = mp.mpf('4.2')  # Updated SiO2
CHARGE_DISSIPATIVE_RESISTIVITY = mp.mpf('1e8')  # Tuned a-Si:H
PASSIVE_LAYER_ROUGHNESS = mp.mpf('5e-9')  # Nano-textured

# Advanced QM for Hamaker using PySCF with DFT (simplified for compatibility)
def compute_hamaker_quantum_dft():
    """
    Simplified quantum mechanical calculation of Hamaker constant.
    Falls back to classical approximation if PySCF is not available.
    """
    try:
        if not PYSCF_AVAILABLE:
            # Classical approximation
            return DUST_HAMAKER_CONSTANT
            
        # Dust: Fe2O3 cluster
        dust_mol = gto.M(atom='Fe 0 0 0; O 0 0 1.4; O 1.4 0 0; O -1.4 0 0; Si 0 2 0; O 0 3.4 0', 
                        basis='sto-3g', spin=5)  # Simplified basis for speed
        mf_dust = dft.UKS(dust_mol)
        mf_dust.xc = 'lda'  # Faster than b3lyp
        mf_dust.kernel()

        # Surface: SiO2 with a-Si:H
        surf_mol = gto.M(atom='Si 0 0 0; O 0 0 1.6; Si 1.6 0 0; O 1.6 0 1.6; H 0 0 -1', 
                        basis='sto-3g')
        mf_surf = dft.RKS(surf_mol)
        mf_surf.xc = 'lda'
        mf_surf.kernel()

        # Medium: CO2
        med_mol = gto.M(atom='C 0 0 0; O 0 0 1.16; O 0 0 -1.16', basis='sto-3g')
        mf_med = dft.RKS(med_mol)
        mf_med.xc = 'lda'
        mf_med.kernel()

        # Simplified interaction energy calculation
        interaction_energy = (mf_dust.e_tot + mf_surf.e_tot - 
                            (mf_dust.energy_nuc() + mf_surf.energy_nuc()))
        
        return mp.mpf(abs(interaction_energy) * const.hartree * 1e20)  # Convert to J
        
    except Exception as e:
        logging.warning(f"Quantum calculation failed: {e}. Using classical approximation.")
        return DUST_HAMAKER_CONSTANT

HAMAKER_QM = compute_hamaker_quantum_dft()

# Dust particle class with bipolar charging
class DustParticle:
    def __init__(self, position, radius=None):
        self.position = np.array([mp.mpf(str(x)) for x in position])
        
        if radius is None:
            # Use numpy for random generation, then convert to mpmath
            log_mean = float(mp.log(DUST_PARTICLE_RADIUS_MEAN))
            radius_val = np.random.lognormal(log_mean, 0.5)
            self.radius = mp.mpf(str(radius_val))
        else:
            self.radius = mp.mpf(str(radius))
            
        # Charge assignment based on size
        if self.radius < mp.mpf('2e-6'):
            charge_mean = float(DUST_CHARGE_MEAN_SMALL)
        else:
            charge_mean = float(DUST_CHARGE_MEAN_LARGE)
            
        charge_val = np.random.normal(charge_mean, float(DUST_CHARGE_STD))
        self.charge = mp.mpf(str(charge_val))
        
        self.mass = (mp.mpf('4')/mp.mpf('3')) * mp.pi * (self.radius**3) * DUST_DENSITY
        self.velocity = np.array([mp.mpf('0')] * 3)
        self.acceleration = np.array([mp.mpf('0')] * 3)
        self.spin = mp.mpf(str(np.random.uniform(-10, 10)))  # Angular velocity
        self.temperature = MARS_TEMP + mp.mpf(str(np.random.normal(0, 20)))
        self.composition = random.choice(['silicate', 'iron_oxide', 'perchlorate_mix'])
        self.shape_factor = mp.mpf(str(np.random.uniform(0.5, 1.5)))  # Asphericity
        self.stuck_to_surface = False  # Track adhesion state

    def compute_vdw_force(self, distance):
        """Van der Waals force calculation"""
        D = max(mp.mpf(str(distance)), mp.mpf('1e-10'))
        F = -HAMAKER_QM * self.radius / (mp.mpf('6') * D**2) * self.shape_factor
        return np.array([mp.mpf('0'), mp.mpf('0'), F])

    def compute_electrostatic_image(self, eps_s):
        """Image charge force from conducting surface"""
        D = self.position[2] + mp.mpf('1e-10')  # Avoid division by zero
        factor = (eps_s - CO2_DIELECTRIC) / (eps_s + CO2_DIELECTRIC)
        epsilon_0 = mp.mpf(str(const.epsilon_0))
        F = -factor * (self.charge**2) / (mp.mpf('16') * mp.pi * epsilon_0 * D**2)
        return np.array([mp.mpf('0'), mp.mpf('0'), F])

    def compute_capillary_force(self):
        """Capillary force from liquid bridging"""
        if random.random() < float(PERCHLORATE_CONC) and self.temperature < mp.mpf('273'):
            cos_angle = mp.cos(mp.radians(CONTACT_ANGLE))
            menisci = (BRINE_SURFACE_TENSION * cos_angle * mp.mpf('2') * 
                      mp.pi * self.radius * HUMIDITY_MARS * mp.mpf('10'))  # Enhanced by salts
        else:
            menisci = mp.mpf('0')
        return np.array([mp.mpf('0'), mp.mpf('0'), -menisci])

    def compute_gravity(self):
        """Gravitational force"""
        return np.array([mp.mpf('0'), mp.mpf('0'), -self.mass * MARS_GRAVITY])

    def compute_drag(self, wind_vel):
        """Aerodynamic drag force"""
        rel_vel = wind_vel - self.velocity
        rel_speed = mp.sqrt(sum(v**2 for v in rel_vel))
        
        if rel_speed == 0:
            return np.array([mp.mpf('0')] * 3)
            
        Cd = mp.mpf('0.47')  # Sphere approximation
        area = mp.pi * self.radius**2
        
        F_magnitude = mp.mpf('0.5') * Cd * MARS_ATM_DENSITY * rel_speed**2 * area
        F_direction = rel_vel / rel_speed
        
        return F_magnitude * F_direction

    def compute_magnus(self, wind_vel):
        """Magnus force from particle rotation"""
        rel_vel = wind_vel - self.velocity
        # Simplified Magnus force (perpendicular to both spin and velocity)
        F_magnitude = (mp.pi**2 * self.radius**3 * DUST_DENSITY * 
                      abs(self.spin) * mp.sqrt(sum(v**2 for v in rel_vel)))
        
        # Assume spin is around z-axis, force is in xy-plane
        if rel_vel[0] != 0 or rel_vel[1] != 0:
            F_x = -self.spin * rel_vel[1] * F_magnitude / mp.sqrt(rel_vel[0]**2 + rel_vel[1]**2)
            F_y = self.spin * rel_vel[0] * F_magnitude / mp.sqrt(rel_vel[0]**2 + rel_vel[1]**2)
        else:
            F_x = F_y = mp.mpf('0')
            
        return np.array([F_x, F_y, mp.mpf('0')])

    def compute_tribo_charge(self, other_particle):
        """Triboelectric charging from particle collisions"""
        distance = mp.sqrt(sum((self.position[i] - other_particle.position[i])**2 for i in range(3)))
        
        if distance < (self.radius + other_particle.radius):
            # Size-dependent charge transfer
            delta_q = mp.mpf('1e-17') * (self.radius - other_particle.radius)
            self.charge += delta_q
            other_particle.charge -= delta_q

    def compute_quantum_binding(self):
        """Simplified quantum mechanical binding energy"""
        if not PYSCF_AVAILABLE:
            # Classical approximation based on surface potential
            binding_energy = self.charge * EDS_VOLTAGE_AMPLITUDE / self.position[2]
            return mp.mpf(str(float(binding_energy) * const.e))  # Convert to Joules
            
        try:
            # Use PySCF for particle-surface interaction (simplified)
            atom_str = 'Fe 0 0 0' if self.composition == 'iron_oxide' else 'Si 0 0 0'
            mol_p = gto.M(atom=atom_str, basis='sto-3g', 
                         charge=int(float(self.charge / mp.mpf(str(const.e)))))
            mf_p = scf.RHF(mol_p)
            mf_p.kernel()
            
            # Surface fragment
            mol_s = gto.M(atom=f'Si 0 0 -{float(self.position[2])}', basis='sto-3g')
            mf_s = scf.RHF(mol_s)
            mf_s.kernel()
            
            # Interaction energy approximation
            int_energy = abs(mf_p.e_tot - mf_s.e_tot)
            return mp.mpf(str(int_energy * const.hartree))
            
        except Exception as e:
            logging.warning(f"Quantum binding calculation failed: {e}")
            # Fallback to classical
            binding_energy = self.charge * EDS_VOLTAGE_AMPLITUDE / (self.position[2] + mp.mpf('1e-9'))
            return mp.mpf(str(abs(float(binding_energy)) * const.e))

    def update_temperature(self, dt):
        """Update particle temperature based on radiative balance"""
        solar_flux = mp.mpf('590')  # W/m² at Mars
        albedo = mp.mpf('0.25')
        emissivity = mp.mpf('0.9')
        heat_cap = mp.mpf('800')  # J/kg/K
        stefan_boltzmann = mp.mpf(str(const.sigma))
        
        absorbed = solar_flux * (mp.mpf('1') - albedo) * mp.pi * self.radius**2
        emitted = emissivity * stefan_boltzmann * (self.temperature**4) * mp.mpf('4') * mp.pi * self.radius**2
        
        dT = dt * (absorbed - emitted) / (self.mass * heat_cap)
        self.temperature += dT
        
        # Limit temperature to reasonable range
        self.temperature = max(mp.mpf('150'), min(mp.mpf('400'), self.temperature))

# HDMS Surface with 2025 updates
class HDMSSurface:
    def __init__(self, size=(0.2, 0.2), num_electrodes=200):
        self.size = np.array([mp.mpf(str(s)) for s in size])
        self.electrodes = self.generate_electrodes(num_electrodes)
        self.phases = [mp.mpf(str(i * 2 * math.pi / EDS_PHASE_COUNT)) for i in range(EDS_PHASE_COUNT)]
        
        # Initialize control system if available
        if CONTROL_AVAILABLE:
            self.control_system = self.init_control()
        else:
            self.control_system = None
            
        self.voltage_history = []
        self.dust_load_history = []

    def generate_electrodes(self, n):
        """Generate electrode positions in a grid pattern"""
        n_side = int(np.sqrt(n))
        x = np.linspace(0, float(self.size[0]), n_side)
        y = np.linspace(0, float(self.size[1]), n_side)
        xx, yy = np.meshgrid(x, y)
        
        # Assign phases to electrodes in a checkerboard pattern
        phase_grid = ((np.arange(len(xx.flat)).reshape(xx.shape) % EDS_PHASE_COUNT))
        
        electrodes = []
        for phase in range(EDS_PHASE_COUNT):
            mask = phase_grid == phase
            ex = xx[mask]
            ey = yy[mask]
            electrodes.append((ex, ey))
            
        return electrodes

    def compute_E_field(self, pos, t):
        """Compute electric field at position pos and time t"""
        E = np.array([mp.mpf('0'), mp.mpf('0'), mp.mpf('0')])
        
        for i, (ex, ey) in enumerate(self.electrodes):
            for x_elec, y_elec in zip(ex, ey):
                dx = pos[0] - mp.mpf(str(x_elec))
                dy = pos[1] - mp.mpf(str(y_elec))
                dz = pos[2]
                
                r = mp.sqrt(dx**2 + dy**2 + dz**2) + mp.mpf('1e-10')
                
                # Voltage with phase shift
                phase = self.phases[i]
                omega = mp.mpf('2') * mp.pi * EDS_FREQUENCY
                V = EDS_VOLTAGE_AMPLITUDE * mp.sin(omega * t + phase)
                
                # Electric field with exponential decay in z-direction
                decay_factor = mp.exp(-mp.pi * dz / EDS_ELECTRODE_SPACING)
                traveling_wave = mp.sin(mp.mpf('2') * mp.pi * (pos[0] / EDS_ELECTRODE_SPACING - EDS_FREQUENCY * t))
                
                E_magnitude = V * decay_factor * traveling_wave / r**2
                
                # Direction vector (pointing from electrode to position)
                if r > mp.mpf('1e-10'):
                    E[0] += E_magnitude * dx / r
                    E[1] += E_magnitude * dy / r
                    E[2] += E_magnitude * dz / r
                    
        return E

    def compute_grad_E2(self, pos, t):
        """Compute gradient of E-field squared for dielectrophoretic force"""
        delta = mp.mpf('1e-6')
        
        # Central difference approximation
        E_center = self.compute_E_field(pos, t)
        E_mag_sq_center = sum(E_i**2 for E_i in E_center)
        
        grad_E2 = np.array([mp.mpf('0')] * 3)
        
        for i in range(3):
            pos_plus = pos.copy()
            pos_minus = pos.copy()
            pos_plus[i] += delta
            pos_minus[i] -= delta
            
            E_plus = self.compute_E_field(pos_plus, t)
            E_minus = self.compute_E_field(pos_minus, t)
            
            E_mag_sq_plus = sum(E_i**2 for E_i in E_plus)
            E_mag_sq_minus = sum(E_i**2 for E_i in E_minus)
            
            grad_E2[i] = (E_mag_sq_plus - E_mag_sq_minus) / (mp.mpf('2') * delta)
            
        return grad_E2

    def init_control(self):
        """Initialize PID control system for voltage regulation"""
        if not CONTROL_AVAILABLE:
            return None
            
        try:
            # Simple transfer function model
            sys_tf = control.tf([1], [1, 0.5, 1])
            
            # PID controller parameters
            Kp, Ki, Kd = 1.2, 0.01, 0.5
            pid = control.tf([Kd, Kp, Ki], [1, 0])
            
            # Closed-loop system
            return control.feedback(sys_tf * pid)
            
        except Exception as e:
            logging.warning(f"Control system initialization failed: {e}")
            return None

    def adjust_voltage(self, dust_load):
        """Adjust voltage based on dust load using control system"""
        self.dust_load_history.append(float(dust_load))
        
        if self.control_system is not None and CONTROL_AVAILABLE:
            try:
                # Generate step response
                t_sim = np.linspace(0, 1, 100)
                t, y = control.step_response(self.control_system, t_sim)
                
                # Use final value as voltage multiplier
                voltage_multiplier = y[-1] if len(y) > 0 else 1.0
                new_voltage = EDS_VOLTAGE_AMPLITUDE * mp.mpf(str(abs(voltage_multiplier)))
                
            except Exception as e:
                logging.warning(f"Control system adjustment failed: {e}")
                # Simple proportional control fallback
                new_voltage = EDS_VOLTAGE_AMPLITUDE * (mp.mpf('1') + dust_load)
        else:
            # Simple proportional control
            new_voltage = EDS_VOLTAGE_AMPLITUDE * (mp.mpf('1') + dust_load)
            
        self.voltage_history.append(float(new_voltage))
        return new_voltage

    def get_surface_charge_density(self, pos):
        """Compute surface charge density at position"""
        # Simplified model based on capacitor charging
        epsilon_r = DIELECTRIC_CONSTANT
        epsilon_0 = mp.mpf(str(const.epsilon_0))
        
        # Use average voltage
        if self.voltage_history:
            V_avg = mp.mpf(str(np.mean(self.voltage_history[-10:])))  # Last 10 values
        else:
            V_avg = EDS_VOLTAGE_AMPLITUDE
            
        charge_density = epsilon_r * epsilon_0 * V_avg / DIELECTRIC_THICKNESS
        return charge_density

    def compute_surface_roughness_force(self, particle):
        """Additional force due to surface roughness"""
        if particle.position[2] < particle.radius + PASSIVE_LAYER_ROUGHNESS:
            # Van der Waals force enhancement due to roughness
            roughness_factor = mp.mpf('1.5')  # Empirical enhancement
            base_vdw = particle.compute_vdw_force(particle.position[2])
            return base_vdw * roughness_factor
        else:
            return np.array([mp.mpf('0')] * 3)

# Wind and dust devil model
class MarsEnvironment:
    def __init__(self):
        self.wind_vel = np.array([
            mp.mpf(str(np.random.normal(float(WIND_SPEED_MEAN), float(WIND_SPEED_STD)))), 
            mp.mpf('0'), 
            mp.mpf('0')
        ])
        self.dust_devil_prob = mp.mpf('0.01')  # Per timestep
        self.vortex_strength = mp.mpf('0')
        self.pressure_variation = mp.mpf('1.0')  # Atmospheric pressure multiplier
        self.temperature_variation = mp.mpf('0')  # Temperature offset from mean

    def update_wind(self):
        """Update wind conditions including gusts and dust devils"""
        # Add wind variation
        wind_change = mp.mpf(str(np.random.normal(0, 0.1)))
        self.wind_vel[0] += wind_change
        
        # Limit wind speed to reasonable range
        self.wind_vel[0] = max(mp.mpf('0'), min(mp.mpf('50'), self.wind_vel[0]))
        
        # Check for dust devil formation
        if random.random() < float(self.dust_devil_prob):
            self.vortex_strength = mp.mpf(str(np.random.uniform(1, 5)))
            logging.info(f"Dust devil formed with strength {self.vortex_strength}")
        else:
            # Decay existing vortex
            self.vortex_strength *= mp.mpf('0.95')
            
        # Update atmospheric conditions
        self.pressure_variation *= mp.mpf(str(1 + np.random.normal(0, 0.01)))
        self.temperature_variation += mp.mpf(str(np.random.normal(0, 1)))

    def get_local_wind(self, pos):
        """Get wind velocity at specific position"""
        local_wind = self.wind_vel.copy()
        
        if self.vortex_strength > mp.mpf('0'):
            # Add vortex component
            r = mp.sqrt(pos[0]**2 + pos[1]**2) + mp.mpf('1e-10')
            theta_vel = self.vortex_strength / (mp.mpf('2') * mp.pi * r)
            
            if r > mp.mpf('1e-10'):
                vx = -theta_vel * pos[1] / r
                vy = theta_vel * pos[0] / r
                local_wind[0] += vx
                local_wind[1] += vy
                
        return local_wind

    def get_atmospheric_density(self, altitude=mp.mpf('0')):
        """Get atmospheric density at given altitude"""
        # Simple exponential atmosphere model
        scale_height = mp.mpf('11100')  # meters
        density = MARS_ATM_DENSITY * mp.exp(-altitude / scale_height) * self.pressure_variation
        return density

def _update_particle_worker(args):
    """Update a single particle (for multiprocessing)"""
    particle, t, env, surface, dt = args
    
    try:
        # Get environmental conditions
        wind = env.get_local_wind(particle.position)
        local_density = env.get_atmospheric_density(particle.position[2])
        
        # Compute all forces
        forces = {}
        
        # Van der Waals force
        forces['vdw'] = particle.compute_vdw_force(particle.position[2])
        
        # Electrostatic image force
        forces['image'] = particle.compute_electrostatic_image(DIELECTRIC_CONSTANT)
        
        # Capillary force
        forces['capillary'] = particle.compute_capillary_force()
        
        # Gravitational force
        forces['gravity'] = particle.compute_gravity()
        
        # Drag force (use local density)
        old_density = MARS_ATM_DENSITY
        # Temporarily modify particle's drag calculation
        forces['drag'] = particle.compute_drag(wind) * (local_density / old_density)
        
        # Magnus force
        forces['magnus'] = particle.compute_magnus(wind)
        
        # Electric field forces
        E = surface.compute_E_field(particle.position, t)
        grad_E2 = surface.compute_grad_E2(particle.position, t)
        
        # Coulomb force
        forces['coulomb'] = particle.charge * E
        
        # Dielectrophoretic force
        eps_p = DUST_DIELECTRIC_CONSTANT if particle.composition == 'silicate' else mp.mpf('8.9')  # Hematite
        epsilon_0 = mp.mpf(str(const.epsilon_0))
        K_cm = (mp.mpf('3') * (eps_p - CO2_DIELECTRIC) / 
               (eps_p + mp.mpf('2') * CO2_DIELECTRIC) / 
               (mp.mpf('4') * mp.pi * epsilon_0))
        
        forces['dep'] = (mp.mpf('2') * mp.pi * particle.radius**3 * 
                       CO2_DIELECTRIC * K_cm) * grad_E2
        
        # Quantum binding force (simplified)
        quantum_binding = particle.compute_quantum_binding()
        forces['quantum'] = np.array([mp.mpf('0'), mp.mpf('0'), 
                                    -quantum_binding / (particle.position[2] + mp.mpf('1e-9'))])
        
        # Surface roughness force
        forces['roughness'] = surface.compute_surface_roughness_force(particle)
        
        # Sum all forces
        F_total = np.array([mp.mpf('0')] * 3)
        for force in forces.values():
            F_total += force
        
        # Update particle dynamics
        particle.acceleration = F_total / particle.mass
        particle.velocity += particle.acceleration * dt
        particle.position += particle.velocity * dt + mp.mpf('0.5') * particle.acceleration * (dt**2)
        
        # Boundary conditions
        # Ground collision
        if particle.position[2] < particle.radius:
            particle.position[2] = particle.radius
            
            # Check if particle sticks to surface
            total_attractive_force = (forces['vdw'][2] + forces['image'][2] + 
                                    forces['capillary'][2] + forces['quantum'][2])
            
            if total_attractive_force < mp.mpf('0'):  # Attractive
                particle.stuck_to_surface = True
                particle.velocity = np.array([mp.mpf('0')] * 3)
            else:
                # Inelastic bounce
                restitution = mp.mpf('0.3')
                particle.velocity[2] = -particle.velocity[2] * restitution
        
        # Lateral boundaries (periodic)
        for i in [0, 1]:
            if particle.position[i] < mp.mpf('0'):
                particle.position[i] = surface.size[i] + particle.position[i]
            elif particle.position[i] > surface.size[i]:
                particle.position[i] = particle.position[i] - surface.size[i]
        
        # Upper boundary (escape condition)
        if particle.position[2] > mp.mpf('0.01'):  # 1 cm height limit
            particle.position[2] = mp.mpf('0.01')
            particle.velocity[2] = mp.mpf('0')
        
        # Update particle temperature
        particle.update_temperature(dt)
        
        return particle
        
    except Exception as e:
        logging.error(f"Particle update failed: {e}")
        return particle

# Simulation with parallelism
class HDMSSimulation:
    def __init__(self, num_particles=1000, sim_time=3600, dt=0.001, surface_size=(0.2, 0.2)):
        """
        Initialize HDMS simulation
        
        Args:
            num_particles: Number of dust particles to simulate
            sim_time: Total simulation time in seconds
            dt: Time step in seconds
            surface_size: (width, height) of surface in meters
        """
        self.surface = HDMSSurface(size=surface_size)
        
        # Generate particles with realistic initial conditions
        self.particles = []
        for _ in range(num_particles):
            x = np.random.uniform(0, surface_size[0])
            y = np.random.uniform(0, surface_size[1])
            z = np.random.exponential(1e-5)  # Height above surface
            self.particles.append(DustParticle([x, y, z]))
            
        self.env = MarsEnvironment()
        self.time = mp.mpf('0')
        self.sim_time = mp.mpf(str(sim_time))
        self.dt = mp.mpf(str(dt))
        self.history = []
        self.dust_load = mp.mpf('0')
        
        # Performance tracking
        self.performance_data = {
            'removal_efficiency': [],
            'power_consumption': [],
            'particle_velocities': [],
            'surface_coverage': []
        }
        
        self.use_multiprocessing = True  # Default, can be overridden by runner

    def run_step(self, t, pool=None):
        """Execute one simulation time step"""
        # Update environment
        self.env.update_wind()
        
        # Prepare arguments for worker function
        args = [(p, t, self.env, self.surface, self.dt) for p in self.particles]
        
        # Update particles
        if self.use_multiprocessing and pool and len(self.particles) > 100:
            try:
                self.particles = pool.map(_update_particle_worker, args)
            except Exception as e:
                logging.warning(f"Multiprocessing pool.map failed: {e}. Running serially for this step.")
                self.particles = [_update_particle_worker(arg) for arg in args]
        else:
            # Serial processing
            self.particles = [_update_particle_worker(arg) for arg in args]
        
        # Handle particle interactions
        self.particle_interactions()
        
        # Update system metrics
        self.update_dust_load()
        
        # Store particle velocities for analysis
        velocities = [float(mp.sqrt(sum(v**2 for v in p.velocity))) for p in self.particles]
        self.performance_data['particle_velocities'].append(np.mean(velocities))
        
        # Store history (reduce frequency for large simulations)
        if len(self.history) < 10000:  # Limit memory usage
            self.history.append([p.position.copy() for p in self.particles])

    def run(self):
        """Run the complete simulation"""
        steps = int(float(self.sim_time / self.dt))
        logging.info(f"Starting simulation with {len(self.particles)} particles for {steps} steps")
        
        start_time = time.time()
        
        num_processes = min(cpu_count(), 8)
        
        run_serial = False
        if self.use_multiprocessing and len(self.particles) > 100:
            try:
                # Use a context manager for the pool to ensure it's always closed
                with Pool(processes=num_processes) as pool:
                    for step in range(steps):
                        self.run_step(self.time, pool)
                        self.time += self.dt
                        
                        if step % 1000 == 0:
                            elapsed = time.time() - start_time
                            progress = step / steps * 100
                            logging.info(f"Step {step}/{steps} ({progress:.1f}%) - "
                                       f"Elapsed: {elapsed:.1f}s - "
                                       f"Dust load: {float(self.dust_load):.3f}")
                            gc.collect()
            except Exception as e:
                logging.warning(f"Multiprocessing failed: {e}\n{traceback.format_exc()}. Falling back to serial processing.")
                run_serial = True
        else:
            run_serial = True

        if run_serial:
            if self.time > 0:
                 logging.info("Restarting simulation in serial mode.")
                 self.time = mp.mpf('0')

            for step in range(steps):
                self.run_step(self.time, None)  # No pool passed
                self.time += self.dt
                if step % 1000 == 0:
                    elapsed = time.time() - start_time
                    progress = step / steps * 100
                    logging.info(f"Step {step}/{steps} ({progress:.1f}%) - "
                               f"Elapsed: {elapsed:.1f}s - "
                               f"Dust load: {float(self.dust_load):.3f} (Serial)")
                    gc.collect()

        total_time = time.time() - start_time
        logging.info(f"Simulation completed in {total_time:.2f} seconds")

    def particle_interactions(self):
        """Handle particle-particle interactions"""
        # Simplified O(n) algorithm for large particle counts
        grid_size = 10
        grid = {}
        
        # Spatial hashing for efficient collision detection
        for i, p in enumerate(self.particles):
            grid_x = int(float(p.position[0]) * grid_size / float(self.surface.size[0]))
            grid_y = int(float(p.position[1]) * grid_size / float(self.surface.size[1]))
            grid_key = (grid_x, grid_y)
            
            if grid_key not in grid:
                grid[grid_key] = []
            grid[grid_key].append((i, p))
        
        # Check interactions within neighboring grid cells
        for cell_particles in grid.values():
            for i, (idx1, p1) in enumerate(cell_particles):
                for j, (idx2, p2) in enumerate(cell_particles[i+1:], i+1):
                    p1.compute_tribo_charge(p2)

    def update_dust_load(self):
        """Calculate dust removal efficiency metrics"""
        stuck_particles = sum(1 for p in self.particles if p.stuck_to_surface)
        near_surface = sum(1 for p in self.particles if p.position[2] <= p.radius * mp.mpf('2'))
        
        self.dust_load = mp.mpf(str(near_surface)) / mp.mpf(str(len(self.particles)))
        removal_efficiency = mp.mpf(str(stuck_particles)) / mp.mpf(str(len(self.particles)))
        
        # Update surface voltage based on dust load
        new_voltage = self.surface.adjust_voltage(self.dust_load)
        
        # Store performance data
        self.performance_data['removal_efficiency'].append(float(removal_efficiency))
        self.performance_data['surface_coverage'].append(float(self.dust_load))
        
        # Estimate power consumption
        power = float(new_voltage)**2 / float(CHARGE_DISSIPATIVE_RESISTIVITY) * float(self.surface.size[0] * self.surface.size[1])
        self.performance_data['power_consumption'].append(power)

    def visualize(self):
        """Create 3D visualization of particle dynamics"""
        if not self.history:
            logging.warning("No history data available for visualization")
            return
            
        try:
            from matplotlib.animation import FuncAnimation, PillowWriter
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            def animate(frame_idx):
                ax.clear()
                
                if frame_idx < len(self.history):
                    positions = self.history[frame_idx]
                    pos_array = np.array([[float(p[0]), float(p[1]), float(p[2])] 
                                        for p in positions], dtype=float)
                    
                    if len(pos_array) > 0:
                        # Color particles by height
                        colors = pos_array[:, 2]
                        scatter = ax.scatter(pos_array[:, 0], pos_array[:, 1], pos_array[:, 2], 
                                           c=colors, cmap='viridis', s=2, alpha=0.6)
                        
                        # Set axis limits
                        ax.set_xlim(0, float(self.surface.size[0]))
                        ax.set_ylim(0, float(self.surface.size[1]))
                        ax.set_zlim(0, 1e-3)
                        
                        # Labels and title
                        ax.set_xlabel('X (m)')
                        ax.set_ylabel('Y (m)')
                        ax.set_zlabel('Z (m)')
                        ax.set_title(f'HDMS Particle Dynamics - Step {frame_idx}')
                        
                        # Add colorbar
                        if not hasattr(animate, 'colorbar_added'):
                            fig.colorbar(scatter, ax=ax, label='Height (m)', shrink=0.5)
                            animate.colorbar_added = True
            
            # Create animation
            frames = min(len(self.history), 200)  # Limit frames for performance
            ani = FuncAnimation(fig, animate, frames=frames, interval=50, repeat=True)
            
            # Save as GIF
            try:
                writer = PillowWriter(fps=20)
                ani.save('hdms_simulation.gif', writer=writer)
                logging.info("Animation saved as hdms_simulation.gif")
            except Exception as e:
                logging.warning(f"Could not save animation: {e}")
            
            plt.show()
            
        except Exception as e:
            logging.error(f"Visualization failed: {e}")

    def analyze_statistics(self):
        """Analyze simulation statistics and performance"""
        if not self.performance_data['removal_efficiency']:
            return "No performance data available"
        
        try:
            # Basic statistics
            removal_eff = np.array(self.performance_data['removal_efficiency'])
            power_cons = np.array(self.performance_data['power_consumption'])
            velocities = np.array(self.performance_data['particle_velocities'])
            
            stats = {
                'Average Removal Efficiency': f"{np.mean(removal_eff):.3f} ± {np.std(removal_eff):.3f}",
                'Average Power Consumption': f"{np.mean(power_cons):.2f} ± {np.std(power_cons):.2f} W",
                'Average Particle Velocity': f"{np.mean(velocities):.6f} ± {np.std(velocities):.6f} m/s",
                'Peak Removal Efficiency': f"{np.max(removal_eff):.3f}",
                'Total Simulation Time': f"{float(self.time):.2f} s",
                'Number of Particles': len(self.particles),
                'Final Dust Load': f"{float(self.dust_load):.3f}"
            }
            
            # Statistical analysis if statsmodels is available
            if STATSMODELS_AVAILABLE:
                try:
                    # Linear regression of removal efficiency over time
                    time_points = np.arange(len(removal_eff))
                    X = sm.add_constant(time_points)
                    model = sm.OLS(removal_eff, X)
                    results = model.fit()
                    
                    stats['Efficiency Trend (slope)'] = f"{results.params[1]:.6f}"
                    stats['R-squared'] = f"{results.rsquared:.3f}"
                    
                    return f"Simulation Statistics:\n" + "\n".join([f"{k}: {v}" for k, v in stats.items()]) + f"\n\nRegression Summary:\n{results.summary()}"
                    
                except Exception as e:
                    logging.warning(f"Advanced statistics failed: {e}")
                    
            return f"Simulation Statistics:\n" + "\n".join([f"{k}: {v}" for k, v in stats.items()])
            
        except Exception as e:
            logging.error(f"Statistics analysis failed: {e}")
            return f"Statistics analysis failed: {e}"

    def quantum_ensemble(self):
        """Quantum ensemble analysis of particles"""
        if not QUTIP_AVAILABLE:
            return "QuTip not available - quantum analysis disabled"
            
        try:
            states = []
            for p in self.particles[:10]:  # Subset for performance
                # Create quantum harmonic oscillator for charged particle
                N = 20  # Hilbert space dimension
                a = qt.destroy(N)
                n = qt.num(N)
                
                # Hamiltonian for charged oscillator in electric field
                omega = 2 * math.pi * float(EDS_FREQUENCY)
                H = omega * n + float(p.charge) * (a + a.dag())  # Linear coupling to field
                
                # Initial state based on particle charge
                charge_level = min(N-1, max(0, int(abs(float(p.charge / mp.mpf(str(const.e)))))))
                psi0 = qt.basis(N, charge_level)
                
                # Time evolution
                times = np.linspace(0, 1e-3, 100)  # 1 ms evolution
                result = qt.mesolve(H, psi0, times)
                states.append(result.states[-1])
                
            return f"Quantum ensemble analysis completed for {len(states)} particles"
            
        except Exception as e:
            logging.error(f"Quantum ensemble analysis failed: {e}")
            return f"Quantum analysis failed: {e}"

    def chemical_analysis(self):
        """Chemical composition analysis of dust particles"""
        if not RDKIT_AVAILABLE:
            return "RDKit not available - chemical analysis disabled"
            
        try:
            compositions = [p.composition for p in self.particles]
            comp_counts = {comp: compositions.count(comp) for comp in set(compositions)}
            
            # Simplified molecular property calculation
            molecules = {
                'silicate': 'O=[Si]=O',
                'iron_oxide': '[Fe+3].[O-2].[O-2].[O-2]',
                'perchlorate_mix': 'Cl(=O)(=O)(=O)[O-]'
            }
            
            properties = {}
            for comp, smiles in molecules.items():
                try:
                    mol = Chem.MolFromSmiles(smiles)
                    if mol:
                        AllChem.Compute2DCoords(mol)
                        properties[comp] = {
                            'molecular_weight': Descriptors.MolWt(mol),
                            'logp': Descriptors.MolLogP(mol) if comp != 'iron_oxide' else 'N/A',
                            'count': comp_counts.get(comp, 0)
                        }
                except Exception as e:
                    logging.warning(f"Failed to analyze {comp}: {e}")
                    
            return f"Chemical Analysis:\n" + "\n".join([
                f"{comp}: MW={props.get('molecular_weight', 'N/A'):.2f}, "
                f"LogP={props.get('logp', 'N/A')}, Count={props.get('count', 0)}"
                for comp, props in properties.items()
            ])
            
        except Exception as e:
            logging.error(f"Chemical analysis failed: {e}")
            return f"Chemical analysis failed: {e}"

    def network_graph(self):
        """Create network graph of particle interactions"""
        try:
            G = nx.Graph()
            
            # Add nodes for each particle
            for i, p in enumerate(self.particles[:100]):  # Limit to 100 for visualization
                G.add_node(i, pos=(float(p.position[0]), float(p.position[1])), 
                          charge=float(p.charge), radius=float(p.radius))
            
            # Add edges for particles within interaction range
            interaction_range = 5e-6  # 5 micrometers
            for i in range(len(G.nodes())):
                for j in range(i+1, len(G.nodes())):
                    if i < len(self.particles) and j < len(self.particles):
                        dist = float(mp.sqrt(sum((self.particles[i].position[k] - 
                                                self.particles[j].position[k])**2 for k in range(3))))
                        if dist < interaction_range:
                            weight = 1.0 / (dist**2 + 1e-12)  # Inverse square law
                            G.add_edge(i, j, weight=weight)
            
            # Create visualization
            plt.figure(figsize=(10, 8))
            pos = nx.get_node_attributes(G, 'pos')
            
            if pos:
                # Draw network
                nx.draw(G, pos, node_size=20, node_color='red', edge_color='gray', 
                       alpha=0.6, with_labels=False)
                plt.title('Particle Interaction Network')
                plt.xlabel('X Position (m)')
                plt.ylabel('Y Position (m)')
                
                # Save plot
                plt.savefig('particle_network.png', dpi=300, bbox_inches='tight')
                plt.show()
                
                return f"Network analysis: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
            else:
                return "No position data available for network visualization"
                
        except Exception as e:
            logging.error(f"Network analysis failed: {e}")
            return f"Network analysis failed: {e}"

    def ml_predict_removal(self):
        """Machine learning prediction of particle removal"""
        if not TORCH_AVAILABLE:
            return "PyTorch not available - ML prediction disabled"
            
        try:
            class ParticleDataset(Dataset):
                def __init__(self, particles):
                    self.data = []
                    self.labels = []
                    
                    for p in particles:
                        features = [float(p.radius), float(p.charge), float(p.position[2]), 
                                  float(p.mass), float(p.temperature)]
                        self.data.append(torch.tensor(features, dtype=torch.float32))
                        
                        # Label: 1 if particle is removed (stuck to surface), 0 otherwise
                        label = 1 if p.stuck_to_surface else 0
                        self.labels.append(torch.tensor(label, dtype=torch.float32))

                def __len__(self):
                    return len(self.data)

                def __getitem__(self, idx):
                    return self.data[idx], self.labels[idx]

            # Create dataset and dataloader
            dataset = ParticleDataset(self.particles)
            
            if len(dataset) == 0:
                return "No particle data available for ML training"
                
            dataloader = DataLoader(dataset, batch_size=min(32, len(dataset)), shuffle=True)
            
            # Simple neural network model
            model = nn.Sequential(
                nn.Linear(5, 64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
                nn.Sigmoid()
            )
            
            optimizer = optim.Adam(model.parameters(), lr=0.001)
            criterion = nn.BCELoss()
            
            # Training
            model.train()
            total_loss = 0
            num_batches = 0
            
            for epoch in range(10):  # Reduced epochs for speed
                epoch_loss = 0
                epoch_batches = 0
                
                for batch_data, batch_labels in dataloader:
                    optimizer.zero_grad()
                    outputs = model(batch_data).squeeze()
                    loss = criterion(outputs, batch_labels)
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                    epoch_batches += 1
                
                if epoch_batches > 0:
                    avg_loss = epoch_loss / epoch_batches
                    total_loss += avg_loss
                    num_batches += 1
            
            final_loss = total_loss / num_batches if num_batches > 0 else float('inf')
            
            # Evaluation
            model.eval()
            with torch.no_grad():
                correct = 0
                total = 0
                for batch_data, batch_labels in dataloader:
                    outputs = model(batch_data).squeeze()
                    predicted = (outputs > 0.5).float()
                    total += batch_labels.size(0)
                    correct += (predicted == batch_labels).sum().item()
                
                accuracy = correct / total if total > 0 else 0
            
            return f"ML Model Training Complete:\nFinal Loss: {final_loss:.4f}\nAccuracy: {accuracy:.3f}"
            
        except Exception as e:
            logging.error(f"ML prediction failed: {e}")
            return f"ML prediction failed: {e}"

    def compress_data(self):
        """Compress and save simulation data"""
        try:
            # Prepare data for compression
            data_dict = {
                'particles': [(float(p.position[0]), float(p.position[1]), float(p.position[2]),
                             float(p.radius), float(p.charge), p.composition) for p in self.particles],
                'performance': self.performance_data,
                'parameters': {
                    'num_particles': len(self.particles),
                    'sim_time': float(self.sim_time),
                    'dt': float(self.dt),
                    'surface_size': [float(s) for s in self.surface.size]
                }
            }
            
            # Pickle and compress
            data_bytes = pickle.dumps(data_dict)
            compressed_data = lzma.compress(data_bytes, preset=6)
            
            # Save to file
            with open('hdms_simulation_data.xz', 'wb') as f:
                f.write(compressed_data)
            
            compression_ratio = len(compressed_data) / len(data_bytes)
            return f"Data compressed and saved. Compression ratio: {compression_ratio:.3f}"
            
        except Exception as e:
            logging.error(f"Data compression failed: {e}")
            return f"Data compression failed: {e}"

    def generate_report(self):
        """Generate comprehensive simulation report"""
        report = [
            "="*60,
            "HDMS SIMULATION REPORT",
            "="*60,
            f"Simulation completed at: {datetime.datetime.now()}",
            f"Total simulation time: {float(self.time):.2f} seconds",
            f"Number of particles: {len(self.particles)}",
            f"Surface dimensions: {float(self.surface.size[0]):.3f} x {float(self.surface.size[1]):.3f} m",
            "",
            "PERFORMANCE METRICS:",
            self.analyze_statistics(),
            "",
            "CHEMICAL ANALYSIS:",
            self.chemical_analysis(),
            "",
            "QUANTUM ANALYSIS:",
            self.quantum_ensemble(),
            "",
            "MACHINE LEARNING PREDICTION:",
            self.ml_predict_removal(),
            "",
            "DATA COMPRESSION:",
            self.compress_data(),
            "="*60
        ]
        
        report_text = "\n".join(report)
        
        # Save report to file
        try:
            with open('hdms_simulation_report.txt', 'w') as f:
                f.write(report_text)
            logging.info("Report saved to hdms_simulation_report.txt")
        except Exception as e:
            logging.warning(f"Could not save report: {e}")
        
        return report_text

# Additional analysis methods for completeness
def generate_symbolic_forces():
    """Generate symbolic representation of all forces"""
    try:
        # Define symbolic variables
        q, E, r, eps_p, eps_m, gradE2, A, D, gamma, theta, rho, g = sp.symbols(
            'q E r eps_p eps_m gradE2 A D gamma theta rho g', real=True, positive=True)
        
        # Define forces symbolically
        F_coul = q * E
        K = (eps_p - eps_m) / (eps_p + 2 * eps_m)
        F_dep = sp.pi * r**3 * eps_m * K * gradE2
        F_vdw = -A * r / (6 * D**2)
        F_cap = -2 * sp.pi * r * gamma * sp.cos(theta)
        F_grav = -(4/3) * sp.pi * r**3 * rho * g
        
        total_F = F_coul + F_dep + F_vdw + F_cap + F_grav
        
        # Generate LaTeX representation
        latex_F = sp.latex(total_F)
        
        # Save to file
        with open('force_equations.tex', 'w') as f:
            f.write(f"Total Force Equation:\n\\begin{{equation}}\nF = {latex_F}\n\\end{{equation}}")
        
        return f"Symbolic forces generated and saved to force_equations.tex"
        
    except Exception as e:
        logging.error(f"Symbolic force generation failed: {e}")
        return f"Symbolic analysis failed: {e}"

def high_precision_calculation():
    """Demonstrate high-precision calculations with mpmath"""
    try:
        original_dps = mp.dps
        results = []
        
        # Test precision scaling
        for precision in [50, 100, 200]:
            mp.dps = precision
            
            # Calculate a complex integral
            result = mp.quad(lambda x: mp.exp(-x**2) * mp.cos(x), [0, mp.inf])
            results.append(f"Precision {precision}: {result}")
            
        mp.dps = original_dps  # Restore
        
        return f"High-precision calculations:\n" + "\n".join(results)
        
    except Exception as e:
        logging.error(f"High-precision calculation failed: {e}")
        return f"High-precision calculation failed: {e}"

def simulate_mars_conditions():
    """Simulate various Mars environmental conditions"""
    conditions = {
        'dust_storm': {
            'wind_speed': mp.mpf('25'),
            'dust_flux': mp.mpf('1e-6'),
            'visibility': mp.mpf('10')
        },
        'clear_day': {
            'wind_speed': mp.mpf('5'),
            'dust_flux': mp.mpf('1e-10'),
            'visibility': mp.mpf('1000')
        },
        'polar_winter': {
            'wind_speed': mp.mpf('15'),
            'dust_flux': mp.mpf('1e-9'),
            'temperature': mp.mpf('150')
        }
    }
    
    return f"Mars environmental conditions database created with {len(conditions)} scenarios"

# Main execution block with proper Windows multiprocessing support
def main():
    """Main execution function"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hdms_simulation.log'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Starting HDMS Simulation")
    logging.info(f"Platform: {sys.platform}")
    logging.info(f"Python version: {sys.version}")
    
    # Check available libraries
    availability_report = [
        f"PySCF: {PYSCF_AVAILABLE}",
        f"Control: {CONTROL_AVAILABLE}",
        f"RDKit: {RDKIT_AVAILABLE}",
        f"PyTorch: {TORCH_AVAILABLE}",
        f"QuTip: {QUTIP_AVAILABLE}",
        f"Statsmodels: {STATSMODELS_AVAILABLE}",
        f"Unix modules: {UNIX_AVAILABLE}"
    ]
    
    logging.info("Library availability:\n" + "\n".join(availability_report))
    
    try:
        # Create simulation with reduced parameters for demonstration
        logging.info("Initializing simulation...")
        sim = HDMSSimulation(
            num_particles=500,   # Reduced for demo
            sim_time=10,         # 10 seconds
            dt=0.01,            # 10ms time step
            surface_size=(0.1, 0.1)  # 10cm x 10cm surface
        )
        
        logging.info("Running simulation...")
        sim.run()
        
        logging.info("Generating visualizations...")
        sim.visualize()
        
        logging.info("Performing analysis...")
        print("\n" + "="*60)
        print("SIMULATION RESULTS")
        print("="*60)
        
        # Generate comprehensive report
        report = sim.generate_report()
        print(report)
        
        # Additional analyses
        print("\nSYMBOLIC ANALYSIS:")
        print(generate_symbolic_forces())
        
        print("\nHIGH-PRECISION CALCULATIONS:")
        print(high_precision_calculation())
        
        print("\nMARTS CONDITIONS DATABASE:")
        print(simulate_mars_conditions())
        
        # Network analysis
        print("\nNETWORK ANALYSIS:")
        network_result = sim.network_graph()
        print(network_result)
        
        logging.info("Simulation completed successfully!")
        
    except Exception as e:
        logging.error(f"Simulation failed: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == '__main__':
    # Required for Windows multiprocessing
    if sys.platform == "win32":
        freeze_support()
    
    main()
