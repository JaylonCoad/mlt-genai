import requests # allows us to make HTTP requests

class SecEdgar:
    def __init__(self, fileurl): # given the URL, create a class with the URL, and 3 empty dictionaries
        self.fileurl = fileurl
        self.namedict = {} # maps company name to CIK info
        self.tickerdict = {} # maps ticker to CIK info
        self.cikdict = {} # maps CIK string/number to CIK info
        
        headers = {'user-agent' : 'MLT CP jayloncoad@gmail.com'} # header needed so the SEC API can identify us
        r = requests.get(self.fileurl, headers=headers) # request the info from the SEC API

        self.filejson = r.json() # stores the JSON data into a dictionary in our class
        
        #print(r.text) # prints the data from the SEC API
        #print(self.filejson) # prints the dictionary of the JSON data

        self.cik_json_to_dict() # calls this function on our current object to populate the cik_tuple

    def name_to_cik(self, name):
        return self.namedict.get(name.lower()) # given the name of a company, returns the CIK number, company name, and ticker. otherwise returns None if not found

    def ticker_to_cik(self, ticker):
        return self.tickerdict.get(ticker.lower()) # given the ticker of a company, returns the CIK number, company name, and ticker. otherwise returns None if not found

    def cik_json_to_dict(self):
        for company in self.filejson.values(): # loops through each company in the JSON file
            cik_str = str(company['cik_str']) # string more consistent than int when dealing with large numbers
            name = company['title'].lower() # finds the company name
            ticker = company['ticker'].lower() # finds the company ticker

            cik_info = (cik_str, name, ticker) # common tuple to store in the dictionaries
            self.namedict[name] = cik_info
            self.tickerdict[ticker] = cik_info
            self.cikdict[cik_str] = cik_info

    def get_filings(self, cik):
        headers = {'user-agent' : 'MLT CP jayloncoad@gmail.com'} # header needed so the SEC API can identify us
        cik = cik.zfill(10) # make sure the CIK number is 10 characters by adding zeroes
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        print(f"url im going to: {url}")
        r = requests.get(url, headers=headers) # request the info from the SEC API
        return r.json() # gives us the general company json file that includes everything and then we will use this to create a link to the specific file the user wants

    def annual_filing(self, cik, year):
        filings = self.get_filings(cik)["filings"]["recent"] # indexes the recent filings list
        formsList = filings["form"] # finds the forms list according to how it's stored in the json
        datesList = filings["filingDate"] # finds the dates list according to how it's stored in json
        accessionNumberList = filings["accessionNumber"] # finds the accession number lists
        primaryDocumentList = filings["primaryDocument"] # finds the primary document lists
        found = False # used to see if we found the accession number
        for i in range(len(formsList)):
            if formsList[i] == "10-K" and datesList[i][0:4] == str(year): # trying to find the correct form at the correct year and then get the corresponding accessionNumber and primaryDocument
                accessionNumber = accessionNumberList[i].replace("-", "") # remove the dashes
                primaryDocument = primaryDocumentList[i]
                found = True
        if not found: # handles not found
            print("Year not found. Try again")
        else:
            return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}" # returns the url of the 10-K report
    

    def quarterly_filing(self, cik, year, quarter):
        pass

se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
# unit testing website: https://www.guru99.com/unit-testing-guide.html

cik = se.ticker_to_cik("AAPL")[0]
print(se.annual_filing(cik, 2024))


