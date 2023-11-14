# immobiliare-scraper
Scraper for Italian real state website www.immobiliare.it.

With this scraper you can get the information of the listed real estates in json, csv and also use the pd.DataFrame that it creates.

Simple usage:

    pip install -r requirements.txt
    python3 scraper.py

Code:

    immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza", get_data_of_following_pages=True)
    immo.save_data_json()
    immo.save_data_csv()
    data = immo.data_frame

get_data_of_following_pages paremeter specifies whether to get the data of this page only or get the data of the following pages as well.

Also here's how to get data with different filters and save them in single json/csv file:

    immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&prezzoMassimo=1200", get_data_of_following_pages=True)
    immo.url = "https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&prezzoMinimo=1200&prezzoMassimo=1600"
    immo.gather_real_estate_data()
    immo.url = "https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&prezzoMinimo=1600&prezzoMassimo=2500"
    immo.gather_real_estate_data()
    immo.save_data_json()
    immo.save_data_csv()
    data = immo.data_frame
