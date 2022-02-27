import pygame
from PIL import Image
import time
import pandas as pd
import re
import math
import checks


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original)
    scaled_height = int(image_height_original)
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# Keyword-based Search Function - to be implemented
def find_and_group_matches(keywords):
    # Note: AND has precedence over OR. Refer to README.md, for explanation on concept of and_groups.
    or_groups = keywords.strip().lower().split(' or ')  # ['...', '...']
    and_groups = [re.split(' and | ', g) for g in or_groups]  # [[...], [...]]
    and_group_match_count = {}
    for i in range(1, len(or_groups) + 1):
        and_group_match_count[i] = []

    total_matches = 0

    for canteen in canteen_stall_keywords:
        for stall in canteen_stall_keywords[canteen]:
            no_of_and_group_matches = 0
            for and_group in and_groups:
                match_all_and_keywords = True
                for keyword in and_group:
                    if keyword not in canteen_stall_keywords[canteen][stall].lower().split(', '):
                        match_all_and_keywords = False
                if match_all_and_keywords:
                    no_of_and_group_matches += 1
            if no_of_and_group_matches >= 1:
                and_group_match_count[no_of_and_group_matches].append(canteen + ' - ' + stall)
                total_matches += 1

    return and_group_match_count, total_matches


def search_by_keyword(keywords):
    and_group_match_count, total_matches = find_and_group_matches(keywords)

    if total_matches == 0:
        print(f'Food Stalls found: No food stall found with input keyword.')
    else:
        print(f'Food stalls found: {total_matches}')

    if len(and_group_match_count) > 1:
        # Print from the highest match to 1 match
        for i in range(len(and_group_match_count.keys()), 0, -1):
            print(f'Food stalls that match {i} keyword:')
            for stall in and_group_match_count[i]:
                print(stall)
    else:
        for stall in and_group_match_count[1]:
            print(stall)
    # print(and_group_match_count)


# Price-based Search Function - to be implemented
def search_by_price(keywords, max_price):
    stall_min_price = ''
    stalls_within_range = []

    and_group_match_count, total_matches = find_and_group_matches(keywords)
    if total_matches == 0:
        return print(f'Food Stalls found: No food stall found with input keyword.')

    for count in and_group_match_count:
        for canteen_stall in and_group_match_count[count]:
            canteen, stall = canteen_stall.split(' - ')
            price = canteen_stall_prices[canteen][stall]
            if price <= max_price:
                stalls_within_range.append(canteen_stall + ' - S$' + str(price))
            if stall_min_price == '' or price < float(stall_min_price.split('S$')[1]):
                stall_min_price = canteen_stall + ' - S$' + str(price)

    if len(stalls_within_range) == 0:
        print('Food Stalls found: No food stall found with specified price range.')
        print('Recommended Food Stall with the closest price range.')
        print(stall_min_price)
    else:
        print(f'Food Stalls found: {len(stalls_within_range)}')
        for stall in stalls_within_range:
            print(stall)


# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):
    canteen_dist = []
    for canteen in canteen_locations:
        distA = math.sqrt((canteen_locations[canteen][0] - user_locations[0][0])**2
                          + (canteen_locations[canteen][1] - user_locations[0][1])**2)
        distB = math.sqrt((canteen_locations[canteen][0] - user_locations[1][0])**2
                          + (canteen_locations[canteen][1] - user_locations[1][1])**2)
        ave_dist = int((distA + distB)/2)
        canteen_dist.append([canteen, ave_dist])

    # sort by distance of each canteen (2nd item of inner list)
    canteen_dist.sort(key=lambda x: x[1])
    print(f'{k} Nearest Canteen found: ')
    for i in range(k):
        print(f'{canteen_dist[i][0]} - {canteen_dist[i][1]}m')


# Any additional function to assist search criteria

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            keywords = input("Enter type of food: ")
            search_by_keyword(keywords)

        elif option == 3:
            # price-based search
            keywords = input("Enter type of food: ")
            max_price = checks.get_max_price("Enter maximum meal price (S$): ")
            search_by_price(keywords, max_price)

        elif option == 4:
            # location-based search

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)
            k = checks.get_k("Number of canteens: ")

            user_locations = [userA_location, userB_location]
            # call location-based search function
            search_nearest_canteens(user_locations, k)

        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
