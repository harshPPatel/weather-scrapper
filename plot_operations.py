import matplotlib.pyplot as plot
#data will be formatted
# Plot will show the average for all januaries across all years

class PlotOperations():
  def __init__(self, data):
    self.data = data

  def show_lineplot(self, month_to_plot):
    plot.plot(month_to_plot)
    plot.xticks(range(min(1), max(len(month_to_plot))+1)) # This should show the x label as each days
    plot.show()

  def show_boxplot(self):
    labels = self.data.keys()
    data = self.data.values()
    # Method 1
    # TODO: Format data
    # TODO: Make it dynamic
    plot.title('Monthly Temperature Distribution for: 2000 to 2020')
    plot.xlabel('Month')
    plot.ylabel('Temperature (Celsius)')
    plot.xticks(range(1, len(labels) + 1), labels)
    plot.boxplot(data)

    # Method 2
    # subplots = plot.subplots()
    # ax = subplots[1]
    # # TODO: Make it dynamic
    # ax.set_title('Monthly Temperature Distribution for: 2000 to 2020')
    # ax.boxplot(data)
    plot.show()

#Dictionary fo dictionaries
# Find out how to map this data, in the format
# data wil be the year, the key is the month, and each
# entry is a mean value for a particular day

data =  {
  1: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
  2: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
  3: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
  4: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
  5: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
  6: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
  7: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
  8: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
  9: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 100],
  10: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
  11: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
  12: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40]
}

#mockup of a month for testing
month_to_plot = [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6]


plt = PlotOperations(data)
plt.show_boxplot()