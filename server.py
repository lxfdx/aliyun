from flask import Flask,request,redirect
import json
import requests
import hashlib
import time
import AEScry
import string
import random

khbh = 1965

def get_signature(nonce, payload, secret, timestamp):
    content = ':'.join([nonce, payload, secret, timestamp]).encode('utf-8')
    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()

def dingsignature(nonce,payload,token,timestamp):
	slist = [nonce,payload,token,timestamp]
	slist.sort()
	content = ''.join(slist).encode('utf-8')
	m = hashlib.sha1()
	m.update(content)
	return m.hexdigest()

def getrandomstring(n=8):
	rule = string.ascii_letters+string.digits
	thestring = random.sample(rule,n)
	return ''.join(thestring)

def success():
	encrypt2 = AEScry.encrypto('success')
	timestamp2 = str(int(round(time.time()*1000)))
	nonce2 = getrandomstring()
	sing3 = dingsignature(nonce2,encrypt2,'123456',timestamp2)
	data = {'msg_signature':sing3,'encrypt':encrypt2,'timeStamp':timestamp2,'nonce':nonce2}
	return json.dumps(data)

def upzibiao(alist,key,value,**kw):
	emptylist = []
	count = 0
	ll = len(alist)
	for i in range(ll):
		if alist[i][key]==value:
			count = i
	# find the no. of row
	for i in range(ll):
		emptydic = {}
		if i == count:
			emptydic = dict(alist[i],**kw)
			for k,v in emptydic.items():
				emptydic[k] = {'value':v}
			emptylist.append(emptydic)
	#change the value of the row
		else:
			emptydic = alist[i]
			for k,v in emptydic.items():
				emptydic[k] = {'value':v}
			emptylist.append(emptydic)
	#keep the origin value 
	#print(emptylist)
	return emptylist

def getzibiao(shujuid,url,head,kongjian):
	data = {"data_id":shujuid}
	chaxun = requests.post(url,headers=head,data=json.dumps(data))
	try:
		return json.loads(chaxun.text)['data'][kongjian]
	except:
		return 0

def get_id(hd,url,**kw):
	keys = []
	values = []
	cond = [] 
	for k,v in kw.items():
		dic = {}
		keys.append(k)
		values.append(v)
		dic["field"] = k
		dic["method"] = "eq"
		dic["value"] = v
		cond.append(dic)
	data = {'data_id':"",
            "limit":3,
            "fields":keys,
            "filter":{
                "rel":"and",
                "cond":cond
                }}
	result = requests.post(url,headers=hd,data=json.dumps(data))
	if result.text == '{"data":[]}':
        	return 0
	else:
		try:
			return json.loads(result.text)["data"][0]["_id"]
		except KeyError:
			return 0
	


app = Flask(__name__)

