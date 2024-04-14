import reportlab
from reportlab.pdfgen import canvas 
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import subprocess
import sys
import requests

def function(id_rapport):
	rapport_query = requests.get(f'http://')