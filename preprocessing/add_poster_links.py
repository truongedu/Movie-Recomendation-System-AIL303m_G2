from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os


def fetch_single_poster(driver, imdb_url):
    
    try:
        driver.get(imdb_url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "script[type='application/ld+json']")))

        html_content= driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts_tag = soup.find('script', type = 'application/ld+json')
        if scripts_tag:
            movie_information= json.loads(scripts_tag.string)
            movie_poster_url= movie_information.get('image')
            return movie_poster_url
        else:
            return ''
        
    except TimeoutException:
        print(f"Timeout: Không tìm thấy thẻ JSON cho {imdb_url} sau 10 giây.")
        return ''
    except Exception as e:
        print(f'Errol when get poster {imdb_url}: {e}')

def get_posters_in_batch(driver, list_of_imdb_urls):
    poster_links = {}
    for url in list_of_imdb_urls:
        print(f"Fetching poster for: {url}")
        link = fetch_single_poster(driver, url)
        poster_links[url] = link
        time.sleep(0.5) 
    return poster_links

if __name__ == '__main__':
    links_df = pd.read_csv('tmp_final_dataset.csv')
    urls_to_process = links_df['imdb'].dropna().unique().tolist()
    # urls_to_process= urls_to_process
    batch_size = 10
    all_poster_links = {}

    checkpoint_file = 'merged_checkpoint.csv'
    if os.path.exists(checkpoint_file):
        print("Đã tìm thấy file checkpoint, đang tải dữ liệu đã cào...")
        df_checkpoint = pd.read_csv(checkpoint_file)
        all_poster_links = pd.Series(df_checkpoint.poster_link.values, index=df_checkpoint.imdb_url).to_dict()
        urls_to_fetch = [url for url in urls_to_process if url not in all_poster_links]
        print(f"Còn lại {len(urls_to_fetch)} link cần cào.") 
        
    else:
        urls_to_fetch = urls_to_process

    batches = [urls_to_fetch[i:i + batch_size] for i in range(0, len(urls_to_fetch), batch_size)]

    if not batches:
        print("Không còn link nào để cào. Tiến hành xử lý dữ liệu cuối cùng.")
    else:
        driver = webdriver.Chrome() 
        try:
            for i, batch in enumerate(batches):
                print(f"--- Đang xử lý lô {i+1}/{len(batches)} ---")
                batch_posters = get_posters_in_batch(driver, batch)
                all_poster_links.update(batch_posters)
                
                temp_df = pd.DataFrame(list(all_poster_links.items()), columns=['imdb_url', 'poster_link'])
                temp_df.to_csv(checkpoint_file, index=False)
                print(f"Đã lưu checkpoint sau khi xử lý lô {i+1}.")
        finally:
            print('........Đóng Chrome........')
            driver.quit()

    print("Đang gộp link poster vào DataFrame chính...")
    links_df['poster_link'] = links_df['imdb'].map(all_poster_links)
    links_df['poster_link'] = links_df['poster_link'].replace('', pd.NA)
    
    final_csv_path = 'final_dataset_with_poster.csv'
    # print(links_df[['userId', 'movieId']].duplicated().sum(), "bản ghi trùng lặp trong DataFrame.")
    links_df.to_csv(final_csv_path, index=False)

    print("\n--- HOÀN TẤT --- ")
    print(f"Đã lưu DataFrame cuối cùng vào file: {final_csv_path}")
    print("5 dòng đầu của file kết quả:")
    print(links_df.head())



  