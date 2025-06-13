import os
import urllib.request
import json
import uuid
from app import app
from app import port
from flask import Flask, request, redirect, render_template, url_for, session, jsonify, send_file
from functools import wraps
from util import is_valid_session
from dbutil import delete, purge, getSids, updusageCount, getMasterCount,getMaster, getMMCount, getMaterialMaster, loadCustomers, getCustCodeCountGW, getBp2ItemCount, getBp1ItemCount, getBp1Count, getTicketCount, getCustCodeCount, getSysCount, getCustCount, getSaleCount, getPurCount, getPlantCount, getBp2Count, get_trans_names,updateCustomCode, insertSysCodeValue, insertCustomCode, get_trans_details,getTicketGraph,get_org_details, get_com_master, get_cust_code, get_sys_master, get_sys_details, getTickets, cleanup, updtransdetails, insertCodeValue
import logging
from config import *

custId = ''

@app.route('/',methods=['get'])
def home():
	cust = loadCustomers()
	return render_template('login.html', cust=cust)

@app.route('/dashboard/<client>',methods=['get'])
def dashboard(client):
	# if not is_valid_session(session):
	# 	return redirect(url_for('login'))
	print("load dashboard")
	# user = User.query.filter_by(username = "punniyamoorthy.govindhan@bs.nttdata.com").first()
	return render_template('dashboard.html', clientid=client)

@app.route('/login', methods=['post'])
def login():
	print('inside login.....')
	username = request.form.get('username')
	pwd = request.form.get('password')
	print(username)
	print(pwd)
	if username.upper() == 'ADMIN' and pwd.upper() == 'NTTDATA@BS':
		customer = request.form.get('customer')
		print('befor redirect')
		return redirect(url_for('dashboard', client=customer))
	else: 
		cust = loadCustomers()
		return render_template('login.html', cust=cust, message='Invalid User Name/Password')
	
@app.route('/logout')
def logout():
	# if session and 'user' in session.keys():
	# 	app.logger.info('LOGOUT - {0}'.format(session['user']['email']))
	# session.clear()
	cust = loadCustomers()
	return render_template('login.html', cust=cust)

@app.route('/trans_menuitem/<client>', methods=['get'])
def trans_menuitem(client):
	print('inside trans_menuitem')
	lscap = getSysCount(client)
	ccounts = getCustCount(client)
	salorgCount = getSaleCount(client)
	purCount = getPurCount(client)
	plantCount = getPlantCount(client)
	bp1Count = getBp1Count(client)
	bp2Count = getBp2Count(client)
	CCCount = getCustCodeCount(client)
	ticketCount = getTicketCount()
	MMCount = getMMCount(client)
	MCount = getMasterCount(client)
	return render_template('_cms_tran.html',clientid=client, MCount=MCount, MMCount=MMCount, ticketCount=ticketCount, CCCount=CCCount,bp1Count=bp1Count, bp2Count=bp2Count, plantCount=plantCount, scount=lscap, ccount=ccounts, salorgCount=salorgCount, purCount=purCount, title="Transition")

@app.route('/sys_graph/<client>', methods=['get'])
def sys_graph(client):
	print('inside sys_graph' + str(uuid.uuid4()))
	ret = []
	head = '['
	nuid = uuid.uuid4()
	print(nuid)
	orgs = get_sys_master(client, str(nuid))
	for org in orgs:
		s2 = '{ "id": "' + org[2] + '", "centerId": "' + org[3] + '", "title": "' + org[0] + '",' 
		s3 = '"data": {' 
		s4 = '"labels": ["Standard", "Customized"],'
		s5 = '"datasets": [{'
		s6 = '"data": [' + str(org[1]) + ', 0 ],' 
		s7 = '"backgroundColor": ["#19A3FC", "#D1EDFE"],' 
		s8 = '"hoverBackgroundColor": ["#1BB5FF", "#E0F4FF"]'
		s9 = '}]}}'
		datachart = s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
		try:
			json_object = json.loads(datachart)
		except Exception as e:
			print('Exception: {}'.format(e))
		ret.insert(0,json_object)
	print('before return')
	return render_template('_cms_sysl_main_graph.html', datachart=ret, heads=orgs, title='System Landscape')

@app.route('/sys_menuitem/<code>/<client>', methods=['get'])
def sys_menuitem(code, client):
	print('inside sys_menuitem')
	sids = getSids(client)
	return render_template("_cms_sysl_main.html",code=code, sids=sids, clientid=client, title="System Landscape")

@app.route('/sys_menugraph/<sid>/<client>', methods=['get'])
def sys_menugraph(sid, client):
	print('inside sys_menugraph ' + sid) 
	sids = get_sys_details(sid, client)
	return render_template("_cms_sysl_main_graph.html", sids=sids, clientid=client, title=sid)


