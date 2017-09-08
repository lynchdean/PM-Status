from bs4 import BeautifulSoup
import getpass
import mechanize
import cookielib

def login(username, password):
    br = mechanize.Browser()

    cookie_jar = cookielib.LWPCookieJar()
    br.set_cookiejar(cookie_jar)

    #Debugging
    #br.set_debug_http(True)
    #br.set_debug_responses(True)

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]

    # Login
    br.open("https://my.parcelmotel.com/Account/Login")
    br.select_form(nr=0)

    br.form['UserName'] = username
    br.form['Password'] = password

    res = br.submit()
    request = br.request

    soup = BeautifulSoup(res.read(), "lxml")

    for span in soup.findAll('span'):
        if str(span).find("Sign In was unsuccessful.") != -1:
            print("Incorrect username or password.")
            quit()

    return br

def get_status(br):
    page = br.open("http://my.parcelmotel.com/Member#divRecentActivityHeading")
    soup = BeautifulSoup(page, "lxml")

    table = soup.find('table', attrs={'class':'Report MemberPackageHistory'})
    rows = table.find_all('tr')

    parcels = False
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if cols != [] and cols[7] != "Delivered":
            time_date = cols[1].split(" ")
            print("[" + cols[3] + "]")
            print(" " + u"\u2022" + " Arrived: " + cols[2] + " on " + time_date[0] + " " + time_date[1] + " @ " + time_date[3])
            print(" " + u"\u2022" + " Status: " + cols[7] + " @ " + cols[8].split(" ")[3] + "\n")
            if cols[6] != "":
                print(" " + u"\u2022" + " Code: " + cols[6] + "\n")
            parcels = True

    if not parcels:
        print("There is no active parcels.")

def main():
    print "Username:",
    username = raw_input()
    password = getpass.getpass()
    print("")


    br = login(username, password)
    get_status(br)

if __name__ == '__main__':
    main()
