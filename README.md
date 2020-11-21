# Aircraft Evaluators

Aircraft Evaluators is a library containing definitions and a simplified aerodynamics
and propulsion model for aircraft performance calculations

This lib uses atmosphere models provided by fluis.atmosphere lib
## Installation

Use pip to install the downloaded whl

```bash
<python_path> -m pip install <downloaded_wheel_location/acft_evaluators-1.0.0-py3-none-any.whl>
```

## Usage

```python
import acft_evaluators

#Aircraft definition

acft=acft_evaluators.aiplane_evaluator('aircraft1',S=25) # creates an aircraft with 25m2 of area
acft.load_aerodynamics('.\inut.xlsx') #loads aerodynamics
acft.load_engines(static_trust=1000,dTDh=-0.1,TSFC=0.56) #adds an engine
acft.add_friction(mu=0.2) #adds friction coefficient for runway
acft.opWeights(10000,'MZFW') #defines operation weights

#Model evaluators
acft.aero_evaluator(atmos=atmos,V=200,alpha=10) #calculates aerodynamic forces
acft.thrust_evaluator(atmos=atmos,V=200,engine_set=1) #calculates thrust and consumption
```