import pandas as pd
import numpy as np
import math

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
        self.engines=[]

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

    def load_engines(self,static_trust,dTDh,TSFC):
        """adds one given engine to the aircraft
        Parameters:
            statis_trust (float): statius thrust at sea level [Newtons]
            dTDh (float): thrust derivative over altitude [N/m]
            TSFC (float): thrust specific fuel consumption [kg/Nh]
        """
        engine={'static_trust':static_trust,
                'derivative':dTDh
                'TSFC':TSFC}
        self.engines.append(engine)

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

    def aero_evaluator(self,atmos,V,alpha,engine_set=1):
        """Evaluate net force on earth axis X and Y, for takeoff evaluations
        Parameters:
            atmos (fluid.atmosphere object): atmospheric object for a given state of the aircraft
            V (float): Velocity of the aircraft [m/s EAS]
            alpha(float): angle of attack [degrees]
            engine_set: engine power setting from 0-1 (or higher if emergency power)
        Returns:
            net_forces(numpy array): Net aero forces acting on the aircraft [N]
        """

    def thrust_evaluator(self,atmos,V,engine_set=1):
        """Evaluate the net excess power for a given condition
        Parameters:
            atmos (fluid.atmosphere object): atmospheric object for a given state of the aircraft
            V (float): Velocity of the aircraft (m/s EAS)
            engine_set: engine power setting from 0-1 (or higher if emergency power)
        Returns:
            thrust(float): Sum of all engines thrust [N]
            Consumption(float): engine fuel consumption [Kg/h]
        """
