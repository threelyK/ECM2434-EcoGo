from django.test import TestCase
from apps.qrgenerator.models import Website
import os
from django.core.files.storage import default_storage
# Create your tests here.

class QRCodeTesting(TestCase):
    
    def setUp(self):
        self.website = Website.objects.create(
            name="Testing",
            url="http://127.0.0.1:8000/Testing"
        )

    def testingQRCodes(self):
        """
        Tests that the qrcode attribute of the website is updated.
        """
        self.website.save()
        self.assertIsNotNone(self.website.qr_code, "QRCode should not be empty")

        qr_code_path = self.website.qr_code.path
        self.assertTrue(os.path.exists(qr_code_path), f"no qrcode at path at {qr_code_path}")



    def DelTestQRCode(self):
        """
        Tests that qr code images are being deleted correctly.
        """
        qr_code_path = self.website.qr_code.path
        
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)  # Delete the file
            self.assertFalse(os.path.exists(qr_code_path))

    #old version of tests
    #Manually tested each QRCode generated myself to see if it leads to the right link
        