import numpy as np
import sys, os
import pandas as pd
import pyreadr


FRIDA_Filenames = {'realGDP': 'gdp_real_gdp_in_2021c.RDS',
                   'realGDPpc': 'demographics_real_gdp_per_person.RDS',
                   'realGDPgrowth': 'gdp_real_gdp_growth_rate.RDS',
                   'inflation': 'inflation_inflation_rate.RDS',
                   'Deaths': 'demographics_total_deaths.RDS',
                   'CO2emis': 'emissions_total_co2_emissions_gtc.RDS',
                   'Temperature': 'energy_balance_model_surface_temperature_anomaly.RDS',
                   'SLR': 'sea_level_total_global_sea_level_anomaly.RDS',
                   'SLR_thermo': 'sea_level_sea_level_anomaly_from_thermal_expansion.RDS',
                   'SLR_LWS': 'sea_level_sea_level_anomaly_from_lws.RDS',
                   'SLR_MG' : 'sea_level_sea_level_anomaly_from_mountain_glaciers.RDS',
                   'SLR_GIS': 'sea_level_sea_level_anomaly_from_greenland_ice_sheet.RDS',
                   'SLR_AIS': 'sea_level_sea_level_anomaly_from_antarctic_ice_sheet.RDS',
                   'Hydrowater': 'sea_level_land_water_storage_from_water_impoundment.RDS',
                   'Groundwater': 'freshwater_total_groundwater_anomaly.RDS',
                   'CoastalAssets_ip': 'coastal_assets_coastal_assets_insufficient.RDS',
                   'CoastalAssets_wp': 'coastal_assets_coastal_assets_well_protected.RDS',
                   'CoastalPopulation_ip': 'coastal_population_coastal_population_insufficient.RDS',
                   'CoastalPopulation_wp': 'coastal_population_coastal_population_well_protected.RDS',
                   'debtRatio': 'government_debt_to_gdp_ratio.RDS',
                   'ProdRedFac': 'sea_level_rise_costs_and_impacts_productivity_reduction_factor_from_coastal_flooding.RDS',
                   'PeopleRCost': 'sea_level_rise_costs_and_impacts_total_people_retreat_costs.RDS',
                   'AssetRCost': 'sea_level_rise_costs_and_impacts_total_asset_retreat_costs.RDS',
                   'FloodFatal': 'sea_level_rise_costs_and_impacts_total_fatalities_due_to_coastal_floods.RDS',
                   'Nflood': 'sea_level_rise_costs_and_impacts_total_number_of_people_flooded.RDS',
                   'AssetLoss': 'sea_level_rise_costs_and_impacts_total_loss_of_assets_from_slr.RDS',
                   'TCB_peat': 'terrestrial_carbon_balance_annual_carbon_uptake_in_peatlands.RDS',
                   'TCB_deforest': 'terrestrial_carbon_balance_deforestation_carbon_loss.RDS',
                   'TCB_reforest': 'terrestrial_carbon_balance_forest_regrowth_carbon_uptake.RDS',
                   'TCB': 'terrestrial_carbon_balance_terrestrial_carbon_balance.RDS',
                   'TCB_npp': 'terrestrial_carbon_balance_terrestrial_net_primary_production.RDS',
                   'CO2emis_FLU': 'emissions_co2_emissions_from_food_and_land_use_gtc.RDS',
                   'CO2emis_other': 'emissions_co2_emissions_from_other_gtc.RDS',
                   'CO2emis_energy': 'emissions_realized_co2_emissions_from_energy_gtc.RDS',
                   'CO2conc': 'co2_forcing_atmospheric_co2_concentration.RDS',
                   'CO2growth': 'co2_forcing_atmospheric_co2_growth_gtc.RDS',
                   'OceanCO2uptake': 'ocean_air_sea_co2_flux.RDS',
                   'LandCO2uptake': 'emissions_land_carbon_sink.RDS',
                   'EBM_Tsurf': 'energy_balance_model_land_and_ocean_surface_temperature.RDS',
                   'EBM_Tthermo': 'energy_balance_model_thermocline_ocean_temperature.RDS',
                   'EBM_Tdeep': 'energy_balance_model_deep_ocean_temperature.RDS',
                   'EBM_Csurf': 'energy_balance_model_heat_capacity_of_land_and_ocean_surface.RDS',
                   'EBM_Cthermo': 'energy_balance_model_heat_capacity_of_thermocline_ocean.RDS',
                   'EBM_Cdeep': 'energy_balance_model_heat_capacity_of_deep_ocean.RDS',
                   'Forcing_CO2': 'co2_forcing_co2_effective_radiative_forcing.RDS',
                   'Forcing_anthro': 'forcing_anthropogenic_effective_radiative_forcing.RDS',
                   'Forcing_all': 'forcing_total_effective_radiative_forcing.RDS'
                   }



