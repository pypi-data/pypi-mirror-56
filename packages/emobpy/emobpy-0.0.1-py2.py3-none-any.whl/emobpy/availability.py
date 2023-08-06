import pandas as pd
import numpy as np
import uuid
import os
import pickle
from numba import jit
from .constants import TIME_FREQ


##############################################################################
# These functions are for charging availability profile creation
##############################################################################
# TODO:
# - CHECK CONSISTSTENCY WITH MORE OPTIONS in function SOC()

# function descriptions pending
class Availability:
    """docstring for Availability."""

    def __init__(self, input):
        self.kind = 'availability'
        self.input = input
        self.name = self.input + '_avai_' + uuid.uuid4().hex[0:5]

    def setScenario(self, charging_data):
        self.prob_charging_point = charging_data['prob_charging_point']
        self.capacity_charging_point = charging_data['capacity_charging_point']

    def setVehicleFeature(self, battery_capacity, charging_eff):
        self.battery_capacity = battery_capacity
        self.charging_eff = charging_eff

    def setBatteryRules(self, soc_init, soc_min):
        self.soc_init = soc_init
        self.soc_min = soc_min

    def loadSettingDriving(self, DataBase):
        if DataBase[self.input]:
            if DataBase[self.input]['kind'] == 'driving':
                self.df = DataBase[self.input]['profile']
                self.t = DataBase[self.input]['t']
                self.hours = DataBase[self.input]['hours']
                self.freq = TIME_FREQ[DataBase[self.input]['numb_dayblocks']]['f']
                self.refdate = DataBase[self.input]['refdate']
                self.energy_consumption = DataBase[self.input]['energy_consumption']
            else:
                raise ValueError('The driving profile {} can not be found in the database'.format(self.input))
        else:
            raise ValueError('The driving profile {} can not be found in the database'.format(self.input))

    def deleteDrivingAttrib(self):
        for attr in ['df', 't', 'hours', 'freq', 'refdate']:
            self.__dict__.pop(attr, None)

    def ChooseChargingPoint(self, state):
        self.chrg_points = [key for key in self.prob_charging_point[state].keys()]
        self.prob = [val for val in self.prob_charging_point[state].values()]
        self.rnd_name = np.random.choice(self.chrg_points, p=self.prob)
        return self.rnd_name

    def fill_rows(self):  # df,hours,t

        self.repeats = ['hr', 'state', 'charging_point', 'charging_cap']
        self.fixed = ['distance', 'consumption']
        self.copied = ['departure', 'last_dep', 'purpose', 'duration', 'weekday', 'person']
        self.calc = ['dayhrs']
        self.same = []

        self.dt = pd.DataFrame(columns=self.db.columns)
        self.dt.loc[:, 'hh'] = np.arange(0, self.hours*self.t, self.t)
        self.idx = self.dt[self.dt['hh'].isin(self.db['hr'].tolist())].index.tolist()
        self.mixed = self.repeats + self.fixed + self.copied
        for r in self.mixed:
            self.val = self.db[r].values.tolist()
            self.dt.loc[self.idx, r] = self.val
        self.dt.loc[self.hours-1, 'state'] = self.db['state'].iloc[-1]
        self.dt.loc[self.hours-1, 'hr'] = self.dt['hh'][self.hours-1]
        self.rp = self.dt[::-1].reset_index(drop=True)
        self.rp.loc[:, self.repeats] = self.rp[self.repeats].fillna(method='ffill')
        self.rp.loc[:, self.fixed] = self.rp[self.fixed].fillna(0)
        self.dt = self.rp[::-1].reset_index(drop=True)
        for sm in self.same:
            self.dt.loc[:, sm] = self.db[sm].values.tolist()[0]
        for cal in self.calc:
            self.dt.loc[:, cal] = self.dt['hh'].apply(lambda x: x % 24)

    def checkprofile(self):
        numpy_array = self.dt[['consumption', 'charging_cap']].values.T
        self.dt.loc[:, 'soc'] = self.soc(self.charging_eff, self.battery_capacity, self.soc_init, *numpy_array)

    @staticmethod
    @jit(nopython=True)
    def soc(charging_eff, battery_capacity, soc_init, consumption, charging_cap):
        '''
        state of charge of battery
        '''
        soc = np.empty(consumption.shape)
        for i in range(soc.shape[0]):
            if i == 0:
                zero = soc_init
                current_soc = zero - consumption[i]/battery_capacity + charging_cap[i]*charging_eff/battery_capacity
                if current_soc > 1:
                    soc[i] = 1
                else:
                    soc[i] = current_soc
            else:
                zero = soc[i-1]
                current_soc = zero - consumption[i]/battery_capacity + charging_cap[i]*charging_eff/battery_capacity
                if current_soc > 1:
                    soc[i] = 1
                else:
                    soc[i] = current_soc
        return soc

    def SelectChargingAvailability(self, altern=[]):  # df, hours, prob_charging_point,capacity_charging_point,battery_capacity,soc_init,soc_min,t
        self.battopt = altern[:]
        self.battopt.sort()
        self.n = 0
        self.df.loc[:, 'dayhrs'] = self.df['hr'] % 24
        self.df.loc[:, 'consumption'] = self.df['distance']*self.energy_consumption
        while True:
            self.n += 1
            self.db = self.df.copy()
            self.db.loc[:, 'charging_point'] = self.df['state'].apply(lambda state: self.ChooseChargingPoint(state))
            self.db.loc[:, 'charging_cap'] = self.db['charging_point'].apply(lambda charging_point: self.capacity_charging_point[charging_point])
            self.fill_rows()
            self.checkprofile()
            self.failed_chrg = self.dt[self.dt['soc'] < self.soc_min].copy()
            if self.failed_chrg.empty:
                self.success = True
                break
            if self.n % 40 == 0:
                print('still in while loop after ', self.n, ' iterations. Battery may be small, or many "none" charging points available...')
            if self.n % 160 == 0:
                if self.battopt:
                    print('Change battery capacity from {} kWh to {} kWh'.format(self.battery_capacity, self.battopt[0]))
                    self.battery_capacity = self.battopt[0]
                    self.battopt.remove(self.battopt[0])
                else:
                    self.success = False  # save anyway but it must be verified
                    self.name = self.name + '_FAIL'
                    print(" ----- !!! UNSUCCESSFUL profile creation !!! ----- please check this '{}', it may need to increase battery capacity or soc init is too low".format(self.name))
                    break

        self.profile = self.dt[['hh', 'state', 'distance', 'consumption', 'charging_point', 'charging_cap', 'soc']].copy()
        self.deleteDrivingAttrib()
        for attr in ['n', 'db', 'chrg_points', 'prob', 'rnd_name', 'dt', 'repeats', 'fixed', 'copied', 'calc', 'same', 'idx', 'mixed', 'val', 'rp', 'zero', 'current_soc', 'failed_chrg']:
            self.__dict__.pop(attr, None)

    def save_profile(self, folder, description=' '):
        self.description = description
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, self.name + '.pickle')
        with open(filepath, 'wb') as datei:
            pickle.dump(self.__dict__, datei)
        del self.__dict__
        print('=== profile saved === : ' + filepath)