@app.route('/com_graph/<code>/<client>', methods=['get'])
def com_graph(code, client):
	print('inside com_graph' + str(uuid.uuid4()))
	ret = []
	head = '['
	nuid = uuid.uuid4()
	print(nuid)
	orgs = get_com_master(client,"'Company Code','Cost Center','Profit Center'", str(nuid))
	for org in orgs:
		s2 = '{ "id": "' + org[2] + '", "centerId": "' + org[3] + '", "title": "' + org[0] + '",' 
		s3 = '"data": {' 
		s4 = '"labels": ["Standard", "Customized"],'
		s5 = '"datasets": [{'
		s6 = '"data": [' + str(org[1]) + ', 0 ],' 
		s7 = '"backgroundColor": ["#19A3FC", "#D1EDFE"],' 
		s8 = '"hoverBackgroundColor": ["#1BB5FF", "#E0F4FF"]'
		s9 = '}]}}'
		datachart = s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
		try:
			json_object = json.loads(datachart)
		except Exception as e:
			print('Exception: {}'.format(e))
		ret.insert(0,json_object)
	return render_template('_cms_tran_org_com_graph.html', datachart=ret, heads=orgs, title='Company')

@app.route('/com_menuitem/<code>/<client>', methods=['get'])
def com_menuitem(code, client):
	print('inside com_menuitem')
	orgs = []
	tit = "Company"
	ccode = get_org_details('Company Code', client)
	ccent = get_org_details('Cost Center', client)
	pcent = get_org_details('Profit Center', client)
	return render_template('_cms_tran_org_com.html', clientid=client, code=code,ccode=ccode, ccent=ccent,pcent=pcent, transmaster=orgs, title=tit)

@app.route('/sal_graph/<code>/<client>', methods=['get'])
def sal_graph(code, client):
	print('inside sal_graph' + str(uuid.uuid4()))
	ret = []
	head = '['
	nuid = uuid.uuid4()
	print(nuid)
	orgs = get_com_master(client,"'Sales Org','Distribution Channel','Division'", str(nuid))
	for org in orgs:
		s2 = '{ "id": "' + org[2] + '", "centerId": "' + org[3] + '", "title": "' + org[0] + '",' 
		s3 = '"data": {' 
		s4 = '"labels": ["Standard", "Customized"],'
		s5 = '"datasets": [{'
		s6 = '"data": [' + str(org[1]) + ', 0 ],' 
		s7 = '"backgroundColor": ["#19A3FC", "#D1EDFE"],' 
		s8 = '"hoverBackgroundColor": ["#1BB5FF", "#E0F4FF"]'
		s9 = '}]}}'
		datachart = s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
		try:
			json_object = json.loads(datachart)
		except Exception as e:
			print('Exception: {}'.format(e))
		ret.insert(0,json_object)
	return render_template('_cms_tran_org_sal_graph.html', datachart=ret, heads=orgs,  title='Sales Org')

@app.route('/sal_menuitem/<code>/<client>', methods=['get'])
def sal_menuitem(code, client):
	print('inside sal_menuitem')
	orgs = []
	tit = "Sales Org"
	sal = get_org_details('Sales Org', client)
	dc = get_org_details('Distribution Channel', client)
	divi = get_org_details('Division', client)
	return render_template('_cms_tran_org_sal.html',  clientid=client, code=code,sal=sal, dc=dc, divi=divi, transmaster=orgs, title=tit)

@app.route('/pur_graph/<code>/<client>', methods=['get'])
def pur_graph(code, client):
	print('inside sal_graph' + str(uuid.uuid4()))
	ret = []
	nuid = uuid.uuid4()
	print(nuid)
	orgs = get_com_master(client,"'Purchase Org','Purchase Group'", str(nuid))
	for org in orgs:
		s2 = '{ "id": "' + org[2] + '", "centerId": "' + org[3] + '", "title": "' + org[0] + '",' 
		s3 = '"data": {' 
		s4 = '"labels": ["Standard", "Customized"],'
		s5 = '"datasets": [{'
		s6 = '"data": [' + str(org[1]) + ', 0 ],' 
		s7 = '"backgroundColor": ["#19A3FC", "#D1EDFE"],' 
		s8 = '"hoverBackgroundColor": ["#1BB5FF", "#E0F4FF"]'
		s9 = '}]}}'
		datachart = s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
		try:
			json_object = json.loads(datachart)
		except Exception as e:
			print('Exception: {}'.format(e))
		ret.insert(0,json_object)
	return render_template('_cms_tran_org_pur_graph.html', datachart=ret, heads=orgs, title='Purchase Org')

