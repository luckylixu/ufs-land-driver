#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 01:17:03 2021
@author: li.xu

contact:
    Li Xu
    CPC/NCEP/NOAA
    (301)683-1548
    li.xu@noaa.gov

"""
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

from xu import ndates, run2


def nml(restart='2021-08-01', day='30'):
    nml = f'''

    &run_setup

  static_file      = "/cpc/drought/pdf/noahmp/conus3439/ll_0p5_static_conus_3439.nc"
  init_file        = "/cpc/home/li.xu/lxu/Py/ufs/p05/ll_0p5_init_19790102t23_3439.nc"
  forcing_dir      = "/cpc/drought/pdf/noahmp/conus3439/forcing"
  separate_output = .true.
  output_dir       = "/run/user/4986/"

  restart_frequency_s = 86400
  restart_simulation  = .True.
  restart_date        = "{restart} 23:00:00"
  restart_dir         = "/cpc/drought/pdf/noah/noah3439/restart/"

  timestep_seconds = 3600

! simulation_start is required
! either set simulation_end or run_* or run_timesteps, priority
!   1. simulation_end 2. run_[days/hours/minutes/seconds] 3. run_timesteps

  simulation_start = "1979-01-03 00:00:00"   ! start date [yyyy-mm-dd hh:mm:ss]
  !simulation_end   = "1979-02-01 00:00:00"   !   end date [yyyy-mm-dd hh:mm:ss]

  run_days         = {day}   ! number of days to run
  run_hours        = 0   ! number of hours to run
  run_minutes      = 0   ! number of minutes to run
  run_seconds      = 0   ! number of seconds to run

  run_timesteps    = 0   ! number of timesteps to run

  !begloc           = 1
  !endloc           = 3439
  location_start = 1
  location_end = 3439

/


&land_model_option
 land_model        = 1   ! choose land model: 1=noah, 2=noahmp
/

&structure
 num_soil_levels   = 4     ! number of soil levels
 forcing_height    = 10     ! forcing height [m]
/

&soil_setup
 soil_level_thickness   =  0.10,    0.30,    0.60,    1.00      ! soil level thicknesses [m]
 soil_level_nodes       =  0.05,    0.25,    0.70,    1.50      ! soil level centroids from surface [m]
/

&noahmp_options
 dynamic_vegetation_option         = 4
 canopy_stomatal_resistance_option = 1
 soil_wetness_option               = 1
 runoff_option                     = 1
 surface_exchange_option           = 1
 supercooled_soilwater_option      = 1
 frozen_soil_adjust_option         = 1
 radiative_transfer_option         = 3
 snow_albedo_option                = 2
 precip_partition_option           = 1
 soil_temp_lower_bdy_option        = 2
 soil_temp_time_scheme_option      = 3
 surface_evap_resistance_option    = 1
 glacier_option                    = 1
/


&forcing
 forcing_timestep_seconds       = 3600
 forcing_type                   = "nldas2"
 forcing_filename               = "ll_0p5_nldas2_"
 forcing_interp_solar           = "linear"  ! gswp3_zenith or linear
 forcing_time_solar             = "instantaneous"  ! gswp3_average or instantaneous
 forcing_name_precipitation     = "precipitation_conserve"
 forcing_name_temperature       = "temperature"
 forcing_name_specific_humidity = "specific_humidity"
 forcing_name_wind_speed        = "wind_speed"
 forcing_name_pressure          = "surface_pressure"
 forcing_name_sw_radiation      = "solar_radiation"
 forcing_name_lw_radiation      = "longwave_radiation"

/


    '''
    with open('ufs-land.namelist', 'w') as f:
        f.write(nml)







def ufs(restart='20210821', n=35):
    date = ndates(0, restart, fmt='%Y-%m-%d')
    nml(date, n)
    run2('./ufsLand.exe')
    from mean2day import do_day2
    do_day2(restart, n, 1)


def main(yyyymmdd):
    print(yyyymmdd)
    ufs(yyyymmdd)


if __name__ == '__main__':
    import sys
    import fire
    if len(sys.argv) <= 1:
        print('input: YYYYMMDD or -h')
    else:
        if len(sys.argv[1]) == 8:
            main(sys.argv[1])
        else:
            fire.Fire()
