from matplotlib import pyplot as plt
# make a square figure and axes
plt.figure(figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
fracs = [15,30,45, 10]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

explode=(0, 0.05, 0, 0)
p = plt.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
plt.title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})

w = p[0][0]
plt.show()