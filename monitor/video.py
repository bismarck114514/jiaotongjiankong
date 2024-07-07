import cv2 as cv
import base64
import requests

ACCESS_TOKEN = '24.5815d1e3cd770f6c72bad588eebad458.2592000.1722736808.282335-90892277'

def vehicle_detect(img):
    try:
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
        _, encoded_image = cv.imencode('.jpg', img)
        base64_image = base64.b64encode(encoded_image).decode()
        params = {"image": base64_image}
        request_url = request_url + "?access_token=" + ACCESS_TOKEN
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        vehicles = []
        if response:
            data = response.json()
            for item in data.get('vehicle_info', []):
                vehicles.append({
                    'type': item['type'],
                    'score': item.get('score', 0),
                })
        return vehicles
    except Exception as e:
        print(f"Error in vehicle_detect: {e}")
        return []

def car_type_detect(img):
    try:
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"
        _, encoded_image = cv.imencode('.jpg', img)
        base64_image = base64.b64encode(encoded_image).decode()
        params = {"image": base64_image}
        request_url = request_url + "?access_token=" + ACCESS_TOKEN
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        car_types = []
        if response:
            data = response.json()
            car_types = data.get('result', [])
        return car_types
    except Exception as e:
        print(f"Error in car_type_detect: {e}")
        return []

def person_detect(img):
    try:
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num"
        _, encoded_image = cv.imencode('.jpg', img)
        base64_image = base64.b64encode(encoded_image).decode()
        params = {"image": base64_image}
        request_url = request_url + "?access_token=" + ACCESS_TOKEN
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            person_num = data.get('person_num', 0)
            return person_num
        return 0
    except Exception as e:
        print(f"Error in person_detect: {e}")
        return 0
