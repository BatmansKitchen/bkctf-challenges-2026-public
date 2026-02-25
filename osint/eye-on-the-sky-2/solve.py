import numpy

FOCAL = 85e-3

X_RES_PX = 4000
Y_RES_PX = 6000


print('using the distance from Rainier and Little Tahoma')
DIAG_PX_LEN = 7212

fov = numpy.deg2rad(15.5)
px_size = fov/DIAG_PX_LEN

SIZE_Y_PX = abs(4671 - 5022)
SIZE_Y_M = 4392.168 - 3395
SIZE_X_PX = 1896 - 643
SIZE_X_M = 3687.0 # using online distance calc


aov_y = SIZE_Y_PX * px_size
distance_y = SIZE_Y_M / numpy.tan(aov_y)
print (f"distance w y: {distance_y}")

aov_x = SIZE_X_PX * px_size
distance_x = SIZE_X_M / numpy.tan(aov_x)
print (f"distance w x: {distance_x}")


print (f"Avg Distnace from Rainier {numpy.mean([distance_x, distance_y])}")

print ('using distnace from the plane')

SIZE_Y_PX = abs(1182 - 1200)
SIZE_Y_M = 41.76
SIZE_X_PX = abs(1879 - 1931)
SIZE_X_M = 12.30 # using online distance calc

aov_y = SIZE_Y_PX * px_size
distance_y = SIZE_Y_M / numpy.tan(aov_y)
print (f"distance w y: {distance_y}")

aov_x = SIZE_X_PX * px_size
distance_x = SIZE_X_M / numpy.tan(aov_x)
print (f"distance w x: {distance_x}")


print (f"Avg Distnace from Plane {numpy.mean([distance_x, distance_y])}")
