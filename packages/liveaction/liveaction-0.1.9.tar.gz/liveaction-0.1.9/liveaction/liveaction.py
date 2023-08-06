#!/usr/bin/env python3
'''
Description: LiveAction class to make API requests to LiveNX
Author: Vecheka Chhourn <vecheka.chhourn@nordstrom.com>
Version: 0.5.6
'''

# import grequests
import requests, urllib3, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # suppress SSL warning

class LiveAction:

	def __init__ (self, domain, apiToken):
		'''
		Constructor
		@param: domain - LiveAction's domain name.
		@param: api_token - LiveAction's bearer token.
		'''
		self.domain = domain
		# self.proxies = {'http': 'http://webproxy.nordstrom.net:8181/', 'https': 'http://webproxy.nordstrom.net:8181/'}
		self.headers = {"Authorization":"Bearer " + apiToken, 'Content-type':'application/json', 'Accept':'application/json'}


	def get(self, endpoint, params = None, isJob = False):
		'''
		GET request to RESTFUL API endpoint
		@param: endpoint - endpoint of the API
		@return: response of the request
		'''
		try:
			if isJob:
				return requests.get(endpoint, headers = self.headers, verify = False)
			if params != None:
				return requests.get(self.domain + endpoint, headers = self.headers, params = params, verify = False)

			return requests.get(self.domain + endpoint, headers = self.headers, verify = False)
		except Exception as err:
			return {'error': err}

	def post(self, endpoint, data):
		'''
		POST request to RESTFUL API endpoint
		@param: endpoint - endpoint of the API
		@param: data - data to be posted in the body of the request
		@return: response of the request
		'''
		try:
			return requests.post(self.domain + endpoint, headers = self.headers, json = data, verify = False)
		except Exception as err:
			return {'error': err}

	def put(self, endpoint, data = None):
		'''
		PUT request to RESTFUL API endpoint
		@param: endpoint - endpoint of the API
		@param: data - data to be posted in the body of the request
		@return: response of the request
		'''
		try:
			if data is None:
				return requests.put(self.domain + endpoint, headers = self.headers, verify = False)
			return requests.put(self.domain + endpoint, headers = self.headers, verify = False, data = json.dumps(data))
		except Exception as err:
			return {'error': err}

	def delete(self, endpoint):
		'''
		DELETE request to RESTFUL API endpoint
		@param: endpoint - endpoint of the API
		@return: response of the request
		'''
		try:
			return requests.delete(self.domain + endpoint, headers = self.headers, verify = False)
		except Exception as err:
			return {'error': err}

	def close_connection(self, request):
		'''
		Closes http requests.
		'''
		request.close()


	def startDeviceDiscovery(self, nodeID = None, siteID = '', isDataCenter = False, ipRanges = [], deviceIdentificationType = 'DISCOVERY'):
		'''
		Starts a device discovery on LA.
		@param: nodeID - node's ID of the device
		@param: siteID - site's ID of the device
		@param: isDataCenter - true if a device is at a Datacenter
		@param: ipRanges - ip addresses of the devices
		@param: deviceIdentificationType - type of device 'DISCOVERY (DEFAULT)', 'REFRESH' OR 'EDIT'
		@return: job's ID and job's result URL
		'''
		if nodeID is None:
			return {'success': False, 'message': 'Node ID has to be provided'}
		else:
			body = {
				"nodeId": nodeID,
				"siteIpRanges": [
				{
					"siteId": siteID,
					"isDataCenter": isDataCenter,
					"ipRanges": ipRanges
				}
				],
				"snmpCredential": {
					"type": "default",
					"credential": {}
				},
				"deviceIdentificationType": deviceIdentificationType

			}

			response = self.post('/deviceDiscovery/start/siteIpRange', body)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			if status_code == 200 or status_code == 201 :
				results = response.json()
				self.close_connection(response)
				return {'success': True, 'message': 'Device Discovery Started', 'data' : [results['jobId'], results['resultUrl']]}
			else:
				self.close_connection(response)
				return {'success': False, 'message': 'Device Discovery Failed with status code ' + str(status_code)}


	def getDeviceDiscovery(self):
		'''
		Gets current device discovery jobs.
		@return: jobs' IDs list if there are jobs
		'''

		response = self.get('/deviceDiscovery/jobs')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code == 200:
			results = response.json()
			job_ids = []
			for res in results:
				job_ids.append(res['jobId'])
			self.close_connection(response)
			return {'success': True, 'message': 'Successfully retrieve job IDs', 'data': job_ids}
		self.close_connection(response)
		return {'success': False, 'message': 'Failed to retrieve job IDs with status code ' + str(status_code)}

	def cancelDeviceDiscovery(self, jobID):
		'''
		Cancles a current running device discovery by ID
		@param: job_id - current running job's ID
		@return: True if the cacellation is a success
		'''

		response = self.put('/deviceDiscovery/jobs/' + jobID + '/cancel')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code == 202 or status_code == 200:
			self.close_connection(response)
			return {'success': True, 'message': 'Job cancelled successfully'}
		self.close_connection(response)
		return {'success': False, 'message': 'Job cancelled unsuccessfully with status code ' + str(status_code)}


	def getDevices(self):
		'''
		Gets all devices from LA
		@return list of devices info from LA
		'''
		response = self.get('/devices')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code == 200:
			results = response.json()
			self.close_connection(response)
			if 'devices' in results:
				return {'success': True, 'message': 'Retrieving devices successfully', 'data': results['devices']}
			else:
				return {'success': False, 'message': 'No devices currently exist on Liveaction'}
		self.close_connection(response)
		return {'success': False, 'message': 'Retrieving devices unsuccessfully with status code ' + str(status_code)}

	def deleteDevice(self, id = None):
		'''
		Deletes a device from LA by the given ID.
		@param: id - device's id to be deleted
		@return: True if deletion is successful
		'''

		if id is not None:
			response = self.delete('/devices/' + id)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			self.close_connection(response)
			if status_code == 200:
				return {'success': True, 'message': 'Device deleted successfully'}
			else:
				return {'success': False, 'message': 'Device deleted unsuccessfully with status code ' + str(status_code)}
		else:
			self.close_connection(response)
			return {'success': False, 'message': 'Device\'s ID has to be provided'}


	def getJobResult(self, jobResultUrl = None, waitTime = 20):
		'''
		Gets devices information from job's result endpoint
		@param: jobResultUrl - job's result endpoint
		@param: wait_time - wait time for device discovery to finished
		@return: list of devices information
		'''
		if jobResultUrl is None:
			return {'success': False, 'message': 'Job\'s result endpoint is not provided'}
		else:
			print('Waiting for a job to finish...')
			response = self.get(jobResultUrl, isJob = True).json()
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			while 'results' not in response:
				try:
					response = self.get(jobResultUrl, isJob = True).json()
				except:
					return {'success': False, 'message': response}
			print('Job\'s Finished')
			results = response
			return {'success': True, 'message': 'Retrieving devices\' info successfully', 'data': results['results']}



	def addDevice(self, jobID = None, deviceInfo = None):
		'''
		Adds a device/devices to LA.
		@param: jobID - current job's ID of device discovery
		@param: deviceInfo - a list of device's infomation
		@return: False if failed to add a device
		'''

		if jobID is None or deviceInfo is None:
			return {'success': False, 'message': 'Job\'s ID or Device\'s information has to be provided'}
		else:

			body = {
				'jobId': jobID,
				'devices': deviceInfo
			}

			response = self.post('/devices', body)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			self.close_connection(response)
			if status_code == 200 or status_code == 202:
				return {'success': True, 'message': 'Devices added successfully'}
			self.close_connection(response)
			return {'success': False, 'message': 'Devices added unsuccessfully with status code ' + str(status_code)}

	def updateDevice(self, jobID = None, deviceInfo = None):
		'''
		Updates a device/devices on LA.
		@param: jobID - current job's ID of device discovery
		@param: deviceInfo - a list of device's infomation
		@return: False if failed to update a device
		'''
		if jobID is None or deviceInfo is None:
			return {'success': False, 'message': 'Job\'s ID or Device\'s information has to be provided'}
		else:
			body = {
				'jobId': jobID,
				'devices': deviceInfo
			}

			response = self.put('/devices', body)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			self.close_connection(response)
			print(status_code)
			if status_code == 200 or status_code == 202:
				return {'success': True, 'message': 'Devices updated successfully'}
			return {'success': False, 'message': 'Devices updated unsuccessfully with status code ' + str(status_code)}


	def findNodeID(self, nodeName = 'Local/Server'):
		'''
		Finds node id on LiveAction
		@param: nodeName associated with the node's ID
		@return Liveaction id that corresponds to the name provided/Local node id by default (currently the only node)
		'''
		response = self.get('/nodes')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		nodes = response.json()
		self.close_connection(response)
		for node in nodes['nodes']:
			if node['name'] == nodeName:
				return {'success': True, 'message': 'Node\'s ID is found', 'data': node['id']}
		return {'success': False, 'message': 'Node\'s ID cannot be found'}


	def createSite(self, siteName = None, siteDescription = None, site_type = '', tags = [], isDataCenter = False, address = '',
				city = '', state = '', zipCode = '', country = '', latitude = 0, longitude = 0):
		'''
		Creates site in LA
		@param: siteName - name of the site
		@param: siteDescription - description of the site
		@param: site_type - type of the site
		@param: tags - site's unique tags
		@param: isDataCenter - true if the site is a data center
		@param: address - street address of the site
		@param: city - city location of the site
		@param: state - state location of the site
		@param: zipCode - zip code of the site
		@param: country - site's country location
		@param: latitude
		@param: longitude
		@return: True if site's creation is successful
		'''

		if siteName is not None and siteDescription is not None:
			site_body = {
				"siteName": siteName,
				"siteDescription": siteDescription,
				"type": site_type,
				"tags": tags,
				"isDataCenter": isDataCenter,
				"isConfigured": True,
				"mailingAddress": {
					"address1": address,
					"address2": "",
					"city": city,
					"state": state,
					"zip": zipCode,
					"country": country
				},
				"position": {
					"latitude": latitude,
					"longitude": longitude
				},

			}

			response = self.post('/sites', site_body)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			self.close_connection(response)
			if status_code == 200:
				return {'success': True, 'message': 'Site created successfully'}
			else:
				return {'success': False, 'message': 'Site created unsuccessfully with status code ' + str(status_code)}
		else:
			return {'success': False, 'message': 'Site\'s name or description is not provided'}


	def getSites(self):
		'''
		Gets all sites that exist in LA.
		@return: list of sites IDs with respect to siteName if there are existing sites
		'''

		response = self.get('/sites')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code != 200:
			self.close_connection(response)
			return {'success': False, 'message': 'Retrieving sites unsuccessfully with status code ' + str(status_code)}

		results = response.json()
		if 'sites' not in results:
			self.close_connection(response)
			return {'success': False, 'message': 'No sites currently exist on LiveAction'}

		# sites = []
		# for site in results['sites']:
		# 	name = site['siteName']
		# 	sites.append({
		# 		name: site['id']
		# 	})

		self.close_connection(response)

		return {'success': True, 'message': 'Retrieving sites\' status successfully', 'data': results['sites']}

	def getDownSites(self):
		'''
		Gets all sites that are down on LA.
		@return: a list of sites ID if there are existing sites with down status
		'''
		response = self.get('/siteStatus')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code != 200:
			self.close_connection(response)
			return {'success': False, 'message': 'Retrieving sites\' status unsuccessfully with status code ' + str(status_code)}

		results = response.json()
		if 'nxSiteStatusAggregations' not in results:
			self.close_connection(response)
			return {'success': False, 'message': 'No sites currently exist on Liveaction'}

		sites = []
		for site in results['nxSiteStatusAggregations']:
			if site['status'] == 'NO_DATA' or site['status'] == 'DOWN':
				sites.append(site['entityId']['siteId'])
		self.close_connection(response)
		return {'success': True, 'message': 'Retrieving sites\' status successfully', 'data': sites}



	def deleteSite(self, siteID = None):
		'''
		Deletes a site from LA given its ID
		@param: site_id - id of the site
		@return: True if deletion is a success.
		'''
		if siteID is None:
			return {'success': False, 'message': 'Site\'s ID has to be provided'}
		else:
			response = self.delete('/sites/' + siteID)
			if isinstance(response, dict) and 'error' in response:
				return {'success': False, 'message': response['error']}
			status_code = response.status_code
			if status_code != 200:
				self.close_connection(response)
				return {'success': False, 'message': 'Deleting site unsuccessfully with status_code ' + str(status_code)}
			self.close_connection(response)
			return {'success': True, 'message': 'Deleting site successfully'}


	def getFlowReports(self):
		'''
		Gets all available flow reports from LA 2.
		@return: all flow reports from LA 2.
		'''

		response = self.get('/reports/flow')
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code == 200:
			results = response.json()
			result = []
			for res in results['reports']:
				result.append({
					'name': res['name'],
					'id': res['id']
				})
			self.close_connection(response)
			return {'success': True, 'message': 'Retrieving flow reports successfully', 'data': result}
		self.close_connection(response)
		return {'success': False, 'message': 'Retrieving flow reports unsuccessfully with status code ' + str(status_code)}


	def getTimeSeriesReport(self, flowID = None, params = None):
		'''
		Gets time series report of a specific flow from LA 2.
		@param: flowID - flow ID of the report
		@param: params - post body to be sent with the request including:
					- startTime: start time of the report
					- endTime: end time of the report
					- deviceSerial: a device's serial number
					- direction: flow direction(Inbound/Outbound)
					- interface: interface to run report on (eg: Tunnel900. Tunnel9001)
		@return: data of the traffic flow in a specific interval
		'''

		if flowID is None or params is None:
			return {'success': False, 'message': 'Flow\'s ID or Request\'s body is missing'}

		# if isGrequest == False:
		response = self.get(endpoint = '/reports/flow/' + flowID + '/runTimeSeries.csv', params = params)
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		if response.status_code == 200:
			response = response.content.decode('utf-8')
			return {'success': True, 'message': 'Retrieving reports successfully from Liveaction', 'data': response}

		response = json.loads(response.content.decode('utf-8'))
		return {'success': False, 'message': response['message']}
		# else:
		# 	endpoint = self.domain + '/reports/flow/' + flowID + '/runTimeSeries.csv'
		# 	unsent_requests = (grequests.get(endpoint, headers = self.headers, verify = False, params = p) for p in params)
		# 	results = grequests.map(unsent_requests)
		# 	return {'success': True, 'message': 'Retrieving reports successfully from Liveaction', 'data': results}


	def getCustomApplicationNameByID(self, appID = None):
		'''
		Gets custom appliation's name by app's ID from LA 2.
		@param: appID - application's ID
		@return: application's name
		'''
		if appID is None:
			return {'success': False, 'message': 'Application\'s ID has to be provided'}

		response = self.get(endpoint = '/applications/custom/' + appID)
		if isinstance(response, dict) and 'error' in response:
			return {'success': False, 'message': response['error']}
		status_code = response.status_code
		if status_code == 200:
			results = response.json()
			self.close_connection(response)
			return {'success': True, 'message': 'Retrieving application\'s name successfully', 'data': results['name']}

		results = response.json()
		self.close_connection(response)
		return {'success': False, 'message': results['message']}

	def updateDeviceInterfaceInfo(self, device_id = None, interface_name = None, params = None):
		'''
		Updates a device's interface.
		@param: a device's serial
		@param: interface_name - name of the interface
		@param: params - post body to be sent with the request
		@return: true on success; otherwise False
		'''
		if params is None or device_id is None or interface_name is None:
			return {'success': False, 'message': 'Missing parameters'}

		response = self.put(endpoint = '/devices/' + device_id + '/interfaces/' + interface_name + '/config', data = params)
		# response = self.get(endpoint = '/devices/' + device_id + '/interfaces/' + interface_name + '/config')
		status_code = response.status_code
		if status_code == 200:
			self.close_connection(response)
			return {'success': True, 'message': 'Updated device\'s interface successfully'}

		results = response
		self.close_connection(response)
		return {'success': False, 'message': results.json()}
