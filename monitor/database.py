import pytz
from .models import BridgeIdentity, BridgeData, SensorStatus

def getData(amount, bridge_id):
    """get 'amount' data(s) of bridge sensor reading from postgreSQL"""
    objs = BridgeData.objects.order_by('-date').filter(bridge=bridge_id)[:amount]
    list_of_dict = list(objs.values('date','health_index','mean_frequency', 'ideal_frequency','mode_shape'))
    for dict_ in list_of_dict:
        mode_shape_list = dict_.pop('mode_shape')
        dict_['date'] = dict_.get('date').astimezone(pytz.timezone("Asia/Jakarta")).replace(tzinfo=None).isoformat(' ')
        for i in range(10):
            dict_['mode_shape'+str(i+1)] = mode_shape_list[i]
    return list_of_dict

def get_bridges_dropdown():
    objs = BridgeIdentity.objects.all()
    bridge_dict = [entry for entry in objs.values('name','id')]
    for entry in bridge_dict:
        entry['label'] = entry.pop('name')
        entry['value'] = entry.pop('id')
    return bridge_dict

def updateFreq(frequency):
    """Update bridge ideal frequency"""
    BridgeIdentity.objects.filter(id=1).update(ideal_frequency=frequency)

def getValue(amount, bridge_id):
    """get 'amount' data(s) of bridge sensor reading from postgreSQL"""
    objs = BridgeData.objects.order_by('-date').filter(bridge=bridge_id)[:amount]
    list_of_dict = list(objs.values('value'))
    for dict_ in list_of_dict:
        value_list = dict_.pop('value')
        for i in range(8):
            dict_['value'+str(i+1)] = value_list[i]
    return list_of_dict

def getCracks(amount, bridge_id):
    objs = BridgeData.objects.order_by('-date').filter(bridge=bridge_id)[:amount]
    list_of_dict = list(objs.values('bridge_crack'))
    for dict_ in list_of_dict:
        bridge_crack_list = dict_.pop('bridge_crack')
        for i in range(8):
            dict_['bridge_crack'+str(i+1)] = bridge_crack_list[i]
    return list_of_dict

def getSensor(amount, bridge_id):
    objs = SensorStatus.objects.order_by('-date').filter(bridge=bridge_id)[:amount]
    list_of_dict = list(objs.values('status'))
    for dict_ in list_of_dict:
        status_list = dict_.pop('status')
        for i in range(10):
            dict_['status'+str(i+1)] = status_list[i]
    return list_of_dict

