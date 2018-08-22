from flask import Flask
from flask import render_template
from flask import request

import insert

app = Flask(__name__)

@app.route('/')
def hello_world():
    return  render_template('index.html')

@app.route('/about')
def about():
    return 'this is a testing inventory system, only for demo use, please do not use at production environment'


@app.route('/addInventory')
def addInventory():
	item = {}
	item['equpitment_name'] = ''
	item['group'] = ''
	item['serial'] = ''
	return render_template('add.html', item = item)


#@app.route('/addHistory')
#def addHistory():
#	return render_template('addHistory.html')

@app.route('/currentInv')
@app.route('/currentInv/')
def currentInv():
	current_store = insert.search('', '')

	return render_template('currentInv.html', current=current_store)

	

@app.route('/currentInv/grp/<grp>')
def currentInv2(grp=None):
	current_store = None
	
	if 'grp' is not None:
		print 'type for grp ' + grp
		current_store = insert.search(grp, '')
	else:
		print 'search all'
		current_store = insert.search('', '')

	return render_template('currentInv.html', current=current_store)


@app.route('/currentInv/serial/<serial>')
def currentInv3(serial=None):
	current_store = insert.search('', serial)

	for key, value in current_store.items():
		return render_template('add.html', item=value)
	

@app.route('/addHistory/<serial>')
def addHistory(serial=None):
	item = insert.search('', serial)	

	return render_template('add.html', serial)


@app.route('/updateHistory', methods=['POST'])
def updateHistory():
	
	if request.method == 'POST':
		equipment_name = request.form['eq']
		group = request.form['gr']
		serial =  request.form['serial']
		history =  request.form['txarea']
		#print 'updateing item ' + serial
		#print 'updateing data ' + history
		
		if len(insert.search(group, serial)) == 0: #new, add new one
			insert.insert_equipment(equipment_name, group, serial, history)
		else:
			insert.add_history(serial, history)

		f = {}
		f['equipment_name'] = equipment_name
		f['group'] = group 
		f['serial'] = serial
		f['history'] = history
		return render_template('add.html', item=f)

