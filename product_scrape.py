from bs4 import BeautifulSoup
import requests
import csv
from sqlconnect import insert_bank

#card_name='hdfc'

def get_bank_disc(cname):

    insert_bank(cname)

    cname = cname.lower()

    cardlist1=['icici','sbi','axis','hdfc']

    card_disc = []

    if cname in cardlist1:

        link = 'https://www.coupondunia.in/' + cname + '-bank-offers'

        #csv_file=open('offer_others.csv','w')
        #csv_writer=csv.writer(csv_file)
        #csv_writer.writerow([' Franchise ',' Offer Name ',' Offer Description ',' Coupon Code ',' Expiry Date '])

        src=requests.get(link).text

        soup=BeautifulSoup(src,'lxml')

        section=soup.find('section',class_='offer-cards')

        offer_div=section.find('div',class_='pre-render')

        offer_list=offer_div.find_all('div',class_='ofr-card-wrap')

        for i in range(len(offer_list)):

            fr_name=offer_list[i].find('div',class_='card-content-top').find('span',class_='store-name').text

            offer_name=offer_list[i].find('div',class_='card-content-top').find('div',class_='offer-title offer-get-code-link').text

            offer_desc=offer_list[i].find('div',class_='card-content-bottom').find('div',class_='offer-desc').find('ol').text

            offer_cpn=offer_list[i].find('div',class_='card-content-top').find('div',class_='get-codebtn-holder')

            cpn=offer_cpn.find('div',class_='get-offer-code')

            offer_exp=offer_cpn.find('div',class_='expiry-txt expiring-soon')

            cpn_code="No Coupon needed"

            exp_date="Not mentioned by the Franchise"

            if cpn is not None:
                cpn_code = "Paste this code at checkout : "+cpn['data-offer-value']

            if offer_exp is not None:
                exp_date = offer_exp.text

            fr_name=fr_name.strip()

            offer_name=offer_name.strip()

            offer_desc=offer_desc.strip()

            #csv_writer.writerow([fr_name,offer_name,offer_desc,cpn_code,exp_date])
            card_disc.append(["Franchise Name: "+fr_name, "Offer Name: "+offer_name,"Offer Description: "+offer_desc,"Coupon code: "+cpn_code,"Expiry date: "+exp_date])

        #csv_file.close

    else:

        link2 = 'https://www.americanexpress.com/in/network/offer/onlineoffers.html'

        #csv_file=open('card_offer_amex.csv','w')
        #csv_writer=csv.writer(csv_file)
        #csv_writer.writerow([' Franchise ',' Offer Description '])

        src2 = requests.get(link2).text

        soup2 = BeautifulSoup(src2,'lxml')

        section = soup2.find('div',class_='contain').find_all('div',class_='newsitem newspanel-grey')

        for j in range(len(section)):
            offer_name = section[j].find('div',class_='text').find('h2',class_='title').text.strip()
            offer_descr = section[j].find('div',class_='text').find('div',class_='description').text.strip()
            offer_descr = offer_descr.replace('T&Cs apply','')
            offer_descr = offer_descr.replace('Â', '')
            offer_descr = offer_descr.replace('\xa0', '')
            #csv_writer.writerow([offer_name,offer_descr])
            card_disc.append(["Franchise Name: "+offer_name, "Offer Description: "+offer_descr])

        #csv_file.close
    var = ""
    for i in card_disc:
        for j in i:
            var = var + j + '<br>'
        var = var + '<br>'+'<hr>'
    return var

#get_card_list = get_bank_disc(card_name)
#print(get_card_list)







