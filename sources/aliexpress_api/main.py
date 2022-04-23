import requests
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


REMOTE_FEED_URL = 'https://stripmag.ru/datafeed/p5s_full_stock.xml'
OUR_FEED_URL = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
SAVING_PATH = ''


def get_filename_from_url(url: str) -> str:
    """Get file name from url format.

    Arguments:
    • url — must be str, else raise TypeError

    Usage:
    >>> fname = get_filename_from_url('https://domain.com/file.xml')
    >>> print(fname)  # file.xml
    """
    if not isinstance(url, str):
        raise TypeError(f'Argument <url> must be str, not {type(url)}')
    return url[url.rfind('/') + 1:]


def download_file_from_url(url: str, file: str) -> None:
    """Download file from url.

    Arguments:
    • url — link to file that we need to download.
    • file — path where to save downloaded file.
    """
    if not isinstance(url, str):
        raise TypeError(f'Argument <url> must be str, not {type(url)}')

    if not isinstance(file, str):
        raise TypeError(f'Argument <file> must be str, not {type(file)}')

    response = requests.get(url)
    with open(file, 'wb') as f_out:
        f_out.write(response.content)


def update_feed(source: str, destination: str) -> None:
    """Upadate all data in destination file from source.

    Arguments:
    • source — path to source XML file from which we will get data.
    • destination — path to file that we need to update.
    """

    # Get Tree of source file
    s_tree = ET.parse(source)
    s_root = s_tree.getroot()
    s_products = s_root.findall('product')
    send_logs('Got data from source file')

    # Get tree of destination file
    d_tree = ET.parse(destination)
    d_root = d_tree.getroot()
    d_offers = d_root.find('shop').find('offers')
    send_logs('Got data from destination file')

    counter = 0
    for item in s_products:
        counter += 1
        if counter % 100 == 0:
            send_logs(f'Processed {counter} items', flush=True)

        id = item.get('prodID')
        offer = d_offers.find(f'offer[@id="{id}"]')
        if offer is None:
            continue

        s_price = item.find('price')
        s_count = item.find('assortiment').find('assort')

        d_price = offer.find('price')
        d_count = offer.find('quantity')

        # Change quantity
        d_count.text = s_count.get('sklad')

        # Change prices
        d_price.set('BaseRetailPrice', s_price.get('BaseRetailPrice'))
        d_price.set('BaseWholePrice', s_price.get('BaseWholePrice'))
        d_price.set('RetailPrice', s_price.get('RetailPrice'))
        d_price.set('WholePrice', s_price.get('WholePrice'))

    send_logs('All tree processed successfuly')
    d_tree.write(destination)
    send_logs(f'File saved: {destination}')


def send_logs(message: str, flush: bool = False) -> None:
    """Send logs to stdout with variabe flush.

    Arguments:
    • message — str that needed to be printed.
    • flush — True if we need to rewrite last line or False if we don't.
    """
    if not isinstance(message, str):
        raise TypeError(f'Argument <message> must be str, not {type(message)}')
    if not isinstance(flush, bool):
        raise TypeError(f'Argument <flush> must be bool, not {type(flush)}')

    # Get time now for logs
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    if flush:
        sys.stdout.write(f'\r[{now}]: {message}')
        sys.stdout.flush()
        send_logs.flush_before = True
    else:
        if send_logs.flush_before:
            sys.stdout.write('\n')
            send_logs.flush_before = False
        print(f'[{now}]: {message}')


if __name__ == '__main__':
    send_logs.flush_before = False

    # Get file names from url
    remote_file = f'{SAVING_PATH}{get_filename_from_url(REMOTE_FEED_URL)}'
    our_file = f'{SAVING_PATH}{get_filename_from_url(OUR_FEED_URL)}'

    # Download files
    download_file_from_url(REMOTE_FEED_URL, remote_file)
    download_file_from_url(OUR_FEED_URL, our_file)

    # Update and save files
    update_feed(remote_file, our_file)
