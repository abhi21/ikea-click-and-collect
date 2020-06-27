import time
import requests
import argparse
import os

IKEA_STORES_URL = ' https://api.ikea-status.dong.st/prod/locations'


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def poll_availability(store_country, store_state, store_name, timeout):
    start = time.time()
    counter = 0
    notify('Test Ikea Stores status', 'Test notification for Ikea Store {} status check.'.format(store_name))

    while True:
        counter += 1
        try:
            stores_data = requests.get(IKEA_STORES_URL)
            for store in stores_data.json()['locations']:
                if store['countryCode'] == store_country and store['subdivisionCode'] == store_state \
                        and store['locationName'] == store_name \
                        and store['status'] == 'open' \
                        and store['changes'][-1]['newStatus'] == 'open':
                    print("Store Open!!! ")
                    notify('Hurry! Ikea Store {} is Open!!'.format(store), 'Online Click & Collect')

        except Exception as e:
            print("Exception:", e)
            pass

        if time.time() - start > timeout * 60 * 60:
            break
        print('Iteration: {}'.format(counter))
        time.sleep(45)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check status for IKEA store')
    parser.add_argument('-c', '--country', help='Country', required=True)
    parser.add_argument('-s', '--state', help='State', required=True)
    parser.add_argument('-n', '--name', help='Name/ City of your Ikea Store. Ex: Portland', required=True)
    parser.add_argument('-t', '--timeout', help='Time out in hours', required=False)

    args = parser.parse_args()

    r = requests.get(IKEA_STORES_URL)
    stores = []
    for store in r.json()['locations']:
        stores.append(store['locationName'])
    name = args.name
    if name not in stores:
        notify("Ikea Store {} not found. Please a enter a valid name/ city of your Ikea store!".format(name))
    else:
        poll_availability(args.country, args.state, args.name, int(args.timeout) if args.timeout else 42)
