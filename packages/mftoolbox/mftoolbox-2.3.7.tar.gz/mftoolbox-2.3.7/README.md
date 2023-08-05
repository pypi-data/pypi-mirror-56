# mftoolbox

Package created to support my **MF2** project development.

Functions:

* encoding(): returns the proper encoding for handling config files with configparser. It's based on the based on the operating system:
    * UTF-16 for Windows;
    * UTF-8 for Mac.

Classes:

* Build: automatically controls build number based on changes made to the file;
* UltimaCotacaoDolar: gets the last available BRL/USD exchange rate from Brazilian's Central Bank;
* Proventos: works with dividends data;
* Timestamp: formats execution start time information
    * self.str_yyyymmdd: now() formatted as YYYYMMDD
    * str_hhmmss: now() formatted as HHMMSS
    * dtt_timestamp: now() as timestamp
    * dtt_now: now() as datetime
* CotacaoDolarData: gets USD/BRL exchange rate for a specific date
    * Arguments:
        * Date: string with date formatted as DD/MM/YYYY
    * Returns:
        * self.valor: float of the exchange rate for the specific date
* CotacaoDolarHistorico: gets a list of USD/BRL exchange rate for a range of dates
    * Arguments:
        * Start Date: string with date formatted as DD/MM/YYYY
        * End Date: string with date formatted as DD/MM/YYYY
    * Returns:
        * self.cotacoes: list of tuples in the format [Date, Exchange Rate]
        * self.itens: total itens in the list
        

# Version history

2.3.7
* Changed from a single module ('mftoolbox') containing all classes and functions to a multi-module approach
* Changed internal imports to hide objects that don't need to be exposed (import xxx as _xxx)
* implemented error handling to cotacaodolar module

2.3.0 - 2.3.6
* perfecting the process of package generation. No changes to code

