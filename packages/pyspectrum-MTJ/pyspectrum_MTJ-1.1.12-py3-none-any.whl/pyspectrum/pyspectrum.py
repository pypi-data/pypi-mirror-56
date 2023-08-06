# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 18:16:45 2019

SPECTRUM CLASS

@author: mjaszczykowski
"""
import matplotlib.pyplot as plt # plotting
import numpy as np # methamatical operations
import pandas as pd
import os, glob # file name extraction
import struct   # reading floats
from scipy.optimize import curve_fit # curve fit 

class spectra_analyzer:
    '''
    Designed to read UV-VIS spectra and process them.
    
    Supported format files:
        - .dsp
        - .dat
    '''
    recipe_file = "recipes.csv" 
    
    def __init__(self):
        self.load_recipes()
    
    def load_recipes(self):
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.recipes = pd.read_csv(root_path + "/" + self.recipe_file)
        
    def save_recipes(self):
        ''' function saves current recipes file overwriting existing one '''
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.recipes.to_csv(root_path + "/" + self.recipe_file, index=False)
        
    def print_recipes(self):
        df = self.recipes["name"]
        
        print(df.values)
        return  self.recipes
    
    def set_thickness_from_list(self, spectra, d_list):
        '''
            sets thickness from the list
            
            Arguments:
                spectra - [] list of spectra
                d_list  - [] list of thicknesses in um
                
            Returns:
                none
        '''
        for i in range(min(len(spectra), len(d_list))):
            spectra[i].set_thickness(d_list[i])
    
    def _tsallis_double(self, l, q, W1, lc1, A1, W2, lc2, A2):
        return  A1 * (1 + (2**(q-1) -1) * ((l - lc1) / W1)**2)**(-1/(q-1)) + A2 * (1 + (2**(q-1) -1) * ((l - lc2) / W2)**2)**(-1/(q-1)) 

    def _tsallis_single(self, l, q, W, lc, A):
        return A * (1 + (2**(q-1) -1) * ((l - lc) / W)**2)**(-1/(q-1))

    def fit_peak(self, sp, defect, show=False):
        # if defect doesn't exist raise exception
        if not defect in self.recipes["name"].values:
            raise Exception("Defect {} doesn't exist".format(defect))
        
        r = self.recipes.loc[self.recipes["name"] == defect].to_dict("list")
        
        df = pd.DataFrame()
        df["X"] = sp.X
        df["Y"] = sp.Y
        
        df = df.loc[(df["X"] <= (r["b"][0]+sp.step)) & (df["X"] >= r["a"][0])]
        
        # baselineing with polynomial of order n
        df_left = df.loc[df["X"] <= (r["a"][0] + r["nL"][0] + sp.step)]
        df_right = df.loc[df["X"] >= (r["b"][0] - r["nR"][0] - sp.step)]
                    
        df_baseline = pd.concat((df_left, df_right))
        
        coef = np.polyfit(df_baseline["X"], df_baseline["Y"], r["p order"][0])
        f = np.poly1d(coef)
        
        # substracy baseline
        df["Y"] -= f(df["X"])
        
        # some fitting variables
        width = r["b"][0]-r["a"][0]
        middle = (r["b"][0]+r["a"][0]) / 2.0
        amp_max = np.max(df["Y"])
        
        # check if it has single or double ZPL peak
        if r["double ZPL"][0] == False:
            lower = [1.0, # q
                    0, # peak width W
                    r["a"][0], # peak center
                    0] # amplitude
        
            upper = [5.0, # q
                    r["b"][0]-r["a"][0], # peak width W
                    r["b"][0], # peak center
                    2*np.max(df["Y"])] # amplitude
            
            initial_guess = [1.5, 0.5, middle, amp_max]
            model = self._tsallis_single
        else: 
            lower = [1.0, # q1
                     
                    -1.0, # peak1 width W1
                    r["a"][0], # peak1 center l1
                    0, # amplitude A1
                     
                    -1.0, # peak2 width W2
                     r["a"][0], # peak2 center l2
                    0] # amplitude A2
        
            upper = [5.0, # q1
                     
                    width, # peak1 width W1
                    r["b"][0], # peak1 center l1
                    amp_max, # amplitude A1
                     
                    r["b"][0], # peak2 center l2
                    width, # peak2 width W2                
                    amp_max] # amplitude A2
             
            initial_guess = [1.5, 0.5, middle - 1.0, amp_max ,-0.5, middle + 1.0, amp_max / 2]
            model = self._tsallis_double
                     
        popt, pov = curve_fit(model, df["X"], df["Y"],  method="trf", p0=initial_guess)
        df["Y fit"] = model(df["X"], *popt)
        if show:        
           
            plt.plot(df["X"], df["Y"], "b.", markersize=2, label="spectrum")
            plt.plot(df["X"], df["Y fit"], "r--", label="fit")
       
            # plot formatting
            plt.grid()
            plt.title(sp.name + " " + defect)
            plt.xlabel("Wavelenght $\lambda$ [nm]")
            plt.ylabel("Absorbance [1]")
            plt.legend()
            plt.show()
        
        # Goodness of fit R2
        SSres = np.sum((df["Y"] - df["Y fit"])**2)
        y_avg = np.average(df["Y"])
        SStot = np.sum((df["Y"] - y_avg)**2)
        
        R2 = 1 - SSres / SStot
        
        model_values = pd.DataFrame()
        fields = ["q", "W1", "lc1", "A1", "W2", "lc2", "A2"]
        
        
        model_values.loc[0, "name"] = sp.name
        model_values.loc[0, "defect"] = r["name"][0]
        for i in range(len(fields)):
            model_values[fields[i]] = np.NaN
        
        for i in range(len(popt)):
            model_values.loc[0,fields[i]] = popt[i]
        
        model_values["R2"] = R2
        
        return model_values
    
    def _color_R2(self, val):
        if val <= 0.8:
            color = "yellow"
        else:
            color = "white"
        return 'background-color: %s' % color
        
    def fit_peaks_batch(self,spectra, defects, show=False):
        df = pd.DataFrame()
        
        for s in spectra:
            for d in defects:
                df = df.append(self.fit_peak(s, d, show=show), sort=False)
        
        df = df.reset_index(drop=True)     
        
        return df
    
    def format_peaks_batch(self, df):
        s = df.style.applymap(self._color_R2, subset=["R2"])
            
        df['q'] = df['q'].map('{:,.3f}'.format)
        df['lc1'] = df['lc1'].map('{:,.1f}'.format)
        df['lc2'] = df['lc2'].map('{:,.1f}'.format)
        df['W1'] = df['W1'].map('{:,.2f}'.format)
        df['W2'] = df['W2'].map('{:,.2f}'.format)
        #df['R2']= df['R2'].map('{:,.2f}'.format)
        df['A1'] = df['A1'].map('{:,.3f}'.format)
        df['A2']= df['A2'].map('{:,.3f}'.format)
        
        return s
    
    def integrate(self, spect, recipe_name, show=False):
        '''
            integrates spectrum with recipe passed as an argument
            
            Arguments:
                spect - spectrum instance to be intagrated
                reciepe_name - [string] name of the recipe to be applied (eg "NV-") to get list of all recipes use "print recipes"
                show [optional] - [boolean] True plots the part of spectrum containing defect and baseline
                
            Returns:
                intagrated absorbtion [float] [meV/cm]
        '''
        
        # check if reciepe exists
        if (not recipe_name in self.recipes["name"].values):
            raise Exception("Reciepe {} doesn't exist".format(recipe_name))
        
        X = spect.X.copy()
        Y = spect.Y.copy()
        step = spect.step
        
        # reciepe as dictionnary
        r = self.recipes.loc[self.recipes["name"] == recipe_name].to_dict("list")
        
        # exttract part of the spectrum from a to b
        i1 = int((r["a"] - X[0])/step)
        i2 = int((r["b"] - X[0])/step)
        
        X = X[i1:i2+1]
        Y = Y[i1:i2+1]
        
        # baselineing with polynomial of order n
        X_left = X[X <= float(r["a"][0] + r["nL"][0] + 0.001)]
        X_right = X[X >= float(r["b"][0] - r["nR"][0] - 0.001)]
                
        Xbaseline = np.concatenate((X_left, X_right))
        Ybaseline = np.concatenate((Y[:len(X_left)], Y[-len(X_right):])) 
        coef = np.polyfit(Xbaseline, Ybaseline, r["p order"][0])
        
        f = np.poly1d(coef)
        
        if show:
            # plot
            fig, ax = plt.subplots()
            ax.plot(X, Y, "b.", label= spect.name )
            ax.plot(X, f(X), "r-", label="baseline p(lambda) order {}".format(r["p order"][0]))
        
            # formatting
            ax.set_title(spect.name + " " + recipe_name)
            ax.set_xlabel("Wave lenght [nm]")
            ax.set_ylabel("Absorbance [1]")
            ax.grid()
            ax.legend()
        
            # show
            plt.show()
        
        # substract baseline
        Y -= f(X)
        
        # X in meV
        # E = hc / lambda
        hc = 1.23984193 # [eVum]
        
        X = 1 / X * hc * 10**6
        
        # integration - method trapezoidal
        S = 0.0
        
        for i in range(0, len(X)-1):
            S += (X[i] - X[i+1]) * (Y[i] + Y[i+1]) * 0.5 
        
        I = np.log(10) / spect.d * S * 10**4
        
        
        c77K = r["c 77K"][0] * I
        c300K = r["c 300K"][0] * I
        
        return (I, c300K, c77K)
    
    def analyze(self,spectra, what, show=False):
        '''
        quantifies few defects for few spectra at once
        results are shown as intagrated absorbtion, concentration at 300K and 77K
        
        Arguments:
            spectra - [] list of spectra
            what    - [string] list of defects eg. ["GR1", "ND1"]
            show    - [boolean] look integrate
        
        Returns:
            table containing the following columns:
            name - name of the sample
            d    - thickness of the sample [um]
            Ia of defect A - integrated absorbtion of defect A
            ...
            In of defect N 
        
        '''
        col = ["name", "d"] + what
        df = pd.DataFrame(columns=col)
        
        for i in range(len(spectra)):
            df.loc[i, "name"] = spectra[i].name
            df.loc[i, "d"] = spectra[i].d
            for w in what:
                 result = self.integrate(spectra[i],w,show)
                 df.loc[i, w] = result[0] # integareted absorbtion [meV / cm]
                 df.loc[i, "[{}] ppm at 300K".format(w) ] = result[1] # concentration at 300K in ppm
                 df.loc[i, "[{}] ppm at 77K".format(w) ] = result[2]  # concentration at 77K in ppm
                
        return df
    
    def read_dsp_file(self, path):
        '''
        function reads .dsp file
        
        - wavelenght related values are in lines 5, 6, 7 of the file 
        - absorbance values are in lines after line containg following value "#DATA"
          Each line contains one absorbance as ASCI 
        
        Arguments:
            path - string path to the file
        
        Returns 
            spectrum 
        '''
        # open file
        file = open(path, "r")
        
        # file in the list
        lines = []
        for l in file:
            lines.append(l)
        
        # wave lenght lambda [nm]
        # start, end, step of spectra 
        x0 = float(lines[5])
        xn = float(lines[6])
        step = float(lines[7])
        
        # absorbance [1]
        index = lines.index("#DATA\n") + 1

        y_list = []

        for i in range(index, len(lines)):
            y_list.append(float(lines[i]))
        
        # lambda, absorbance
        X = np.arange(x0, xn+step, step)
        Y = np.array(y_list)
        
        # take name from file name
        name, ext = os.path.splitext(path)
        
        s = spectrum(name, X, Y, step)
        return  s
    
    def read_file(self, path):
        '''
        function reads spectrum from supported format file
        
        Arguments:
            path - string path to the file
        
        Returns 
            spectrum 
        '''
        path = path.replace("\\", "/")
        name, ext = os.path.splitext(path)
        
        # check extension
        if ext == ".dat":
            return self.read_dat_file(path)
        
        if ext == ".dsp":
            return self.read_dsp_file(path)
        
        raise Exception("Unknown file format.")
    
    def read_dat_file(self, path):
        '''
        function reads .dat file
        all values are encoded as 4 bit single precision floating numbers
        
        Arguments:
            path - string path to the file
        
        Returns 
            spectrum 
        '''
         # open file 
        file = open(path, "r", encoding="Latin-1")      
        
        # file in the list
        lines = []
        for l in file:
            lines.append(l)        
        
        # XDATA=
        i1 = lines.index("XDATA=\n") + 1
        i2 = lines.index("YDATA=\n")
        i3 = lines.index("OrgXData=\n")
        
        XDATA = ""
        for l in lines[i1:i2]:
            XDATA += l
        
        x_list = []
        for i in range(0,len(XDATA)-1,4):
            x_list.append(struct.unpack("f",bytes(XDATA[i:(i+4)], encoding="Latin-1"))[0])
      
        YDATA = ""
        for l in lines[(i2+1):i3]:
            YDATA += l
        
        y_list = []
        for i in range(0,len(YDATA)-1,4):
            y_list.append(struct.unpack("f",bytes(YDATA[i:(i+4)], encoding="Latin-1"))[0])
            
        X = np.array(x_list)
        Y = np.array(y_list)
        step = X[1] - X[0]
        
        # take name from file name
        name, ext = os.path.splitext(path)
        
        s = spectrum(name, X, Y, step)
        return  s
        
    
    def read_spectra_from_folder(self, folder):
        '''
        reads all the spectra from the folder
        
        Arguments:
            folder - string path to the folder
        
        Returns:
            spectra - list of class spectrum instances
        '''
        folder = folder.replace("\\", "/")
        try:
            os.chdir(folder)
        except:
            print("Folder doesn't exist.")
        
        spectra = []
        for file in glob.glob("*.dsp"):
            spectra.append(self.read_dsp_file(file))
        
        for file in glob.glob("*.dat"):
            spectra.append(self.read_dat_file(file))

        return spectra
    
    def ask_for_thickness(self, spectra):
        '''
        reads a list of spectra and prompts for a thickness value
        thickness value is set for each by set_thickness() method
        
        Arguments:
            spectra - list of spectra
            
        Returns
            thickness_list - list of thicknesses in um
            
            as a by-product excel file is being created.
            Excel table looks like this
            [name] [thickness]
        '''
        # thickness list
        thickness_list = []
        
        df = pd.DataFrame()
        
        for i in range(len(spectra)):
            print(spectra[i].name)
            d = float(input("d = "))
            thickness_list.append(d)
            spectra[i].set_thickness(d)
            df.loc[i,"name"] = spectra[i].name 
            df.loc[i, "thickness"] = d   
            print("\n")
            
        df.to_excel("thickness_list.xlsx")
            
        return thickness_list
                

class spectrum:
    def __init__(self):
        self.name = "Anonymous Sample"
        self.d_flag = False # thickiness has not been set
        self.d = 1000       # default thickness
        self.X = np.empty()
        self.Y = np.empty()
        self.step = 0.0
    
    def __init__(self, _name, _X, _Y, _step):
        self.name = _name
        self.X = _X
        self.Y = _Y
        self.step = _step
        self.d_flag = False # thickiness has not been set
        self.d = 1000       # default thickness
    
    def plot(self, start=0.0, end=0.0, style="b-"):
        '''
        prints a plot of the spectrum
        
        if you don't pass any arguments full spectra will be displyed
        
        Arguments:
            start - beginning of the range [nm]
            end   - end of the range [nm]
            
        Returns:
            none
        '''
        # make a plot
        fig, ax = plt.subplots()
        
        # full spectrum
        if start == 0.0 and end == 0.0:
            ax.plot(self.X, self.Y, style)
        # extract from start to end
        else:
            k = len(self.X)
            X_prim = self.X[self.X >= (start - 0.01)]
            left = k - len(X_prim)
            X_prim = X_prim[X_prim <= (end + 0.01)]
            right = k - left - len(X_prim)
            Y_prim = self.Y[(left):(-right)]
            
            ax.plot(X_prim, Y_prim, style)
        
        
        # formatting
        ax.set_title(self.name)
        ax.set_xlabel("Wave lenght [nm]")
        ax.set_ylabel("Absorbance [1]")
        ax.grid()
        
        # show
        plt.show()

    def set_thickness(self, _d):
        '''sets thickness of the sample [um]'''
        self.d = _d
        self.d_flag = True
