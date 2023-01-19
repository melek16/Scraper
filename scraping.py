from selenium import webdriver
from selenium.webdriver.common.by import By
PATH='C:\Program Files (x86)\chromedriver_win32\chromedriver.exe'
driver=webdriver.Chrome(PATH)

driver.get('https://www.edmunds.com/audi/e-tron/')

#collect car model
carModel=driver.find_element(By.CSS_SELECTOR,'.intro-title.heading-2.mt-0_5.mb-0.m-lg-0').text

#collect price range
priceRange=driver.find_element(By.CLASS_NAME,'d-inline-block').text.split('\n')[0]
#collectin expert ratings and putting them in a dictionary expertR
expertRatingCriteria=[el.text for el in driver.find_elements(By.CSS_SELECTOR,".heading-5.text-primary-darker.mb-0.mr-1")]
expertRatings=[el.text for el in driver.find_elements(By.CSS_SELECTOR,".heading-3.text-primary-darker")]
expertR=dict(zip(expertRatingCriteria,expertRatings))


#going to the specs page
clickable = driver.find_element(By.LINK_TEXT,"See all features & specs")
clickable.click()


#collecting specs and making specDict dictionary 
categories=[]
specList=[]
tables=driver.find_elements(By.CSS_SELECTOR,"table.table-striped-custom.text-gray-darker.mb-0")
for table in tables:
    #get category of specs
    category=table.find_element(By.TAG_NAME,'caption').text
    categories.append(category)
    #get specs
    specKeys=[el.text for el in table.find_elements(By.XPATH,'.//th[@class="p-0_5"]')]
    specVals=[el.text.split('\n') for el in table.find_elements(By.XPATH,'.//td[@class="px-1 px-lg-0_75 px-xl-1 py-0_5"]')]
    for i in range(len(specVals)):
        if len(specVals[i])==1 :
            specVals[i]=specVals[i][0]
    specs=dict(zip(specKeys,specVals))
    specList.append(specs)
specDict=dict(zip(categories,specList))



#go back to previous page
driver.back()

#collect pros and cons
#mainDiv has pros, cons and What's new (to be deleted)
try:
    mainDiv=driver.find_element(By.CSS_SELECTOR,".editorial-highlights-lists.text-gray-darker.mb-1_5.mb-md-2.mt-2")
    l=[el.text for el in mainDiv.find_elements(By.TAG_NAME,'h3')]
    s=[el.text for el in mainDiv.find_elements(By.TAG_NAME,'ul')]
    del l[-1]
    del s[-1]
    prosAndCons=dict(zip(l,[i.split('\n') for i in s]))
except:
    prosAndCons={'Pros':[],'Cons':[]}

#collect average Rating
try:
    averageRating=driver.find_element(By.CLASS_NAME,"average-user-rating").text.split('\n')[0]
except:
    averageRating=None

#collect rating percentages 
ratings=[]
percentages=[]
try:
    mainDiv2=driver.find_element(By.CLASS_NAME,'summary-ratings')
    childDivs=mainDiv2.find_elements(By.TAG_NAME,'div')
    for childDiv in childDivs:
        ratings.append(childDiv.text.split('\n')[0])
        percentages.append(childDiv.find_element(By.CSS_SELECTOR,".summary-percent.text-right").text[1:-1])
    ratingPercentages={'ratings':dict(zip(ratings,percentages))}
except:
    ratingPercentages={'ratings':None}



#merge all data into one dictionary
modelData={'Car model':carModel, 'MSRP range':priceRange} |expertR | specDict | prosAndCons | {'averageRating':averageRating} |ratingPercentages
print(modelData)

driver.quit()