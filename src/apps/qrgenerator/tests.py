from django.test import TestCase
from .models import Website
import os

# Create your tests here.

class QRCodeTesting(TestCase):
    
    def setUp(self):
        self.website = Website.objects.create(
            name="Testing",
            url="http://127.0.0.1:8000/Testing"
        )

    def testingQRCodes(self):
        self.website.save()
        self.assertIsNotNone(self.website.qr_code, "QRCode should not be empty")

        qr_code_path = self.website.qr_code.path
        self.assertTrue(os.path.exists(qr_code_path), f"no qrcode at path at {qr_code_path}")

    def RemoveQR(self):
        if self.website.qr_code:
            os.remove(self.website.qr_code.path)
    
        