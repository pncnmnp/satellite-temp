file = open('Maps\main3.js','r')

s= file.read()
l1 = s.split(';')
l1[1] ='\n\nvar addressPoints ='+ open('lists/list1.txt').read() + ';\n\n'
file.close()

with open('Maps\main2.js','w') as file2:
    file2.write(';'.join(l1))
