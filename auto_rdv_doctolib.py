from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import winsound


def find_rdv(path_to_chromedriver, page_centre, motifs_de_consultation, n_tries=10000, response_wait_time=0.1,
             check_delay=0.01, my_email=None, my_password=None):
    """
    this function automatically clicks on a vaccination rendez-vous as soon as it becomes available. The program will
     automatically select the first rendez-vous that appears in the displayed time frame (3 days with the
     default window size). If successful, alarm sound will be played.
    :param path_to_chromedriver: path to chromedriver.exe
    :param page_centre: eb page of the chosen vaccination centre
    :param motifs_de_consultation: array of str - desired vaccine options as they appear in the dropdown menu
    :param n_tries: number of refreshes
    :param response_wait_time: time for rdv slots to load, once reached the info will reload
    :param check_delay: short delay time between rapid checks
    :param my_email: your email
    :param my_password: your Doctolib password
    :return:
    """
    driver = webdriver.Chrome(path_to_chromedriver)

    if my_email is not None:
        login(driver, my_email, my_password)

    motifs_de_consultation += ['Choisissez un motif']  # add default motif used for reloading
    driver.get(page_centre)

    # cycle of reloading info. Reloading is done by switching to a different motif_de_consultation which avoids having
    # to reload the whole page
    count = 0
    motif_ind = 0
    while count < n_tries:
        print('try number', count)

        # choose motif de consultation
        motif = motifs_de_consultation[motif_ind]
        select_motif_de_consultation(driver, motif)

        # continuously check for slots
        rdv_is_chosen = False
        if motif != 'Choisissez un motif':
            rdv_is_chosen = check_for_slots(driver, response_wait_time, check_delay)

        if rdv_is_chosen:
            play_success_sound()
            break
        else:
            count += 1
            motif_ind = (motif_ind + 1) % len(motifs_de_consultation)

        if count == n_tries:
            print('maximum number of page refreshes reached')
            

def login(driver, my_email, my_password):
    """
    log in to your Doctolib account automatically
    :param driver: selenium driver
    :param my_email: your email
    :param my_password: your Doctolib password
    :return:
    """
    driver.get("https://www.doctolib.fr/sessions/new")
    driver.find_element(By.ID, "username").click()
    driver.find_element(By.ID, "username").send_keys(my_email)
    driver.find_element(By.ID, "username").send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "(//input[@id='password'])[2]").click()
    driver.find_element(By.XPATH, "(//input[@id='password'])[2]").send_keys(my_password)
    driver.find_element(By.XPATH, "(//input[@id='password'])[2]").send_keys(Keys.ENTER)
    time.sleep(5)  # wait to submit credentials


def select_motif_de_consultation(driver, motif):
    """
    when on the page of the vaccination centre, select motif_de_consultation
    :param driver: selenium driver
    :param motif: motif_de_consultation (string as it appears in the dropdown)
    :return:
    """
    driver.find_element(By.ID, "booking_motive").click()
    dropdown = driver.find_element(By.ID, "booking_motive")
    dropdown.find_element(By.XPATH, "//option[. = '" + motif + "']").click()
    driver.find_element(By.ID, "booking_motive").click()
    driver.execute_script("window.scrollTo(0,0)")


def check_for_slots(driver, response_wait_time, check_delay):
    """
    continuously check for available time slots, until "Aucun rendez-vous" message appears, or rendez-vous is selected,
    or response wait time is reached. 
    :param driver: selenium driver
    :param response_wait_time: time for rdv slots to load - once reached the info will reload
    :param check_delay: short delay time between rapid checks
    :return: boolean - True if rdv is chosen, False otherwise
    """
    time_passed = 0
    while time_passed < response_wait_time:
        time.sleep(check_delay)
        time_passed += check_delay
        print('mini-cycle time_passed', time_passed)

        if is_aucun_rdv_message(driver):  # if aucun rendez-vous shows up, break and start next iteration
            print('check_for_slots complete: Aucun rendez-vous message appeared')
            return False
        elif is_rdv_selection_menu(driver):  # if selector shows up, press immediately!
            driver.find_element(By.CSS_SELECTOR, ".availabilities-slot:nth-child(1)").click()
            print('check_for_slots complete: Rendez-vous is chosen!')
            return True

        if time_passed >= response_wait_time:
            print('check_for_slots complete: response wait time reached')
    return False


def is_aucun_rdv_message(driver):
    """
    if "aucun rendez-vous" message appears, return true
    :param driver: selenium driver
    :return:
    """
    if len(driver.find_elements_by_xpath("//*[contains(text(),'Aucun rendez-vous')]")) > 1:
        return True
    else:
        return False


def is_rdv_selection_menu(driver):
    """
    if rendez-vous selector appears, return true
    :param driver: selenium driver
    :return:
    """
    if len(driver.find_elements(By.CSS_SELECTOR, ".availabilities-slot:nth-child(1)")) != 0:
        return True
    else:
        return False


def play_success_sound():
    """
    plays alarm sound (modify if not on Windows)
    :return:
    """
    print('Success!  Stopping cycle')
    winsound.PlaySound("*", winsound.SND_ALIAS)


