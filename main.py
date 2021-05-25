from auto_rdv_doctolib import find_rdv

path_to_chromedriver = 'C:\\Users\\Username\\Downloads\\chromedriver.exe'  # driver for chrome - to be controlled with python
page_centre = "https://www.doctolib.fr/vaccination-covid-19/saint-denis/centre-de-vaccination-covid-19-stade-de-france"
motifs_de_consultation = ['1re injection vaccin COVID-19 (Pfizer-BioNTech)', '1re injection vaccin COVID-19 (Moderna)']  # string array of all wanted vaccine options (Pfizer, Moderna, etc) offered by the centre

# run the program
find_rdv(path_to_chromedriver, page_centre, motifs_de_consultation, n_tries=10000, response_wait_time=0.1,
             check_delay=0.01, my_email=None, my_password=None)