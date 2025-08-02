from escpos.printer import Usb
from escpos.image import EscposImage

p = Usb(0x154F, 0x154F, interface=1)

# Load and print logo
logo = "Resources/icofi.ico"  # path to your image
p.set(align='center')
p.image(logo)
p.text("Fashion Paradise\n")
p.cut()