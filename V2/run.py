import os
import logging
import datetime

from V2.src.gui import AuDGUI

# Configure Log
logging.basicConfig(
    level=logging.DEBUG,
    filename=f"log/{str(datetime.date.today())}_AuDGUI.log",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)

if __name__ == '__main__':
    start_path = os.path.dirname(__file__)
    a = AuDGUI(start_path=start_path)
    try:
        a.mainloop()
    except KeyboardInterrupt:
        a.save()
