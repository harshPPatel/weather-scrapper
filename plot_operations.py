import matplotlib.pyplot as plot

class PlotOperations():
  def __init__(self, data):
    self.data = data
    
  def show_boxplot(self):
    labels = self.data.keys()
    data = self.data.values()
    # figure = plot.figure(1, figsize=(10,8))
    plot.boxplot(data)
    plot.xticks(range(1, len(labels) + 1), labels)
    # figure, ax = plot.subplots()
    # TODO: Make it dynamic
    plot.title('Monthly Temperature Distribution for: 2000 to 2020')
    plot.xlabel('Month')
    plot.ylabel('Temperature (Celsius)')
    # ax.set_title('Monthly Temperature Distribution for: 2000 to 2020')
    plot.show()
    

data =  {
  1: [1.1, 5.5, 6.2, 7.1],
  2: [8.1, 5.4, 9.6, 4.7],
  3: [1.1, 5.5, 6.2, 7.1],
  4: [8.1, 5.4, 9.6, 4.7],
  5: [1.1, 5.5, 6.2, 7.1],
  6: [8.1, 5.4, 9.6, 4.7],
  7: [1.1, 5.5, 6.2, 7.1],
  8: [8.1, 5.4, 9.6, 4.7],
  9: [1.1, 5.5, 6.2, 7.1],
  10: [8.1, 5.4, 9.6, 4.7],
  11: [1.1, 5.5, 6.2, 7.1],
  12: [8.1, 5.4, 9.6, 4.7]
}

plt = PlotOperations(data)
plt.show_boxplot()