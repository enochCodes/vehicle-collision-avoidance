import carla
import cv2
import numpy as np

def initialize_carla():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    return world

def create_vehicle(world):
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle.*')[0]
    spawn_point = carla.Transform(carla.Location(x=0, y=0, z=2))
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    return vehicle

def process_camera_data(image):
    img = np.array(image.raw_data)
    img = img.reshape((image.height, image.width, 4))
    img = img[:, :, :3]
    return img

def filter_objects(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    relevant_objects = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            relevant_objects.append(contour)

    return relevant_objects

def measure_distances_and_speed(relevant_objects, vehicle_x, vehicle_y):
    distances = []
    speeds = []

    for obj in relevant_objects:
        x, y, w, h = cv2.boundingRect(obj)

        object_centroid_x = x + w / 2
        object_centroid_y = y + h / 2

        longitudinal_distance = object_centroid_x - vehicle_x
        lateral_distance = object_centroid_y - vehicle_y

        if 'prev_x' in obj:
            delta_x = object_centroid_x - obj['prev_x']
            delta_y = object_centroid_y - obj['prev_y']
            time_interval = 1.0
            speed = np.sqrt((delta_x / time_interval) ** 2 + (delta_y / time_interval) ** 2)
        else:
            speed = 0.0

        obj['prev_x'] = object_centroid_x
        obj['prev_y'] = object_centroid_y

        distances.append((longitudinal_distance, lateral_distance))
        speeds.append(speed)

    return distances, speeds

# Main loop
def main():
    world = initialize_carla()
    vehicle = create_vehicle(world)

    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')

    camera_location = carla.Transform(carla.Location(x=1.5, y=0.0, z=2.4))

    camera = world.spawn_actor(camera_bp, camera_location)

    vehicle_x = 0.0
    vehicle_y = 0.0

    try:
        while True:
            world_snapshot = world.get_snapshot()

            image = process_camera_data(world_snapshot.find(camera))

            relevant_objects = filter_objects(image)

            distances, speeds = measure_distances_and_speed(relevant_objects, vehicle_x, vehicle_y)

            for i, (longitudinal_distance, lateral_distance) in enumerate(distances):
                cv2.putText(image, f"Long. Dist.: {longitudinal_distance}", (10, 30 * i + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f"Lat. Dist.: {lateral_distance}", (10, 30 * i + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f"Speed: {speeds[i]}", (10, 30 * i + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            cv2.imshow("Camera View", image)
            cv2.waitKey(1)

            vehicle_x = vehicle.get_location().x
            vehicle_y = vehicle.get_location().y

    finally:
        vehicle.destroy()
        camera.destroy()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
