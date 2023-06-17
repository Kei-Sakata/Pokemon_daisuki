import cv2

def main():
    # Open the first available camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Failed to open camera")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        if not ret:
            print("Failed to retrieve frame from camera")
            break

        # Check if the frame size is valid
        if frame.shape[0] > 0 and frame.shape[1] > 0:
            # Display the resulting frame
            cv2.imshow('Camera', frame)

        # Wait for the 'q' key to be pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