@app.route('/dingtalk/',methods=['POST'])
def dingtalk():
	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	dingtoken = json.loads(requests.get(r'https://oapi.dingtalk.com/gettoken',params={'corpid':'ding614949de72a0b8a2','corpsecret':'T_mc8bKh1_XV87k2ydBZ1h2rdf5d4CNmEQ7EGe46aANrWswtE6YiAp5IfTm-_s4w'}).text)['access_token']
	headers = {'Content-Type':r'application/json'}
	headers_jiandaoyun = {'Authorization':'Bearer '+'JDbXZjnci8k679jJBugsy7m68s0JuPCd','Content-Type': 'application/json;charset=utf-8'}
	hturl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fb8cd1d1e260bca03edc/'
	signature = request.args.get('signature')
	payload = request.data.decode('utf-8')
	encrypt = json.loads(payload)['encrypt']
	content2 = json.loads(AEScry.decrypto(encrypt))
	#print(content)
	EventType = content2['EventType']
	try:
		shenpitype = content2['type']
		print(shenpitype)
	except KeyError:	
		data2dingding = success()
		return data2dingding
	processCode = content2['processCode']
	staffId = content2['staffId']
	if processCode == 'PROC-QQXJ732V-JRNP7OFDN0XWW17ITBP92-FHGUCF9J-1' and shenpitype != "comment":
		#print("Qiyue zai luru huikuan le")
		data = {'process_instance_id':content2['processInstanceId']}
		url = r'https://oapi.dingtalk.com/topapi/processinstance/get?access_token=' + dingtoken
		shenpi = requests.post(url,headers=headers,data=json.dumps(data))
		huitiao = json.loads(shenpi.text)
		try:
			if huitiao['process_instance']['operation_records'][-2]['userid']=='15204862616815034':
				huikuan = json.loads(huitiao['process_instance']["form_component_values"][33]['value'])[0]['rowValue']
				daokuanchangdu = len(huikuan)
				if daokuanchangdu == 4:
					daokuanzhanghu = huikuan[0]['value']
					daokuanriqi = huikuan[1]['value']
					daokuanzhuti = huikuan[2]['value']
					daokuanjine = huikuan[3]['value']
				msg = b'\xe6\x9f\x92\xe6\x9c\x88\xe5\x9c\xa8\xe5\xbd\x95\xe5\x85\xa5\xe5\x9b\x9e\xe6\xac\xbe'.decode('utf-8')
		
				caiwu = {"msgtype": "text","text": {"content":msg+','+daokuanzhuti+','+daokuanjine}}
				caiwuurl = r'https://oapi.dingtalk.com/robot/send?access_token=522debd269ea8edd436e10cdd431eeb8a392c5545aaaf6cc9d37aa909ff6e9ad'
				requests.post(caiwuurl,headers=headers,data=json.dumps(caiwu))
		except:
			pass
		'''
		try:
			huikuan = json.loads(huitiao['process_instance']["form_component_values"][33]['value'])[0]['rowValue']
			daokuanchangdu = len(huikuan)
			if daokuanchangdu == 4:
				daokuanzhanghu = huikuan[0]['value']
				daokuanriqi = huikuan[1]['value']
				daokuanzhuti = huikuan[2]['value']
				daokuanjine = huikuan[3]['value']
			htbh = huitiao["process_instance"]["form_component_values"][32]['value']
			yishou = b'\xe5\xb7\xb2\xe6\x94\xb6'.decode('utf-8')
			htid = get_id(headers_jiandaoyun,hturl+'data',_widget_1516698509185=htbh)
			print(htid)
			if huitiao['process_instance']['tasks'][-1]['userid']=='15304953559712814':
				skmx = getzibiao(htid,hturl+"data_retrieve",headers_jiandaoyun,'_widget_1516698509441')
				if skmx:
					htdata = {"data_id":htid,
						"data":{"_widget_1516698509441":{"value":upzibiao(skmx,'_widget_1516698509458',daokuanjine,_widget_1516698509493=yishou,_widget_1548307984358=daokuanzhanghu,_widget_1548307984428=daokuanzhuti,_widget_1547106268040=daokuanriqi)}}}
					gengxin = requests.post(hturl+'data_update',headers=headers_jiandaoyun,data=json.dumps(htdata))
			#huikuan.append(huitiao["process_instance"]["form_component_values"][32])
			'''
			#caiwu = {"msgtype": "text","text": {"content":json.loads(gengxin.text)}}
		caiwu2 = {"msgtype": "text","text": {"content":huitiao}}
		caiwuurl2 = r'https://oapi.dingtalk.com/robot/send?access_token=82c3441cc9313a680164d117159fbc887627ace25a7d5a4f00021d6afa70e963'
			#caiwuurl = r'https://oapi.dingtalk.com/robot/send?access_token=522debd269ea8edd436e10cdd431eeb8a392c5545aaaf6cc9d37aa909ff6e9ad'
			#requests.post(caiwuurl,headers=headers,data=json.dumps(caiwu))
		requests.post(caiwuurl2,headers=headers,data=json.dumps(caiwu2))
		#except:
			#pass
		
	if EventType == 'bpms_instance_change' and shenpitype =='start' and processCode == 'PROC-QQXJ732V-JRNP7OFDN0XWW17ITBP92-FHGUCF9J-1':
		print(content2['processInstanceId'])
		data = {'process_instance_id':content2['processInstanceId']}
		url = r'https://oapi.dingtalk.com/topapi/processinstance/get?access_token=' + dingtoken
		shenpi = requests.post(url,headers=headers,data=json.dumps(data))
		huitiao = json.loads(shenpi.text)
		content = huitiao['process_instance']['form_component_values']
		try:
			userid = huitiao['process_instance']['operation_records'][0]['userid']
		except KeyError:
			pass
		faqiren = huitiao["process_instance"]['title'][:-11]
		gongsimingcheng = content[1]['value']
		bumen = content[2]['value']
		yewuleixing = content[3]['value']
		hangye = content[14]['value']
		qiyeguimo = content[16]['value']
		shengfen = content[17]['value']
		chengshi = content[18]['value']
		lianxiren = content[19]['value']
		zhiwei = content[20]['value']
		lianxidianhua = content[21]['value']
		xiansuoren = content[22]['value']
		dizhi = content[23]['value']
		#xiansuoren = content[24]['value']
		kp = json.loads(content[25]['value'])
		kpmingxi = kp[0]['rowValue']
		kaipiaoleixing = kpmingxi[0]['value']
		if len(kpmingxi[1]['value'])==0:
			kaipiaodanwei = kpmingxi[2]['value']
			shuihao = kpmingxi[3]['value']
		else:
			kaipiaodanwei = kpmingxi[1]['value']
			shuihao = kpmingxi[2]['value']
		try:
			kaihuyinhang = kp[0]['rowValue'][4]['value']
		except IndexError:	
			kaihuyinhang = ""
		try:
			yinhangzhanghao = kp[0]['rowValue'][5]['value']
		except IndexError:	
			yinhangzhanghao = ""
		try:
			kaipiaodizhi = kp[0]['rowValue'][6]['value']
		except IndexError:	
			kaipiaodizhi = ""
		try:
			kaipiaodianhua = kp[0]['rowValue'][7]['value']
		except IndexError:	
			kaipiaodianhua = ""
		userinfo = {'_id':userid,'name':faqiren,'username':faqiren}
		headers_jiandaoyun = {'Authorization':'Bearer '+'JDbXZjnci8k679jJBugsy7m68s0JuPCd','Content-Type': 'application/json;charset=utf-8'}
		jdycy = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5c2375499bc4eb5275d01df2/'
		cydata = {
			"data_id":"",
			"limit":1,
			"fields":['_widget_1545827657601'],
			"filter":{
				"cond":[{
					"field":"_widget_1545827657601",
					"method":"eq",
					"value":faqiren
					}]
				}
			}
		cyresult = requests.post(jdycy+'data',headers=headers_jiandaoyun,data=json.dumps(cydata))
		cyid = json.loads(cyresult.text)['data'][0]['_id']
		cydata2 = {"data_id":cyid}
		cychaxun = requests.post(jdycy+'data_retrieve',headers=headers_jiandaoyun,data=json.dumps(cydata2))
		cy = json.loads(cychaxun.text)['data']
		cykongjian = cy['_widget_1545827657617']['_id']
		cybumen = cy['_widget_1545878256148']
		bumen1 = cy['_widget_1545831700373']
		bumen2 = cy['_widget_1545831700389']
		global khbh
		khurl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fd86144a170349c2d189/'
		oldid = get_id(headers_jiandaoyun,khurl+'data',_widget_1547519109440=content2['processInstanceId'])
		if oldid != 0:
			scdata = {"data_id":oldid}
			requests.post(khurl+'data_delete',headers=headers_jiandaoyun,data=json.dumps(scdata))
			khbh -= 1
		xinzeng_data = {"data":{
					'_widget_1531221265045':{'value':'FW'+str(khbh)},
					'_widget_1516699004461':{'value':gongsimingcheng},
					'_widget_1517210886231':{'value':hangye},
					'_widget_1532329930172':{'value':qiyeguimo},
					'_widget_1536226897546':{'value':qiyeguimo},
					'_widget_1516699004474':{'value':lianxiren},
					'_widget_1532329930186':{'value':zhiwei},
					'_widget_1516699004487':{'value':lianxidianhua},
					'_widget_1516784498871':{'value':dizhi},
					'_widget_1516783129535':{'value':faqiren},
					'_widget_1516774132754':{'value':shuihao},
					'_widget_1516774132849':{'value':kaipiaoleixing},
					'_widget_1516699004500':{'value':kaipiaoleixing+'\n'+gongsimingcheng+'\n'+shuihao+'\n'+kaihuyinhang+'\n'+yinhangzhanghao+'\n'+kaipiaodizhi+'\n'+kaipiaodianhua},
					'_widget_1516850835655':{'value':xiansuoren},
					'_widget_1517210273985':{'value':{"province":shengfen}},
					'_widget_1516852050227':{'value':dizhi},
					'_widget_1516774132890':{'value':cykongjian},
					'_widget_1516782672226':{'value':bumen1},
					'_widget_1516783129574':{'value':bumen2},
					'_widget_1547519109440':{'value':content2['processInstanceId']}
					}}
		xinzeng_result = requests.post(khurl+'data_create',headers=headers_jiandaoyun,data=json.dumps(xinzeng_data))
		khbh += 1
		todingding = b'\xe5\x97\xa8\xef\xbc\x81'.decode('utf-8')+faqiren+b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\x86\xe4\xb8\x80\xe4\xb8\xaa\xe5\xa2\x9e\xe5\x80\xbc\xe4\xb8\x9a\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe5\x93\xa6\xef\xbc\x81'.decode('utf-8')
		cuowu = {"msgtype": "text","text": {"content":todingding}}
		
		fenxi = {"msgtype": "text","text": {"content":huitiao}}

		fenxiurl = r'https://oapi.dingtalk.com/robot/send?access_token=0c636db35b9d7fb5f0d2f22c08c2b7544e262ea4cd0bce1b21fa714c8387518f'
		
		
		jqr = r'https://oapi.dingtalk.com/robot/send?access_token=069098ad86129df9f90f664b7702b22e010828d48467bdeda9586f6628d6ad0b'
		requests.post(jqr,headers=headers,data=json.dumps(cuowu))
		requests.post(fenxiurl,headers=headers,data=json.dumps(fenxi))
	else:
		pass
	data2dingding = success()
	return data2dingding


