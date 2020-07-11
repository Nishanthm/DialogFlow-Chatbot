from bs4 import BeautifulSoup
import requests
import csv
from sqlconnect import insert_item

#p="redmi mobile"

def get_prod_disc(prod_name):
    # prod_name = prod_name.lower()
    insert_item(prod_name)
    prod_disc = []

    new_prod_name = prod_name.replace(" ", '+')

    flip_url = "https://www.flipkart.com/search?q=" + new_prod_name

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    src_flip = requests.get(flip_url, headers=headers)
    soup_flip = BeautifulSoup(src_flip.content, "lxml")

    container_flip = soup_flip.find('div', attrs={'id': 'container'})

    if container_flip is not None:

        section_flip = container_flip.find_all('div', class_='_3O0U0u')
        if section_flip is not None:

            l2 = len(section_flip)

            if l2 > 2:
                l2 = 3

            for j in range(l2):

                prod_link_flip = section_flip[j].find('a', attrs={'rel': 'noopener noreferrer'})['href']

                prod_link_flip = prod_link_flip.strip()

                org_link_flip = "https://www.flipkart.com" + prod_link_flip

                prod_src_flip = requests.get(org_link_flip, headers=headers)
                prod_soup_flip = BeautifulSoup(prod_src_flip.content, "lxml")

                prod_title_div_flip = prod_soup_flip.find('div', class_='_29OxBi')
                prod_title_flip = prod_title_div_flip.find('span', class_='_35KyD6').text.strip()

                offer_list_present_flip = prod_soup_flip.find('div', attrs={'id': 'container'}).find('div',
                                                                                                     class_='_3nSGUy')

                offer_desc_flip = "<br>Franchise Name : Flipkart "


                # no_offer_desc_flip = ""

                #  offer_desc_flip += '\n'

                # no_offer_desc_flip += '\n'

                if offer_list_present_flip is not None:
                    offer_list_flip = offer_list_present_flip.find_all('span', class_='_7g_MLT row')

                    offer_desc_flip += "<br>Product title as in Flipkart website : " + prod_title_flip

                    # no_offer_desc_flip += "Product title as in Flipkart website : " + prod_title_flip + '\n'

                    # offer_desc_flip += '\n'

                    # no_offer_desc_flip += '\n'

                    flag = 0

                    for i in range(len(offer_list_flip)):
                        a = offer_list_flip[i].text
                        a = a.strip()
                        a = a.replace('\n', ' ')
                        a = a.replace('\xa0', '')
                        a = a.replace('  ', ' ')
                        a = a.replace('\u20b9', '')
                        a = a.replace('T&C', ' ')
                        a = a.replace('Offer', 'Offer ')
                        if "Bank Offer" in a:
                            offer_desc_flip += '<br>'+a
                            #   offer_desc_flip += '\n'
                            flag = 1

                    if flag == 0:
                        offer_desc_flip += "Sorry :( There are currently no offers matching your product."
                        offer_desc_flip += "You can rather consider the following Bank Offers ! " + '\n'

                    offer_desc_flip += "<br>For more details about the product " + '\n'
                    offer_desc_flip += '<a href="' + org_link_flip + '" target="_blank"> Click Here </a>'

                else:
                    offer_desc_flip += "Product title as in Flipkart website : " + prod_title_flip
                    offer_desc_flip += '\n'
                    offer_desc_flip += " Sorry :( There are currently no offers for this product matching your Credit or Debit Card "
                    offer_desc_flip += '\n'
                    offer_desc_flip += "For more details about the product  " + '\n'
                    offer_desc_flip += '<a href="' + org_link_flip + '" target="_blank"> Click Here </a>'

                    # name_flip = "Redmi Note 7 pro" # Name of the product as mentioned by the user to the chatbot

                # csv_writer.writerow([prod_name, offer_desc_flip])
                prod_disc.append([prod_name, offer_desc_flip])
        else:
            offer_desc_flip_sry1 = "Ooops ! That didn't work :( "
            # csv_writer.writerow([prod_name, offer_desc_flip_sry1])
            prod_disc.append([prod_name, offer_desc_flip_sry1])
    else:
        offer_desc_flip_sry2 = "Ooops ! That didn't work :( "
        # csv_writer.writerow([prod_name, offer_desc_flip_sry2])
        prod_disc.append([prod_name, offer_desc_flip_sry2])
        # print()
        # print(offer_desc_flip)

    var = ""
    for i in prod_disc:
        for j in i:
            var = var + j
        var += '<hr>'

    return var

#get_off_list=get_prod_disc(p)
#print(get_off_list)
