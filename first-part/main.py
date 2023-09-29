import carla
import cv2
import numpy as np

# Initialize Carla simulation environment
def initialize_carla():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    return world

# Function to process camera data (assuming you have a camera sensor in your simulation)
def process_camera_data(image):
    # Convert Carla image to a format usable by OpenCV
    img = np.array(image.raw_data)
    img = img.reshape((image.height, image.width, 4))
    img = img[:, :, :3]  # Remove alpha channel
    return img

# Filter objects based on color (you can use more advanced techniques)
def filter_objects(image):
    # Convert the image to grayscale for simple filtering
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a color threshold to isolate relevant objects (you can fine-tune the values)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Find contours of objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter objects based on size, shape, or other criteria as needed
    relevant_objects = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Adjust the threshold as needed
            relevant_objects.append(contour)

    return relevant_objects

# Measure distances and speed of relevant objects
def measure_distances_and_speed(relevant_objects, vehicle_x, vehicle_y):
    # Calculate longitudinal and lateral distances and speed for each object
    distances = []
    speeds = []

    for obj in relevant_objects:
        # Get the bounding box coordinates (x, y, width, height)
        x, y, w, h = cv2.boundingRect(obj)

        # Calculate the centroid of the object
        object_centroid_x = x + w / 2
        object_centroid_y = y + h / 2

        # Calculate longitudinal and lateral distances
        longitudinal_distance = object_centroid_x - vehicle_x
        lateral_distance = object_centroid_y - vehicle_y

        # Calculate speed (for a basic estimation)
        if 'prev_x' in obj:
            delta_x = object_centroid_x - obj['prev_x']
            delta_y = object_centroid_y - obj['prev_y']
            time_interval = 1.0  # Assuming a constant time interval between frames (adjust as needed)
            speed = np.sqrt((delta_x / time_interval) ** 2 + (delta_y / time_interval) ** 2)
        else:
            speed = 0.0  # Initial frame, no speed estimation

        # Store the current object's position for the next frame
        obj['prev_x'] = object_centroid_x
        obj['prev_y'] = object_centroid_y

        distances.append((longitudinal_distance, lateral_distance))
        speeds.append(speed)

    return distances, speeds

# Main loop
def main():
    world = initialize_carla()

    # Assuming you have a camera sensor in your Carla setup
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

            # Process camera data
            image = process_camera_data(world_snapshot.find(camera))

            # Apply image processing to filter out objects
            relevant_objects = filter_objects(image)

            # Measure distances and speed of relevant objects
            distances, speeds = measure_distances_and_speed(relevant_objects, vehicle_x, vehicle_y)

            # Create visualization with distances and speeds (you can customize this part)
            for i, (longitudinal_distance, lateral_distance) in enumerate(distances):
                # Add distance and speed information to the visualization
                cv2.putText(image, f"Long. Dist.: {longitudinal_distance}", (10, 30 * i + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f"Lat. Dist.: {lateral_distance}", (10, 30 * i + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f"Speed: {speeds[i]}", (10, 30 * i + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            cv2.imshow("Camera View", image)
            cv2.waitKey(1)
            vehicle_x =  11
            vehicle_y =  11


    finally:
        camera.destroy()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
