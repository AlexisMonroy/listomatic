info = {
    'accesscode':'12345'
}

if info.get("accesscode"):
    print(info["accesscode"])

if not info.get("otherkey"):
    print("Key Does Not Exist")
else:
    print(info["otherkey"])
