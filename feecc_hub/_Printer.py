import logging
import typing as tp

from PIL import Image
from brother_ql import BrotherQLRaster, conversion
from brother_ql.backends.helpers import send


class Task:

    def __init__(self, picname: str, config: tp.Dict[str, tp.Dict[str, tp.Any]]) -> None:
        """
        :param picname: path to a picture to be printed
        :type picname: str

        When creating an instance of the class, it creates a task for a brother QL-800 printer to print a label with a
        qr-code passed as an argument. picname != qrpic, it contains side fields and logos (optionally)
        """
        logging.info("Initializing printer")
        logging.debug(f"picname: {picname},\nconfig for printer: {config['printer']}")

        basewidth = 554

        qr = Image.open(picname)

        wpercent = basewidth / float(qr.size[0])
        hsize = int((float(qr.size[1]) * float(wpercent)))
        qr = qr.resize((basewidth, hsize), Image.ANTIALIAS)

        printer_config: tp.Dict[str, tp.Any] = config["printer"]
        printer: str = printer_config["address"]  # link to device
        label_name = str(printer_config["paper_width"])  # that depends on paper used for printing

        logging.info("Printing...")

        qlr = BrotherQLRaster(printer_config["printer_model"])
        red: bool = label_name == 62
        conversion.convert(qlr, [qr], label_name, red=red)

        logging.debug(f"Sending task to printer")
        send(
            qlr.data, printer
        )  # this is some standard code for printing with brother label printer with python,
        # red = True means that black and red printing will be done. Only for 62 label paper
        logging.info("Printed!")
