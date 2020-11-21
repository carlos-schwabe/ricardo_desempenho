import pandas as pd
import numpy as np
import math
import fluids.atmosphere

class aiplane_evaluator(object):
    """Airplane class creates an airplane object with all model characteristics adn creates an evaluator funcion of the net
    force acting on the aircraft on a given state
    Parameters:
        id (str): identifier of the aircraft
        S (float): reference aarea [m2]
    Returns:
        airplane_evaluator (obj): class of airplane"""

    def __init__(self,id,S):
        self.__name__=id
        self.ref_area=S
        self.aerodynamics={}
        self.engines.st=0
        self.engines.dTdh=0
        self.engines.TSFC = 0

    def load_aerodynamics(self,polar_path):
        """Loads aerodynamic data from excel sheet: formating: sheet name: M=<mach number>, column names: AoA;CL;CDtot
        Parameters:
            polar_path (str): path to input excel file
        """
        excel=pd.ExcelFile(polar_path)
        sheets=excel.sheet_names
        for sheet in sheets:
            mach=float(sheet.strip('M='))
            data=excel.parse(sheet)
            self.aerodynamics[mach]=data

    def load_engines(self,static_trust,n,TSFC):
        """adds engines to aicraft
        Parameters:
            statis_trust (float): statius thrust at sea level [Newtons]
            n (float): efficiency parameter
            TSFC (float): thrust specific fuel consumption [kg/Nh]
        """

        self.engine.st=static_trust
        self.engine.n = n
        self.engine.TSFC = TSFC

    def add_friction(self,mu=0):
        """adds friction coefficient to the model
        Parameters:
            mu (float): friction coefficient [N/N]
        """
        self.fric_coeff=mu

    def define_opWeights(self,weight,type):
        """stablishes aircraft weights.
        Parameters:
            Weight(float): Weight [N]
            Type(str): specification (MTOW,TOW,MZFW...)
        """
        setattr(self,type,weight)

    def aero_evaluator(self,atmos,V,alpha):
        """Evaluate net force on earth axis X and Y, for takeoff evaluations
        Parameters:
            atmos (fluid.atmosphere object): atmospheric object for a given state of the aircraft
            V (float): Velocity of the aircraft [m/s TAS]
            alpha(float): angle of attack [degrees]
        Returns:
            net_forces(numpy array): Net aero forces acting on the aircraft [N]
        """
        mach=V/atmos.v_sonic
        rho=atmos.rho

        #available machs

        aero_sorted=OrderedDict(sorted(self.aerodynamics.items()))
        available_machs=[key for key in aero_sorted.keys()]

        #check if mach is within range

        if not available_machs[0]<=mach<=available_machs[-1]:
            raise('Mach out of range')

        #find upper and lower machs

        for key, value in aero_sorted:
            if key==mach:
                aoa_array=np.array(aero_sorted[key]['AoA'].tolist())
                CL_array=np.array(aero_sorted[key]['CL'].tolist())
                CD_array=np.array(aero_sorted[key]['CDtot'].tolist())
            elif key<mach:
                lb_mach = key
                lb_data = aero_sorted[key]
            else:
                ub_mach= key
                ub_data= aero_sorted[key]
                break
        if not data:

            #interpolate by mach

            p=(mach-lb_mach)/(ub_mach-lb_mach)
            aoa_array=np.array(lb_data['AoA'].tolist())
            CL_array=np.array(lb_data['CL'].tolist())*(1-p) + np.array(lb_data['CL'].tolist())*p
            CD_array=np.array(lb_data['CDtot'].tolist())*(1-p) + np.array(lb_data['CDtot'].tolist())*p

        #interpolate by AOA

        if not aoa_array[0]<=alpha<=aoa_array[-1]:
            raise ('AOA out of range')
        CL=np.interp(alpha,aoa_array,CL_array)
        CD= np.interp(alpha,aoa_array,CD_array)

        #Dimensionalise values

        L=0.5*rho*V*V*self.ref_area*CL
        D=0.5*rho*V*V*self.ref_area*CD

        return np.array([L,D])

    def thrust_evaluator(self,atmos,engine_set=1,req_thr=None):
        """Evaluate the net thrust and consumption for a given engine setting or required thrust
        Standard response given as engine setting of 100%
        Parameters:
            atmos (fluid.atmosphere object): atmospheric object for a given state of the aircraft
            engine_set: engine power setting from 0-1 (or higher if emergency power)
            req_trust: required combined thrust in N
        Returns:
            thrust(float): Sum of all engines thrust [N]
            Consumption(float): engine fuel consumption [Kg/h]
        """
        if req_thr:
            max_thrust=self.engine.st*(atmos.rho/1.225)**self.engine.n
            if req_thr>max_thrust:
                raise ('Required Thrust Exceeds maximum thrust for the condition')
            return req_thr, req_thr*self.engine.TSFC
        else:
            thrust = engine_set*self.engine.st * (atmos.rho / 1.225) ** self.engine.n
            consumption=thrust*self.engine.TSFC
            return thrust consumption