import base64

data = "AlexisGo-pricepre-PRD-3ca7161d2-d3ef5057:PRD-ca7161d2a58b-663b-4c87-9cec-8cbd"
encoded_data = base64.b64encode(data.encode("utf-8"))
print(encoded_data.decode("utf-8"))