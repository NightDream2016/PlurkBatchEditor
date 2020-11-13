import oauth2 as oauth
import json
import urllib.parse
import array
import webbrowser
import datetime
import Plurk
#region PreDefine

OAUTH_REQUEST_TOKEN = 'https://www.plurk.com/OAuth/request_token'
OAUTH_ACCESS_TOKEN = 'https://www.plurk.com/OAuth/access_token'
OAUTH_VERIFIER = 'https://www.plurk.com/OAuth/authorize'



#endregion



#region Request OAuth Authentication

def get_request_token(app_key, app_secret):
	consumer = oauth.Consumer(app_key, app_secret)
	client = oauth.Client(consumer)
	response = client.request(OAUTH_REQUEST_TOKEN, method='POST')
	return response

def get_access_token(app_key, app_secret, oauth_token, oauth_token_secret, oauth_verifier):
	consumer = oauth.Consumer(app_key, app_secret)
	token = oauth.Token(oauth_token, oauth_token_secret)
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	response = client.request(OAUTH_ACCESS_TOKEN, method='POST')
	return response

def requestOauthClientWithUserAuthentication(appKey, appSecret):

	print ("Start Get Request Token")

	requestTokenResponse = get_request_token(appKey, appSecret)
	requestTokenParseResult = urllib.parse.parse_qs(requestTokenResponse[1])
	oauth_token = requestTokenParseResult[b'oauth_token'][0].decode('utf-8')
	oauth_token_secret = requestTokenParseResult[b'oauth_token_secret'][0].decode('utf-8')

	webbrowser.open(OAUTH_VERIFIER + '?oauth_token=' + oauth_token)

	verifier = input("authorize code:")

	accessTokenResult = get_access_token(appKey, appSecret, oauth_token, oauth_token_secret, verifier) 
	accessTokenParseResult = urllib.parse.parse_qs( accessTokenResult[1])

	oauth_token = accessTokenParseResult[b'oauth_token'][0].decode('utf-8')
	oauth_token_secret = accessTokenParseResult[b'oauth_token_secret'][0].decode('utf-8')

	# print('Token:'+ oauth_token + '\nSecret:' + oauth_token_secret)

	client = requestOauthClient (appKey, appSecret, oauth_token, oauth_token_secret)

	return client

def requestOauthClient(appKey, appSecret, oauth_token, oauth_token_secret):
	
	consumer = oauth.Consumer(appKey, appSecret)
	token = oauth.Token(oauth_token, oauth_token_secret)
	client = oauth.Client(consumer, token)

	print(client.token.to_string())

	return client

def requestOauthClientFromString(appKey, appSecret, tokenString):
	consumer = oauth.Consumer(appKey, appSecret)
	token = oauth.Token.from_string(tokenString)
	client = oauth.Client(consumer, token)

	return client

#endregion


#region - API 

def getUsersMe(client):
	apiUrl = 'https://www.plurk.com/APP/Users/me'
	response = client.request(apiUrl, method='POST')
	return response

def getOwnProfile(client):
	apiUrl = 'https://www.plurk.com/APP/Profile/getOwnProfile'
	response = client.request(apiUrl, method='POST')
	return response

def getPlurk(client, id):
	apiUrl = 'https://www.plurk.com/APP/Timeline/getPlurk'
	bodyData = {'plurk_id' : id}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	# plurk = Plurk.parseFromJSON(response)
	return response

def getPlurks(client, offset, limit, filter):
	apiUrl = 'https://www.plurk.com/APP/Timeline/getPlurks'
	bodyData = {'offset' : offset, 'limit' : limit, 'filter': filter}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

def getPlurks_Multitimes(client, offset, limit, filter):

	getPlurkList = []
	offsetTimeResult = offset
	while len(getPlurkList) < int(limit):
		jsonCurrentResult = getPlurks(client, offsetTimeResult, limit, filter)
		currentPlurkResult = json.loads(jsonCurrentResult[1].decode('utf-8'))
		if len(currentPlurkResult['plurks']) == 0:
			break
		getPlurkList += currentPlurkResult['plurks']
		lastResult = getPlurkList[-1]
		timeOfLastResult = datetime.datetime.strptime(lastResult['posted'], '%a, %d %b %Y %H:%M:%S GMT')
		offsetTimeResult = timeOfLastResult.strftime('%Y-%m-%dT%H:%M:%S')

	return getPlurkList

def getUnreadPlurks(client, offset, limit, filter):
	apiUrl = 'https://www.plurk.com/APP/Timeline/getUnreadPlurks'
	bodyData = {'offset' : offset, 'limit' : limit, 'filter': filter}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

def expireToken(client):
	apiUrl = 'https://www.plurk.com/APP/expireToken'
	response = client.request(apiUrl, method='POST')
	return response

#endregion

#region - API - Response

def getResponse(client, id):
	apiUrl = 'https://www.plurk.com/APP/Responses/get'
	bodyData = {'plurk_id': id}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

def responseDelete(client, response_id, plurk_id):
	apiUrl = 'https://www.plurk.com/APP/Responses/responseDelete'
	bodyData = {'response_id': id, 'plurk_id' : plurk_id}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

#endregion

