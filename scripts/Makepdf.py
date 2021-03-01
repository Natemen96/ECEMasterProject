import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib
import os

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
# nathan_truth = [0,0,0,1,0,
#                 0,0,1,1,1,
#                 1,1,0,0,0,
#                 1,1,1,1,0,
#                 0,0,1,0,1]
os.remove("multipage_pdf.pdf")

with PdfPages('multipage_pdf.pdf') as pdf:

    fig = plt.figure(figsize=(8, 6))

    plt.subplot(311)
    
    plt.plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')
    plt.title('Page One')
    
    plt.subplot(312)
    plt.rc('text', usetex=False)

    x = np.arange(0, 5, 0.1)
    plt.plot(x, np.sin(x), 'b-')
    plt.title('Page Two')

    plt.subplot(313)
    plt.rc('text', usetex=False)

    plt.plot(x, x*x, 'ko')
    plt.title('Page Three')
    pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Multipage PDF Example'
    d['Author'] = u'Jouni K. Sepp\xe4nen'
    d['Subject'] = 'How to create a multipage pdf file and set its metadata'
    d['Keywords'] = 'PdfPages multipage keywords author title subject'
    d['CreationDate'] = datetime.datetime(2009,11,13)
    d['ModDate'] = datetime.datetime.today()

    # Remember to close the object - otherwise the file will not be usable