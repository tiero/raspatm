import RPi.GPIO as GPIO
import sys
import time
import requests

import camera 

PULSES = 0
LASTIMPULSE = 0
FIAT = 0
SATS = 0
INVOICE = ''
# Set btc and sat price
BTCPRICE = 6000 
SATPRICE = round((1 / (BTCPRICE * 100)) * 100000000, 2)


def setup_coin_acceptor(gpio_coin_acceptor):
    """Initialises the coin acceptor parameters
    """
    # Defining GPIO BCM Mode
    GPIO.setmode(GPIO.BOARD)
    # Setup GPIO Pins for coin acceptor and button
    # GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(5, GPIO.RISING, callback=button_event, bouncetime=200)

    # Setup coin interrupt channel (bouncetime for switch bounce)
    GPIO.setup(gpio_coin_acceptor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(gpio_coin_acceptor, GPIO.FALLING, callback=coin_event)


def coin_event(channel):
    """Registers a coin insertion event
    """
    global PULSES
    global LASTIMPULSE
   
   
    LASTIMPULSE = time.time()
    PULSES = PULSES + 1
    print(PULSES)


def coins_inserted():
    global PULSES
    global LASTIMPULSE
    global SATS
    global FIAT
    global SATPRICE
    
    """Actions coins inserted
    """
    if PULSES == 1:
        print("2 euro added")
        process_coin(2)
    if PULSES == 2:
        print("1 euro added")
        process_coin(1)
    if PULSES == 3:
        print("50 cents added")
        process_coin(0.5)
    if PULSES == 4:
        print("20 cents added")
        process_coin(0.2)
    if PULSES == 5:
        print("10 cents added")
        process_coin(0.1)
    # Clean up
    PULSES = 0 


def sats_to_pay(fiat_inserted, btc_price):
    sats = ((fiat_inserted * 100) * (100000000)) / int(round(btc_price * 100)) 
    return sats

def process_coin(fiat_inserted):
    response = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR").json()
    
    sats = sats_to_pay(
        fiat_inserted, 
        response.get('price_eur')
        )
    
    invoice = scan()

    if invoice is not False:
        if payout(invoice) is not False
            return True


def payout(invoice):
    data = {
        "invoice": invoice,
    }
    response = requests.post(
        str(os.environ['VAULT_API']) + "/payout",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )
    res_json = response.json()

    if res_json.get("payment_error"):
        errormessage = res_json.get("payment_error")
        print("Payment failed (%s)" % errormessage)
        print("Error: " + res_json.get("payment_error"))
        return False

    return True


def scan():
    # Hey, we have a timeout of 10 seconds
    invoice = camera.scan()
    while invoice is False:
        #display.update_qr_failed()
        print('Invoice is not valid')
        return False

    return invoice 

def main():

    print("Application started")
    # Display startup startup_screen
    # do stuff with monitor
    setup_coin_acceptor(40)

    while True:
        time.sleep(0.2)
        # Detect when coins are being inserted
        if (time.time() - LASTIMPULSE > 0.5) and (PULSES > 0):
            coins_inserted()


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            # Display: shitdown screen
            GPIO.cleanup()
            print("Application finished (Keyboard Interrupt)")
            sys.exit("Manually Interrupted")
        except Exception:
            print("Oh no, something bad happened! Restarting...")
            GPIO.cleanup()
            # anything else needs to happen for a clean restart?
