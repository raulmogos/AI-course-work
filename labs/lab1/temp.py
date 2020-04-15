import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


config = {
    'normal': {
        'mean': 5.0, # mean (“centre”) of the distribution
        'std': 0.3 # Standard deviation (spread or “width”) of the distribution
    },
    'exponential': {
        'loc': 0,
        'scale': 0.4
    }
}
SIZE = int(input('no of numbers:'))

my_random_normal = lambda : np.random.normal(
    config['normal']['mean'],
    config['normal']['std']
)
my_random_exponential = lambda : np.random.exponential(
    config['exponential']['scale']
)

current_fucntion = None

print('choose:')
print('1 - normal')
print('2 - exponential')
choice = int(input())
if choice == 1:
    current_fucntion = my_random_normal
    # x axis size
    x_max = config['normal']['mean'] + 5 * config['normal']['std']
    x_min = config['normal']['mean'] - 5 * config['normal']['std']
    # plot the mean and mean + - std
    plt.plot(config['normal']['mean'], 0, 'bo')
    plt.plot(config['normal']['mean'] + config['normal']['std'], 0, 'bo')
    plt.plot(config['normal']['mean'] - config['normal']['std'], 0, 'bo')
    # genereate the numbers
    arr = [current_fucntion() for _ in range(SIZE)]
    # plot the numbers
    for i in range(len(arr)):
        plt.plot(arr[i], (i + 1) * 0.1, 'ro')
    # plot the normal distribution
    x = np.linspace(x_min, x_max)
    y = scipy.stats.norm.pdf(x,config['normal']['mean'], config['normal']['std'])
    plt.plot(x,y, color='black')
    # height of the fcuntion (aprox)
    heigth = 0.4 / config['normal']['std']
    # we scale such that we have a nice plot
    y_max = max(SIZE * 0.11, heigth * 1.1)
    plt.axis([x_min, x_max, 0, y_max ])
elif choice == 2:
    current_fucntion = my_random_exponential
    plt.plot(config['exponential']['scale'], 0, 'bo')
    arr = [current_fucntion() for _ in range(SIZE)]
    max_rand = 0
    for i in range(len(arr)):
        plt.plot(arr[i], (i + 1) * 0.1, 'ro')
        max_rand = max(max_rand, arr[i])
    # plot the normal distribution
    x_min, x_max = 0, max_rand + 1
    y_min, y_max = 0, SIZE * 0.11
    x = np.linspace(x_min, x_max)
    y = scipy.stats.expon.pdf(x, config['exponential']['loc'], config['exponential']['scale'])
    plt.plot(x,y, color='black')
    plt.axis([x_min, x_max, y_min, y_max])
else:
    print('no good input')

print(arr)
plt.show()

# citire, random, verificat
