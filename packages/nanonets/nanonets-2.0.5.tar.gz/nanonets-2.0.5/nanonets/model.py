import os
import json
import requests
from tqdm import tqdm

from nanonets.utils import *


class Model:

	def __init__(self, api_key, model_type):
		self.api_key = api_key
		self.model_type = model_type
		self.host = "https://app.nanonets.com/api/v2/"

	def _create_model(self, categories):
		"""
		function to create model given the categories and model type

		Parameters
		----------
		categories: List[str]
		    List of categories for our model

		Returns
		-------
		server response for the request to create model
		"""

		self.categories = categories
		url = self.host + self.model_type + '/Model/' 
		if not self.model_type == 'ImageCategorization':
			headers = {'Content-Type': "application/json"}
			payload = json.dumps({"categories": categories})
		else: 
			headers = {'Accept': "application/x-www-form-urlencoded"}
			payload = {"categories": categories}
		response =  requests.request("POST", url, 
					     headers=headers, 
					     data=payload,
					     auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		self.model_id = response.json()["model_id"]
		print("Your Model ID is: ", self.model_id)
		return response

	def _upload_image_file(self, img_path, annotation):
		"""
		function to upload a single file and it's labels for training to a model that 
		has been created

		Parameters
		----------
		img_path: str
		    path to the image we want to upload

		annotation: 
			List[str] of all labels associated with the image for MLC 
			or JSON file path for OD/OCR 

		Returns
		-------
		server response for the request for uploading image file
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/UploadFile/'
		img_name = img_path.split('/')[-1]
		params = {'file': open(image_path, 'rb'),
				  'modelId': ('', self.model_id),
				  'data' :('', annotation)}
		response = requests.post(url,
					files=params, 
					auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		return response

	def _train(self):
		"""
		function to start training of a model that has been created

		Parameters
		----------
		categories: List[str]
		    List of categories for our model

		Returns
		-------
		server response for the request to initialize training
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/Train/'
		params = {'modelId': self.model_id}
		response = requests.request("POST", url,
					    params=params,
					    auth=requests.auth.HTTPBasicAuth(self.api_key, ''))
		return response

	def _check_model_state(self):
		"""
		function to check model state given you have the model id as a class attribute

		Parameters
		----------
		None

		Returns
		-------
		None
		"""

		if self.model_type != 'ImageCategorization':
			annot_url = self.host + self.model_type + '/Model/' + self.model_id + '/Annotations'
			annot_response = requests.request("GET", annot_url,
						auth=requests.auth.HTTPBasicAuth(self.api_key,''))
			img_count = len(annot_response.json()["Data"])
			categories = annot_response.json()["Meta"]["categories"]
			state = annot_response.json()["Meta"]["state"]
			status = annot_response.json()["Meta"]["status"]
		else:
			annot_url = self.host + self.model_type + '/Model/'
			querystring = {'modelId': self.model_id}
			annot_response = requests.request('GET', annot_url, 
						auth=requests.auth.HTTPBasicAuth(self.api_key,''), 
						params=querystring)
			categories = annot_response.json()["categories"]
			img_count = sum([x['count'] for x in categories])
			state = annot_response.json()["state"]
			status = annot_response.json()["status"]

		if self.model_type != 'ImageCategorization':			
			assert img_count > 50, 'More images and annotations needed. Please upload atleast 50 images and their annotations' 
			for category in categories:
				assert category["count"] > 50, "Need at least 50 annotations for {} label, currently there are {} annotations".format(category["name"], category["count"])
		else:
			for category in categories:
				assert category["count"] > 25, "Need at least 25 annotations for {} label, currently there are {} annotations".format(category["name"], category["count"])

		if state != 5:
			print("The model isn't ready yet, it's status is:", status)
			print("We will send you an email when the model is ready.")
		else:
			print("Model is ready for predictions.")

		fin_dict = {"state": state,
					"status": status,
					"categories": categories}

		return fin_dict

	def _predict_urls(self, image_urls):
		"""
		function to get predictions for images using urls

		Parameters
		----------
		image_urls: List[str]
			urls of the images you want to get predictions for

		Returns
		-------
		JSON repsonse of the predictions 
		"""

		url = self.host + self.model_type + '/Model/' + self.model_id + '/LabelUrls/'
		params = {'modelId': self.model_id, 'urls': image_urls}
		response = requests.post(url,
					auth=requests.auth.HTTPBasicAuth(self.api_key, ''),
					data=params) 
		return response
