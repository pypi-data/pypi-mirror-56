import DracoPy

a = DracoPy.encode_pointcloud_to_buffer([1.2,3.2,4.2])

b = DracoPy.decode_buffer_to_point_cloud(a)
print([1.2,3.2,4.2])
print (b.points)