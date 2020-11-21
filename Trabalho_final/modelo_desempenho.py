from acft_evaluators.Aircraft_evaluators import aiplane_evaluator
import matplotlib
import pandas as pd
import numpy as np
from fluids.atmosphere import ATMOSPHERE_1976

def takeoff_run(aircraft,params):
    results=[]
    for altitude in params['altitudes']:
        for deltaT in params['temperatures']:
            list1=[]
            list2=[]
            for TOW in params['TOWs']:
                list1.append(TOW)
                atmos=ATMOSPHERE_1976(altitude,deltaT)
                x=0
                v=0
                F_aero_max=0
                while x<6000:
                    F_aero=bae146.aero_evaluator(atmos,v,0)
                    F_aero_max=bae146.aero_evaluator(atmos,v,20)
                    Thrust,consumption=bae146.thrust_evaluator(atmos)
                    net_force=Thrust-F_aero[1]-TOW*9.81*bae146.fric_coeff
                    a=net_force/TOW
                    x = x + v + a*a/2
                    v=v+a
                    if F_aero_max[0]>TOW*9.81:
                        break
                results.append({'h':altitude,'deltaT':deltaT,'TOW':TOW,'x-TO':x,'v-TO':v})
    results=pd.DataFrame(results)
    print('xupaita')



if __name__=='__main__':





    ##########################################
    # Definition of aircraft parameters
    ##########################################

    bae146=aiplane_evaluator('Bae-146',77.3)
    bae146.load_aerodynamics('Polares.xlsx')
    bae146.load_engines(static_trust=4*31000,n=0.7,TSFC=4*41.4/1000)
    bae146.add_friction(mu=0.1)
    bae146.define_opWeights(42184,'MTOW')
    bae146.define_opWeights(11233, 'MPL')
    bae146.define_opWeights(24600, 'OEW')
    bae146.define_opWeights(24600+11233, 'MZFW')
    bae146.define_opWeights(0.804*11728, 'MFW')

    ########################################
    # Takeoff modeling
    ########################################
    params={}
    params['Takeoff']={'altitudes':[x for x in range(-500,3500,500)],
                       'temperatures':[x for x in range(-30,35,5)],
                       'TOWs':[x for x in range(25000,42200,3000)]
    }
    params['Takeoff']['TOWs'].append(42184)
    Results={}
    Results['Takeoff']=takeoff_run(bae146,params['Takeoff'])

    print('oi')