from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)





# Get a comma-separated list of ingredients from the user
ingredient_input = input("Enter a comma-separated list of ingredients: ")

# Split the input string into a list of ingredients
ingredients = ingredient_input.split(',')

# Remove leading and trailing whitespaces from each ingredient
ingredients = [ingredient.strip() for ingredient in ingredients]
# print(ingredients)


recipe_details=[]

def recipe():

    global search_box

    driver.get("https://realfood.tesco.com/what-can-i-make-with.html")

    try:

        # print("in try block")

        elements = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'autocomplete-B ')))


        search_box = driver.find_elements(By.XPATH, '//*[@id="ddl-recipe-finder"]/main/div[1]/div[1]/form')
        # print(search_box)





    except:
        print("Cannot load data")



    # print("above for")

    for i in range(0,len(ingredients)):
        for item in search_box:
            search = item.find_element(By.TAG_NAME,'input')
            # print(search)
            search.click()
            search.send_keys(ingredients[i])
            search.send_keys(Keys.RETURN)
            time.sleep(1)


    dishes = driver.find_elements(By.CLASS_NAME,'ddl-recipe-finder__list-item')
    # print(dishes)

    for dish in dishes:
        title = dish.find_element(By.CLASS_NAME,'ddl-recipe-card__title-text').text
        # print(title)
        link = dish.find_element(By.CLASS_NAME,'ddl-recipe-card').get_attribute("href")
        # print(link)
        img = dish.find_element(By.TAG_NAME,'img').get_attribute("src")
        # print(img)
        recipee = [title,link,img]
        recipe_details.append(recipee)

    driver.close()

    return recipe_details





def main():

    recipe_list = recipe()


    for i in range(0,10):
        print(i+1,end=" ")
        print(recipe_list[i][0])

    ch= int(input("Enter your Choice: "))

    for i in range(0,11):
        if i == ch:
            print(recipe_details[i-1])


if __name__ == "__main__":
    main()
