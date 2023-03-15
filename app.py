import requests, time, cv2
from fastapi import FastAPI

app = FastAPI()

regions = ['mx', 'us-ca']

@app.get("/{key}")
async def get_key(key: str):
    return principal(key)

def principal(key):
    if len(key) == 4 or key is None:
        return {"Error":"No key provided"}
    else:
        take_image()
        response = apiPlatesResponse()
        status = apiWebResponse(key, response['results'][0]['plate'])
        return {'plate':response['results'][0]['plate'],'key':key[4:],'status':status['msg']}

def take_image():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Photo")
    while True:
        ret, frame = cam.read()
        time.sleep(1)
        if not ret:
            return {"Error":"Failed to capture image"}
        cv2.imshow("Test", frame)
        img_name = "picture.png".format(0)
        cv2.imwrite(img_name, frame)
        break
    cam.release()
    cv2.destroyAllWindows()

def apiPlatesResponse():
    with open('./picture.png', 'rb') as fp:
        response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions), 
            files=dict(upload=fp),
            headers={'Authorization': 'Token 080c4b462d1ff7a3cd1c8775412f606d89c2687d'})
    return response.json()

def apiWebResponse(key, plate):
    response = requests.get(f'https://truck-manage-production.up.railway.app/api/verify-plate/{key[4:]}/{plate}')
    return response.json()