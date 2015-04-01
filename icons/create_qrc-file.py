import os

liste = os.listdir(".")
text = '''<!DOCTYPE RCC><RCC version="1.0">\n<qresource>\n'''
for name in liste:
    if name.endswith(".png"):
        text = text + "    <file>icons/"+name+"</file>\n"
text = text + "</qresource>\n</RCC>"
print(text)

file = open("icons.qrc", "w")
file.write(text)
file.close()
