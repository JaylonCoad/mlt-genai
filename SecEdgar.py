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

se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
# unit testing website: https://www.guru99.com/unit-testing-guide.html

print(se.ticker_to_cik("AAPL"))
print(se.name_to_cik("Apple Inc."))