@app.route('/pur_menuitem/<code>/<client>', methods=['get'])
def pur_menuitem(code, client):
	print('inside pur_menuitem')
	orgs = []
	tit = "Purchase Org"
	po = get_org_details('Purchase Org', client)
	pg = get_org_details('Purchase Group', client)
	return render_template('_cms_tran_org_pur.html',  clientid=client, code=code, transmaster=orgs, title=tit,po=po,pg=pg)

@app.route('/pla_graph/<soln>/<client>', methods=['get'])
def pla_graph(soln, client):
	return render_template('_cms_tran_org_pla_graph.html', title='Plant')

@app.route('/pla_details/<soln>/<client>/', methods=['get'])
def pla_details(soln, client):
	try:
		print("inside main pla_details")
		orgs = get_org_details(soln, client)
		print('After return')
		print(orgs)
		return render_template('_cms_tran_org_pla_cod.html',  clientid=client, transmaster=orgs, title=soln)
	except Exception as e:
		print('Exception: {}'.format(e))

@app.route('/bp1_db/<client>', methods=['get'])
def bp1_db(client):
	print('inside bp1db')
	amc = getBp1ItemCount('Asset management',client)
	dbc = getBp1ItemCount('DB Management',client)
	fic = getBp1ItemCount('Finance',client)
	hrc = getBp1ItemCount('Humar Resource',client)
	mfc = getBp1ItemCount('Manufacturing',client)
	rdc = getBp1ItemCount('R and D Engeneering',client)
	sac = getBp1ItemCount('Sales',client)
	spc = getBp1ItemCount('Sourcing and Procurement',client)
	scc = getBp1ItemCount('Supplychain',client)
	return render_template('_cms_tran_bp1.html', clientid=client, scc=scc, amc=amc, dbc=dbc, fic=fic, hrc=hrc, mfc=mfc, rdc=rdc, sac=sac, spc=spc, title='BPM Level 1')

@app.route('/bp1_db_item/<soln>/<client>', methods=['get'])
def bp1_db_item(soln, client):
	# print('inside trans sol master master' + soln + " --- " + client)
	trans = []
	trans = get_trans_details(soln,client);
	return render_template('_cms_tran_bp1_bp1.html',  clientid=client, transmaster=trans, title=soln)

@app.route('/bp2_graph/<code>/<client>', methods=['get'])
def bp2_graph(code, client):
	sdc = getBp2ItemCount('Sales Doc Type', client)
	pdc = getBp2ItemCount('Purchase Doc type', client)
	ppc = getBp2ItemCount('Pricing Procedure', client)
	return render_template('_cms_tran_bp2_graph.html', clientid=client, sdc=sdc, pdc=pdc, ppc=ppc, title='BPM Level -2')

@app.route('/bp2_menuitem/<code>/<client>', methods=['get'])
def bp2_menuitem(code, client):
	print('inside bp2_menuitem')
	sales = get_org_details(code, client)
	return render_template('_cms_tran_bp2.html',  clientid=client, code=code, transmaster=sales, title=code)

@app.route('/cust_graph/<client>', methods=['get'])
def cust_graph(client):
	return render_template('_cms_tran_ccd_graph.html', clientid=client, title='Custom Code Analysis')

@app.route('/cust_code/<client>', methods=['get'])
def cust_code(client):
	# print('inside trans sol master master' + soln + " --- " + client)
	# trans = []
	# trans = get_cust_code(client);
	pgc = getCustCodeCountGW('SE38 Program', client)
	fgc = getCustCodeCountGW('Function Group', client)
	clc = getCustCodeCountGW('Class', client)
	pkc = getCustCodeCountGW('Package', client)
	sec = getCustCodeCountGW('SAP Enhancements', client)
	eic = getCustCodeCountGW('Enhancement Implementation', client)
	mcc = getCustCodeCountGW('Message Class', client)
	return render_template('_cms_tran_ccd_graph.html', clientid=client, pgc=pgc, fgc=fgc, clc=clc, pkc=pkc, sec=sec, eic=eic, mcc=mcc,  title='Custom Code')

@app.route('/custcodedetails/<client>/<ttext>', methods=['get'])
def custcodedetails(client, ttext):
	# print('inside trans sol master master' + soln + " --- " + client)
	trans = []
	trans = get_cust_code(client, ttext);
	return render_template('_cms_tran_ccd_cod.html',  clientid=client, title=ttext, transmaster= trans)


@app.route('/material_master/<client>', methods=['get'])
def material_master(client):
	trans = []
	trans = getMaterialMaster(client);
	return render_template('_cms_tran_mat.html',  clientid=client, title='Material Master', transmaster= trans)	

@app.route('/master/<client>', methods=['get'])
def master(client):
	trans = []
	trans = getMaster(client);
	return render_template('_cms_tran_master.html',  clientid=client, title='Master', transmaster= trans)	

