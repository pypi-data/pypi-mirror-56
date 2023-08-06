import time
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
# set matplot theme
mpl.style.use('fivethirtyeight')

# remove logging.csv
if 'logging.csv' in os.listdir():
    print('Removing old logging file...')
    os.remove('logging.csv')


class Timer:
    def __init__(self, name='Process', verbose=True, logging=True):
        self.start = None
        self.end = None
        self.name = name
        self.verbose = verbose
        self.logging = logging

    def __enter__(self):
        self.start = time.time()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        self.total = round(self.end - self.start, 3)
        if self.verbose:
            print('{} Spends {} s'.format(self.name, self.total))
        if self.logging:
            with open('logging.csv', 'a+') as f:
                f.write('{}, {}\n'.format(self.name, self.total))


class TimerPloter:
    def __init__(self, col1='Algorithm', col2='Stage', col3='Time'):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.data = self._get_data()

    def _get_data(self):
        df = pd.read_csv('logging.csv', header=None,
                         names=[self.col1, self.col2, self.col3])
        return df

    def plot(self):
        sns.barplot(x=self.col1, y=self.col3, hue=self.col2, data=self.data)
        plt.title('Time usage of different algorithms')
        plt.ylabel('Time(seconds)')
        plt.savefig('Timer.png', bbox_inches='tight', dpi=300)
        plt.show()


if __name__ == '__main__':
    # dummy testing
    with Timer('NaiveBayes, Train') as t:
        print('training model...')
        time.sleep(2)
