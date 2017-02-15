from django.test import Client
c = Client()

response = c.get('/lecturer/')
print(response.status_code)
