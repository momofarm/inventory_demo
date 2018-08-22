
import redis
import json 
import uuid

r = redis.StrictRedis(
    host='localhost',
    port=6379)

def insert_equipment(eq_name, group, serial, history):
	s = {'equipment_name' : eq_name, 'group' : group, 'serial' : serial, 'history' : history}
	j = json.dumps(s)
	r.set(str(uuid.uuid4()), j)
	return


def search(group, serial):
        # because i'm using redis, so it's a brute-force search
        # search speed will be slow when there are too many objects in redis data storge 
        result = {}

        for key in r.scan_iter():
            w = r.get(key)
            json_object = json.loads(w)
            if (group != ''):
                 if (json_object['group'] != group):
                     continue
                 print 'found one group'

            if (serial != ''):
                if (json_object['serial'] != serial):
                    continue

            print w
            
            result[key] = json_object

        return result


def remove(serial):
        r.delete(serial)
        return


def add_history(serial, text):
        result = search('', serial)
        
        if (len(result) > 1):
            return 'error'    	
			
        for key in result:
            d = result[key]
            d['history'] = text
            json_text = json.dumps(d)
            r.set(key, json_text)


        return 



