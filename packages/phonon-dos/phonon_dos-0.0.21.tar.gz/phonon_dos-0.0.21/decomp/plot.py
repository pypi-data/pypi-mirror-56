#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:56:19 2019

@author: gabriele
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy as np
import os

def from_band(ks):
    Points = {'$\Gamma$':[0,0,0],'X':[0.5,0,0],'M':[0.5,0.5,0],'R':[0.5,0.5,0.5],'boh':[0,0.5,0], 'Z':[0,0,0.5]}
    x_labels = []
    for kpoint in ks:
        a = 0
        for element in Points.items():
            a = a + 1
            if (np.array_equal(kpoint , element[1])):
                x_labels.append(element[0])
                break
            if (a==len(Points.items())):
                x_labels.append(' ')
    return x_labels


def animate(frames,plot):
    plot.collections = []
    
#    Baiimag, Tiiimag, Oiimag = frame_BaTiO3[0:8*3], frame_BaTiO3[8*3:9*3], frame_BaTiO3[9*3::]
    plot._offsets3d = (frames[0::3], frames[1::3], frames[2::3])

#    plotBaimag._offsets3d = (Baiimag[0::3],Baiimag[1::3],Baiimag[2::3])
#    plotTiimag._offsets3d = (Tiiimag[0::3],Tiiimag[1::3],Tiiimag[2::3])
#    plotOimag._offsets3d = (Oiimag[0::3],Oiimag[1::3],Oiimag[2::3])
    return

def plot_eigvec(Ruc, n_uc, k,eigvec,freq, ax, fig):
    t = np.arange(0,100,1)
    
    Rucxyz = np.repeat(Ruc,3,axis=0)
    EIGs = eigvec
    
    exp1 = np.exp(1j*np.sum(np.multiply(k,Rucxyz),axis=1)) #this multiplies by the phase factor exp(i k.R)
    #exp2 = np.exp(1j*freq*t).reshape(1,len(t))
    exp2 = np.sin(t).reshape(1,len(t))
    EIG_exp = np.multiply(EIGs,exp1)
    ut = np.dot(EIG_exp.reshape(len(EIGs),1),exp2)
        
    Rt = Ruc.flatten().reshape(len(EIGs),1) + np.real(ut)
    Rt2 = Ruc.flatten().reshape(len(EIGs),1) + np.imag(ut)

    plot = ax.scatter(Rt[0::3,0], Rt[1::3,0], Rt[2::3,0], s=100)
    ani = animation.FuncAnimation(fig,animate,frames=Rt.T,fargs=(plot,))
    return ani

def plot(x,y,title):
    fig,ax = plt.subplots()
    ax.plot(x,y)
    ax.set_xlabel('Frequency [Thz]')
    ax.set_title(title)
    plt.show()
    return

def plot_eigvec_noani(Ruc, n_uc, k,eigvec,freq, ax,fig):
    t = np.arange(0,100,1)
    
    Rucxyz = np.repeat(Ruc,3,axis=0)
    
    eigvec = eigvec.real
    Ruc = Ruc.flatten()
    
    ax.scatter(Ruc[0::3], Ruc[1::3], Ruc[2::3], alpha=0.5, s=100)
    ax.quiver(Ruc[0::3], Ruc[1::3], Ruc[2::3], eigvec[0::3], eigvec[1::3], eigvec[2::3], color='black')
    return 

