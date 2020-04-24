from random import randint
import matplotlib.pyplot as plt


hyp_x = randint(0, 100)
hyp_y = randint(0, 100)
hyp_z = randint(0, 100)
rate = 0.01
lst = []


def f(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 + x


def df_x(x, y, z):
    return 2 * x + 1


def df_y(x, y, z):
    return 2 * y


def df_z(x, y, z):
    return 2 * z


def gd(n):
    global hyp_x, hyp_y, hyp_z, lst
    lst.append(f(hyp_x, hyp_y, hyp_z))
    for _ in range(n):
        aux_df_x = df_x(hyp_x, hyp_y, hyp_z)
        aux_df_y = df_y(hyp_x, hyp_y, hyp_z)
        aux_df_z = df_z(hyp_x, hyp_y, hyp_z)

        hyp_x = hyp_x - rate * aux_df_x
        hyp_y = hyp_y - rate * aux_df_y
        hyp_z = hyp_z - rate * aux_df_z
        lst.append(f(hyp_x, hyp_y, hyp_z))
        print(hyp_x, ' ', hyp_y, ' ', hyp_z)


print('initial ', hyp_x, ' ', hyp_y, ' ', hyp_z)
gd(500)
print('final ', hyp_x, ' ', hyp_y, ' ', hyp_z)

plt.plot(lst)
plt.show()