#region - API - Timeline

def plurkDelete (client, id):
	plurkEdit(client, id, ' ')
	apiUrl = 'https://www.plurk.com/APP/Timeline/plurkDelete'
	bodyData = {'plurk_id': id}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

def plurkDelete_Mulitple (client, plurkList, preservedIDs):
	failedIDList = []
	for plurk in plurkList:
		id = plurk['plurk_id']

		if id in preservedIDs:
			print('ID'+ str(id) + 'preserved. No delete')
			continue

		user_id = plurk['user_id']
		print('user_id: '+ str(user_id))
		result = plurkDelete(client, id)
		resultString = result[1].decode('utf-8') 
		if resultString != '{"success_text":"ok"}':
			print('plurk_id '+ str(id) + 'delete failed: ' + resultString)
			failedIDList.append({str(id) : resultString})
		else:
			print('plurk_id '+ str(id) + ' delete Success.')
	return failedIDList

def plurkEdit (client, id, content):
	apiUrl = 'https://www.plurk.com/APP/Timeline/plurkEdit'
	bodyData = {'plurk_id': id, 'content': content}
	resultUrlString = urllib.parse.urlencode(bodyData)
	response = client.request(apiUrl, method='POST', body = resultUrlString.encode('utf-8'))
	return response

#endregion


def main():

	client = ''
	isAuthenticated = False

	while isAuthenticated == False:
		appKeyFile = open('Auth.txt', 'r', encoding = 'UTF-8')
		content = appKeyFile.readlines()
		appKey = content[0].rstrip()
		appSecret = content[1].rstrip()
		appKeyFile.close()

		print('Request Client Data With:\n1.User Authentication\n2.Authentication token and secret(Input)\n3.Read File')
		choose = input("Input:")
		if choose == '1':
			client = requestOauthClientWithUserAuthentication(appKey, appSecret)
			tokenfile = open('requestToken', 'w', encoding = 'UTF-8') 
			tokenfile.write(client.token.to_string())
			tokenfile.close()
			isAuthenticated = True
		elif choose == '2':
			oauth_token = input("token:")
			oauth_token_secret = input("token_secret:")
			client = requestOauthClient(appKey, appSecret, oauth_token, oauth_token_secret)
			isAuthenticated = True
		elif choose == '3':
			file = open('requestToken', 'r', encoding='UTF-8')
			content = file.read()
			content = content.rstrip()
			file.close()
			client = requestOauthClientFromString(appKey, appSecret, content)
			isAuthenticated = True
		else:
			print('Unknown Command. Continue.')
			continue

	while True:
		print('Please Choose Your Command:')
		print('1.GetProfile\n2.GetPlurks\n3.GetUnreadPlurks\n4.DeletePlurk\n5.GetPlurks(WithMultiLoad)\n6.GetPlurk(id)\n7.EditPlurk\n8.MultipleDeletePlurk\n9.My User Data\n10.Expire Token\n11.Quit')
		choose = input("Input:")
		result = ''
		if choose == '1':
			result = getOwnProfile(client)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
			print (jsonPlurkResult)
		elif choose == '2':
			time = input('TimeOffset:(YYYY-MM-DDTHH:MM:SS)')
			limit = input('Limit:')
			filter = input('filter:')
			result = getPlurks(client, time, limit, filter)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
		
			# for result in jsonPlurkResult:
				# plurk = Plurk.parseFromJSON(result)

			print (jsonPlurkResult)
		elif choose == '3':
			time = input('TimeOffset:(YYYY-MM-DDTHH:MM:SS)')
			limit = input('Limit:')
			filter = input('filter:')
			result = getUnreadPlurks(client, time, limit, filter)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
			print (jsonPlurkResult)
		elif choose == '4':
			id = input('plurk_id:')
			result = plurkDelete(client, id)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
			print (jsonPlurkResult)
		elif choose == '5':
			time = input('TimeOffset:(YYYY-MM-DDTHH:MM:SS)')
			limit = input('Limit:')
			filter = input('filter:')
			result = getPlurks_Multitimes(client, time, limit, filter)
			for object in result:
				print(object['plurk_id'])
		elif choose == '6':
			id = input('plurk_id:')
			result = getPlurk(client, id)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
			print (jsonPlurkResult)
		elif choose == '7':
			id = input('plurk_id:')
			editContent = input('content:')
			result = plurkEdit(client, id, editContent)
			jsonPlurkResult = json.loads(result[1].decode('utf-8'))
			print (jsonPlurkResult)
		elif choose == '8':
			time = input('TimeOffset:(YYYY-MM-DDTHH:MM:SS)')
			limit = input('Limit:')
			filter = input('filter:')
			plurksToDelete = getPlurks_Multitimes(client, time, limit, filter)
			failedIDList = plurkDelete_Mulitple(client, plurksToDelete, [])
			print(failedIDList)
		elif choose == '9':
			result = getUsersMe(client)
			jsonResult = json.loads(result[1].decode('utf-8'))
			print(jsonResult)
		elif choose == '10':
			result = expireToken(client)
		elif choose == '11':
			break
		else:
			print('Unknown Command. Continue.')
			continue

		

if __name__== "__main__":
    main()