@app.route('/xfwfapiao/',methods=['POST'])
def xfwfapiao():
	payload = request.data.decode('utf-8')
	headers = {'Authorization': 'Bearer ' + 'JDbXZjnci8k679jJBugsy7m68s0JuPCd', 'Content-Type': 'application/json;charset=utf-8'}
	data = json.loads(payload)
	shuju = data['data']
	shoujihao = shuju['_widget_1543303621462']
	invoiceCode = shuju['_widget_1543296188294']
	invoiceNumber = shuju['_widget_1543296188310']
	billTime = shuju['_widget_1543296188981']
	invoiceAmount = shuju['_widget_1543296188339']
	checkCode = shuju['_widget_1547697009119']
	tokenurl = requests.get(r'https://open.leshui365.com/getToken',params={'appKey':'606d29e9d84148fea94ca1970c1eb81b','appSecret':'e64a675f-5df5-40b8-a024-009cddb5d7a1'})
	token = json.loads(tokenurl.text)['token']
	fp_data = {
            "invoiceCode":invoiceCode,
            "invoiceNumber": invoiceNumber,
            "billTime": billTime,
	    "checkCode":checkCode,
            "invoiceAmount": invoiceAmount,
            "token": token
            }
	fapiao_url = "https://open.leshui365.com/api/invoiceInfoForCom"
	fp_head = {'Content-Type': 'application/json'}
	chaxun = requests.post(fapiao_url,headers=fp_head,data=json.dumps(fp_data))
	rlt = json.loads(chaxun.text)
	try:
		print(rlt['resultMsg'])
	except KeyError:
		return 'success'

	fenxi = {"msgtype": "text","text": {"content":rlt['resultMsg']}}
	fenxiurl = r'https://oapi.dingtalk.com/robot/send?access_token=ee7e64f4e763996abe23c621340987ab67dca9cbdea36db1f3aa0348e8ad0c82'
	requests.post(fenxiurl,headers=headers,data=json.dumps(fenxi))
	chenggong2 = b'\xe6\x9f\xa5\xe9\xaa\x8c\xe7\xbb\x93\xe6\x9e\x9c\xe6\x88\x90\xe5\x8a\x9f'
	chenggong = b'\xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8f\x91\xe7\xa5\xa8\xe4\xbf\xa1\xe6\x81\xaf\xe6\x88\x90\xe5\x8a\x9f'
	if rlt['resultMsg'] == chenggong.decode('utf-8') or rlt['resultMsg'] == chenggong2.decode('utf-8'):
		if True:
			mingxi = json.loads(rlt['invoiceResult'])
			invoiceTypeName = mingxi['invoiceTypeName']
			purchaserName = mingxi['purchaserName']
			taxpayerNumber = mingxi['taxpayerNumber']
			taxpayerAddressOrId = mingxi['taxpayerAddressOrId']
			taxpayerBankAccount = mingxi['taxpayerBankAccount']
			salesName = mingxi['salesName']
			salesTaxpayerNum = mingxi['salesTaxpayerNum']
			salesTaxpayerAddress = mingxi['salesTaxpayerAddress']
			salesTaxpayerBankAccount = mingxi['salesTaxpayerBankAccount']
			totalAmount = mingxi['totalAmount']
			totalTaxNum = mingxi['totalTaxNum']
			totalTaxSum = mingxi['totalTaxSum']
			if float(totalTaxNum)/float(totalTaxSum)>6:
				shuilv = 6
			else:
				shuilv = 16
			detail = mingxi['invoiceDetailData']
			detail_len = len(detail)
			create_url = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5c05f9a09c058e58d1885863/data_create'
			data1 = {
            'data':{
                '_widget_1543903420621':{'value':invoiceCode},
                '_widget_1543903420638':{'value':invoiceNumber},
                '_widget_1543895509336':{'value':invoiceTypeName},
                '_widget_1543895508987':{'value':billTime},
                '_widget_1543895508863':{'value':purchaserName},
                '_widget_1547723602952':{'value':taxpayerNumber},
                '_widget_1547723603040':{'value':taxpayerAddressOrId},
                '_widget_1547723603129':{'value':taxpayerBankAccount},
                '_widget_1543895508783':{'value':salesName},
                '_widget_1547723603259':{'value':salesTaxpayerNum},
                '_widget_1547723603350':{'value':salesTaxpayerAddress},
                '_widget_1547723603442':{'value':salesTaxpayerBankAccount},
                '_widget_1543900369237':{'value':totalAmount},
                '_widget_1543895509244':{'value':totalTaxNum},
                '_widget_1543900369445':{'value':totalTaxSum},
                '_widget_1543895509212':{'value':shuilv}
                }
            }
			mingxilist = []
			for i in range(detail_len):
				goodserviceName = detail[i]['goodserviceName']
				model = detail[i]['model']
				unit = detail[i]['unit']
				number = detail[i]['number']
				price = detail[i]['price']
				sum_price = detail[i]['sum']
				taxRate = detail[i]['taxRate']
				tax = detail[i]['tax']
				newdic = {
                '_widget_1547723603663':{'value':goodserviceName},
                '_widget_1547723603666':{'value':model},
                '_widget_1547723603671':{'value':unit},
                '_widget_1547723603687':{'value':number},
                '_widget_1547723603678':{'value':price},
                '_widget_1547723603698':{'value':sum_price},
                '_widget_1547723604779':{'value':taxRate},
                '_widget_1547723604943':{'value':tax},
                }
				mingxilist.append(newdic)
			mingxidic = {'value':mingxilist}
			data1['data']['_widget_1547723603628'] = mingxidic
			data1['is_start_workflow'] = True
			requests.post(create_url,headers=headers,data=json.dumps(data1))
	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	if request.headers['x-jdy-signature'] != get_signature(nonce,payload,'OFlQ5zlc0meuer4nhQpSMINT',timestamp):
		return 'fail',401
	return 'success'

@app.route('/zibo/')
def zibo():
	return redirect('https://www.jiandaoyun.com/app/5c18698ebdd33a29f6fe9d25/entry/5c18699d7af9de310852aca6')

@app.route('/zibobaobiao/')
def zibobaobiao():
	return redirect('https://www.jiandaoyun.com/app/5c18698ebdd33a29f6fe9d25/entry/5c22e0f4cdacdf48e8b5dd9c')

@app.route('/liladafen/')
def liladafen():
	return redirect('https://jiandaoyun.com/app/5bf2813c9901821f3871547d/entry/5c26e8cd0f87f348fecd9ec0')
@app.route('/')
def helloworld():
	return 'Hello'

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80,debug=True)