@app.route('/signov', methods=['get'])
def signov():
	return render_template('_cms_tran_sig_ove.html', title='SAP Signavio Overview')

@app.route('/showDocument/<client>', methods=['get'])
def showDocument(client):
	return render_template('_cms_trans_doc.html', title='Documents', clientid=client)

@app.route('/sigins', methods=['get'])
def sigins():
	return render_template('_cms_tran_sig_ins.html', title='SAP Signavio Insigts')

@app.route('/tickets_graph', methods=['get'])
def tickets_graph():
	print('inside ... graph...')
	ticgraph = getTicketGraph();
	l1 = ticgraph[0][0]
	v1 = str(ticgraph[0][1])
	l2 = ticgraph[1][0]
	v2 = str(ticgraph[1][1])
	l3 = ticgraph[2][0]
	v3 = str(ticgraph[2][1])
	s2 = '{ "id": "bpmChart1", "centerId": "bpmCC1", "title": "Tickets",' 
	s3 = '"data": {' 
	s4 = '"labels": ["'+ l1 + '", "' + l2 +'", "' + l3 + '"],'
	s5 = '"datasets": [{'
	s6 = '"data": [' + v1 + ',' + v2 + ',' + v3 + '],' 
	s7 = '"backgroundColor": ["#19A3FC", "#D1EDFE", "#00EDFE"],' 
	s8 = '"hoverBackgroundColor": ["#1BB5FF", "#E0F4FF", "#00F4FF"]'
	s9 = '}]}}'
	datachart = s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
	try:
		json_object = json.loads(datachart)
	except Exception as e:
		print('Exception: {}'.format(e))
	ret = []
	ret.insert(0,json_object)
	return render_template('_cms_tran_tick_graph.html', datachart=ret, id='bpmChart1', centerId='centerId', title='Ticket Analysis')

@app.route('/tickets/<client>', methods=['get'])
def tickets(client):
	# print('inside  sys_menudetails ' + soln + " --- " + client)
	trans = []
	trans = getTickets();
	return render_template('_cms_tran_tick.html',  clientid=client, transmaster=trans, title="Tickets")

@app.route('/admin', methods=['get'])
def admin():
	return render_template('_cms_admin.html', title="Administration")

@app.route('/demo', methods=['get'])
def demo():
	return jsonify({"message":'Success'}),200

@app.route('/postrecord', methods=['POST'])
def postrecord():
	req_data = request.get_json()
	print(req_data);
	for data in req_data:
		print(data['code'])
		print(data['value'])
	return req_data,200

@app.route('/cleanup', methods=['POST'])
def srvcleanup():
	req_data = request.get_json()
	cleanup(req_data)
	req_data = '{"message":"Success"}';
	return req_data,200

@app.route('/updtransdetails', methods=['POST'])
def updatetransdetails():
	req_data = request.get_json()
	updtransdetails(req_data);
	# print(req_data);
	# for keys in req_data:
	# 	print(keys);
	# 	print(req_data[keys])
	# 	scope = req_data[keys]
	# 	print(scope['scopeID'])
	# 	print(scope['status'])
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/insertcv', methods=['POST'])
def insertCV():
	req_data = request.get_json()
	insertCodeValue(req_data);
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/insertscv', methods=['POST'])
def insertSCV():
	req_data = request.get_json()
	insertSysCodeValue(req_data);
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/insertcc', methods=['POST'])
def insertCustCode():
	req_data = request.get_json()
	insertCustomCode(req_data);
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/updatecc', methods=['POST'])
def updateCustCode():
	req_data = request.get_json()
	updateCustomCode(req_data);
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/updusage', methods=['POST'])
def updateUsageCount():
	req_data = request.get_json()
	updusageCount(req_data);
	reqdata = '{"message":"Success"}';
	return reqdata,200

@app.route('/download_client', methods=['GET'])
def download_client():
	file_name = 'it.transition_v1.0.zip'
	response = send_file('build/'+file_name,file_name,as_attachment=True)
	return response

@app.route('/purge/<client>', methods=['GET'])
def purge_client(client):
	nclientid = client + 'P'
	purge(client, nclientid)
	return "{'Message' : 'Success'}"

@app.route('/unpurge/<client>', methods=['GET'])
def unpurge_client(client):
	purge(client +'P', client)
	return "{'Message' : 'Success'}"

@app.route('/delete/<client>', methods=['GET'])
def delete_client(client):
	delete(client)
	return "{'Message' : 'Success'}"


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=port)
	#serve(app, host = '0.0.0.0',port=8000,url_scheme='http')
	#serve(app, listen='0.0.0.0:8443', url_scheme='https')