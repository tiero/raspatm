import time
from PIL import Image
from io import BytesIO
import zbarlight
from picamera import PiCamera

def scan():

    with PiCamera() as camera:
        try:
            camera.start_preview()
            time.sleep(1)
            print("Start scanning for QR code")
        except:
            print("Picture couldn't be taken..")

        stream = BytesIO()
        qrcodes = None
        # Set timeout to 10 seconds
        timeout = time.time() + 10

        while qrcodes is None and (time.time() < timeout):
            stream.seek(0)
            ## Start camera stream 
            # (make sure RaspberryPi camera is focused correctly - manually adjust it, if not)
            camera.capture(stream, "jpeg")
            stream.seek(0)
            qrcodes = zbarlight.scan_codes("qrcode", Image.open(stream))
            time.sleep(0.05)
        camera.stop_preview()

        if qrcodes:
            invoice = qrcodes[0].decode().lower()

        if not (time.time() < timeout):
            print("No QR within 10 seconds detected")
            return False
        elif "ln" in invoice:
            return invoice
        else:
            print("This QR does not contain a Lightning invoice")
            return False

