from app.get_enem import Crawler
from app.etl import ETL
from settings import PATH
import os

def main() -> None:
    
    crawler = Crawler()
    crawler.download_file()

    etl = ETL()
    etl.run_etl()

    os.system(f'rm -rf {PATH + "/data"}')


if __name__ == '__main__':
    main()



    

