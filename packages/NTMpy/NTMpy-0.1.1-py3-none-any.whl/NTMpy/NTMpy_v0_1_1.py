"""
Created on Thu Oct. 10 2019
Recent changes for the version 0.1.1: 
    1) Insead of giving the input optical penetration depth only give the input 
        of the complex refractive index "n". This is a material parameter, so 
        the input is given in the simulation --> add_layer(.) command. 
        Now "LB" and "TMM" source are initialized almost in the same way
    2) One of the Outputs of sim.run() is T. But now we change it to be a 
        3 dimensional array, with dim0 = time; dim1 = space; dim2 = subsystem
    3) The input for the visual class in the v.contour() function should not be
        a string but just numbers corresponding to different systems.   
@author: Lukas Alber
lukas.alber@fysik.su.se 
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from bspline import Bspline
from bspline.splinelab import aptknt
import time
from matplotlib.animation import FuncAnimation as movie
from tqdm import tqdm #Progressbar

#==============================================================================
class temperature(object): 
        
    def __init__(self): 
        self.plt_points     = 30                    #number of points in x grid
        self.length         = np.array([0,0])       #length of x space,starting from 0
        self.Left_BC_Type   = 1                     #Boundary conditions Default is Neumann
        self.Right_BC_Type  = 1                     #1=> Neumann; 0=> Dirichlet
        self.init           = lambda x: 300+0*x     # initial temperature of probe
        self.n              = np.array([1,1],dtype=complex)       # Initial refractive index air|...|air
        self.conductivity   =  [1]                  #This gets deleted after initialisation
        self.heatCapacity   =  [1]                  #those values are just here to make space
        self.rho            = [1]                   #Actual values are given, when 'addLayer(length, conductivity,heatCapacity,rho)' is executed
        self.collocpts      = 12
        self.setup          = False                 #first time setup to not double calculated
    
    def getProperties(self):                        #to depict the properties of the object
        for i in (self.__dict__): 
            name = str(i)
            value = str(self.__dict__[i])
            print('{:<20}{:>10}'.format( name,value ))
            
    def __repr__(self): 
        return('Temperature')
    #for every layer, a function to calculate the derivative of k(T)        
    def diff_conductivity(self,phi,num_of_material): 
        eps =1e-9
        dc = (self.conductivity[num_of_material](phi+eps)-self.conductivity[num_of_material](phi))/eps
        return(dc)
    #Creating the key matrices for B-splines. Those are A0,A1,A2
    #A0 => Zero derivative; A1 => 1st order derivative.... 
    #We create the matices for every layer, with respective length ect
    #then we put them together to Abig => Boundary and interface conditions are applied here.         
    def Msetup(self):
        #Deleting the ifrst element of the default initialization
        #After creating the element with 'addLayer' we dont need them!
        if not self.setup:
            self.length         = self.length[1:]
            self.conductivity   = self.conductivity[1:]
            self.heatCapacity   = self.heatCapacity[1:]
            self.rho            = self.rho[1:]
            self.setup          = True
        #Length and numper of grid points for each respective layer    
        length          = self.length
        plt_points      = self.plt_points
        num_of_points   = self.collocpts  #Number of points per layer used in the spline for collocation
        order           = 5   #order of the spline
        x               = np.array(np.zeros([np.size(length)-1,num_of_points]))
        x_plt           = np.array(np.zeros([np.size(length)-1,plt_points]))
        knot_vector     = np.array(np.zeros([np.size(length)-1,num_of_points+order+1]))
        basis           = np.array(np.zeros(np.size(length)-1))
        A0h = []; A1h = []; A2h = []; Ch = [];
        LayerMat        = np.array([np.zeros((num_of_points,num_of_points))])
        
        #Create all the big matices A0,A1,A2 & C. C is used to map on a fine mesh in x- space.
        #For every layer we set up splines between the boundaries
        for i in range(0,np.size(length)-1):
            x[i,:]   = np.linspace(length[i], length[i+1] , num_of_points)
            x_plt[i,:]       = np.linspace(length[i], length[i+1] , plt_points)
            knot_vector[i,:] = aptknt(x[i,:], order) #prepare for Spline matrix
            basis    = Bspline(knot_vector[i,:],order)
            A0hinter = basis.collmat(x[i,:], deriv_order = 0); A0hinter[-1,-1] = 1
            A1hinter = basis.collmat(x[i,:], deriv_order = 1); A1hinter[-1] = -np.flip(A1hinter[0],0)
            A2hinter = basis.collmat(x[i,:], deriv_order = 2); A2hinter[-1,-1] = 1
            Chinter  = basis.collmat(x_plt[i,:], deriv_order = 0); Chinter[-1,-1] = 1
            LayerMat = np.append(LayerMat,np.array([np.dot(A2hinter,np.linalg.inv(A0hinter))]),axis = 0)
            A0h      =  np.append(A0h,A0hinter)
            A1h      =  np.append(A1h,A1hinter)
            A2h      =  np.append(A2h,A2hinter)
            Ch       = np.append(Ch,Chinter)
        #Reshape the long string of appended Matrix, such that
        #rows: x-points; colums: i´th basis spline
        LayerMat = LayerMat[1:,:,:]
        A0h = np.reshape(A0h, (-1,num_of_points)) 
        A1h = np.reshape(A1h, (-1,num_of_points))
        A2h = np.reshape(A2h, (-1,num_of_points))
        Ch  = np.reshape(Ch,(-1,num_of_points)) 
        #Ch => More points in x, but same number of basis splines
        #Clearing the interface points, to not double count 
        N               = num_of_points 
        plp             = plt_points
        interfaces      = np.shape(x)[0]-1
        sizeA           = np.shape(x)[0]*N-interfaces
        sizeCb          = np.shape(x)[0]*plp-interfaces
        Abig            = np.zeros([sizeA,sizeA]) 
        A1b             = np.zeros([sizeA,sizeA])
        A2b             = np.zeros([sizeA,sizeA])
        Cb              = np.zeros([sizeCb,sizeA])
        #Clearing the double counts from the space grid 
        xflat = x.flatten()
        x_plt_flat = x_plt.flatten()
        #index of double counts        
        doublec = np.array([np.arange(1,len(length)-1)])*N
        doublec_plt = np.array([np.arange(1,len(length)-1)])*plp
        xflat = np.delete(xflat,doublec)
        x_plt_flat = np.delete(x_plt_flat,doublec_plt)
        #Filling the big matrices.
        startA = 0; endA = N-1
        startC = 0; endC = plp-1 
        for i in range(0,interfaces+1):
            Abig[startA:endA,startA:endA+1]  = A0h[startA+i:endA+i,:]   
            A1b[startA:endA+1,startA:endA+1] = A1h[startA+i:endA+i+1,:]
            A2b[startA:endA+1,startA:endA+1] = A2h[startA+i:endA+i+1,:]
            Cb[startC:endC+1,startA:endA+1]  = Ch[startC+i:endC+i+1,:] 
            startA += N-1; endA += N-1
            startC += plp-1; endC += plp-1
            
        #Create A00 with no interface condition to correctly compute phi in loop
        #The copy needs to be done befor interface conditions are applied in Abig
        A00 = Abig.copy() 
        A00[-1,-1] = 1;
        #Here we make init, conductivity & capacity all functions, in case they are
        # given as integeres or floats. Also thorw warinings if not every layer has a
        # conducitvity or capacity ============================================
        #Making init a function, in case it is given as a scalar
        if np.size(self.init) == 1 and isinstance(self.init,(int,float)):
            dummy   = self.init                                      
            self.init    = lambda x: dummy + 0*x        
        if len(length) > 2: #multilayer case
            if len(length)-1 !=(  len(self.heatCapacity) & len(self.conductivity) ): 
                print('--------------------------------------------------------')
                print('The number of different layers must match the number of number of' \
                      'inputs for Conductivity, heatCapacity, rho.')
                print('--------------------------------------------------------')
            if np.size(self.conductivity) is not interfaces+1:
                print('--------------------------------------------------------')
                print('Not every Layer has been given a conductivity function' \
                      'Adjust your input of the conductivity functions with respect to the layers.')
                print('--------------------------------------------------------')
            if np.size(self.heatCapacity) is not interfaces+1:
                print('--------------------------------------------------------')
                print('Not every Layer has been given a heatCapacity function value.'\
                      'Adjust your input of the heatCapacity functions with respect to the layers.')   
                print('--------------------------------------------------------')
        #Make Functions in case heat capacity/conductivity are given as variables
        if (all(self.conductivity) or all(self.heatCapacity) or all(self.init)) == False:
            print('No heatCapacity, conductivity or initial function given.')
            print('--------------------------------------------------------')
            #make the conductivity always a function
        if len(length) >2 or np.size(self.conductivity)>=2:
            for j in list(range (0,np.size(self.conductivity))):
                if isinstance(self.conductivity[j],(int,float,list)) :  
                    dummy3 = self.conductivity[j]
                    self.conductivity[j] = (lambda b: lambda a: b+0*a)(dummy3) 
            #make the conductivity always a function 
            for j in list(range (0,np.size(self.heatCapacity))):  
                if isinstance(self.heatCapacity[j],(int, float,list)) : 
                    dummy4 = self.heatCapacity[j]
                    self.heatCapacity[j] = (lambda b: lambda a: b+0*a)(dummy4)  
        else : 
            if isinstance(self.conductivity[0],(int,float)):
                dummy1 = self.conductivity
                self.conductivity = [lambda phi: dummy1 + 0*phi]
               
            if isinstance(self.heatCapacity[0],(int,float)):
                dummy2 = self.heatCapacity
                self.heatCapacity = lambda phi: dummy2 + 0*phi
                self.heatCapacity = [self.heatCapacity]          
        #End of function creation for init(x), conductivity[l](phi), heatCapacity[l](phi)
        # with respect to every layer 'l' =====================================
        def interconditions(phi,interfaces):
            N = num_of_points
            end_i = N-1
            intercondiL = np.zeros((interfaces,N)) 
            intercondiR = np.zeros((interfaces,N)) 
            for i in range(interfaces): 
                intercondiL[i] = self.conductivity[i](phi[end_i])*A1h[end_i+i]
                intercondiR[i] = self.conductivity[i+1](phi[end_i])*A1h[end_i+i+1]
                end_i += N-1
            return(intercondiL,intercondiR) 
        #Initial Electron temperature   
        initphi = self.init(xflat)       
        initphi_large = self.init(x_plt_flat)
        intercon = interconditions(initphi,interfaces)           
        #filling up Abig wiht the interface condition in the middle of the grid
        start_i = 0; end_i = N-1  
        for i in range(0,interfaces): 
            Abig[end_i,start_i:end_i]    =  intercon[0][i][:-1]#Lhs interface flow
            Abig[end_i,end_i+1:end_i+N]  = -intercon[1][i][1:]#Rhs interface flow
            Abig[end_i,end_i]            = intercon[0][i][-1] -intercon[1][i][0]
            start_i += N-1; end_i += N-1
        Abig[-1,-1] = 1 #to correct Cox algorithm        
        #Now Matrix Abig is completed and interface condition is applied.
        #Treating 2 types of boundary conditions: 0=> Dirichlet; 1=> Neumann, 
        # where 0´th and -1´th row need to be first order derivatives for flux.
        neumannBL = A1b[0].copy(); 
        neumannBR = A1b[-1].copy(); 
        if self.Left_BC_Type  == 1: Abig[0]  = -neumannBL
        if self.Right_BC_Type == 1: Abig[-1] = neumannBR    
        #Clear for BC! (first and last row need to be cleared to correctly apply BC)         
        A1b[0]     = 0; A2b[0]     = 0;
        A1b[-1]    = 0; A2b[-1]    = 0;
        #Get inital c coefficients for splines using init (=phi_init)
        c = np.dot(np.linalg.inv(A00),self.init(xflat))
        #Passed on properties to the simulation class
        return(c,A00,Abig,A1b,A2b,Cb,length,N,plp,xflat,x_plt_flat,initphi_large,interfaces,LayerMat,A1h)
        
    def addLayer(self,L,refind,conductivity,heatCapacity,rho):
        """
        Add parameters of every layer: 
        (length,conductivity[electron,lattice,spin],heatCapacity[electron, lattice, spin],density, coupling[E-L,L-S,S-E])
        The units in SI are: 
            [length]        = m
            [n]             = complex refractive index
            [conductivity]  = W/(mK)
            [heatCapacity]  = J/(m^3K^2)
            [density]       = kg/m^3
            [Coupling]      = W/(m^3K)
        """
        self.length = np.append(self.length,self.length[-1]+L)
        #Squeez in the refracitve index between two layers of air: air|...|...|air
        self.n      = np.concatenate((self.n[:-1],[refind],[self.n[-1]])) 
        self.conductivity.append(conductivity)
        self.heatCapacity.append(heatCapacity)
        self.rho    = np.append(self.rho,rho)
        
#==============================================================================        
class simulation(object): 
    
    def __init__(self,num_of_temp,source): 
        self.temp_data          = temperature() #import the temperatuer object
        self.num_of_temp        = num_of_temp   #1 if only electron temp. 2 if electron and lattice temp.
        self.start_time         = 0             #starting time (can be negative)
        self.final_time         = 10            #time when simulation stops
        self.time_step          = []            #can either be given or is automatically calculated in stability
        self.left_BC            = 0             #function or constant what the boundary condition 
        self.right_BC           = 0             #on the left or right side of the problem is.
        self.stability_lim      = [270,3000]
        self.temp_data_Lat      = []            #Default case is without lattice temperature
        self.temp_data_Spin     = []
        if num_of_temp >= 2:                    #if Lattice temp is considered
            self.temp_data_Lat  = temperature() #in case also a lattice module is given
            self.coupling       = []            #Coupling between Electron and Lattice system
            self.left_BC_L      = 0             #Setting the default to zero flux
            self.right_BC_L     = 0             #The BC type is indicated in the temperature class
        if num_of_temp == 3:                    #In case spin coupling is also considered
            self.temp_data_Spin = temperature()
            self.coupling_LS    = []            #Coupling between Lattice and Spin system
            self.coupling_SE    = []            #Coupling between Electron and Spin system
            self.left_BC_S      = 0             #Default zero flux Neumann boundary conditions
            self.right_BC_S     = 0             #On both sides
        self.source             = source        #object source can be passed on
    #to depict the properties of the object   
    def getProperties(self): 
        for i in (self.__dict__): 
            name = str(i)
            value = str(self.__dict__[i])
            print('{:<20}{:>10}'.format( name,value ))
            
    def __repr__(self): 
        return('Simulation')
    
    def changeInit(self,system,function): 
        """
        Change the initial condition of every system. 
        .changeInit(system,function) has 2 input arguments
        system      --> string "electron" or "lattice" or "spin"
        function    --> a function handle or a number defining the value of the
                        system at t=0 over the entire domain x. 
        """
        if (system == "electron") or (system == "Electron") or (system == 1): 
            self.temp_data.init = function
        if (system == "lattice") or (system == "Lattice") or (system == 2):
            self.temp_data_Lat.init = function
        if (system == "spin") or (system == "Spin") or (system == 3):
            self.temp_data_Spin = function
            
    def changeBC_Type(self,system,side,BCType):
        """
        Function to change the type of the boundary condition on the left and 
        right side of the material, for every system, "electron", "lattice", "spin"
        respectively. 
        .changeBC_Type(system,side,BCType) has 3 inputs, all of them are strings. 
        system  --> "electron" or "lattice" or "spin". Altenatively: "1", "2", "3"
        side    --> "left" or "right"
        BCType  --> "dirichlet" fixing the value/ "neumann" fixing the flux.
        """
        if (system == "electron") or (system == "Electron") or (system == 1):
            if side == "left": 
                if (BCType == "dirichlet") or (BCType == 0):  
                    self.temp_data.Left_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data.Left_BC_Type  = 1 
            if side == "right": 
                if (BCType == "dirichlet") or (BCType == 0): 
                    self.temp_data.Right_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data.Right_BC_Type  = 1
        if (system == "lattice") or (system == "Lattice") or (system == 2):
            if side == "left":
                if (BCType == "dirichlet") or (BCType == 0):  
                    self.temp_data_Lat.Left_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data_Lat.Left_BC_Type  = 1 
            if side == "right": 
                if (BCType == "dirichlet") or (BCType == 0): 
                    self.temp_data_Lat.Right_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data_Lat.Right_BC_Type  = 1
        if (system == "spin") or (system == "Spin") or (system == 3):
            print("Line 326 Spinsystem")
            if side == "left":
                if (BCType == "dirichlet") or (BCType == 0):  
                    self.temp_data_Spin.Left_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data_Spin.Left_BC_Type  = 1 
            if side == "right": 
                if (BCType == "dirichlet") or (BCType == 0): 
                    self.temp_data_Spin.Right_BC_Type  = 0 
                if (BCType == "neumann") or (BCType == 1): 
                    self.temp_data_Spin.Right_BC_Type  = 1
                    
    def changeBC_Value(self,system,side,function):
        """
        Function to change the value of the boundary condition on the left and 
        right side of the material, for every system, "electron", "lattice", "spin"
        respectively. 
        .changeBC_Value(system,side,function) the first two are strings, 
        the last one is a function handle or a number. 
        system  --> "electron" or "lattice" or "spin"| Altenatively: "1", "2", "3"
        side    --> "left" or "right"
        function--> function or number fixing the value on the boundaries for all times.
        """
        if (system == "electron") or (system == "Electron")  or (system == 1):
            if side == "left":  
                self.left_BC        = function 
            if side == "right": 
                self.right_BC       = function
        if (system == "lattice") or (system == "Lattice") or (system == 2):
            if side == "left":  
                self.left_BC_L      = function
            if side == "right": 
                self.right_BC_L     = function
        if (system == "spin") or (system == "Spin") or (system == 3):
            if side == "left":
                self.left_BC_S      = function 
            if side == "right": 
                self.right_BC_S     = function
                
    def addSubstrate(self,name = "silicon"): 
        """
        Automatically create in the silicon substrate using input
        parameters, mostly taken from:
            Contribution of the electron-phonon interaction 
            to Lindhard energy partition at low energy in Ge and Si 
            detectors for astroparticle physics applications, by 
            Ionel Lazanu and Sorina Lazanu
        Note: Refractive index for 400 nm light!
        """
        if (name == "Silicon") or (name =="silicon") or (name =="Si"):
            k_el_Si      = 130#W/(m*K);
            k_lat_Si     = lambda T: np.piecewise(T,[T<=120.7,T>120.7],\
                                                  [lambda T: 100*(0.09*T**3*(0.016*np.exp(-0.05*T)+np.exp(-0.14*T))), 
                                                   lambda T: 100*(13*1e3*T**(-1.6))])
            rho_Si       = 2.32e3#kg/(m**3)
            C_el_Si      = lambda Te: 150/rho_Si *Te
            C_lat_Si     = 1.6e6/rho_Si
            G_Si         = 1e17*18#W/(m**3*K)
            #Set three layers of Silicon after each other. 
            #The space resolution on the Film|Substrate edge is high
            #and decreases as one moves in bulk direction
            if self.num_of_temp == 2:#Lattice only in the 2T
                self.temp_data_Lat.addLayer(20e-9,5.5674+0.38612j,k_lat_Si,C_lat_Si,rho_Si)
                self.coupling = np.append(self.coupling,G_Si)
                self.temp_data_Lat.addLayer(100e-9,5.5674+0.38612j,k_lat_Si,C_lat_Si,rho_Si)
                self.coupling = np.append(self.coupling,G_Si)
                self.temp_data_Lat.addLayer(100000e-9,5.5674+0.38612j,k_lat_Si,C_lat_Si,rho_Si)
                self.coupling = np.append(self.coupling,G_Si)
            #In the 1 and 2 temperature case electron always gets appended
            self.temp_data.addLayer(20e-9,5.5674+0.38612j,k_el_Si,C_el_Si,rho_Si)
            self.temp_data.addLayer(100e-9,5.5674+0.38612j,k_el_Si,C_el_Si,rho_Si)
            self.temp_data.addLayer(100000e-9,5.5674+0.38612j,k_el_Si,C_el_Si,rho_Si)

            
    def addLayer(self,L,n,conductivity,heatCapacity,rho,coupling=0,*args):
        """
        Add parameters of every layer: 
        (length,conductivity[electron,lattice,spin],heatCapacity[electron, lattice, spin],density, coupling[E-L,L-S,S-E])
        The units in SI are: 
            [length]        = m
            [n]             = complex refractive index
            [conductivity]  = W/(mK)
            [heatCapacity]  = J/(m^3K^2)
            [density]       = kg/m^3
            [Coupling]      = W/(m^3K)
        """
        #check all input arguments and make them to lists, for the multi layer case
        #make list when given as int or float
        typecheck = np.array([])
        if type(conductivity) is not (list or type(typecheck)):
            conductivity = [conductivity]
        if type(heatCapacity) is not (list or type(typecheck)):
            heatCapacity = [heatCapacity]
        #do typecheck only for the lattice system in the 2TM-case
        if self.num_of_temp == 2:
            if (np.size(conductivity) or np.size(heatCapacity))<2: 
                print('Lattice parameters are missing.\n Add parameters for Lattice system.')
                return(128)
            self.temp_data_Lat.addLayer(L,n,conductivity[1],heatCapacity[1],rho)
            #Only electron spin coupling is under consideration
            self.coupling = np.append(self.coupling,coupling)   
        #do typecheck for the Lattice and the Spin system
        if self.num_of_temp == 3:
            if (np.size(conductivity) or np.size(heatCapacity) or np.size(coupling))<3: 
                print('Input parameters are missing.\n Add parameters for '\
                      'conductivity/heatCapacity or coupling for Lattice/Spin system.')
                return(128)
            self.temp_data_Lat.addLayer(L,n,conductivity[1],heatCapacity[1],rho)
            self.temp_data_Spin.addLayer(L,n,conductivity[2],heatCapacity[2],rho)
            #In the 3Tm case the coupling input arg is a vector of len 3. Unwrap them:
            self.coupling    = np.append(self.coupling,coupling[0])
            self.coupling_LS = np.append(self.coupling_LS,coupling[1])
            self.coupling_SE = np.append(self.coupling_SE,coupling[2])
        #For the electronic system always add the parameters!
        self.temp_data.addLayer(L,n,conductivity[0],heatCapacity[0],rho)
            
    def interconditions(self,phi,interfaces,conductivity,N,A1h):
        """
        A function which gives back an array where the intereface condition is returned
        for the left and right side of the interface. Gets called in the E.E.-loop.  
        """
        end_i = N-1
        intercondiL = np.zeros((interfaces,N)) 
        intercondiR = np.zeros((interfaces,N)) 
        for i in range(interfaces): 
            intercondiL[i] = conductivity[i](phi[end_i])*A1h[end_i+i] 
            intercondiR[i] = conductivity[i+1](phi[end_i])*A1h[end_i+i+1]
            end_i += N-1        
        return(intercondiL,intercondiR) 
        
    def sourceprofile(self,absorptionprofile,timeprofile,xflat,x0,t,N): 
        #Consider Lambert Beers law in space and different types in time
        if (absorptionprofile == "LB")  and (self.source.fluence is not 0):
            optical_penetration_depth = self.source.ref2delta(self.temp_data.n,self.source.lambda_vac)
            if (timeprofile == "Gaussian"):
                print('-----------------------------------------------------------')
                print('Lambert Beer´s absorption law and a Gaussian time profile is applied as source.')
                print('-----------------------------------------------------------')
                sourceM = self.source.init_G_source(xflat,x0,t,optical_penetration_depth,N,self.source.Gaussian)
            if (timeprofile == "repGaussian") or (timeprofile == "RepGaussian"):
                print('-----------------------------------------------------------')
                print('Lambert Beer absorption profile and a repeated Gaussian time profile is taken into account for the source.'\
                      'The frequency of the pulse repetition has to be indicated via s.frequency = number (in 1/seconds).')
                print('-----------------------------------------------------------')
                self.source.multipulse = True
                xmg, tmg = np.meshgrid(xflat,t)
                if (self.source.frequency is not False):
                    time_range  = tmg[-1,-1]-self.source.t0
                    pulses      = int(round(time_range * self.source.frequency)) 
                    #Add up Gaussian pulses with different t0, according to the frequency given
                    #from t0 onwards, until the end of the time grid
                    customtime = np.zeros(np.shape(tmg))
                    for i in range(0,pulses): 
                        t00 = self.source.t0 + i/self.source.frequency
                        customtime +=np.exp(-(tmg-t00)**2*np.log(2)/(self.source.FWHM**2))
                    sourceM = self.source.init_G_source(xflat,x0,t,optical_penetration_depth,N,self.source.Gaussian,customtime)
                if(self.source.frequency is not False) and (self.source.num_of_pulses is not False):
                    #Creating a certain number of pulses according to self.num_of_pulses
                    time_range = tmg[-1,-1]-self.source.t0
                    pulses = self.source.num_of_pulses
                    #If num_of_pulses is bigger too big to fit in the timerange [t0,t_end] throw warning
                    if (pulses > int(round(time_range * self.source.frequency))):
                        pulses      = int(round(time_range * self.source.frequency)) 
                        print('Number of pulses is too big to fit in the timerange under consideration. \n'\
                              'Adjust t_end or consider a smaller number of pulses.')
                    customtime = np.zeros(np.shape(tmg))
                    for i in range(0,pulses):
                        t00 = self.source.t0 +i/self.source.frequency
                        customtime +=np.exp(-(tmg-t00)**2*np.log(2)/(self.source.FWHM**2))
                    sourceM = self.source.init_G_source(xflat,x0,t,optical_penetration_depth,N,self.source.Gaussian,customtime)
                if(self.source.frequency is False) and (self.source.num_of_pulses is False): 
                    print('-----------------------------------------------------------')
                    print('Assign the propertiy s.frequncy, to consider a certain pulse frequency.\n'\
                          'If only a certain number of pulses should be considered, assign the value s.num_of_pulses = integer.')
                    print('-----------------------------------------------------------')
                
            if (timeprofile == "custom") or (timeprofile == "Custom"): 
                [ttime,amplitude] = self.source.loadData
                #To extract the custom time profile and the scaling factor
                [sourcemat,customtime,scaling] = self.source.custom(t,xflat,ttime,amplitude,optical_penetration_depth[0])
                #To get the space profile: Source with different optical penetration depth defined on the xflat gird   
                sourceM = self.source.init_G_source(xflat,x0,t,optical_penetration_depth,N,self.source.Gaussian,customtime,scaling)
                            
        #Consider Transfer Matrix in space and different types in time    
        if (absorptionprofile == "TMM") and (self.source.fluence is not 0):
            """
            This will implement a transfer matrix approach to local absorption
            instead as using the Lambert Beer´s law considered in the Gaussian
            source type.
            """
            #Multiplying with 1e9, since the absorption()-function. In the source module only works if length is in units of nm!
            x0m = x0*1e9#converte the lentgh into nm
            if len(x0) is not (len(self.temp_data.n)-1):
                print('-----------------------------------------------------------')
                print('Number of considered layers does not match with given refractive indices.\n'\
                      'in ´temperature.n(Air|Film layer1|Film layer2|...|Air)´ anly consider the film layers. \n'\
                      'The refractive index of the substrate gets added automatically later when \n'\
                      '`simulation.addSubstrate(\'name\')` gets called.')                
                print('-----------------------------------------------------------')
            if (timeprofile == "Gaussian"):
                sourceM = self.source.createTMM(self.temp_data.n,xflat,t,x0m)
                print('-----------------------------------------------------------')
                print('Transfer matrix absorption profile and a Gaussian time profile is taken into account for the source.\n'\
                      'Length of every layer has to be given in units of meter.')
                print('-----------------------------------------------------------')
            if (timeprofile == "custom") or (timeprofile == "Custom"): 
                print('-----------------------------------------------------------')
                print('Transfer matrix absorption profile of and a custom time profile is taken into account for the source.\n'\
                      'Length of every layer has to be given in units of meter.')
                print('-----------------------------------------------------------')
                if self.source.loadData is False: 
                    print('-----------------------------------------------------------')
                    print('Import an array, containing the data of the custom pulse.'\
                          'arr[0,:] = time; arr[1,:] = amplitude')
                    print('-----------------------------------------------------------')
                [ttime,amplitude] = self.source.loadData
                lam = 1#Lamda does not matter here since the spacial absorption is calculated via TMM
                [sourceM,customtime,scaling] = self.source.custom(t,xflat,ttime,amplitude,lam)
                #The cfeateTMM(xgrid,timegrid,length,*args) has customtime as an optional argument
                sourceM = self.source.createTMM(self.temp_data.n,xflat,t,x0m,customtime,scaling)
                
            if (timeprofile == "RepGaussian") or (timeprofile== "repGaussian"): 
                print('-----------------------------------------------------------')
                print('Transfer matrix absorption profile and a repeated Gaussian time profile is taken into account for the source.'\
                      'Length of every layer has to be given in units of meter.')
                print('-----------------------------------------------------------')
                self.source.multipulse = True
                xmg, tmg = np.meshgrid(xflat,t)
                if (self.source.frequency is not False):
                    time_range  = tmg[-1,-1]-self.source.t0
                    pulses      = int(round(time_range * self.source.frequency)) 
                    #Add up Gaussian pulses with different t0, according to the frequency given
                    #from t0 onwards, until the end of the time grid
                    customtime = np.zeros(np.shape(tmg))
                    for i in range(0,pulses): 
                        t00 = self.source.t0 + i/self.source.frequency
                        customtime +=np.exp(-(tmg-t00)**2*np.log(2)/(self.source.FWHM**2))
                    sourceM = self.source.createTMM(self.temp_data.n,xflat,t,x0m,customtime)
                if(self.source.frequency is not False) and (self.source.num_of_pulses is not False):
                    #Creating a certain number of pulses according to self.num_of_pulses
                    time_range = tmg[-1,-1]-self.source.t0
                    pulses = self.source.num_of_pulses
                    #If num_of_pulses is bigger too big to fit in the timerange [t0,t_end] throw warning
                    if (pulses > int(round(time_range * self.source.frequency))):
                        pulses      = int(round(time_range * self.source.frequency)) 
                        print('Number of pulses is too big to fit in the timerange under consideration. \n'\
                              'Adjust t_end or consider a smaller number of pulses.')
                    customtime = np.zeros(np.shape(tmg))
                    for i in range(0,pulses):
                        t00 = self.source.t0 +i/self.source.frequency
                        customtime +=np.exp(-(tmg-t00)**2*np.log(2)/(self.source.FWHM**2))
                    sourceM = self.source.createTMM(self.temp_data.n,xflat,t,x0m,customtime)
                if(self.source.frequency is False) and (self.source.num_of_pulses is False): 
                    print('-----------------------------------------------------------')
                    print('Assign the propertiy s.frequncy, to consider a certain pulse frequency.\n'\
                          'If only a certain number of pulses should be considered, assign the value s.num_of_pulses = integer.')
                    print('-----------------------------------------------------------')
        return(sourceM)
    # This is the main Explicit Euler loop where the solution to T(x,t) is calculated.
    def run(self):
        idealtimestep = self.stability()
        if not self.time_step: 
            self.time_step  = idealtimestep
            print('-----------------------------------------------------------')            
            print(' No specific time constant has been indicated. \n '\
                  'The stability region has been calculated and an appropriate timestep has been chosen.\n '\
                  'Timestep = {idealtimestep:.2e} s'.format(idealtimestep=idealtimestep))
            print('-----------------------------------------------------------') 
        if (self.time_step-idealtimestep)/idealtimestep > 0.1: 
            print('-----------------------------------------------------------')            
            print('The manually chosen time step of {time_step:.2e} is eventually too big and could cause instabilities in the simulation.\n '\
                  'We suggest a timestep of {idealtimestep:.2e} s'.format(time_step=self.time_step,idealtimestep=idealtimestep))
            print('-----------------------------------------------------------')
        if(self.time_step-idealtimestep)/idealtimestep < -0.2: 
            print('-----------------------------------------------------------')  
            print('The maunually chosen time step of {time_step:.2e} is very small and will eventually cause a long simulation time.\n'\
                  'We suggest a timestep of {idealtimestep:.2e} s'.format(time_step=self.time_step,idealtimestep=idealtimestep))
            print('-----------------------------------------------------------')            
        #loading simulation relevant properties from the structural tmeperature object
        [c_E,A00,Abig,A1b,A2b,Cb,length,N,plp,xflat,x_plt_flat,initphi_large,interfaces,LayerMat,A1h]  = self.temp_data.Msetup()
        t = np.arange(self.start_time,self.final_time,self.time_step)
        #only if the injection would make the time grid smaller, to not move into instable regime
        if self.source.FWHM:
            if (6*self.source.FWHM/200 < idealtimestep):
                #inject 200 extra points around pulse to fully capture the shape of the pulse
                tinj    = np.linspace(self.source.t0 - 3*self.source.FWHM,self.source.t0 + 3*self.source.FWHM,200)
                smaller = np.where(t<self.source.t0 - 3*self.source.FWHM)[0]
                bigger  = np.where(t>self.source.t0 + 3*self.source.FWHM)[0]
            #new time grid with higher resolution
                t = np.concatenate((t[smaller],tinj,t[bigger]),axis=0)
        tstep = np.ones(len(t))
        tstep[:-1] = np.diff(t); tstep[-1] = np.diff(t)[-1]
        #If a more refined grid is choosen around t0. We inject a fine time grid around t0, to correctly capture the pulse shape
        if self.source.adjusted_grid is not False: 
            if self.source.dt0 == False:
                print('-----------------------------------------------------------')            
                print('The option for an adjusted grid is True, but no interval for a more refined grid has been given.'/
                      'Indicate dt0 (around which values the time grid should have higher resolution) in the source object')
                print('-----------------------------------------------------------')

            if 2*self.source.dt0/self.source.extra_points < idealtimestep:
                print('-----------------------------------------------------------')            
                print('A refined Grid around t0 has been applied')
                print('-----------------------------------------------------------')
                tinj    = np.linspace(self.source.t0-self.source.dt0,self.source.t0+self.source.dt0,self.source.extra_points)
                smaller = np.where(t<self.source.t0 - self.source.dt0)[0]
                bigger  = np.where(t>self.source.t0 + self.source.dt0)[0]
                #new time grid with higher resolution
                t = np.concatenate((t[smaller],tinj,t[bigger]),axis=0)
                tstep = np.ones(len(t))
                tstep[:-1] = np.diff(t); tstep[-1] = np.diff(t)[-1]
            else: 
                print('-----------------------------------------------------------')            
                print('No refined time grid is applied. The timestep is alerady very small.' \
                      'You can use the simulation class with the property self.time_step and '\
                      'assign it to a smaller value as the current time step.')
                print('-----------------------------------------------------------')
        #Initialize the systems and load the matrices         
        if self.temp_data_Lat: 
            if self.temp_data.plt_points is not self.temp_data_Lat.plt_points: 
                self.temp_data_Lat.plt_points = self.temp_data.plt_points 
                print('-----------------------------------------------------------')
                print('The number of plotting points in the electron system \n'\
                      'is not the same as in the lattice system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------')
            if self.temp_data.collocpts is not self.temp_data_Lat.collocpts: 
                self.temp_data_Lat.collocpts = self.temp_data.collocpts 
                print(self.temp_data_Lat.collocpts)
                print('-----------------------------------------------------------')
                print('The number of collocation points in the electron system \n'\
                      'is not the same as in the lattice system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------') 
            [c_L,A00,Abig,A1b,A2b,Cb,length,N,plp,xflat,x_plt_flat,initphi_large_L,interfaces,LayerMat,A1h] = self.temp_data_Lat.Msetup()
        if self.temp_data_Spin: 
            print("Line 728 Spinsystem")
            if self.temp_data.plt_points is not self.temp_data_Spin.plt_points: 
                self.temp_data_Spin.plt_points = self.temp_data.plt_points 
                print('-----------------------------------------------------------')
                print('The number of plotting points in the electron system \n'\
                      'is not the same as in the spin system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------')
            if self.temp_data.collocpts is not self.temp_data_Spin.collocpts: 
                self.temp_data_Spin.collocpts = self.temp_data.collocpts 
                print('-----------------------------------------------------------')
                print('The number of collocation points in the electron system \n'\
                      'is not the same as in the spin system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------') 
            [c_S,A00,Abig,A1b,A2b,Cb,length,N,plp,xflat,x_plt_flat,initphi_large_S,interfaces,LayerMat,A1h] = self.temp_data_Spin.Msetup()
         
        if  (self.source.fluence == 0): 
            print('-----------------------------------------------------------')
            print('No source is applied.\n'\
                  'source.fluence = 0')
            print('-----------------------------------------------------------')  
            xmg, tmg = np.meshgrid(xflat,t)
            sourceM = np.zeros_like(xmg)
        else:
            sourceM = self.sourceprofile(self.source.spaceprofile,self.source.timeprofile,xflat,self.temp_data.length,t,N)
            
        #Making the boundary conditions a function of t, in case they are given as scalars
        if isinstance(self.left_BC,(int,float)): 
            dummy = self.left_BC
            self.left_BC = lambda t: dummy + 0*t
        if isinstance(self.right_BC,(int,float)): 
            dummy1 = self.right_BC
            self.right_BC = lambda t: dummy1 + 0*t
        #Makint the boundary conditions a matrix for the electron case      
        BC_E      = np.zeros((len(c_E),len(t))) 
        BC_E[0]   = self.left_BC(t)
        BC_E[-1]  = self.right_BC(t)
        #Checking the Lattice system boundary conditions
        if self.temp_data_Lat:
            if isinstance(self.left_BC_L,(int,float)): 
                dummy2 = self.left_BC_L
                self.left_BC_L = lambda t: dummy2 + 0*t 
            if isinstance(self.right_BC_L,(int,float)): 
                dummy3 = self.right_BC_L
                self.right_BC_L = lambda t: dummy3 + 0*t 
        #Makint the boundary conditions a matrix for the lattice case
            BC_L      = np.zeros((len(c_L),len(t))) 
            BC_L[0]   = self.left_BC_L(t)
            BC_L[-1]  = self.right_BC_L(t)
            #Checking the Spine system boundary conditions 
            #It impies that we at least consider 2 temperatures -> under this "if-tree"
            if self.temp_data_Spin:
                if isinstance(self.left_BC_S,(int,float)): 
                    dummy4 = self.left_BC_S
                    self.left_BC_S = lambda t: dummy4 + 0*t 
                if isinstance(self.right_BC_S,(int,float)): 
                    dummy5 = self.right_BC_S
                    self.right_BC_S = lambda t: dummy5 + 0*t 
                #Makint the boundary conditions a matrix for the Spin case
                BC_S      = np.zeros((len(c_S),len(t))) 
                BC_S[0]   = self.left_BC_S(t)
                BC_S[-1]  = self.right_BC_S(t)
                #Check if the Lattice/Spin and Spin/Electron coupling constants have the right size
                if np.size(self.coupling_LS)<np.size(length)-1:
                    self.coupling_LS = self.coupling_LS*np.ones(np.size(self.temp_data.length)-1)
                    print('-----------------------------------------------------------')
                    print('Not every layer has a unique Lattice-Spin coupling constant \'G_LS \'.\n')\
                    ('=> G_LS will be set to the value of the first layer = {coupling_LS[0]:.2e}\n  for all other layers.'.format(coupling_LS=self.coupling_LS))
                    print('-----------------------------------------------------------')
                if np.size(self.coupling_SE)<np.size(length)-1:
                    self.coupling_SE = self.coupling_SE*np.ones(np.size(self.temp_data.length)-1)
                    print('-----------------------------------------------------------')
                    print('Not every layer has a unique Spin-Electron coupling constant \'G_SE \'.\n')\
                    ('=> G_SE will be set to the value of the first layer = {coupling_SE[0]:.2e}\n  for all other layers.'.format(coupling_SE=self.coupling_SE))
                    print('-----------------------------------------------------------')                    
            #If only the two temperature model is considered I only need to check one coupling constant
            if np.size(self.coupling)<np.size(length)-1:
                self.coupling = self.coupling*np.ones(np.size(self.temp_data.length)-1)
                print('-----------------------------------------------------------')
                print('Not every layer has a unique coupling constant \'G \'.\n')\
                ('=> G will be set to the value of the first layer = {coupling[0]:.2e}\n  for all other layers.'.format(coupling=self.coupling))
                print('-----------------------------------------------------------')
        
        # The 3 Temperature Case is being considered        
        if self.temp_data_Spin:
            #Setup arrays for electron temperature
            phi_E = np.zeros((len(t),len(x_plt_flat))); phi_E[0] = initphi_large
            Flow_1E = np.zeros(len(c_E))
            Flow_2E = np.zeros(len(c_E)) 
            dphi_E = np.zeros(len(c_E))
            intphi_E = np.zeros(len(c_E))
            #Setup arrays for lattice temperature
            phi_L = np.zeros((len(t),len(x_plt_flat))); phi_L[0] = initphi_large_L    #300*np.ones(len(phi_L[0]))
            Flow_1L = np.zeros(len(c_L))
            Flow_2L = np.zeros(len(c_L)) 
            dphi_L = np.zeros(len(c_L))
            intphi_L = np.zeros(len(c_L))
            #Setup arrays for the spin temperature
            phi_S = np.zeros((len(t),len(x_plt_flat))); phi_S[0] = initphi_large_S    #300*np.ones(len(phi_L[0]))
            Flow_1S = np.zeros(len(c_S))
            Flow_2S = np.zeros(len(c_S)) 
            dphi_S = np.zeros(len(c_S))
            intphi_S = np.zeros(len(c_S))
            #General setup for E.E. loop
            condi       = np.array([np.arange(1,len(length)-1)])*(N-1) #Index to apply interface condition
            cnfill      = np.array([np.arange(1,len(length)-1)])*(plp-1)#correct interface condition with real value for phi
            A00[0]      = 1; A00[-1] = 1 #Avoide devide through 0 in dphi_L! Clar for BC before intphi calc.
            Abig_E      = np.copy(Abig)  #Since Abig can change due to interconditions we split it here
            Abig_L      = np.copy(Abig)  #The interface conditions are applied on every time step 
            Abig_S      = np.copy(Abig)  #Every system gets individual matrix
            start_EL    = time.time()
            for i in tqdm(range(1,len(t)),position = 0):
                #Calculate Solution at every time step and respective derivatives
                phi0_E = np.dot(A00,c_E); phi1_E = np.dot(A1b,c_E); phi2_E = np.dot(A2b,c_E)
                phi0_L = np.dot(A00,c_L); phi1_L = np.dot(A1b,c_L); phi2_L = np.dot(A2b,c_L)
                phi0_S = np.dot(A00,c_S); phi1_S = np.dot(A1b,c_S); phi2_S = np.dot(A2b,c_S)
                #Calculating interface conditions which are applied later
                intercon_E = self.interconditions(phi_E[i-1],interfaces,self.temp_data.conductivity,N,A1h)    
                intercon_L = self.interconditions(phi_L[i-1],interfaces,self.temp_data_Lat.conductivity,N,A1h)
                intercon_S = self.interconditions(phi_S[i-1],interfaces,self.temp_data_Spin.conductivity,N,A1h)
                startf = 0;endf = N-1
                #Construct all picewise flows and piecewise dphi. Iterate over layers
                for j in range(0,interfaces+1): 
                    #electron: d/dx[k(phi) * d/dx(phi)]
                    Flow_1E[startf:endf] = self.temp_data.diff_conductivity(phi0_E[startf:endf],j)
                    Flow_2E[startf:endf] = self.temp_data.conductivity[j](phi0_E[startf:endf])
                    Flow_1E[startf:endf] *=phi1_E[startf:endf]**2
                    Flow_2E[startf:endf] *= phi2_E[startf:endf] 
                    #lattice
                    Flow_1L[startf:endf] = self.temp_data_Lat.diff_conductivity(phi0_L[startf:endf],j)
                    Flow_2L[startf:endf] = self.temp_data_Lat.conductivity[j](phi0_L[startf:endf])
                    Flow_1L[startf:endf] *=phi1_L[startf:endf]**2
                    Flow_2L[startf:endf] *= phi2_L[startf:endf] 
                    #Spin
                    Flow_1S[startf:endf] = self.temp_data_Spin.diff_conductivity(phi0_S[startf:endf],j)
                    Flow_2S[startf:endf] = self.temp_data_Spin.conductivity[j](phi0_S[startf:endf])
                    Flow_1S[startf:endf] *=phi1_S[startf:endf]**2
                    Flow_2S[startf:endf] *= phi2_S[startf:endf]
                    #calculate delta phi for electron, lattice and spin
                    #This is the core of the problem
                    dphi_E[startf:endf] = 1/(self.temp_data.heatCapacity[j](phi0_E)[startf:endf]*self.temp_data.rho[j])*\
                    (Flow_1E[startf:endf]+Flow_2E[startf:endf]+sourceM[i,startf:endf] +\
                     self.coupling[j]*(phi0_L[startf:endf]-phi0_E[startf:endf])+self.coupling_SE[j]*(phi0_S[startf:endf]-phi0_E[startf:endf]))  
                    #Lattice time derivative
                    dphi_L[startf:endf] = 1/(self.temp_data_Lat.heatCapacity[j](phi0_L)[startf:endf]*self.temp_data_Lat.rho[j])*\
                    (Flow_1L[startf:endf]+Flow_2L[startf:endf] +\
                     self.coupling[j]*(phi0_E[startf:endf]-phi0_L[startf:endf])+self.coupling_LS[j]*(phi0_S[startf:endf]-phi0_L[startf:endf])) 
                    #Spin system time derivative
                    dphi_S[startf:endf] = 1/(self.temp_data_Spin.heatCapacity[j](phi0_S)[startf:endf]*self.temp_data_Spin.rho[j])*\
                    (Flow_1S[startf:endf]+Flow_2S[startf:endf] +\
                     self.coupling_LS[j]*(phi0_L[startf:endf]-phi0_S[startf:endf])+self.coupling_SE[j]*(phi0_E[startf:endf]-phi0_S[startf:endf])) 
                    startf += N-1; endf +=N-1 #Move one layer further
                start_i = 0; end_i = N-1 
                #Apply interface conditions for all layers in every time step, i.e.: 
                #filling up Abig wiht the interface condition in the middle of the grid
                for k in range(0,interfaces): 
                    #for the electron system 
                    Abig_E[end_i,start_i:end_i]    =  intercon_E[0][k][:-1]#Lhs interface flow
                    Abig_E[end_i,end_i+1:end_i+N]  = -intercon_E[1][k][1:]#Rhs interface flow
                    Abig_E[end_i,end_i]            = intercon_E[0][k][-1] -intercon_E[1][k][0]
                    #for the lattice system
                    Abig_L[end_i,start_i:end_i]    =  intercon_L[0][k][:-1]#Lhs interface flow
                    Abig_L[end_i,end_i+1:end_i+N]  = -intercon_L[1][k][1:]#Rhs interface flow
                    Abig_L[end_i,end_i]            = intercon_L[0][k][-1] -intercon_L[1][k][0]
                    #for the Spin system
                    Abig_S[end_i,start_i:end_i]    =  intercon_S[0][k][:-1]#Lhs interface flow
                    Abig_S[end_i,end_i+1:end_i+N]  = -intercon_S[1][k][1:]#Rhs interface flow
                    Abig_S[end_i,end_i]            = intercon_S[0][k][-1] -intercon_S[1][k][0]
                    start_i += N-1; end_i += N-1
                #computing the flux for every time step at the boundaries
                #If Neumann BC-> devide over k(T) since BC_Type = 1
                #If Dirichlet BC -> devide over 1 since BC_Type = 0
                Flux_E = BC_E[:,i]#Avoidint 0 in denominator
                Flux_E[0] /= self.temp_data.conductivity[0](c_E[0])**self.temp_data.Left_BC_Type + 1e-12 
                Flux_E[-1] /= self.temp_data.conductivity[-1](c_E[-1])**self.temp_data.Right_BC_Type + 1e-12
                Flux_L = BC_L[:,i]
                Flux_L[0] /= self.temp_data_Lat.conductivity[0](c_L[0])**self.temp_data_Lat.Left_BC_Type + 1e-12
                Flux_L[-1] /= self.temp_data_Lat.conductivity[-1](c_L[-1])**self.temp_data_Lat.Right_BC_Type + 1e-12
                Flux_S = BC_S[:,i]
                Flux_S[0] /= self.temp_data_Spin.conductivity[0](c_S[0])**self.temp_data_Spin.Left_BC_Type   + 1e-12
                Flux_S[-1] /= self.temp_data_Spin.conductivity[-1](c_S[-1])**self.temp_data_Spin.Right_BC_Type + 1e-12
                #Clear for boundary conditions at the edgeds of the grid
                dphi_E[0] = 0; dphi_E[-1] = 0; 
                phi0_E[0] = 0; phi0_E[-1] = 0;
                dphi_L[0] = 0; dphi_L[-1] = 0;
                phi0_L[0] = 0; phi0_L[-1] = 0; 
                dphi_S[0] = 0; dphi_S[-1] = 0;
                phi0_S[0] = 0; phi0_S[-1] = 0;
                #intermediate phi with low resolution in space according to explicit euler
                intphi_E  = phi0_E + tstep[i] * dphi_E + Flux_E
                intphi_L  = phi0_L + tstep[i] * dphi_L + Flux_L
                intphi_S  = phi0_S + tstep[i] * dphi_S + Flux_S
                #Interface condition: Setting the rhs to 0, such that the heat transported (flux = Q = k*d/dx phi)
                #from left is what comes out at the right hand side Q_1 -> Q_2
                intphi_E[condi] = 0 #Interface condition: Q_1 -Q_2 = 0
                intphi_L[condi] = 0 
                intphi_S[condi] = 0 
                #electron: use c to map on high resolution x-grid
                #since in Abig, k(T(t)) is inserted we have to solve the system for every step
                c_E                 = np.linalg.solve(Abig_E,intphi_E)  # c(t) for every timestep
                phi_E[i]            = np.dot(Cb,c_E)                    # map spline coefficients to fine Cb grid
                phi_E[i,cnfill]     = c_E[condi]                        #correct the values for phi at interface
                #lattice
                c_L                 = np.linalg.solve(Abig_L,intphi_L)   
                phi_L[i]            = np.dot(Cb,c_L)
                phi_L[i,cnfill]     = c_L[condi] 
                #spin
                c_S                 = np.linalg.solve(Abig_S,intphi_S)   
                phi_S[i]            = np.dot(Cb,c_S)
                phi_S[i,cnfill]     = c_S[condi]
            end_EL = time.time()
            print('-----------------------------------------------------------')  
            print('Heat diffusion in a coupled electron-latticelspin system has been simulated')
            print('Eleapsed time in E.E.- loop:', end_EL-start_EL)
            print('-----------------------------------------------------------') 
            T = []
            T.append(phi_E); T.append(phi_L); T.append(phi_S)
            return(x_plt_flat,t,T)
    #=======End 3 temp Case =================================
        #The two temperature model is considered   
        if self.temp_data_Lat: 
            #Setup arrays for electron temperature
            phi_E = np.zeros((len(t),len(x_plt_flat))); phi_E[0] = initphi_large
            Flow_1E = np.zeros(len(c_E))
            Flow_2E = np.zeros(len(c_E)) 
            dphi_E = np.zeros(len(c_E))
            intphi_E = np.zeros(len(c_E))
            #Setup arrays for lattice temperature
            phi_L = np.zeros((len(t),len(x_plt_flat))); phi_L[0] = initphi_large_L
            Flow_1L = np.zeros(len(c_L))
            Flow_2L = np.zeros(len(c_L)) 
            dphi_L = np.zeros(len(c_L))
            intphi_L = np.zeros(len(c_L))
            #General setup for E.E. loop
            condi       = np.array([np.arange(1,len(length)-1)])*(N-1) #Index to apply interface condition
            cnfill      = np.array([np.arange(1,len(length)-1)])*(plp-1)#correct interface condition with real value for phi
            A00[0]      = 1; A00[-1] = 1 #Avoide devide through 0 in dphi_L! Clar for BC before intphi calc.
            Abig_E      = np.copy(Abig)  #Since Abig can change due to interconditions we split it here
            Abig_L      = np.copy(Abig)  #The interface conditions are applied on every time step 
            start_EL    = time.time()
            for i in tqdm(range(1,len(t)),position = 0):
                #Calculate Solution at every time step and respective derivatives
                phi0_E = np.dot(A00,c_E); phi1_E = np.dot(A1b,c_E); phi2_E = np.dot(A2b,c_E)
                phi0_L = np.dot(A00,c_L); phi1_L = np.dot(A1b,c_L); phi2_L = np.dot(A2b,c_L)
                #Calculating interface conditions which are applied later
                intercon_E = self.interconditions(phi_E[i-1],interfaces,self.temp_data.conductivity,N,A1h)    
                intercon_L = self.interconditions(phi_L[i-1],interfaces,self.temp_data_Lat.conductivity,N,A1h)
                startf = 0;endf = N-1
                #Construct all picewise flows and piecewise dphi Iterate over layers
                for j in range(0,interfaces+1): 
                    #electron
                    Flow_1E[startf:endf] = self.temp_data.diff_conductivity(phi0_E[startf:endf],j)
                    Flow_2E[startf:endf] = self.temp_data.conductivity[j](phi0_E[startf:endf])
                    Flow_1E[startf:endf] *=phi1_E[startf:endf]**2
                    Flow_2E[startf:endf] *= phi2_E[startf:endf] 
                    #lattice
                    Flow_1L[startf:endf] = self.temp_data_Lat.diff_conductivity(phi0_L[startf:endf],j)
                    Flow_2L[startf:endf] = self.temp_data_Lat.conductivity[j](phi0_L[startf:endf])
                    Flow_1L[startf:endf] *=phi1_L[startf:endf]**2
                    Flow_2L[startf:endf] *= phi2_L[startf:endf]  
                    #calculate delta phi for electron and lattice
                    #This is the core of the problem
                    dphi_E[startf:endf] = 1/(self.temp_data.heatCapacity[j](phi0_E)[startf:endf]*self.temp_data.rho[j])*\
                    (Flow_1E[startf:endf]+Flow_2E[startf:endf]+sourceM[i,startf:endf] + self.coupling[j]*(phi0_L[startf:endf]-phi0_E[startf:endf]))  
                    dphi_L[startf:endf] = 1/(self.temp_data_Lat.heatCapacity[j](phi0_L)[startf:endf]*self.temp_data_Lat.rho[j])*\
                    (Flow_1L[startf:endf]+Flow_2L[startf:endf] + self.coupling[j]*(phi0_E[startf:endf]-phi0_L[startf:endf])) 
                    startf += N-1; endf +=N-1 
                #filling up Abig wiht the interface condition in the middle of the grid
                start_i = 0; end_i = N-1  
                for k in range(0,interfaces): #Apply interface conditions for all layers in every time step 
                    #for the electron system 
                    Abig_E[end_i,start_i:end_i]    =  intercon_E[0][k][:-1]#Lhs interface flow
                    Abig_E[end_i,end_i+1:end_i+N]  = -intercon_E[1][k][1:]#Rhs interface flow
                    Abig_E[end_i,end_i]            = intercon_E[0][k][-1] -intercon_E[1][k][0]
                    #for the lattice system
                    Abig_L[end_i,start_i:end_i]    =  intercon_L[0][k][:-1]#Lhs interface flow
                    Abig_L[end_i,end_i+1:end_i+N]  = -intercon_L[1][k][1:]#Rhs interface flow
                    Abig_L[end_i,end_i]            = intercon_L[0][k][-1] -intercon_L[1][k][0]
                    start_i += N-1; end_i += N-1
                #computing the flux for every time step for the boundaries
                Flux_E = BC_E[:,i]
                Flux_E[0] /= self.temp_data.conductivity[0](c_E[0])**self.temp_data.Left_BC_Type + 1e-12
                Flux_E[-1] /= self.temp_data.conductivity[-1](c_E[-1])**self.temp_data.Right_BC_Type + 1e-12
                Flux_L = BC_L[:,i]
                Flux_L[0] /= self.temp_data_Lat.conductivity[0](c_L[0])**self.temp_data_Lat.Left_BC_Type + 1e-12
                Flux_L[-1] /= self.temp_data_Lat.conductivity[-1](c_L[-1])**self.temp_data_Lat.Right_BC_Type + 1e-12
                #Clear for boundary conditions at the edgeds of the grid
                dphi_E[0] = 0; dphi_E[-1] = 0; dphi_L[0] = 0; dphi_L[-1] = 0
                phi0_E[0] = 0; phi0_E[-1]  = 0; phi0_L[0] = 0; phi0_L[-1] = 0;   
                #intermediate phi with low resolution in space according to explicit euler
                intphi_E        = phi0_E + tstep[i] * dphi_E + Flux_E
                intphi_E[condi] = 0
                intphi_L        = phi0_L + tstep[i] * dphi_L + Flux_L
                intphi_L[condi] = 0 #Interface condition: Q_1 -Q_2 = 0
                #electron: use c to map on high resolution x-grid
                #since in Abig, k(T(t)) is inserted we have to solve the system for every step
                c_E                 = np.linalg.solve(Abig_E,intphi_E)  # c(t) for every timestep
                phi_E[i]            = np.dot(Cb,c_E)                    # map spline coefficients to fine Cb grid
                phi_E[i,cnfill]     = c_E[condi]                        #correct the values for phi at interface
                #lattice
                c_L                 = np.linalg.solve(Abig_L,intphi_L)   
                phi_L[i]            = np.dot(Cb,c_L)
                phi_L[i,cnfill]     = c_L[condi]             
            end_EL = time.time()
            print('-----------------------------------------------------------')  
            print('Heat diffusion in a coupled electron-lattice system has been simulated')
            print('Eleapsed time in E.E.- loop:', end_EL-start_EL)
            print('-----------------------------------------------------------')
            T = []
            T.append(phi_E); T.append(phi_L)
            return(x_plt_flat,t,T)
        #=============End 2Temp Case ========================
        else: #this is the single temperature case. (Only electron temperature)
            #prepare space to store phi solution on fine plt grid. And Flow_1,2 vectors
            phi = np.zeros((len(t),len(x_plt_flat))); phi[0] = initphi_large
            Flow_1 = np.zeros(len(c_E))
            Flow_2 = np.zeros(len(c_E)) 
            dphi = np.zeros(len(c_E))
            intphi = np.zeros(len(c_E))
            condi = np.array([np.arange(1,len(length)-1)])*(N-1)    #Index to apply interface condition
            cnfill = np.array([np.arange(1,len(length)-1)])*(plp-1) #correct interface condition with real value for phi
            A00[0] = 1; A00[-1] = 1 #Avoid 1/0 division in dphi calculation. See E.E. loop
            
            startE = time.time()
            for i in tqdm(range(1,len(t)),position = 0):
                phi0 = np.dot(A00,c_E); phi1 = np.dot(A1b,c_E); phi2 = np.dot(A2b,c_E)  
                intercon_E = self.interconditions(phi[i-1],interfaces,self.temp_data.conductivity,N,A1h) #get interface conditions for every time step
                startf = 0;endf = N-1
                #construct all picewise flows and piecewise dphi
                for j in range(0,interfaces+1): 
                    Flow_1[startf:endf] = self.temp_data.diff_conductivity(phi0[startf:endf],j)
                    Flow_2[startf:endf] = self.temp_data.conductivity[j](phi0[startf:endf])
                    Flow_1[startf:endf] *=phi1[startf:endf]**2
                    Flow_2[startf:endf] *= phi2[startf:endf] 
                    dphi[startf:endf] = 1/(self.temp_data.heatCapacity[j](phi0)[startf:endf]*self.temp_data.rho[j])*\
                    (Flow_1[startf:endf]+Flow_2[startf:endf]+sourceM[i,startf:endf])  
                    startf += N-1; endf +=N-1 
                #filling up Abig wiht the interface condition in the middle of the grid
                start_i = 0; end_i = N-1  
                for k in range(0,interfaces): #Apply interface conditions for all layers in every time step 
                    Abig[end_i,start_i:end_i]    =  intercon_E[0][k][:-1]#Lhs interface flow
                    Abig[end_i,end_i+1:end_i+N]  = -intercon_E[1][k][1:]#Rhs interface flow
                    Abig[end_i,end_i]            = intercon_E[0][k][-1] -intercon_E[1][k][0]
                start_i += N-1; end_i += N-1
                #computing the flux for every time step for the boundaries
                Flux_E = BC_E[:,i]
                Flux_E[0] /= self.temp_data.conductivity[0](c_E[0])**self.temp_data.Left_BC_Type + 1e-12
                Flux_E[-1] /= self.temp_data.conductivity[-1](c_E[-1])**self.temp_data.Right_BC_Type + 1e-12
                #Make space for BC    
                dphi[0] = 0; dphi[-1] = 0
                phi0[0] = 0; phi0[-1]  = 0
                
                intphi = phi0 + tstep[i] * dphi + Flux_E
                intphi[condi] = 0                               #Interface condition: Q_1 -Q_2 = 0
                # c(t) for every timestep
                #since in Abig k(T(t)) is inserted we have to solve the system for every step
                c_E             = np.linalg.solve(Abig,intphi)  #this system has to be solved in every time step
                phi[i]          = np.dot(Cb,c_E)                  # map spline coefficients to fine Cb grid
                phi[i,cnfill]   = c_E[condi]                      #correct the values for phi at interface
            endE = time.time()
            print('-----------------------------------------------------------')  
            print('Electron temperature heat diffusion has been simulated.')
            print('Eleapsed time in E.E.- loop:', endE-startE)
            print('-----------------------------------------------------------')  
        return(x_plt_flat,t,phi)
        
    def stability(self):
        """
        If only the electron temperature system is under consideration, we only 
        compute the eigenvalues of lambda_i = k/(C*rho)*A00^-1*A2b. This is 
        we consider the minimum Eigenvalue for each layer to represent the time konstant.
        The time constant for E.E. is then given by -2/min(lambda_i), which is 
        the criterion for stability for E.E. loops, to obtain convergence.
        """
        [c,A00,Abig,A1b,A2b,Cb,length,N,plp,xflat,x_plt_flat,initphi_large,interfaces,LayerMat,A1h]  = self.temp_data.Msetup()
        A00[0,0] = 1; A00[-1,-1] = 1
        rho_E = self.temp_data.rho
        conductivity_E = self.temp_data.conductivity
        conductivity_E = np.asarray(conductivity_E)
        typecheck      = np.array([1])[0]
        for i in range(0,len(conductivity_E)):
            #In case conductivity is a function k(T) we compute a worst case scenario
            #this is because we can only compare integers. 
            if not isinstance(conductivity_E[i],(int,float,type(typecheck))): 
                testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                conductivity_E[i] = max(conductivity_E[i](testT))
        
        heatCapacity_E = self.temp_data.heatCapacity
        heatCapacity_E = np.asarray(heatCapacity_E)
        for i in range(0,len(heatCapacity_E)): 
            #In case heatCapacity is a function C(T) we compute a worst case scenario
            #and take an integer value to compare
            if not isinstance(heatCapacity_E[i],(int,float,type(typecheck))): 
                testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                heatCapacity_E[i] = min(heatCapacity_E[i](testT))
        Eval = np.zeros(interfaces+1) #for each layer there will be an eigenvalue    
        koeff1   = conductivity_E/(heatCapacity_E*rho_E)
        for i in range(0,interfaces+1):
            Lambda   = koeff1[i]*LayerMat[i]
            Eval[i]  = min(np.real(np.linalg.eig(Lambda)[0]))
        tkonst_E = -1.9/Eval
        
        if self.num_of_temp == 2:
            """
            In the multy temperature case, we also consider the lattice dynamics,
            with respective k_L/(C_L*rho_L) dynamics. In addition, we also have to
            consider, the coupling between those two layers. I.e. G_mat. 
            with coefficients koeff_2 = G/(heatCapacity*rho)
            Therefor we compute eigenvalues of the combined system:
            lambda_i = eval(Lambda + G_mat) for each layer.
            The time constant is again -2/min(lambda_i)
            """
            if self.temp_data.collocpts is not self.temp_data_Lat.collocpts: 
                self.temp_data_Lat.collocpts = self.temp_data.collocpts 
                print('-----------------------------------------------------------')
                print('The number of collocation points in the electron system \n'\
                      'is not the same as in the lattice system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------')             
            [c,A00_L,Abig,A1b,A2b_L,Cb,length,N,plp,xflat,x_plt_flat,initphi_large,interfaces,LayerMat,A1h]  = self.temp_data_Lat.Msetup()
            A00_L[0,0] = 1; A00_L[-1,-1] = 1  
            rho_L = self.temp_data_Lat.rho
            G = self.coupling
            G = np.asarray(G)
             
            conductivity_L = self.temp_data_Lat.conductivity
            conductivity_L = np.asarray(conductivity_L)
            #In case conductivity is a function k(T) we compute a worst case scenario
            for i in range(0,len(conductivity_L)): 
                if not isinstance(conductivity_L[i],(int ,float,type(typecheck))):
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    conductivity_L[i] = max(conductivity_L[i](testT))
                    
            heatCapacity_L = self.temp_data_Lat.heatCapacity
            heatCapacity_L = np.asarray(heatCapacity_L)
            #In case heatCapacity is a function C(T) we compute a worst case scenario
            for i in range(0,len(heatCapacity_L)): 
                if not isinstance(heatCapacity_L[i],(int,float,type(typecheck))): 
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    heatCapacity_L[i] = min(heatCapacity_L[i](testT))
            #M: for every layer we load the respective matrix from the temperature class                    
            M                       = np.shape(LayerMat)[1] 
            Lambda                  = np.zeros((2*M,2*M))
            Eval                    = np.zeros(interfaces+1)
            G_mat                   = np.zeros((2*M,2*M))          
            koeff1_E                = conductivity_E/(heatCapacity_E*rho_E)
            koeff1_L                = conductivity_L/(heatCapacity_L*rho_L)
            koeff2_E                = G/(heatCapacity_E*rho_E)            
            koeff2_L                = G/(heatCapacity_L*rho_L)
            
            for i in range(0,interfaces+1):
                Lambda[0:M,0:M]     = koeff1_E[i]*LayerMat[i]
                Lambda[M:,M:]       = koeff1_L[i]*LayerMat[i]
                G_mat[0:M,0:M]      = -koeff2_E[i]*np.eye(M)
                G_mat[0:M,M:]       = koeff2_E[i]*np.eye(M)
                G_mat[M:,0:M]       = koeff2_L[i]*np.eye(M)
                G_mat[M:,M:]        = -koeff2_L[i]*np.eye(M)
                Eval[i]             = min(np.real(np.linalg.eig(Lambda+G_mat)[0]))
            tkonst = -1.9/Eval
            return(min(tkonst))   
            
        if self.num_of_temp == 3: 
            """
            Consider the case of a three temperature odel and follow the same 
            procedure as in the two TM case, except for now take all the coupling
            constants int consideration! 
            """
            if self.temp_data.collocpts is not self.temp_data_Lat.collocpts: 
                self.temp_data_Lat.collocpts = self.temp_data.collocpts 
                print('-----------------------------------------------------------')
                print('The number of collocation points in the electron system \n'\
                      'is not the same as in the lattice system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------') 
            if self.temp_data.collocpts is not self.temp_data_Spin.collocpts: 
                self.temp_data_Spin.collocpts = self.temp_data.collocpts 
                print('-----------------------------------------------------------')
                print('The number of collocation points in the electron system \n'\
                      'is not the same as in the spin system.\n'\
                      'They are set equal to avoid matrix dimension missmatch.')
                print('-----------------------------------------------------------') 
            [c,A00_L,Abig,A1b,A2b_L,Cb,length,N,plp,xflat,x_plt_flat,initphi_large,interfaces,LayerMat,A1h]  = self.temp_data_Lat.Msetup()
            A00_L[0,0] = 1; A00_L[-1,-1] = 1  
            rho = self.temp_data_Lat.rho
            #Load different coupling constants and make them arrays
            G_EL = self.coupling;       G_EL = np.asarray(G_EL)
            G_LS = self.coupling_LS;    G_LS = np.asarray(G_LS)
            G_SE = self.coupling_SE;    G_SE = np.asarray(G_SE)
            conductivity_L = self.temp_data_Lat.conductivity
            conductivity_L = np.asarray(conductivity_L)
            conductivity_S = self.temp_data_Spin.conductivity
            conductivity_S = np.asarray(conductivity_S)
            heatCapacity_L = self.temp_data_Lat.heatCapacity
            heatCapacity_L = np.asarray(heatCapacity_L)
            heatCapacity_S = self.temp_data_Spin.heatCapacity
            heatCapacity_S = np.asarray(heatCapacity_S)
            #In case heatCapacity is a function C(T) we compute a worst case scenario
            #That is we reduce the problem into a constant coefficient case
            for i in range(0,len(conductivity_L)): 
                if not isinstance(conductivity_L[i],(int,float,type(typecheck))): 
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    conductivity_L[i] = max(conductivity_L[i](testT))
            for i in range(0,len(conductivity_S)): 
                if not isinstance(conductivity_S[i],(int,float,type(typecheck))): 
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    conductivity_S[i] = max(conductivity_S[i](testT))
            for i in range(0,len(heatCapacity_L)): 
                if not isinstance(heatCapacity_L[i],(int,float,type(typecheck))): 
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    heatCapacity_L[i] = min(heatCapacity_L[i](testT))
            for i in range(0,len(heatCapacity_S)): 
                if not isinstance(heatCapacity_S[i],(int,float,type(typecheck))): 
                    testT = np.linspace(self.stability_lim[0],self.stability_lim[1],50)
                    heatCapacity_S[i] = min(heatCapacity_S[i](testT))
            #construct Matrices for the Kronecker product
            K11 = np.array([[1,0,0],[0,0,0],[0,0,0]])
            K12 = np.array([[0,1,0],[0,0,0],[0,0,0]])
            K13 = np.array([[0,0,1],[0,0,0],[0,0,0]])
            K21 = np.array([[0,0,0],[1,0,0],[0,0,0]])
            K22 = np.array([[0,0,0],[0,1,0],[0,0,0]])
            K23 = np.array([[0,0,0],[0,0,1],[0,0,0]])
            K31 = np.array([[0,0,0],[0,0,0],[1,0,0]])
            K32 = np.array([[0,0,0],[0,0,0],[0,1,0]])
            K33 = np.array([[0,0,0],[0,0,0],[0,0,1]])
            #Unity matrix for kronecker product on the RHS and palce to store Eval
            unity = np.eye(np.shape(LayerMat)[1])
            Eval  = np.zeros(interfaces+1)
            #Compute the minimum eigenvalue for every layer
            for i in range(0,interfaces+1): 
                coeff_E = conductivity_E[i]/(heatCapacity_E[i]*rho[i])
                coeff_L = conductivity_L[i]/(heatCapacity_L[i]*rho[i])
                coeff_S = conductivity_S[i]/(heatCapacity_S[i]*rho[i])
                Lambda =  np.kron(K11,coeff_E*LayerMat[i])
                Lambda += np.kron(K22,coeff_L*LayerMat[i])
                Lambda += np.kron(K33,coeff_S*LayerMat[i])
                G_mat = np.kron(K11,-unity*coeff_E*(G_EL[i]+G_SE[i]))
                G_mat += np.kron(K12,unity*coeff_E*G_EL[i]) 
                G_mat += np.kron(K13,unity*coeff_E*G_SE[i]) 
                G_mat += np.kron(K21,unity*coeff_L*G_EL[i])
                G_mat += np.kron(K22,-unity*coeff_L*(G_EL[i]+G_LS[i]))
                G_mat += np.kron(K23,unity*coeff_L*G_LS[i])
                G_mat += np.kron(K31,unity*coeff_S*G_SE[i])
                G_mat += np.kron(K32,unity*coeff_S*G_LS[i])
                G_mat += np.kron(K33,-unity*coeff_S*(G_SE[i]+G_LS[i]))
                #Compute the minimum eigenvalue for each layer
                Eval[i] = min(np.real(np.linalg.eig(Lambda+G_mat)[0]))
            tkonst = -1.9/Eval
            #The global time constant will be guided by the fastest dynamics
            #of all the layers!
            return(min(tkonst))
   
        else: 
            #if there is only electron temperature, only those dynamics will be
            #considered, when time step for the E.E. loop is calculated.
            return(min(tkonst_E))
        

class source(object):

    def __init__(self): 
        self.spaceprofile   = 'TMM'
        self.timeprofile    = 'Gaussian'
        self.fluence        = 0
        self.t0             = 0
        self.FWHM           = False
        self.loadData       = False
        self.multipulse     = False
        self.frequency      = False
        self.num_of_pulses  = False
        self.adjusted_grid  = False
        self.dt0            = False
        self.extra_points   = 200
        self.theta_in       = 0# 0 is perpendicular to surface/ pi/2 is grazing
        self.lambda_vac     = False
        self.polarization   = 'p' 
        
    def getProperties(self): # to depict the properties of the object
        for i in (self.__dict__): 
            name = str(i)
            value = str(self.__dict__[i])
            print('{:<20}{:>10}'.format( name,value ))
            
    def __repr__(self): 
        return('Source')
        
    def ref2delta(self,refindex,lambdavac): 
        """
        Use the refractive index and compute the optical penetration depth
        This is used for Lambert Beer´s absorption law. 
        """
        lambdavac_m = lambdavac*1e-9 
        #corp away the two layers of air and only consider target film layers
        refindex = refindex[1:-1]
        #If there is no imaginary part we avoid dividing over 0
        for i in range(0,len(refindex)): 
            if np.imag(refindex[i]) == 0: 
                refindex[i] = refindex[i] + 1e-9j        
        deltap = (4*np.pi/lambdavac_m*np.imag(refindex))**(-1)
        return(deltap)
           
    def Gaussian(self,xmg,tmg,lam,A,sigma2,x0,customtime = None):
        if not (self.fluence or self.FWHM):
            print('------------------------------------------------------------')
            print('Create a pulse with defining pulse properties. \n ' +\
                  '.fluence, .optical_penetration_depth, .FWHM')
            print('------------------------------------------------------------')
        if np.any(customtime) == None:
            #Create a source with respect to each lam of every layer. Use the init_G_source function
            Gauss = A*np.exp(-(tmg-self.t0)**2/(2*sigma2)) #Gaussian in time
        else: 
            Gauss = A*customtime#custom in time
        Gauss *= lam*np.exp(-lam*(xmg-x0))#space profile: LB decay
        return(Gauss)
        
    def init_G_source(self,xflat,x0,t,opt_pen,N,func,customtime = None,scaling = 0):
        """
        First an empty array 'sourceM' is created.
        Then we iterate over the different layers and call
        func --> Gaussian. 
        This will create a 2D (time, space) Gaussian source grid
        with different lam[i].
        For each layer, the problem is receted, i.e. we have new
        Amplitude, new scope of the x-grid, new lambda. Only sigma stays the same.
        """
        lam = 1/opt_pen 
        #create space for solution of source in matrix form
        xmg, tmg = np.meshgrid(xflat,t)
        sourceM  = np.zeros(np.shape(xmg))
        if np.any(customtime) == None:
            #Convert the input, fluence & FWHM given in 'source' class to Amplitude and sigma
            sigma2 = self.FWHM**2/(2*np.log(2))
            A = self.fluence/np.sqrt(2*np.pi*sigma2)
            #loop over all layers and change lambda, Amplitude and scope of the x-grid
            startL = 0; endL = N-1
            for i in range(2,len(opt_pen)+2):
                sourceM[:,startL:endL] = func(xmg[:,startL:endL],tmg[:,startL:endL],lam[i-2],A,sigma2,x0[i-2])            
                #at the end of each loop: the intensity of the end of previous layer
                #will be the starting intensity of the next layer
                A = A*np.exp(-(x0[i-1]-x0[i-2])*lam[i-2])
                startL = endL; endL = i*N-i+1
        else:#In the case of LB in space and custom in time
            if (self.timeprofile== "RepGaussian") or (self.timeprofile=="repGaussian"):
                sigma2 = self.FWHM**2/(2*np.log(2))
                A = self.fluence/np.sqrt(2*np.pi*sigma2)
                startL = 0; endL = N-1
                for i in range(2,len(opt_pen)+2):
                    sourceM[:,startL:endL] = func(xmg[:,startL:endL],tmg[:,startL:endL],lam[i-2],A,sigma2,x0[i-2],customtime[:,startL:endL])            
                    #at the end of each loop: the intensity of the end of previous layer
                    #will be the starting intensity of the next layer
                    A = A*np.exp(-(x0[i-1]-x0[i-2])*lam[i-2])
                    startL = endL; endL = i*N-i+1
            if (self.timeprofile== "custom") or (self.timeprofile == "Custom"):
                A      = scaling#calculated in the custom() function
                sigma2 = 0#It is not needed
                startL = 0; endL = N-1
                for i in range(2,len(opt_pen)+2):
                    sourceM[:,startL:endL] = func(xmg[:,startL:endL],tmg[:,startL:endL],lam[i-2],A,sigma2,x0[i-2],customtime[:,startL:endL])            
                    #at the end of each loop: the intensity of the end of previous layer
                    #will be the starting intensity of the next layer
                    A = A*np.exp(-(x0[i-1]-x0[i-2])*lam[i-2])
                    startL = endL; endL = i*N-i+1
        return(sourceM)

    #mytime is the timegrid of the simulation
    #time, amplitude are the timegrids of the inputdata collected from the lab    
    def custom(self,mytime,myspace,ttime,amplitude,opt_pen):
        lam = 1/opt_pen
        #Mapping the obtained data to the simulation time grid via interpolation
        ampl1D = np.interp(mytime,ttime,amplitude**2)
        #Compute the right amplitude. using the area under the curve
        integr = np.trapz(ampl1D,mytime,np.diff(mytime))
        #scling factore to get the amplitude right
        scaling = self.fluence/integr
        xmg,tmg = np.meshgrid(myspace,mytime)
        ampltime= np.interp(tmg,ttime,amplitude**2)
        #ampltime *= scaling
        ampl2D = ampltime*lam*np.exp(-lam*xmg)
        return(ampl2D,ampltime,scaling)
        
        
    def fresnel(self,theta_in,n_in,n_out,pol): 
        n_in = complex(n_in); n_out = complex(n_out)
        theta_out = np.arcsin(n_in*np.sin(theta_in)/n_out)
        if pol == 's': 
            rs = (n_in*np.cos(theta_in) - n_out*np.cos(theta_out))/\
                 (n_in*np.cos(theta_in) + n_out*np.cos(theta_out))
            ts = 2*n_in*np.cos(theta_in)/(n_in*np.cos(theta_in)+n_out*np.cos(theta_out))
            return(theta_out,rs,ts)
        if pol == 'p':
            rp = (n_out*np.cos(theta_in)-n_in*np.cos(theta_out))/\
                 (n_out*np.cos(theta_in)+n_in*np.cos(theta_out))
            tp = 2* n_in*np.cos(theta_in)/(n_out*np.cos(theta_in)+n_in*np.cos(theta_out))
            return(theta_out,rp,tp) 
    
    def TM(self,theta_in,lambda0,n_vec,d_vec,pol): 
        #create complex arrays for variables
        theta   = np.zeros(len(n_vec), dtype = complex); theta[0] = theta_in
        phi     = np.zeros(len(n_vec),dtype = complex)
        rn      = np.zeros(len(n_vec)-1, dtype = complex) 
        tn      = np.zeros_like(rn,dtype = complex)
        M_n     = np.zeros((len(n_vec),2,2), dtype = complex)
        M       = np.eye(2,dtype = complex)
        for i in range(len(n_vec)-1): # to obtian all angels/rn/tn for each layer
            [theta[i+1],rn[i],tn[i]] = self.fresnel(theta[i],n_vec[i],n_vec[i+1],pol)
        #M = M0*M1*M2*M4*....
        for k in range(1,len(n_vec)-1):#loop over all interfaces except 1st
            phi[k]  = 2*np.pi*n_vec[k]*np.cos(theta[k])*d_vec[k]/lambda0
            Tn      = np.array([[np.exp(-1j*phi[k]),0],[0,np.exp(1j*phi[k])]],dtype = complex)/tn[k]
            Pn      = np.array([[1,rn[k]],[rn[k],1]],dtype = complex)
            M_n[k]     = np.dot(Tn,Pn)
            M = np.dot(M,M_n[k])
        #compute for the first interface: 
        trans0 = np.array([[1,rn[0]],[rn[0],1]],dtype= complex)/tn[0]
        M = np.dot(trans0,M)
        #Complex transmission/reflection amplitude
        t = 1/M[0,0]
        r = M[1,0]/M[0,0]
        #Fraction of power transmitted
        if pol == 's': #s-polarized
            T = np.abs(t)**2*np.real(n_vec[-1]*np.cos(theta[-1]))/\
                np.real(n_vec[0]*np.cos(theta[0]))
        elif pol == 'p': #p-polarized
            T = np.abs(t)**2*np.real(n_vec[-1]*np.cos(np.conj(theta[-1])))/\
                np.real(n_vec[0]*np.cos(np.conj(theta[0])))
        #Fraction of power reflected
        R = np.abs(r)**2
        A = 1.-T-R
        return(M,M_n,t,r,T,R,A,theta)
    
    def layerAmpl(self,theta_in,lambda0,n_vec,d_vec,pol): 
        """
        After r & t have been calculated and all the respective matrices M_n
        for each layer are known, we can go 'backwards', i.e. from the last to the
        first layer, and compute all the amplituedes for the forward v_n and 
        backward w_n traveling wave. -> [v_n,w_n].T = M_n @ [v_{n+1},w_{n+1}].T
        """
        [M,M_n,t,r,T,R,A,theta] = self.TM(theta_in,lambda0,n_vec,d_vec,pol)
        vw_list = np.zeros((len(n_vec),2),dtype = complex)
        vw =np.array([[t],[0]])
        vw_list[-1,:] = vw.T
        for i in range(len(n_vec)-2,0,-1):
            vw = np.dot(M_n[i],vw)
            vw_list[i,:] = vw.T
        return(vw_list,theta)
        
    def absorption(self,theta_in,lambda0,n_vec,d_vec,pol,points):
        #reload the forward and backward wave coefficients for every layer
        [vw_n,theta]  = self.layerAmpl(theta_in,lambda0,n_vec,d_vec,pol)
        total_len = np.sum(d_vec[1:-1])
        pointcount = 0
        #a is an array where the normalized absorbtion for the entire grid is stored 
        a = []
        for i in range(1,len(n_vec)-1):
            kz      = 2*np.pi*n_vec[i]*np.cos(theta[i])/lambda0
            #How many points, out of the total 'points' does each layer get, with respect to 
            #the length of the layer
            if i == 1: 
                points_per_layer = int(np.floor(points/(len(d_vec)-2)))+1
                if len(n_vec)-1 == 2: #only one layer is considered
                    points_per_layer = points
            else: #All other layers get 11 points because of interface cutting
                points_per_layer = int(np.floor(points/(len(d_vec)-2)))
            #for every layer, the space grid is reset. I.e. every layer starts at 0
            layer   = np.linspace(0,d_vec[i],points_per_layer)
            v = vw_n[i,0]; w = vw_n[i,1];#complex wave amplitudes for every layer
            Ef = v * np.exp(1j * kz * layer)#forward traveling wave 
            Eb = w * np.exp(-1j * kz *layer)#backward traveling wave
            if pol == 'p':#p-polarized
                a_layer = (n_vec[i]*np.conj(np.cos(theta[i]))*(kz*np.abs(Ef-Eb)**2-np.conj(kz)*np.abs(Ef+Eb)**2)).imag /\
                        (n_vec[0]*np.conj(np.cos(theta[0]))).real
            if pol == 's': 
                a_layer = (np.abs(Ef+Eb)**2 *np.imag(kz*n_vec[i]*np.cos(theta[i])))/\
                        (np.real(n_vec[0]*np.cos(theta[0])))
            #for every layer calculate the absorbtion grid and append it to the total 
            a   = np.append(a,a_layer)
            #to get the right amount of points considered in the grid, since we round.
            pointcount += points_per_layer 
        a = np.real(a)
        grid = np.linspace(0,total_len,pointcount)
        return(a,grid)
           
    def createTMM(self,nvec,xflat,t,x0,timeprof = False,scaling=0): 
        #The distances and hence x0 have to be given in units of nm!
        xmg, tmg = np.meshgrid(xflat,t)
        #Adding infinite layer at the beginning and at the end of the distance vector
        d_vec   = np.diff(x0); d_vec = np.insert(d_vec,(0,len(d_vec)),np.inf) 
        #Calculating the 1D absorption profile according to TMM
        [absorption,grid] = self.absorption(self.theta_in,self.lambda_vac,nvec,d_vec,self.polarization,np.shape(xflat)[0])
        #Evaluate the Gaussian time profile 
        if np.any(timeprof) == False:
            #Convert the input, fluence & FWHM given in 'source' class to Amplitude and sigma
            sigma2  = self.FWHM**2/(2*np.log(2))
            A       = self.fluence/np.sqrt(2*np.pi*sigma2)
            sourceM = A*np.exp(-(tmg-self.t0)**2/(2*sigma2))
        if (self.timeprofile == "repGaussian") or (self.timeprofile == "RepGaussian"):
            sigma2  = self.FWHM**2/(2*np.log(2))
            A       = self.fluence/np.sqrt(2*np.pi*sigma2)
            sourceM = A*timeprof
        if (self.timeprofile == "Custom") or (self.timeprofile == "custom"):
            #Check the custom function in this class! It is already multiplied with a scaling factor 
            sourceM = scaling*timeprof
        #Multiplying it with the absorption profile to obtain 2D (space-time source map)
        sourceM *= absorption/1e-9
        return(sourceM)
        
class visual(object): 
    
    def __init__(self,*args):
        self.data = False
        typecheck = np.array([])
        if isinstance(args[0],(float,int,list,type(typecheck)))== True:
            #If arrays are passed on
            if len(args) == 4:
                self.T_E = args[0]
                self.T_L = args[1]
                self.x = args[2]
                self.t = args[3]
            if len(args) == 3:
                self.T_E = args[1]
                self.x = args[2]
                self.t = args[3]
            if len(args) < 3: 
                print('Not enough input arguments are given. \n Pass on \'Electron temperature\', \'x-grid\', \'time grid\'. \n'\
                      'They are output of simulation.run(). ')
            if len(args)>5: 
                print('Too many input arguments are given. \n Pass on \'Electron temperature\', \'x-grid\', \'time grid\'. \n'\
                      'They are output of simulation.run(). ')
        #If the simulation object is passed on          
        else:
            self.sim = args[0]
            print('------------------------------------------------------------')
            print('The simulation object of the '+str(self.sim.num_of_temp)+' temerature system has been passed on to the visual class.')
            print('------------------------------------------------------------') 
            #three temperature case 
            if (self.sim.num_of_temp == 3 and self.data == False):   
                [self.x, self.t,T] = self.sim.run()
                self.T_E = T[0]; self.T_L = T[1]; self.T_S = T[2]
                self.so     = self.sim.source
                x0          = self.sim.temp_data.length
                d_vec       = np.diff(x0);
                d_vec       = np.insert(d_vec,(0,len(d_vec)),np.inf) 
                self.dvec   = d_vec
                self.data   = True
                #two temperature case (Electron, Lattice)
            if (self.sim.num_of_temp == 2 and self.data == False):  
                [self.x, self.t,T]    = self.sim.run()
                self.T_E = T[0]; self.T_L = T[1]
                self.so                                 = self.sim.source
                x0          = self.sim.temp_data.length
                d_vec       = np.diff(x0);
                d_vec       = np.insert(d_vec,(0,len(d_vec)),np.inf) 
                self.dvec   = d_vec
                self.data   = True
                #1 temperature case Electron
            if (self.sim.num_of_temp == 1 and self.data == False): 
                [self.x, self.t,self.T_E]              = self.sim.run()
                self.so                                 = self.sim.source 
                x0          = self.sim.temp_data.length
                d_vec       = np.diff(x0);
                d_vec       = np.insert(d_vec,(0,len(d_vec)),np.inf)
                self.dvec   = d_vec
                self.data   = True
    def __repr__(self): 
        return('Visual')
        
    def source(self):
        s = self.sim.sourceprofile(self.so.spaceprofile,self.so.timeprofile,self.x,self.sim.temp_data.length,self.t,self.sim.temp_data.plt_points)
        xx,tt = np.meshgrid(self.x,self.t)
        fig  = plt.figure()
        ax   = fig.gca(projection='3d')
        if (np.mean(self.x) <1e-7 and np.mean(self.t)<1e-10):
            surf = ax.plot_surface(xx/1e-9,tt/1e-12,s,cmap = 'jet')
            plt.xlabel('Depth from surface into material in nm',fontsize = 14)
            plt.ylabel('time  in ps',fontsize = 14)
        else: 
            surf = ax.plot_surface(xx,tt,s,cmap = 'jet')
            plt.xlabel('Depth from surface into material in m',fontsize = 14)
            plt.ylabel('time in s',fontsize = 14) 
            
        cb = plt.colorbar(surf,orientation='vertical', shrink=0.8,aspect = 5)
        cb.ax.tick_params(labelsize=14)
        cb.set_label(r"Absorbed power density $\mathrm{W}/\mathrm{m}^3$",fontsize = 14)
        plt.title(r'S(x,t)',fontsize = 14)
        plt.show()
        #A contour plot
        plt.figure()
        plt.title("Contour plot of input source",fontsize = 14)
        plt.xlabel("Depth into material from surface in m",fontsize = 14)
        plt.ylabel("Time profile in s",fontsize = 14)
        plt.contourf(xx,tt,s,cmap = 'jet')
        cb = plt.colorbar(surf,orientation='vertical', shrink=0.8,aspect = 5)
        cb.ax.tick_params(labelsize=14)
        cb.set_label(r"Absorbed power density $\mathrm{W}/\mathrm{m}^3$",fontsize = 14)
        plt.show()
        return(s)
        
    def localAbsorption(self): 
        """
        Gives back the local absorption profile in space at a given point in time. 
        This only works when Transfer matrix is being considered! 
        """
        #Adding infinite layer at the beginning and at the end of the distance vector
        d_vec   = np.diff(self.sim.temp_data.length*1e9);
        d_vec  = np.insert(d_vec,(0,len(d_vec)),np.inf) 
        xflat = self.x
        
        #Calculating the 1D absorption profile according to TMM
        [absorption,grid] = self.so.absorption(self.so.theta_in,self.so.lambda_vac,self.sim.temp_data.n,d_vec,self.so.polarization,np.shape(xflat)[0])
        [M,M_n,trans,r,T,R,A,theta] = self.so.TM(self.so.theta_in,self.so.lambda_vac,self.sim.temp_data.n,d_vec,self.so.polarization)
        
        plt.figure()
        plt.suptitle("Local absorption profile",fontsize = 14)
        plt.title("Total absorption = {abso:.2f}".format(abso = A ),fontsize=12)
        plt.xlabel("Distance from surface",fontsize = 14)
        plt.ylabel("Absorption per unit incident power",fontsize = 14)
        plt.plot(xflat,absorption)
        return(T,R,A,absorption,xflat,grid)
        
    def contour(self,*args):
        T = self.T_E
        if args:
            name = args
        if '3' in args:
            T = self.T_S
            name = args
            if self.sim.num_of_temp != 3:
                print('The spin temperature can not be considered, since it has not been simulated yet. \n '\
                      'Initialize spin parameters and simulate them first. \n '\
                      'First argument of the simulation class sould be 3 for 3 temperatures.')
        if '2' in args:
            T = self.T_L
            name = args
            if self.sim.num_of_temp < 2:
                print('The lattice temperature can not be considered, since it has not been simulated yet. \n '\
                      'Initialize lattice parameters and simulate them first.\n '\
                      'First argument of the simulation class sould be 2 for 2 temperatures.')
        #cblabels = np.linspace(np.floor(np.min(T)),np.ceil(np.max(T)),5)
        plt.figure()
        plt.title(r'$T(x,t)$ in K',fontsize = 14)
        plt.xlabel('x- Space in m')
        plt.ylabel('Time in s')
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        xx,tt = np.meshgrid(self.x,self.t)
        if ((np.mean(self.x) <1e-6) and (np.mean(self.t)<1e-9)):
            xx,tt = np.meshgrid(self.x/1e-9,self.t/1e-12) 
            plt.xlabel('x- Space in nm',fontsize = 14)
            plt.ylabel('Time in ps',fontsize = 14)
        plt.contourf(xx,tt,T,50,cmap = 'plasma')
        cb = plt.colorbar( orientation='vertical', shrink=0.8)
        cb.ax.tick_params(labelsize=14)
        cb.set_label(r"$T(x,t)$ in K",fontsize = 14)
        if args:
            plt.title(r'Temperature of system ' +str(name),fontsize = 14)    
        plt.show()
    
    def average(self):
        """
        Averages the temperature map in space and depicts the data
        with respect to time. 
        Note, that if one includes a substrate this routine is not very insightful, 
        since the averaging will mostly depic the temperature of the substrate 
        and not the one of the target layer. 
        It returns [timegrid, Averagedtemperatures]
        Here timegrid is a vectro and Averaged_Temperature is an array, where
        the rows correspond to different systems and the colums to 
        averaged points at a certain time.
        """
        #load Data for weighted means
        points          = self.sim.temp_data.plt_points
        tot_length      = self.sim.temp_data.length[-1]
        len_of_layer    = np.diff(self.sim.temp_data.length)
        tps             = self.t.copy()
        if self.sim.num_of_temp == 3:#electron lattice and spin temperature under consideration
            #Take weighted averages with respect to the length of each layer
            avT_E = len_of_layer[0]/tot_length*np.mean(self.T_E[:,0:points-1],1)
            avT_L = len_of_layer[0]/tot_length*np.mean(self.T_L[:,0:points-1],1)
            avT_S = len_of_layer[0]/tot_length*np.mean(self.T_S[:,0:points-1],1)
            for i in range(1,len(len_of_layer)):
                avT_E += len_of_layer[i]/tot_length*np.mean(self.T_E[:,i*points:(i+1)*points],1)
                avT_L += len_of_layer[i]/tot_length*np.mean(self.T_L[:,i*points:(i+1)*points],1)
                avT_S += len_of_layer[i]/tot_length*np.mean(self.T_S[:,i*points:(i+1)*points],1)
            T = np.concatenate(([avT_E],[avT_L],[avT_S]),axis=0) 
            plt.figure()
            plt.xlabel(r'Time in s',fontsize = 14)
            plt.ylabel(r'Temperature in K',fontsize = 14)
            plt.tick_params(axis='x', labelsize=14)
            plt.tick_params(axis='y', labelsize=14)
            if np.mean(tps) < 1e-9: 
                tps/=1e-12
                plt.xlabel(r'Time in ps',fontsize = 14)
                plt.ylabel(r'Temperature in K',fontsize = 14)
            plt.plot(tps,avT_S,c = 'b',label = 'System 3')
            plt.plot(tps,avT_L,c = 'k',label = 'System 2')
            plt.plot(tps,avT_E,c = 'r',label = 'System 1')
            plt.title('Temperature averaged in space vs time',fontsize = 14)
            plt.grid()
            plt.legend()
            plt.show()
            return(self.t,T)
        
        if self.sim.num_of_temp == 2:#electron and lattice temperature under consideration
            #Take weighted averages with respect to the length of each layer
            avT_E = len_of_layer[0]/tot_length*np.mean(self.T_E[:,0:points-1],1)
            avT_L = len_of_layer[0]/tot_length*np.mean(self.T_L[:,0:points-1],1)
            for i in range(1,len(len_of_layer)):
                avT_E += len_of_layer[i]/tot_length*np.mean(self.T_E[:,i*points:(i+1)*points],1)
                avT_L += len_of_layer[i]/tot_length*np.mean(self.T_L[:,i*points:(i+1)*points],1)
            T = np.concatenate(([avT_E],[avT_L]),axis=0) 
            plt.figure()
            plt.xlabel(r'Time in s',fontsize = 14)
            plt.ylabel(r'Temperature in K',fontsize = 14)
            if np.mean(tps) < 1e-9: 
                tps/=1e-12
                plt.xlabel(r'Time in ps',fontsize = 14)
                plt.ylabel(r'Temperature in K',fontsize = 14)   
            plt.plot(tps,avT_L,c = 'k',label = 'System 2')
            plt.plot(tps,avT_E,c = 'r',label = 'System 1')
            plt.title('Temperature averaged in space vs time',fontsize = 14)
            plt.grid()
            plt.legend()
            plt.show()
            return(self.t,T)
            
        else:#only electron temperature under consideration
            #Take the weighted mean with respect to length of layer only for T_E
            avT_E = len_of_layer[0]/tot_length*np.mean(self.T_E[:,0:points-1],1)
            for i in range(1,len(len_of_layer)):
                avT_E += len_of_layer[i]/tot_length*np.mean(self.T_E[:,i*points:(i+1)*points],1)
                
            plt.figure()
            plt.xlabel(r'Time in s',fontsize = 14)
            plt.ylabel(r'Temperature in K',fontsize = 14)
            if np.mean(tps) < 1e-9: 
                tps/=1e-12                
                plt.xlabel(r'Time in ps',fontsize = 14)
                plt.ylabel(r'Temperature in K',fontsize = 14)   
            plt.plot(tps,avT_E,c = 'r',label = 'System 1')
            plt.title('Temperature averaged in space vs time')
            plt.grid()
            plt.legend()
            plt.show()
            return(self.t,avT_E)
            
    #IN: vector to block, time grid, num_blocks,   
    def blocking(self,vector,tt,blocks):
        """
        This is a function which helps to process big data files more easily
        by the method of block averaging. 
        For this the first argument is a vector with data, e.g. averaged temperature
        the second argument is another vector, e.g. time grid. 
        The third argument should be the number of blocks. 
        The more blocks, the more data points are taken into consideration. 
        If less blocks, more averaging takes place.
        """
        blockvec = np.zeros(blocks)
        elements = len(vector) 
        rest     = elements % blocks
        if rest != 0: #truncate vector if number of blocks dont fit in vector
            vector   = vector[0:-rest]
            tt       = tt[0:-rest]
            elements = len(vector)   
        meanA  = np.mean(vector)        
        bdata  = int((elements/blocks))#how many points per block
        sigBsq = 0; 
        for k in range(0,blocks):
            blockvec[k] = np.average(vector[k*bdata : (k+1)*bdata]) 
            sigBsq      = sigBsq + (blockvec[k]-meanA)**2    
        sigBsq *= 1/(blocks-1); 
        sigmaB = np.sqrt(sigBsq)
        error  = 1/np.sqrt(blocks)*sigmaB
        blocktt = tt[0:-1:bdata]
        return(blockvec,blocktt, error , sigmaB)
            
    def timegrid(self):
        """
        Plotting delta t_i vs t_i. This is the width of the timesteps
        with respect to the point of the timegrid where we are right now.:
        This is relevant, once adjusted_grid (in the source class )is True.
        """
        tstep = np.ones(len(self.t))
        tstep[:-1] = np.diff(self.t); tstep[-1] = np.diff(self.t)[-1]
        plt.figure()
        plt.plot(self.t,tstep,'-o')
        plt.xlabel('Time grid $t_i$'); plt.ylabel('$\Delta t_i$')
        plt.title('$\Delta t_i = t_{i+1}-t_i$ vs t_i')    
            
    def animation(self,speed,sve = 0): 
        """
        The animation function has two arguments animation(speed,save). 
        Speed is an integer number, the higher, the faster the simulation
        If save == 1, then the animation gets saved to the local machine. 
        Note for this you have to have a ffmpeg write installed and included to your 
        local variables. 
        https://m.wikihow.com/Install-FFmpeg-on-Windows
        """
        if len(self.t) % speed != 0:
            speed = speed-(len(self.t)%speed)
            print('Speed of animation',speed)
         
        fig, ax = plt.subplots()
        lineE, = ax.plot([], [],'r' , animated=True,label = 'System 1 Temp. in [K]')
        #if there is only one temperature, then the lineL is just a placeholder for the update function
        if self.sim.num_of_temp == 3:
            lineL, = ax.plot([],[],'k',animated = True,label = 'System 2 Temp. in [K]')
            lineS, = ax.plot([],[],'b',animated = True,label = 'System 3 Temp. in [K]')
            ax.set_xlim(0, self.x[-1]); ax.set_ylim(np.min((self.T_L,self.T_E,self.T_S))-(np.mean(self.T_E)-np.min((self.T_L,self.T_E,self.T_S)))/2,\
                        np.max((self.T_E,self.T_L,self.T_S))+(np.max(self.T_E)-np.mean(self.T_E))/2)
        if self.sim.num_of_temp == 2:
            print("Simulation of a 2- temperature system")
            lineS, = ax.plot([],[],'r',animated = True)
            self.T_S = self.T_E
            lineL, = ax.plot([],[],'k',animated = True,label = 'System 2 Temp. in [K]')
            ax.set_xlim(0, self.x[-1]); ax.set_ylim(np.min((self.T_L,self.T_E))-(np.mean(self.T_E)-np.min((self.T_L,self.T_E)))/2,\
                        np.max((self.T_E,self.T_L))+(np.max(self.T_E)-np.mean(self.T_E))/2)
        if self.sim.num_of_temp == 1: 
            print("Simulation of a 1-temperature system")
            lineL, = ax.plot([],[],'r',animated = True)
            lineS, = ax.plot([],[],'r',animated = True)
            self.T_L = self.T_E
            self.T_S = self.T_E
            ax.set_xlim(0, self.x[-1]); ax.set_ylim(np.min((self.T_L,self.T_E))-(np.mean(self.T_E)-np.min((self.T_L,self.T_E)))/2,\
                        np.max((self.T_E,self.T_L))+(np.max(self.T_E)-np.mean(self.T_E))/2)
        time_text = ax.text(0.02, 0.95, "", transform = ax.transAxes)
        plt.xlabel('Depth of Material',fontsize = 14); plt.ylabel('Temperature',fontsize = 14)
        plt.title('Evolution of Temperature in space and time',fontsize = 14)
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        plt.legend()
        
        def update(frame):
            lineE.set_data(self.x,self.T_E[speed*frame,:])
            lineL.set_data(self.x,self.T_L[speed*frame,:])
            lineS.set_data(self.x,self.T_S[speed*frame,:])
            time_text.set_text(f"time =  {self.t[speed*frame]:.2e}  s")
            if speed*frame >= len(self.t)-speed: 
                ani.event_source.stop()
            return lineS, lineL,lineE, time_text
        
        ani = movie(fig, update, blit=True,save_count = 2000,interval = 15, repeat = True) 
        plt.grid()
        plt.show()
        if sve ==1: 
            ani.save("animation.mp4")
            return(ani) 
