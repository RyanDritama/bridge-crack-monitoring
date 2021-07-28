from django.db import models
from django.contrib.postgres import fields

#Only support postgreSQL because of mode_shape array column

class BridgeIdentity(models.Model):
    """Identity and physical parameter of bridge"""
    name = models.CharField(max_length=25)
    province = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    street = models.CharField(max_length=25)

    #Physic parameter
    '''
    Islam, A.K. M. Anwarul & Jaroo, Amer & Li, Frank. (2014).
    Bridge Load Rating Using Dynamic Response.
    Journal of Performance of Constructed Facilities.
    29. 04014120. 10.1061/(ASCE)CF.1943-5509.0000620.
    '''
    #Box Beam
    ideal_frequency_Hz = models.FloatField()
    # psbb_length =  models.FloatField(name="PSBB length (m)")
    # outside_width =  models.FloatField(name="Outside Width (m)")
    # inside_width =  models.FloatField(name="Inside Width (m)")
    # outside_height =  models.FloatField(name="Outside Height (m)")
    # inside_height =  models.FloatField(name="Inside Height (m)")
    # n_box_beams =  models.IntegerField(name="Number of Box Beams")
    # n_diaphragms =  models.IntegerField(name="Number of Diaphragms")
    # diaphragm_thickness =  models.FloatField(name="Diaphragm Thickness (m)")
    # box_beam_end_thickness =  models.FloatField(name="Box Beam End Thickness (m)")
    # #Concrete
    # compressive_strength =  models.FloatField(name="28-day Compressive Strength (Pa)")
    # unit_weight =  models.FloatField(name="Unit Weight (kg/m^3)")

def get_neuron_value():
    value =  [0, 0 ,0, 0, 0,0, 0 ,0]
    return value

def get_cracks():
    value =  ["0","0" ,"0", "0","0","0", "0","0"]
    return value
CRACKS = (
    ('0', 'Tidak Rusak'),
    ('1', 'Rusak'),
)

def get_sensor():
    value =  [1, 1 ,1, 1, 1,1, 1 ,1,1, 1]
    return value

def get_frequency():
    value =  [0.0, 0.0 ,0.0, 0.0, 0.0,0.0, 0.0 ,0.0,0.0, 0.0]
    return value

class BridgeData(models.Model):
    """Timely vibration sensor data of bridge"""
    bridge = models.ForeignKey(BridgeIdentity, on_delete=models.CASCADE)
    date = models.DateTimeField()
    health_index = models.PositiveSmallIntegerField()
    mean_frequency = models.FloatField()
    ideal_frequency = models.FloatField(default=26.0)
    mode_shape = fields.ArrayField(models.FloatField(),size=10)
    value = fields.ArrayField(models.FloatField(),size=8, default = get_neuron_value)
    bridge_crack = fields.ArrayField(models.CharField(max_length=1, choices=CRACKS),size=8, default = get_cracks)
    bridge_sensor = fields.ArrayField(models.IntegerField(),size=10, default = get_sensor )
    frequency = fields.ArrayField(models.FloatField(),size=10, default = get_frequency)

class SensorStatus(models.Model):
    bridge = models.ForeignKey(BridgeIdentity, on_delete=models.CASCADE)
    status = fields.ArrayField(models.FloatField(),size=10, null=True, blank=True)
    date = models.DateTimeField()

