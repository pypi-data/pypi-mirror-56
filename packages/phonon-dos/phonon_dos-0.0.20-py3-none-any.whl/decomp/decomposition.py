#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:11:33 2019

@author: Gabriele Coiana
"""
import numpy as np
from decomp import cell, read, plot, util
import os, sys

def corr(tall,X,tau,mode):
    M = len(tall)
    dt = tall[1] - tall[0]
    tmax = M - tau
    N = np.size(X[0])   
    X0 = X[0:tmax,:]
    X2 = 1/tmax*np.sum(X[0:tmax,:]*X[0:tmax,:])
    C = []
    for n in range(tau):
        Xjj = X[n:n+tmax,:]
        a = np.multiply(np.conjugate(X0),Xjj)
        b = 1/(tmax) * np.sum(a,axis=0)#/X2
        c = np.multiply(b,1)
        if (mode=='projected'):
            d = c
        else:
            d = np.sum(c)
        C.append(d)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

## =============================================================================
## Parameters
input_file = sys.argv[1]
a = read.read_parameters(input_file)[0]
Masses = read.read_parameters(input_file)[1]
n_atom_unit_cell = read.read_parameters(input_file)[2]
N1,N2,N3 = read.read_parameters(input_file)[3:6]
kinput = read.read_parameters(input_file)[6::][0]
file_eigenvectors = read.read_parameters(input_file)[7]
file_trajectory = read.read_parameters(input_file)[8]
file_initial_conf = read.read_parameters(input_file)[9]
system = read.read_parameters(input_file)[10]
DT = read.read_parameters(input_file)[11]
tau = read.read_parameters(input_file)[12]
T = read.read_parameters(input_file)[13]


tot_atoms_uc = int(np.sum(n_atom_unit_cell)) 
N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*tot_atoms_uc    # Number of atoms
masses, masses_for_animation = util.repeat_masses(Masses, n_atom_unit_cell, N1, N2, N3)
cH = 1.066*1e-6 # to [H]
cev = 2.902*1e-05 # to [ev]
kbH = 3.1668085639379003*1e-06# a.u. [H/K]
kbev = 8.617333262*1e-05 # [ev/K]
### =============================================================================

print('\nHello, lets start!\n')
print(' Getting input parameters and calculating velocities...')
print(' Temperature: ', T, ' K')
Nqpoints, qpoints_scaled, ks, freqs, eigvecs = read.read_phonopy(file_eigenvectors, tot_atoms_uc)
Ruc, R0 = read.read_SPOSCAR(file_initial_conf, N1N2N3, N)                       #rhombo or avg R0



Rt = np.loadtxt(file_trajectory)[:,1:]
Num_timesteps = int(len(Rt[:,0]))
print(' Number of timesteps of simulation: ', Num_timesteps, '\n')
tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
dt_ps = tall[1]-tall[0]
meta = int(Num_timesteps/2)
##Vt = np.gradient(Rt,dt_ps,axis=0)  
Vt = np.diff(Rt,axis=0)/dt_ps*np.sqrt(masses)/np.sqrt(3*(N))
    

##this is for the total C(t)
##t_tot, C_tot, freq_tot, G_tot = corr(tall,Vt,tau, ' ')
##print(' Average total kinetic energy per dof: ', 1/2*C_tot[0]*cH, ' Hartree')
##print(' Kinetic energy per dof according to eqp thm: ', 1/2*kbH*T, ' Hartree')
##print('\t\t ratio: ', np.round((1/2*C_tot[0]*cH)/(1/2*kbH*T)*100,2), ' %\n')

print(' Done. Performing decomposition...\n')

namedir = plot.create_folder(system)
anis = list(range(tot_atoms_uc*3))

for i in range(Nqpoints):
    eigvec = eigvecs[i]
    freq_disp = freqs[i]
    k = ks[i]
    print('\t kpoint ',k)
    
    #Creating the collective variable based on the k point
    Vcoll = np.zeros((Num_timesteps-1,tot_atoms_uc*3),dtype=complex)  
    for j,h,l in zip(range(tot_atoms_uc*3),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),tot_atoms_uc)):
        vels = np.array(Vt[:,h+l:h+N1N2N3*3:3],dtype=complex)
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(1j*np.dot(poss,k)))
        Vcoll[:,j] = np.sum(x,axis=1)
    Tkt = Vcoll
    eigvecH = np.conjugate(eigvec.T)
    Qkt = np.dot(eigvecH,Tkt.T).T#.reshape(Num_timesteps,1)
    
    
    t, C, freq, G = corr(tall,Tkt,tau, ' ')
    Ztot = np.sqrt(np.conjugate(G)*G).real*cev/(kbev*T)
    print('\t\t kinetic energy of this kpoint: ',1/2*C.real[0]*cH, ' Hartree')
    print('\t\t kinetic according to eqp thm: ',1/2*kbH*T, ' Hartree')
    print('\t\t ratio: ', np.round((1/2*C.real[0]*cH)/(1/2*kbH*T)*100,2), ' %')
    
    
    t_proj, C_proj, freq_proj, G_proj = corr(tall,Qkt,tau, 'projected')
    Z = np.sqrt(np.conjugate(G_proj)*G_proj).real*cev/(kbev*T)
    meta = int(len(t)/2)

    for n in range(tot_atoms_uc*3):
#        plot.plot(freq[0:meta],Z[0:meta],'Spectrum of '+str(k))
#        anis[n] = plot.plot_with_ani(freq[0:meta],Z[0:meta,n],Ztot[0:meta], k, eigvec[:,n],freq_disp[n],n,Ruc,file_eigenvectors,masses_for_animation)
        plot.save_proj(freq[0:meta],Z[0:meta,n],Ztot[0:meta], qpoints_scaled[i], Ruc, eigvec[:,n],freq_disp[n],n,namedir,masses_for_animation)
    
    print()






