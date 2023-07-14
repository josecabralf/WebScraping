ar = open('casas.txt', 'r')
links = []

for line in ar.readlines():
    links.append(line.replace('\n', ''))

print(len(links))
