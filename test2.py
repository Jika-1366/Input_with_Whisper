import requests

url = 'https://cool-hiji-1700.schoolbus.jp/programs/test_addition.php'
data = {'num1': 900, 'num2': 9}

response = requests.post(url, data=data)

if response.status_code == 200:
    result = response.json().get('result')
    if result is not None:
        print('Result:', result)
    else:
        print('Error:', response.json().get('error'))
else:
    print('Failed to get response:', response.status_code)
