import carla
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model


client = carla.Client('localhost', 2000)
client.set_timeout(10.0)


world = client.load_world('Town1')


camera_data = []


def preprocess_image(image):
    
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    return image


lidar_data = []


def lidar_callback(data):
    lidar_data.append(data)


def detect_objects(lidar_data):
    from sklearn.cluster import DBSCAN
import numpy as np


def detect_objects(lidar_data):
    detected_objects = []

    
    for frame in lidar_data:
        
        points = np.frombuffer(frame.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (frame.height, frame.width, 4))

        
        lidar_xy = points[:, :, :2]

        
        lidar_points = lidar_xy.reshape(-1, 2)

        
        dbscan = DBSCAN(eps=0.2, min_samples=5)
        dbscan.fit(lidar_points)

        
        labels = dbscan.labels_

        
        unique_labels = np.unique(labels[labels != -1])

        
        for label in unique_labels:
            object_points = lidar_points[labels == label]
            object_center = np.mean(object_points, axis=0)
            detected_objects.append({
                'label': label,
                'center': object_center,
                'points': object_points
            })
    
    
    
    
    
    return detected_objects


def control_logic(detected_objects, vehicle_speed):
    
    
    
    
    return throttle, steering, brake


spawn_point = carla.Transform(carla.Location(x=100, y=200, z=0), carla.Rotation(yaw=0))
vehicle_bp = world.get_blueprint_library().find('your_vehicle_blueprint')
vehicle = world.spawn_actor(vehicle_bp, spawn_point)


model = load_model('your_advanced_model.h5')

try:
    
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '224')
    camera_bp.set_attribute('image_size_y', '224')
    camera_bp.set_attribute('fov', '90')
    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)))

    
    camera.attach_to(vehicle)
    camera.listen(camera_callback)

    
    lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
    lidar_bp.set_attribute('channels', '32')
    lidar_bp.set_attribute('points_per_second', '100000')
    lidar_bp.set_attribute('rotation_frequency', '10')
    lidar = world.spawn_actor(lidar_bp, carla.Transform(carla.Location(x=0, z=2.8), carla.Rotation(pitch=0)))

    
    lidar.attach_to(vehicle)
    lidar.listen(lidar_callback)

    while True:
        
        if len(camera_data) > 0:
            input_image = np.expand_dims(preprocess_image(camera_data[-1]), axis=0)  
            
            
            predicted_control = model.predict(input_image)
            
            
            if len(lidar_data) > 0:
                detected_objects = detect_objects(lidar_data[-1])
                
                
                throttle, steering, brake = control_logic(detected_objects, vehicle.get_velocity())
                
                
                control = carla.VehicleControl()
                control.throttle = throttle
                control.steering = steering
                control.brake = brake
                vehicle.apply_control(control)
            
except KeyboardInterrupt:
    pass
finally:
    
    camera.stop()
    camera.destroy()
    lidar.stop()
    lidar.destroy()
    vehicle.destroy()
