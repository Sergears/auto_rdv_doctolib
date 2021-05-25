# auto_rdv_doctolib
This Python code automates booking a vaccination appointment on Doctolib.fr.

Function find_rdv automatically clicks on a vaccination appointment as soon as it becomes available.
The program will select the first appointment that appears in the displayed time frame (3 days with the default window size).
Alarm sound will be played if successful.
Verify that the date of the appointment suits you, and proceed manually with the following steps (faster if already logged in automatically).

Setup:
1) add selenium package to your python environment
2) Chrome browser is assumed be installed
3) download chromedriver.exe (browser driver for selenium) from https://sites.google.com/a/chromium.org/chromedriver/downloads
4) if not using Windos OS, modify the auto_rdv_doctolib.play_success_sound()

How to use the code:
1) specify chromedriver.exe path with path_to_chromedriver, e.g. "C:\\Users\\Username\\Downloads\\chromedriver.exe"
2) choose your preferred vaccination centre and specify the link to it as page_centre
3) specify all desired vaccine options (motifs_de_consultation) as they appear on the web page
4) specify email and password if to log in automatically (optional)
