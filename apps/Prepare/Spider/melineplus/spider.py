# -*- coding:utf-8 -*-  
""" 
@author: zliu.Elliot
@file: spider.py 
@time: 2020/5/6-16:48 
@email: zliu.Elliot@wind.com.cn
"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
from selenium import webdriver
import random

"""
topic_links = {
    # "Elder Abuse": "https://medlineplus.gov/elderabuse.html",
    # "Falls": "https://medlineplus.gov/falls.html",
    # "Macular Degeneration": "https://medlineplus.gov/maculardegeneration.html",
    "Taste and Smell Disorders": "https://medlineplus.gov/tasteandsmelldisorders.html",
    "Older Adult Health": "https://medlineplus.gov/olderadulthealth.html",
    "Skin Aging": "https://medlineplus.gov/skinaging.html",
    "Alzheimer's Caregivers": "https://medlineplus.gov/alzheimerscaregivers.html",
    "Alzheimer's Disease": "https://medlineplus.gov/alzheimersdisease.html",
    "Memory": "https://medlineplus.gov/memory.html", "Angina": "https://medlineplus.gov/angina.html",
    "Coronary Artery Disease": "https://medlineplus.gov/coronaryarterydisease.html",
    "Cataract": "https://medlineplus.gov/cataract.html",
    "Assisted Living": "https://medlineplus.gov/assistedliving.html",
    "Assistive Devices": "https://medlineplus.gov/assistivedevices.html",
    "Balance Problems": "https://medlineplus.gov/balanceproblems.html",
    "Urinary Incontinence": "https://medlineplus.gov/urinaryincontinence.html",
    "High Blood Pressure": "https://medlineplus.gov/highbloodpressure.html",
    "Osteoporosis": "https://medlineplus.gov/osteoporosis.html",
    "Stroke": "https://medlineplus.gov/stroke.html",
    "Heart Diseases": "https://medlineplus.gov/heartdiseases.html",
    "Heart Failure": "https://medlineplus.gov/heartfailure.html",
    "Menopause": "https://medlineplus.gov/menopause.html",
    "COPD": "https://medlineplus.gov/copd.html",
    "Home Care Services": "https://medlineplus.gov/homecareservices.html",
    # "Hearing Disorders and Deafness": "https://medlineplus.gov/hearingdisordersanddeafness.html",
    # "Osteoarthritis": "https://medlineplus.gov/osteoarthritis.html",
    "Dementia": "https://medlineplus.gov/dementia.html",
    "Diabetes": "https://medlineplus.gov/diabetes.html",
    "Erectile Dysfunction": "https://medlineplus.gov/erectiledysfunction.html",
    "Tremor": "https://medlineplus.gov/tremor.html",
    "Exercise for Older Adults": "https://medlineplus.gov/exerciseforolderadults.html",
    "Glaucoma": "https://medlineplus.gov/glaucoma.html",
    "Healthy Aging": "https://medlineplus.gov/healthyaging.html",
    # "Shingles": "https://medlineplus.gov/shingles.html", "Medicare": "https://medlineplus.gov/medicare.html",
    "Nursing Homes": "https://medlineplus.gov/nursinghomes.html",
    "Mild Cognitive Impairment": "https://medlineplus.gov/mildcognitiveimpairment.html",
    "Medicare Prescription Drug Coverage": "https://medlineplus.gov/medicareprescriptiondrugcoverage.html",
    "Older Adult Mental Health": "https://medlineplus.gov/olderadultmentalhealth.html",
    "Nutrition for Older Adults": "https://medlineplus.gov/nutritionforolderadults.html",
    "Parkinson's Disease": "https://medlineplus.gov/parkinsonsdisease.html",
    "Prostate Cancer": "https://medlineplus.gov/prostatecancer.html",
    # "Prostate Diseases": "https://medlineplus.gov/prostatediseases.html",
    "Sinusitis": "https://medlineplus.gov/sinusitis.html"
}
"""

"""
topic_links = {
    # "Anatomy": "https://medlineplus.gov/anatomy.html", 无see more articles链接
               # "Infertility": "https://medlineplus.gov/infertility.html",
               # "Assisted Reproductive Technology": "https://medlineplus.gov/assistedreproductivetechnology.html",
               # "Penis Disorders": "https://medlineplus.gov/penisdisorders.html",
               # "Enlarged Prostate (BPH)": "https://medlineplus.gov/enlargedprostatebph.html",
               # "Birth Control": "https://medlineplus.gov/birthcontrol.html",
               # "Chlamydia Infections": "https://medlineplus.gov/chlamydiainfections.html",
               "Circumcision": "https://medlineplus.gov/circumcision.html",
               # "Gonorrhea": "https://medlineplus.gov/gonorrhea.html",
               # "Genital Warts": "https://medlineplus.gov/genitalwarts.html",
               # "Sexually Transmitted Diseases": "https://medlineplus.gov/sexuallytransmitteddiseases.html",
               # "Erectile Dysfunction": "https://medlineplus.gov/erectiledysfunction.html",
               # "Genital Herpes": "https://medlineplus.gov/genitalherpes.html",
               # "Herpes Simplex": "https://medlineplus.gov/herpessimplex.html",
               # "Male Infertility": "https://medlineplus.gov/maleinfertility.html",
               # "Testicular Disorders": "https://medlineplus.gov/testiculardisorders.html",
               # "Vasectomy": "https://medlineplus.gov/vasectomy.html",
               "Reproductive Hazards": "https://medlineplus.gov/reproductivehazards.html",
               # "Sexual Problems in Men": "https://medlineplus.gov/sexualproblemsinmen.html",
               # "Prostate Cancer": "https://medlineplus.gov/prostatecancer.html",
               # "Prostate Cancer Screening": "https://medlineplus.gov/prostatecancerscreening.html",
               # "Prostate Diseases": "https://medlineplus.gov/prostatediseases.html",
               # "Testicular Cancer": "https://medlineplus.gov/testicularcancer.html",
               # "Sexual Health": "https://medlineplus.gov/sexualhealth.html",
               # "Syphilis": "https://medlineplus.gov/syphilis.html"
}
"""

topic_links = {"Ectopic Pregnancy": "https://medlineplus.gov/ectopicpregnancy.html",
                "Abortion": "https://medlineplus.gov/abortion.html",
                # "Endometriosis": "https://medlineplus.gov/endometriosis.html",
                # "Teenage Pregnancy": "https://medlineplus.gov/teenagepregnancy.html",
                "HIV/AIDS and Pregnancy": "https://medlineplus.gov/hivaidsandpregnancy.html",
                "Pregnancy and Drug Use": "https://medlineplus.gov/pregnancyanddruguse.html",
                "Menstruation": "https://medlineplus.gov/menstruation.html",
                # "Prenatal Testing": "https://medlineplus.gov/prenataltesting.html",
                "Infertility": "https://medlineplus.gov/infertility.html",
                "Assisted Reproductive Technology": "https://medlineplus.gov/assistedreproductivetechnology.html",
                # "Vaginitis": "https://medlineplus.gov/vaginitis.html",
                "Birth Control": "https://medlineplus.gov/birthcontrol.html",
                "Breast Cancer": "https://medlineplus.gov/breastcancer.html",
                # "Breast Diseases": "https://medlineplus.gov/breastdiseases.html",
                "Breast Reconstruction": "https://medlineplus.gov/breastreconstruction.html",
                "Breastfeeding": "https://medlineplus.gov/breastfeeding.html",
                "Cesarean Section": "https://medlineplus.gov/cesareansection.html",
                # "Yeast Infections": "https://medlineplus.gov/yeastinfections.html",
                # "Cervical Cancer": "https://medlineplus.gov/cervicalcancer.html",
                "Cervical Cancer Screening": "https://medlineplus.gov/cervicalcancerscreening.html",
                "Cervix Disorders": "https://medlineplus.gov/cervixdisorders.html",
                "Menopause": "https://medlineplus.gov/menopause.html",
                "Childbirth": "https://medlineplus.gov/childbirth.html",
                "Chlamydia Infections": "https://medlineplus.gov/chlamydiainfections.html",
                "Gonorrhea": "https://medlineplus.gov/gonorrhea.html",
                "Genital Warts": "https://medlineplus.gov/genitalwarts.html",
                "Sexually Transmitted Diseases": "https://medlineplus.gov/sexuallytransmitteddiseases.html",
                # "Pelvic Floor Disorders": "https://medlineplus.gov/pelvicfloordisorders.html",
                "Diabetes and Pregnancy": "https://medlineplus.gov/diabetesandpregnancy.html",
                # "Vaginal Bleeding": "https://medlineplus.gov/vaginalbleeding.html",
                "Period Pain": "https://medlineplus.gov/periodpain.html",
                "Sexual Problems in Women": "https://medlineplus.gov/sexualproblemsinwomen.html",
                "Uterine Cancer": "https://medlineplus.gov/uterinecancer.html",
                "Hormone Replacement Therapy": "https://medlineplus.gov/hormonereplacementtherapy.html",
                "Female Infertility": "https://medlineplus.gov/femaleinfertility.html",
                "Tubal Ligation": "https://medlineplus.gov/tuballigation.html",
                "Uterine Fibroids": "https://medlineplus.gov/uterinefibroids.html",
                # "Genital Herpes": "https://medlineplus.gov/genitalherpes.html",
                "High Blood Pressure in Pregnancy": "https://medlineplus.gov/highbloodpressureinpregnancy.html",
                # "Health Problems in Pregnancy": "https://medlineplus.gov/healthproblemsinpregnancy.html",
                "Herpes Simplex": "https://medlineplus.gov/herpessimplex.html",
                # "HPV": "https://medlineplus.gov/hpv.html", "Hysterectomy": "https://medlineplus.gov/hysterectomy.html",
                # "Infections and Pregnancy": "https://medlineplus.gov/infectionsandpregnancy.html",
                "Mastectomy": "https://medlineplus.gov/mastectomy.html",
                # "Mammography": "https://medlineplus.gov/mammography.html",
                # "Prenatal Care": "https://medlineplus.gov/prenatalcare.html",
                "Miscarriage": "https://medlineplus.gov/miscarriage.html",
                "Ovarian Cancer": "https://medlineplus.gov/ovariancancer.html",
                "Ovarian Cysts": "https://medlineplus.gov/ovariancysts.html",
                "Ovarian Disorders": "https://medlineplus.gov/ovariandisorders.html",
                "Primary Ovarian Insufficiency": "https://medlineplus.gov/primaryovarianinsufficiency.html",
                "Polycystic Ovary Syndrome": "https://medlineplus.gov/polycysticovarysyndrome.html",
                "Pelvic Inflammatory Disease": "https://medlineplus.gov/pelvicinflammatorydisease.html",
                "Pelvic Pain": "https://medlineplus.gov/pelvicpain.html",
                "Premenstrual Syndrome": "https://medlineplus.gov/premenstrualsyndrome.html",
                "Pregnancy": "https://medlineplus.gov/pregnancy.html",
                "Pregnancy and Opioids": "https://medlineplus.gov/pregnancyandopioids.html",
                "Reproductive Hazards": "https://medlineplus.gov/reproductivehazards.html",
                "Stillbirth": "https://medlineplus.gov/stillbirth.html",
                "Preterm Labor": "https://medlineplus.gov/pretermlabor.html",
                "Sexual Health": "https://medlineplus.gov/sexualhealth.html",
                "Syphilis": "https://medlineplus.gov/syphilis.html",
                "Trichomoniasis": "https://medlineplus.gov/trichomoniasis.html",
                "Uterine Diseases": "https://medlineplus.gov/uterinediseases.html",
                "Vaginal Cancer": "https://medlineplus.gov/vaginalcancer.html",
                "Vaginal Diseases": "https://medlineplus.gov/vaginaldiseases.html",
                "Vulvar Cancer": "https://medlineplus.gov/vulvarcancer.html",
                "Vulvar Disorders": "https://medlineplus.gov/vulvardisorders.html"}


def get_empty_article():
    return {
        "title": None,
        "authors": None,
        "publication": None,
        "abstract": None,
        "references": None,
        "doi_url": None
    }


def open_in_new(url, browser):
    browser.execute_script("window.open('', '__self__')")


def close_tab(browser):
    browser.execute_script("window.close()")


def save_detail(doc_list, topic):
    with open(r"../detail/doc_detail_《{0}》.json".format(topic), "w", encoding="utf-8") as file:
        file.write(json.dumps(doc_list, ensure_ascii=False))


article_list = list()

driver = webdriver.Chrome(executable_path=r"C:\\Users\\Mr.Robot\\Desktop\\workspace\\SmartDocRetrieval-master\\apps\\PreComputeModule\\Spider\\browser_driver\\chromedriver.exe")
for topic in topic_links.keys():
    topic_url = topic_links[topic]
    print(topic_url)
    driver.get(topic_url)
    article_list_url = driver.find_element_by_css_selector("#section59 > ul > li:last-child > a")
    if article_list_url is None:
        continue
    article_list_url = article_list_url.get_attribute("href")
    print("list_url:{0}".format(article_list_url))
    driver.get(article_list_url)
    while True:
        article_items = driver.find_elements_by_css_selector("div.rprt")
        for item in article_items:
            time.sleep(random.randrange(0, 5))
            try:
                detail_url = item.find_element_by_css_selector("a").get_property("href")
                open_in_new(detail_url, driver)
                driver.switch_to.window(driver.window_handles[1])
                driver.get(detail_url)
                publication = driver.find_element_by_css_selector(".cit")
                if publication is not None:
                    publication = publication.text
                title = driver.find_element_by_css_selector("div.rprt_all > div > h1")
                if title is not None:
                    title = title.text
                author_items = driver.find_element_by_css_selector("div.auths").find_elements_by_css_selector("a")
                authors = None
                if author_items is not None and len(author_items) > 0:
                    authors = list()
                    for author in author_items:
                        authors.append(author.text)
                abstract = driver.find_element_by_css_selector("div.abstr")
                if abstract is not None:
                    abstract = abstract.text
                doi_url = driver.find_element_by_css_selector("div.resc > dl > dd > a:last-child").get_property("href")
                doc = get_empty_article()
                doc["topic"] = topic
                doc["title"] = title
                doc["authors"] = authors
                doc["publication"] = publication
                doc["abstract"] = abstract
                doc["doi_url"] = doi_url
                article_list.append(doc)
                save_detail(article_list, topic)
            except Exception as e:
                continue
            finally:
                close_tab(driver)
                driver.switch_to.window(driver.window_handles[0])
        try:
            next_page = driver.find_element_by_css_selector("a.next")
            if next_page is not None:
                next_page.click()
        except Exception as e:
            print(e)
        finally:
            break

