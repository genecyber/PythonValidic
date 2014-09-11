import simplejson as json 

class Profile():
     gender= "M"
     location = "NC"
     birthyear = "1980"
     height = 4
     weight = 5

class Fitness():
    timestamp= "2013-03-10T07:12:16+00:00"
    utc_offset= "-05:00"
    type= "Running"
    intensity= "medium"
    start_time= "2013-03-09T02:12:16-05:00"
    distance= 5149.9
    duration= 1959
    calories= 350
    activity_id= "12345"


class Routine():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    steps = 9355
    distance = 790.33
    floors = 23
    elevation = 3.4
    calories_burned = 2874
    activity_id = "12345"

class Nutrition():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    calories = 865
    carbohydrates = 121
    fat = 31
    fiber = 9
    protein = 21
    sodium = 1129
    water = 14
    meal = "lunch"
    entry_id = "12345"
class Sleep():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    total_sleep = 477
    awake = 34
    deep = 234
    light = 94
    rem = 115
    times_woken = 4
    activity_id = "12345"
class Weight():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    weight = 83.9146
    height = 167.5
    free_mass = 83.9146
    fat_percent = 21.4
    mass_weight = 83.9146
    bmi = 29.9
    data_id = "12345"
class Diabetes():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    c_peptide = 0.6
    fasting_plasma_glucose_test = 95
    hba1c = 4.8
    insulin = 460
    oral_glucose_tolerance_test = 137
    random_plasma_glucose_test = 256
    triglyceride = 128
    blood_glucose = 120
    activity_id = "12345"
class Biometrics():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    blood_calcium = 9.2
    blood_chromium = 1.32
    blood_folic_acid = 8.1
    blood_magnesium = 1.89
    blood_potassium = 3.9
    blood_sodium = 137.8
    blood_vitamin_b12 = 612
    blood_zinc = 93
    creatine_kinase = 87
    crp = 0
    diastolic = 73
    ferritin = 189
    hdl = 44
    hscrp = 0.3
    il6 = 6.4
    ldl = 156
    resting_heartrate = 74
    systolic = 122
    testosterone = 457
    total_cholesterol = 208
    tsh = 0.6
    uric_acid = 4.2
    vitamin_d = 54.8
    white_cell_count = 7453
    spo2 = 96
    temperature = 37
    data_id = "12345"
class TobaccoCessation():
    timestamp = "2013-03-10T07:12:16+00:00"
    utc_offset = "+00:00"
    cigarettes_allowed = 9
    cigarettes_smoked = 2
    cravings = 12
    last_smoked = "2013-03-10T05:55:36+00:00"

    def toJson(self):
        return json.dumps(self.__dict__)


