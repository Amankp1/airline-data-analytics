from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from datetime import datetime 

def date_formatter(input_date):
    from datetime import datetime

    # Convert to datetime object
    date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    # Manually construct the string without leading zero on day
    formatted_date = f"{date_obj.strftime('%A')}, {date_obj.strftime('%B')} {date_obj.day}, {date_obj.year}"

    return formatted_date


def data_scrapper(source, destination, departure, trip_type="Round Trip", arrival=None):
    # Setup headless Chrome browser
    chrome_option = Options()
    chrome_option.add_argument('--headless=new')
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_option)
    driver.get("https://www.google.com/travel/flights?gl=AU&hl=en")
    wait = WebDriverWait(driver, 20)

    print("Page loading")
    sleep(1)

    departure = date_formatter(departure)
    print("Departure date formatted:", departure)
    departure_path = f'//div[@aria-label="{departure}"]'
    if trip_type == "Round Trip":
        arrival = date_formatter(arrival)
        print("Arrival date formatted:", arrival)
        arrival_path = f'//div[@aria-label="{arrival}"]'

    # Select "One Way" option if needed
    if trip_type == "One Way":
        dropdown = driver.find_element(By.XPATH, '//div[@role="combobox" and @aria-haspopup="listbox"]')
        dropdown.click()
        ul_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@role="listbox" and @aria-label="Select your ticket type."]'))
        )
        one_way_option = ul_list.find_element(By.XPATH, '//li[@data-value="2"]')
        one_way_option.click()
        sleep(2)

    # Enter source city
    from_input = driver.find_element(By.XPATH, '//input[@aria-label="Where from? "]')
    from_input.clear()
    from_input.send_keys(f"{source}")
    sleep(1)
    first_option = driver.find_element(By.XPATH, '//li[@role="option" and @data-type="3"]')
    first_option.click()
    sleep(1)

    # Enter destination city
    from_input = driver.find_element(By.XPATH, '//input[@aria-label="Where to? "]')
    from_input.clear()
    from_input.send_keys(f"{destination}")
    sleep(1)
    first_option = driver.find_element(By.XPATH, '//li[@role="option" and @data-type="3"]')
    first_option.click()
    sleep(1)

    # Select departure date
    departure_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Departure"]')))
    departure_input.click()
    sleep(1)
    departure_date_button = wait.until(EC.element_to_be_clickable((By.XPATH, departure_path)))
    departure_date_button.click()
    sleep(1)

    # Select return date if round trip
    if trip_type == "Round Trip":
        return_date_button = wait.until(EC.element_to_be_clickable((By.XPATH, arrival_path)))
        return_date_button.click()
        sleep(1)

    # Click 'Done' after selecting dates
    done_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Done") and contains(., "Done")]')
    done_button.click()

    # Click on 'Search' button
    search_button = driver.find_element(By.XPATH, '//span[text()="Search"]/ancestor::button')
    search_button.click()
    sleep(1)

    # driver.execute_script("window.scrollBy(0, 500);")
    # sleep(3)

    # -------------------- PRICE HISTORY EXTRACTION --------------------
    try:
        if driver.find_element(By.XPATH, '//button[@aria-label="View price history"]'):
            view_price_button = driver.find_element(By.XPATH, '//button[@aria-label="View price history"]')
            driver.execute_script("window.scrollBy(0, 200);")
            view_price_button.click()
            sleep(3)
        else:
            driver.execute_script("window.scrollBy(0, 500);")
            sleep(2)
            view_price_button = driver.find_element(By.XPATH, '//button[@aria-label="View price history"]')
            view_price_button.click()
            sleep(3)

        # Locate the price history graph container
        container_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='yDmH0d']/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div[2]/div[2]"))
        )
        print("0")

        # Locate the SVG element that contains price data
        price_graph_app = container_div.find_element(By.XPATH, './/*[@series-id="Price history"]')
        print("1")

        # Find the target group element that holds aria-labels
        children = price_graph_app.find_elements(By.XPATH, './*[name()="g"]')
        g4 = None
        for g in children:
            try:
                if g.get_attribute("aria-hidden") == "true":
                    continue
                nested_g = g.find_element(By.XPATH, './/*[name()="g"][@aria-label]')
                if nested_g:
                    g4 = g
                    break
            except:
                continue

        # Extract aria-labels from nested <g> tags
        aria_labels = []
        if g4:
            print("Found target <g> element.")
            data_points = g4.find_elements(By.XPATH, './*[name()="g"]')
            for point in data_points:
                try:
                    child_g = point.find_element(By.XPATH, './*[name()="g"]')
                    aria_label = child_g.get_attribute("aria-label")
                    if aria_label:
                        aria_labels.append(aria_label)
                except:
                    continue
            print("Extracted aria-labels:")
        else:
            print("Target <g> element not found.")

        # Save price history to CSV
        with open("price_history_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["aria-label"])
            for label in aria_labels:
                writer.writerow([label])

        print("Saved", len(aria_labels), "points to price_history_data.csv")

        view_price_button = driver.find_element(By.XPATH, '//button[@aria-label="View price history"]')
        view_price_button.click()
        sleep(1)
    except Exception as e:
        print("Error extracting price history:", e)
        pass


    # -------------------- DATE GRID EXTRACTION --------------------
    
    if driver.find_element(By.XPATH, '//button[.//span[text()="Date grid"]]'):
        date_grid_button = driver.find_element(By.XPATH, '//button[.//span[text()="Date grid"]]')
        date_grid_button.click()
        sleep(3)
    else:
        driver.execute_script("window.scrollBy(0, 200);")
        sleep(2)
        date_grid_button = driver.find_element(By.XPATH, '//button[.//span[text()="Date grid"]]')
        date_grid_button.click()
        sleep(3)

    if trip_type == "Round Trip":
        # Extract round trip price matrix
        table_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "OrLtze"))
        )
        price_cells = table_container.find_elements(By.XPATH, './/div[@aria-label and @role="button"]')

        data = []
        for cell in price_cells:
            aria = cell.get_attribute("aria-label")
            if aria and "A$" in aria:
                price_part, date_range = aria.split(",", 1)
                data.append({
                    "Price": price_part.strip(),
                    "Dates": date_range.strip()
                })

        # Save to CSV
        with open("flight_price_matrix.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Price", "Dates"])
            writer.writeheader()
            writer.writerows(data)

        print(f"✅ Extracted {len(data)} entries and saved to 'flight_price_matrix.csv'")

    elif trip_type == "One Way":
        import re
        header_elements = driver.find_elements(By.XPATH, '//div[@jsname="vCVVjd"]/div[contains(@class, "qh9ymb")]/div[contains(@class, "pJYzRb")]')
        column_map = []

        # Extract header positions to align prices
        for header in header_elements:
            try:
                transform_style = header.find_element(By.XPATH, '..').get_attribute('style')
                match = re.search(r'translate3d\(([-\d.]+)px', transform_style)
                x_offset = float(match.group(1)) if match else 0.0
                spans = header.find_elements(By.TAG_NAME, "span")
                day = spans[0].text.strip()
                date = spans[1].text.strip()
                column_map.append({"x_offset": x_offset, "day": day, "date": date})
            except:
                pass

        # Extract prices and match to headers
        price_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-row][data-col].QB2Jof')
        data = []
        for price_el in price_elements:
            try:
                price_text = price_el.text.strip()
                col_style = price_el.find_element(By.XPATH, '..').get_attribute('style')
                match = re.search(r'translate3d\(([-\d.]+)px', col_style)
                x_offset_price = float(match.group(1)) if match else None
                matched_header = min(column_map, key=lambda x: abs(x['x_offset'] - x_offset_price)) if x_offset_price is not None else None
                data.append({
                    "Day": matched_header['day'] if matched_header else '',
                    "Date": matched_header['date'] if matched_header else '',
                    "Price": price_text
                })
            except Exception as e:
                print(f"Error extracting price: {e}")

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv("accurate_flight_prices.csv", index=False)

        # Avoid duplicate entries using a set
        csv_file = 'flight_prices.csv'
        import os
        existing_data = set()
        if os.path.exists(csv_file):
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = (row['Day'], row['Date'], row['Price'])
                    existing_data.add(key)

        fieldnames = ['Day', 'Date', 'Price']
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.stat(csv_file).st_size == 0:
                writer.writeheader()

            # Scroll through chart and capture new data
            for i in range(20):
                try:
                    button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[8]/div[1]/div[3]/div[1]/div/div[2]/span/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/button[2]')
                    button.click()
                    print(f"Clicked {i+1} times")
                    sleep(0.5)

                    # Re-extract headers
                    header_elements = driver.find_elements(By.XPATH, '//div[@jsname="vCVVjd"]/div[contains(@class, "qh9ymb")]/div[contains(@class, "pJYzRb")]')
                    column_map = []
                    for header in header_elements:
                        try:
                            transform_style = header.find_element(By.XPATH, '..').get_attribute('style')
                            match = re.search(r'translate3d\(([-\d.]+)px', transform_style)
                            x_offset = float(match.group(1)) if match else 0.0
                            spans = header.find_elements(By.TAG_NAME, "span")
                            day = spans[0].text.strip()
                            date = spans[1].text.strip()
                            column_map.append({"x_offset": x_offset, "day": day, "date": date})
                        except:
                            pass

                    # Re-extract prices
                    price_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-row][data-col].QB2Jof')
                    for price_el in price_elements:
                        try:
                            price_text = price_el.text.strip()
                            col_style = price_el.find_element(By.XPATH, '..').get_attribute('style')
                            match = re.search(r'translate3d\(([-\d.]+)px', col_style)
                            x_offset_price = float(match.group(1)) if match else None
                            matched_header = min(column_map, key=lambda x: abs(x['x_offset'] - x_offset_price)) if x_offset_price else None
                            new_row = {
                                "Day": matched_header['day'] if matched_header else '',
                                "Date": matched_header['date'] if matched_header else '',
                                "Price": price_text
                            }
                            key = (new_row["Day"], new_row["Date"], new_row["Price"])
                            if key not in existing_data:
                                writer.writerow(new_row)
                                existing_data.add(key)
                        except Exception as e:
                            print(f"Error extracting price: {e}")

                except Exception as e:
                    print(f"Error on click {i+1}: {e}")
                    break

        print("✅ accurate_flight_prices.csv saved.")

    # Final cleanup
    ok_button = driver.find_element(By.XPATH, '//button[.//span[text()="OK"]]')
    ok_button.click()
    sleep(1)
    current_url = driver.current_url
    driver.quit()
    
    return current_url
