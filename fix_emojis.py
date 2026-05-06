with open('kings-and-pigs-main/map.html', 'rb') as f:
    content = f.read()

# Fix garbled 🏠 home emoji: \xc3\xb0\xc5\xb8\xc2\x8f\xc2\xa0 -> \xf0\x9f\x8f\xa0
content = content.replace(b'\xc3\xb0\xc5\xb8\xc2\x8f\xc2\xa0', '🏠'.encode('utf-8'))

# Fix garbled × symbol in comment: \xc3\x83\xe2\x80\x94 -> \xc3\x97
content = content.replace(b'\xc3\x83\xe2\x80\x94', '×'.encode('utf-8'))

with open('kings-and-pigs-main/map.html', 'wb') as f:
    f.write(content)

print("Done")
