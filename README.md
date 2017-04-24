# FBI-Crime-Data
Original Data: https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/tables/table-8/table_8_offenses_known_to_law_enforcement_by_state_by_city_2015.xls/view

Link to group page(Chinese): http://www.minkoder.com/crimerateproj

Current Attributes in Json:


    Num: Number of violent crimes occured in this city during 2015

    Index: Crime Rate / mean Crime Rate (An indicator for city safety compared to US average)
    
    Rate: Number of violent crimes occured annually for 100k people in this city
    
    Ranking: Residents in this city has safter living condition than % of people in U.S.
    
Example:

    "Santa Barbara, CA": {
 
        "Index": 106,
        
        "Num": 363,

        "Ranking": 46.8,
        
        "Rate": 395
        
    }
    