def plot_with_ani(x,y,ytot, k,eigvec,freq,n,Ruc,eigname,masses):
    fig,ax = plt.subplots()
    graph1, = ax.plot(x,y,label='mode-projected DOS')
    graph2, = ax.plot(x,ytot,'--',label='total DOS')
    ax.set_xlim(left=-1,right=30)
    ax.set_xlabel('Frequency [Thz]')
    ax.set_title('Spectrum of mode n. '+str(n)+' kpoint '+str(k))
    
    ax1 = ax.twiny()
    ax1.set_xlabel('Frequency [cm$^{-1}$]')
    ax1.plot(x*33.35641,-np.ones(len(x)),c='white',linewidth=0,label='')
    ax1.set_xlim(-1*33.35641,30*33.35641)

    
    
    graph3, = ax.plot(np.repeat(freq,100),np.linspace(0,ytot.max(),100),':' ,c='r', label='freq from dispersion')
    plt.legend(handles=[graph1, graph2, graph3], loc=2)
    
    
    ax2 = fig.add_axes([0.5, .5, .3, .3],projection='3d')
    ax2.set_title(str(eigname)+'\nfrequency: '+str(freq))
    ampl = 10
    eigvec = eigvec/np.sqrt(masses)*ampl
    ani = plot_eigvec(Ruc, 1, [0,0,0],eigvec,freq,ax2,fig)
    
    
    print('Mode frequency: ', freq, '\n')
    print('Eigenvector components:')
    print(np.round(np.reshape(np.real(eigvec),np.shape(Ruc)),2))
    print()
    print('Imaginary part:')
    print(np.round(np.reshape(np.imag(eigvec),np.shape(Ruc)),2))
    print()
    
    plt.show()
    return ani

def save_proj(x,y,ytot, k,Ruc, eigvec,freq,n,namedir,masses):
    plt.ioff()
    fig,ax = plt.subplots()
    graph1, = ax.plot(x,y,label='mode-projected DOS')
    graph2, = ax.plot(x,ytot,'--',label='total DOS')
    ax.set_xlabel('Frequency [Thz]')
    ax.set_ylabel('DOS [kB T * ps]')
    fig.suptitle('Spectrum of mode n. '+str(n)+' kpoint '+str(k))
    
    ax1 = ax.twiny()
    ax1.set_xlabel('Frequency [cm$^{-1}$]')
    ax1.plot(x*33.35641,-np.ones(len(x)),c='white',linewidth=0,label='')
    ax1.set_xlim(-1*33.35641,30*33.35641)
    
    
    graph3, = ax.plot(np.repeat(freq,100),np.linspace(0,ytot.max(),100),':' ,c='r', label='freq from dispersion')
    #graph3, = ax.axvline(x=freq,  ymin=0.05, ymax=1, c='blue',linestyle=':', label='freq from dispersion')
#    print('Mode frequency: ', freq, '\n')
#    print('Eigenvector components:')
#    print(np.round(np.reshape(np.real(eigvec),(5,3)),2))
#    print()
#    print('Imaginary part:')
#    print(np.round(np.reshape(np.imag(eigvec),(5,3)),2))
#    print()
#    print()
    name_current_dir = namedir+'/'+str(k)
    try:
        os.mkdir(name_current_dir)
        
    except FileExistsError:
        a = 1
    ax.set_ylim(bottom=-10,top=100)
    ax.set_xlim(left=-1,right=30)
    plt.legend(handles=[graph1, graph2, graph3])
    plt.subplots_adjust(top=0.85)
    
    if(np.allclose(k,[0,0,0])):
        ax2 = fig.add_axes([0.7, 0.4, .2, .2],projection='3d')
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.set_zticks([])
        #ax2.xticks([])
    #    ax2.set_title('frequency: '+str(freq))
        ampl = 10
        eigvec = eigvec/np.sqrt(masses)*ampl
        ggraph = plot_eigvec_noani(Ruc, 1 ,[0,0,0],eigvec,freq, ax2, fig)
    
    fig.savefig(name_current_dir+'/proj_'+str(k)+'mode'+str(n)+'.pdf')
    plt.close(fig)
    return 
    