##### Reading data
def readFromFridaOutput(varname, expID, path='', nSample=10000, sy=1980, ey=2150, silent=False, lmedian=False,
        csv=False, dropna=True, axis=0):
    if not silent: print('Loading variable: '+varname)
    path=path+'FRIDA_output/'+expID+'/'
    if varname in ['CoastalAssets', 'CoastalPopulation']:
        if csv:
            df = pd.read_csv(path+FRIDA_Filenames[varname+'_ip'][:-3]+'csv')
        else:
            RDS = pyreadr.read_r(path+FRIDA_Filenames[varname+'_ip'])
            df = RDS[None]

        if dropna: df = df.dropna(axis=axis)
        if df.columns[1]=='sowID': var1 = np.asarray(df.values[1:,2:], dtype=float)
        else: var1 = np.asarray(df.values[1:,1:], dtype=float)

        if csv:
            df = pd.read_csv(path+FRIDA_Filenames[varname+'_wp'][:-3]+'csv')
        else:
            RDS = pyreadr.read_r(path+FRIDA_Filenames[varname+'_wp'])
            df = RDS[None]

        if dropna: df = df.dropna(axis=axis)
        if df.columns[1]=='sowID': var2 = np.asarray(df.values[1:,2:], dtype=float)
        else: var2 = np.asarray(df.values[1:,1:], dtype=float)
        var = var1+var2
        
    else:
        if csv:
            df = pd.read_csv(path+FRIDA_Filenames[varname][:-3]+'csv')
        else:
            RDS = pyreadr.read_r(path+FRIDA_Filenames[varname])
            df = RDS[None]
        if dropna: df = df.dropna(axis=axis)
        
        if df.columns[1]=='sowID': var = np.asarray(df.values[1:,2:], dtype=float)
        else: var = np.asarray(df.values[1:,1:], dtype=float)

    time = np.linspace(sy,ey,int(ey-sy+1))
    if not dropna: var = var[:nSample]

    if lmedian: return np.median(var, axis=0), time
    else: return np.transpose(var), time






##### Plotting data
def plotTimeseriesFRIDA(ax, time, variable, lmean=True, l50=False, l66=True, l95=False, ylabel='',
                   label='', color='tab:blue', title='', font=12):
    
    ax.set_xlim(1980, 2150)
    ax.set_ylabel(ylabel, fontsize=font)
    ax.set_title(title, fontsize=font)
        
    if lmean: ax.plot(time, np.nanmedian(variable, axis=1), linewidth=2, label=label, color=color)
    if l50: ax.fill_between(time, np.nanpercentile(variable, 25, axis=1), np.nanpercentile(variable, 75, axis=1),
            linewidth=2, color=color, alpha=0.5)
    if l66: ax.fill_between(time, np.nanpercentile(variable, 17, axis=1), np.nanpercentile(variable, 85, axis=1),
            linewidth=2, color=color, alpha=0.3)
    if l95: ax.fill_between(time, np.nanpercentile(variable, 2.5, axis=1), np.nanpercentile(variable, 97.5, axis=1),
            linewidth=2, color=color, alpha=0.15)
    
    return




