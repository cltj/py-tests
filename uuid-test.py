import uuid

# pip install uuid

# make a UUID based on the host ID and current time
a = uuid.uuid1()

# make a UUID using an MD5 hash of a namespace UUID and a name
b = uuid.uuid3(uuid.NAMESPACE_DNS, 'cloudlink.ai')

# make a random UUID
c = uuid.uuid4()

# make a UUID using a SHA-1 hash of a namespace UUID and a name
d = uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')

# make a UUID from a string of hex digits (braces and hyphens ignored)
e = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

# convert a UUID to a string of hex digits in standard form
str(e)

# get the raw 16 bytes of the UUID
e.bytes

# make a UUID from a 16-byte string
uuid.UUID(bytes=e.bytes)

print(a)
print(b)
print(c)
print(d)
print(e)