def plot_k(f, data, ks,freqs, title=''):
    """
    Plotting the dispersion from MD and from phonon theory.
    
    Variables:
        f = array of the frequencies [Thz] 
        data = matrix with spectra from all k points: shape = (timesteps,N)
        indexes = list of all kpoints
        freqs = frequencies from phonopy
    """
    fig,ax = plt.subplots()
    plt.suptitle('Spectrum via MD and phonon theory')
    #ax.set_title(title)
    ax.set_ylabel('[Thz]')
    N = len(data[0,:])
    offset = np.zeros(N) + f[0]
    df = f[1]-f[0]
    k = np.linspace(0,1,N)
    dk = k[1] - k[0]
    
    indexes = from_band(ks)

    #norm = [plt.cm.colors.Normalize(vmax=abs(data[0::1,l]).max(), vmin=-abs(data[0::1,l]).min()) for l in range(len(data[0,:]))]
    norm = plt.cm.colors.Normalize(vmax=100, vmin=0)
    
    for j in range(len(data[0::1,0])):
        ax.bar(k, np.repeat(df,N), bottom=offset-df/2,  color=plt.cm.Blues(norm(data[j,:])), tick_label=indexes, align='center', width=dk, alpha=None)
        offset = offset + df
        
    ax2 = plt.twinx()
    ax2.set_ylabel('[Thz]')
    for j in range(14):
        ax2.scatter(k,freqs[:,j], c='b', marker='x', s=100)
    ax2.scatter(k,freqs[:,14], c='b', marker='x', s=100, label='freq from dispersion')
    
        
    ax2.get_shared_y_axes().join(ax, ax2)
    plt.ylim([f[0], f[-1]])
    plt.legend()
    plt.show()
    fig.savefig('spectrum.pdf')
    return
    









































def corr_j(tcorr,X,dt,masses):
    Nsteps = len(tcorr)
    N = np.size(X[0])
    sigma2 = np.var(X,axis=0)
    C = []
    for i in range(Nsteps):
        X_i = X[i::,:]
        Xjj = np.concatenate((X[i::,:],X[0:i,:]))#[i::,:]
        a = np.multiply(np.conjugate(X),Xjj)
        b = 1/(Nsteps) * np.sum(a,axis=0)#/sigma2
        c = np.multiply(b,masses)
        d = 1/N*np.sum(c)
        C.append(d)
    C = np.array(C)
    freq = np.fft.fftfreq(Nsteps,d=dt)
    Z = np.fft.fft(C,axis=0)
    return C, freq, Z

def corr_jaa(tall,X,dt,masses):
    M = len(tall)
    tau = 1000
    tmax = M - tau
    t = np.arange(0,tau)*dt
    N = np.size(X[0])   
    X0 = X[0:tau,:]
    C = []
    for n in range(tau):
        A = []
        for m in range(tmax):
            xj = X[m,:]
            xjj = X[m+n,:]
            a = np.multiply(xj,xjj)
            A.append(a*masses)
        A = np.array(A)
        Cn = np.average(A,axis=0)
        C.append(np.average(Cn))
    C = np.array(C)
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z
    
    

def create_folder(system,prefix=''):
    flag = ''
    try:
        namedir = prefix+'phonDOS_'+system
        os.mkdir(namedir)
        flag = 'created'
    except FileExistsError:
        if(flag=='created'):
            bbb = 1
        else:
            number_of_folders = len(np.sort([x[1] for x in os.walk(prefix+'.')][0]))
            print('Folder '+namedir+' already exists. Creating phonDOS_'+str(system)+'_'+str(number_of_folders))
            namedir = namedir+'_'+str(number_of_folders)
            os.mkdir(namedir)
    return namedir
    
    
#this is if you have the velocities instead of positions    
#Vt = np.loadtxt(file_trajectory)[:,1:]*np.sqrt(masses)/np.sqrt(3*N)#/(2.418884254*1e-05)
#Num_timesteps = int(len(Vt[:,0]))
#print(' Number of timesteps of simulation: ', Num_timesteps, '\n')
#tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
#dt_ps = tall[1]-tall[0] 

#eigvec_exp = np.array([0,0,0,0,0,0.5,0,0,-0.9,0,0,-0.6,0,0,0.6])
#a = np.array([0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1])  

#    print('\t\t sum of projected: ',1/2*np.sum(C_proj[0].real)*cH, ' Hartree')
