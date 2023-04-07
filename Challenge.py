import pandas as pd

class CCYConverter():
    def __init__(self):

        self.converstion_data = {
            "AUDUSD":0.8371,
            "CADUSD":0.8711,
            "USDCNY":6.1715,
            "EURUSD":1.2315, 
            "GBPUSD":1.5683, 
            "NZDUSD":0.7750, 
            "USDJPY":119.95, 
            "EURCZK":27.6028, 
            "EURDKK":7.4405, 
            "EURNOK":8.6651
        }

        self.currency_pair_table = [
        ["1:1","USD","USD","USD","USD","USD","USD","USD","USD","USD","D"],
        ["USD","1:1","USD","USD","USD","USD","USD","USD","USD","USD","D"],
        ["USD","USD","1:1","USD","USD","USD","USD","USD","USD","USD","D"],
        ["USD","USD","USD","1:1","EUR","Inv","USD","USD","EUR","USD","EUR"],
        ["USD","USD","USD","EUR","1:1","Inv","USD","USD","EUR","USD","EUR"],
        ["USD","USD","USD","D","D","1:1","USD","USD","USD","USD","USD"],
        ["USD","USD","USD","USD","USD","USD","1:1","USD","USD","USD","D"],
        ["USD","USD","USD","USD","USD","USD","USD","1:1","USD","USD","Inv"],
        ["USD","USD","USD","EUR","EUR","Inv","USD","USD","1:1","USD","EUR"],
        ["USD","USD","USD","USD","USD","USD","USD","USD","USD","1:1","D"],
        ["Inv","Inv","Inv","EUR","EUR","Inv","Inv","D","EUR","Inv","1:1"]
        ]
        column_index = ["AUD", "CAD","CNY", "CZK", "DKK", "EUR", "GBP", "JPY" ,"NOK", "NZD" ,"USD"]
        self.df = pd.DataFrame(self.currency_pair_table, columns=column_index,index = column_index)

    def calculate(self,From,To,Amount):
        
        try:
            if self.df[To][From] == "D":
                conversion_amount = float(Amount) * self.converstion_data[From + To]
            elif self.df[To][From] == "1:1":
                conversion_amount = float(Amount)
            elif self.df[To][From] == "Inv":
                conversion_amount = float(Amount) / self.converstion_data[To + From]
            elif self.df[To][From] == 'USD':
                #Check From & CCY combination present in Direct feed else From & CCY combination Inverted
                if From + self.df[To][From]  in self.converstion_data.keys():
                    temp_rate = self.converstion_data[From + self.df[To][From]]
                    CCY_amount = temp_rate * float(Amount)
                elif self.df[To][From] + From  in self.converstion_data.keys():
                    temp_rate = self.converstion_data[self.df[To][From] + From]
                    CCY_amount = float(Amount) / temp_rate
                #EUR is the only option
                # Converting given Amount to USD
                else: 
                    temp_rate_1 = self.converstion_data["EURUSD"]
                    if From + "EUR" in self.converstion_data.keys():
                        temp_rate_2 = self.converstion_data[From + "EUR"]
                        CCY_amount = float(Amount) * temp_rate_2 * temp_rate_1
                    else:
                        temp_rate_2 = self.converstion_data["EUR" + From]
                        CCY_amount = float(Amount)* temp_rate_1 / temp_rate_2   


                #Check CCY & To combination present in Direct feed else To & CCY combination Inverted
                if self.df[To][From] + To in self.converstion_data.keys():
                    Final_rate = self.converstion_data[self.df[To][From] + To]
                    conversion_amount =  CCY_amount * Final_rate
                elif To + self.df[To][From] in self.converstion_data.keys():
                    Final_rate = self.converstion_data[To + self.df[To][From]]
                    conversion_amount = CCY_amount / Final_rate
                else:
                    # Converting given Amount from USD to Target Currency
                    temp_rate_1 = self.converstion_data["EURUSD"]
                    if "EUR" + To in self.converstion_data.keys():
                        temp_rate_2 = self.converstion_data["EUR" + To]
                        conversion_amount = CCY_amount * temp_rate_2 / temp_rate_1
                    else:
                        temp_rate_2 = self.converstion_data[To + "EUR" ]
                        conversion_amount = CCY_amount /(temp_rate_2 * temp_rate_1)

            elif self.df[To][From] == 'EUR':
                 #Check From & CCY combination present in Direct feed else From & CCY combination Inverted
                if From + self.df[To][From]  in self.converstion_data.keys():
                    temp_rate = self.converstion_data[From + self.df[To][From]]
                    CCY_amount = temp_rate * float(Amount)
                elif self.df[To][From] + From  in self.converstion_data.keys():
                    temp_rate = self.converstion_data[self.df[To][From] + From]
                    CCY_amount = float(Amount) / temp_rate
                #USD is the only option
                # Converting given Amount to EUR
                else: 
                    temp_rate_1 = self.converstion_data["EURUSD"]
                    if From + "USD" in self.converstion_data.keys():            
                        temp_rate_2 = self.converstion_data[From + "USD"]
                        CCY_amount = float(Amount) * temp_rate_2 / temp_rate_1
                    else:
                        temp_rate_2 = self.converstion_data["USD" + From]
                        CCY_amount = float(Amount)/(temp_rate_1 * temp_rate_2 )


                #Check CCY & To combination present in Direct feed else To & CCY combination Inverted
                if self.df[To][From] + To in self.converstion_data.keys():
                    Final_rate = self.converstion_data[self.df[To][From] + To]
                    conversion_amount =  CCY_amount * Final_rate
                elif To + self.df[To][From] in self.converstion_data.keys():
                    Final_rate = self.converstion_data[To + self.df[To][From]]
                    conversion_amount = CCY_amount / Final_rate
                else:
                    # Converting given Amount from EUR to Target Currency
                    temp_rate_1 = self.converstion_data["EURUSD"]
                    if "USD" + To in self.converstion_data.keys():
                        temp_rate_2 = self.converstion_data["USD" + To]
                        conversion_amount = CCY_amount * temp_rate_2 * temp_rate_1
                    else:
                        temp_rate_2 = self.converstion_data[To + "USD" ]
                        conversion_amount = CCY_amount * temp_rate_1 / temp_rate_2 

            else:
                return "Unable to find rate for {}".format(From + To)

            if To == 'JPY':
                return round(conversion_amount,2)
            else:
                return conversion_amount

        except Exception as e : 
            return "Unable to find rate for {}".format(From + To)


OBJ = CCYConverter()

print("Supported Currencies: AUD, CAD, CNY, CZK, DKK, EUR, GBP, JPY ,NOK, NZD ,USD")
print("***Please note: Currencies are case sensistive")
n = int(input("Enter number of conversions to calculate : "))
for i in range(n):
    From, Amount = input("Currency From and Amount: ").split()
    To = input("Currency To: ")
    print(OBJ.calculate(From,To,Amount))





