"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt

n_groups = 12

means_men = (20, 35, 30, 35, 27, 0, 0, 0, 0, 0, 0, 0)


means_women = (25, 32, 34, 20, 25, 0, 0, 0, 0, 0, 0, 0)


#fig, ax = plt.subplots()


index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, means_men, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='Einnahmen')

rects2 = plt.bar(index + bar_width, means_women, bar_width,
                 alpha=opacity,
                 color='r',
                 error_kw=error_config,
                 label='Ausgaben')

plt.xlabel('Monate')
plt.ylabel('Euro')
plt.title('Einnahmen u. Ausgaben per Monat')
plt.xticks(index + bar_width, ('Januar', 'Februar', 'Maerz', 'April', 'May', 'Juni', 'July', 'August', 'September', 'Oktober', 'November', 'Dezember'))
plt.legend()

#plt.tight_layout()
plt.show()

