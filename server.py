from flask import Flask,request,redirect
import json
import requests
import hashlib
import time
import AEScry
import string
import random

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

app = Flask(__name__)

@app.route('/dingtalk/',methods=['POST'])
def dingtalk():
	nonce = request.args.get('nonce')
	timestamp = request.args.get('timestamp')
	dingtoken = json.loads(requests.get(r'https://oapi.dingtalk.com/gettoken',params={'corpid':'ding614949de72a0b8a2','corpsecret':'T_mc8bKh1_XV87k2ydBZ1h2rdf5d4CNmEQ7EGe46aANrWswtE6YiAp5IfTm-_s4w'}).text)['access_token']
	headers = {'Content-Type':r'application/json'}
	signature = request.args.get('signature')
	payload = request.data.decode('utf-8')
	encrypt = json.loads(payload)['encrypt']
	content = json.loads(AEScry.decrypto(encrypt))
	EventType = content['EventType']
	try:
		shenpitype = content['type']
	except KeyError:	
		data2dingding = success()
		return data2dingding
	processCode = content['processCode']
	if EventType == 'bpms_instance_change' and shenpitype =='start' and processCode == 'PROC-QQXJ732V-JRNP7OFDN0XWW17ITBP92-FHGUCF9J-1':
	#if EventType == 'bpms_instance_change' and shenpitype =='start':
		print(content['processInstanceId'])
		data = {'process_instance_id':content['processInstanceId']}
		url = r'https://oapi.dingtalk.com/topapi/processinstance/get?access_token=' + dingtoken
		shenpi = requests.post(url,headers=headers,data=json.dumps(data))
		#print(shenpi.text)
		huitiao = json.loads(shenpi.text)
		content = huitiao['process_instance']['form_component_values']
		#print(content)
		try:
			userid = huitiao['process_instance']['operation_records'][0]['userid']
			print('UserId:',userid)
		except KeyError:
			pass
			#print(huitiao)
		faqiren = huitiao["process_instance"]['title'][:-11]
		print(faqiren,':',userid)
		hetong = {}
		#mingxi = []
		for i in content:
			if 'name' not in i.keys():
				continue
			else:
				if i['value'] in ('null',b'\xe6\x97\xa0'.decode('utf-8'),'[]',b'\xe6\x94\xb6\xe4\xbb\xb6\xe4\xba\xba\xef\xbc\x9a\n\xe5\x9c\xb0\xe5\x9d\x80\xef\xbc\x9a'.decode('utf-8'),'0'):
       					continue
				else:					
					hetong[i['name']] = i['value']
					
		ht = str(hetong).replace("\'",'').replace('}','').replace('{','')
		gongsimingcheng = content[1]['value']
		bumen = content[2]['value']
		yewuleixing = content[3]['value']
		hangye = content[14]['value']
		qiyeguimo = content[16]['value']
		lianxiren = content[17]['value']
		zhiwei = content[18]['value']
		lianxidianhua = content[19]['value']
		dizhi = content[20]['value']
		xiansuoren = content[21]['value']
		kp = json.loads(content[25]['value'])
		print(kp)
		kaipiaoleixing = kp[0]['rowValue'][0]['value']
		kaipiaodanwei = kp[0]['rowValue'][1]['value']
		shuihao = kp[0]['rowValue'][2]['value']
		kaihuyinhang = kp[0]['rowValue'][3]['value']
		yinhangzhanghao = kp[0]['rowValue'][4]['value']
		kaipiaodizhi = kp[0]['rowValue'][5]['value']
		kaipiaodianhua = kp[0]['rowValue'][6]['value']
		userinfo = {'_id':userid,'name':faqiren,'username':faqiren}
		print('OK,HERE')
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
		#print(cyresult.text)
		cyid = json.loads(cyresult.text)['data'][0]['_id']
		cydata2 = {"data_id":cyid}
		cychaxun = requests.post(jdycy+'data_retrieve',headers=headers_jiandaoyun,data=json.dumps(cydata2))
		#print(cychaxun.text)
		cy = json.loads(cychaxun.text)['data']
		cykongjian = cy['_widget_1545827657617']['_id']
		print(cykongjian)
		cybumen = cy['_widget_1545878256148']
		bumen1 = cy['_widget_1545831700373']
		bumen2 = cy['_widget_1545831700389']
		print(bumen1,bumen2)
		chaxunurl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fd86144a170349c2d189/data'
		chaxun_data = {"data_id":'',"limit":1,"fields":['_widget_1516699004461'],"filter":{"rel": "and","cond": [{"field":'_widget_1516699004461',"method": "eq","value":[gongsimingcheng]}]}}
		chaxun_result = requests.post(chaxunurl,headers=headers_jiandaoyun,data=json.dumps(chaxun_data))
		print(chaxun_result.text)
		if chaxun_result.text == '{"data":[]}':
			xinzengurl = r'https://www.jiandaoyun.com/api/v1/app/5a66fb220e99fa0343e995bc/entry/5a66fd86144a170349c2d189/data_create'
			xinzeng_data = {"data":{
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
					'_widget_1516852050227':{'value':dizhi},
					'_widget_1516774132890':{'value':cykongjian},
					'_widget_1516782672226':{'value':bumen1},
					'_widget_1516783129574':{'value':bumen2}}}
			xinzeng_result = requests.post(xinzengurl,headers=headers_jiandaoyun,data=json.dumps(xinzeng_data))
			print(xinzeng_result.text)
		kaipiao = json.loads(content[25]['value'])[0]['rowValue']
		kpxx = ''
		for i in kaipiao:
				kpxx = kpxx+i['value']+','
		todingding = b'\xe5\x97\xa8\xef\xbc\x81'.decode('utf-8')+faqiren+b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\x86\xe4\xb8\x80\xe4\xb8\xaa\xe5\xa2\x9e\xe5\x80\xbc\xe4\xb8\x9a\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe5\x93\xa6\xef\xbc\x81'.decode('utf-8')
		cuowu = {"msgtype": "text","text": {"content":todingding}}
		
		fenxi = {"msgtype": "text","text": {"content":shenpi.text}}

		fenxiurl = r'https://oapi.dingtalk.com/robot/send?access_token=0c636db35b9d7fb5f0d2f22c08c2b7544e262ea4cd0bce1b21fa714c8387518f'
		
		
		jqr = r'https://oapi.dingtalk.com/robot/send?access_token=069098ad86129df9f90f664b7702b22e010828d48467bdeda9586f6628d6ad0b'
		requests.post(jqr,headers=headers,data=json.dumps(cuowu))
		requests.post(fenxiurl,headers=headers,data=json.dumps(fenxi))
	else:
		pass
	data2dingding = success()
	return data2dingding


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
