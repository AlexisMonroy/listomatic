import base64

data = "data_to_be_encoded"
encoded_data = base64.b64encode(data.encode("utf-8"))
print(encoded_data.decode("utf-8"))