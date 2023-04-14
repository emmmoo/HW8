# Your name: Emma Moore
# Your student id: 52906502
# Your email: emmmoo@umich.edu
# List who you have worked with on this homework: Sibora Berisha and Max Meston 

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    #set up and connect
    """path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    #Retrieve data from the database by joining the dictionary with the foreign keys 
    cur.execute('''SELECT restaurants.name, categories.category, buildings.building, restaurants.rating 
                 FROM restaurants 
                 INNER JOIN categories ON restaurants.category_id = categories.id 
                 INNER JOIN buildings ON restaurants.building_id = buildings.id''')
    data = cur.fetchall()
    # Create the nested dictionary with the info in data
    restaurant_dict = {}
    for row in data:
        name = data[0]
        category = data[1]
        building = data[2]
        rating = data[3]
        if name not in restaurant_dict:
            restaurant_dict[name] = {'category': category, 'building': building, 'rating': rating}
        else:
            restaurant_dict[name]['category'] = category
            restaurant_dict[name]['building'] = building
            restaurant_dict[name]['rating'] = rating
    #Close the database connection
    conn.close()
    #return the nested dict 
    #print(restaurant_dict)
    return restaurant_dict"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    #create empty dict to store info 
    restaurants= {}
    #iterate through the query 
    #print(cursor.fetchall())
    for row in cursor.fetchall(): 
        #get name, category, building, and rating 
        name = row[1]
        cat_id = row[2]
        build_id = row[3]
        rating = row[4]
        #if restaurant not in dict, add it and empty dict as value 
        if name not in restaurants: 
            restaurants[name] = {}
        #get correct catrgoey type 
        cursor.execute("SELECT category FROM categories WHERE id = ?", (cat_id,))
        cat_name = cursor.fetchone()[0]
        #do the same for building 
        cursor.execute("SELECT building FROM buildings WHERE id = ?", (build_id,))
        build_name = cursor.fetchone()[0]

        #add the cat, building, and rating info to the nested dct 
        restaurants[name]["category"] = cat_name 
        restaurants[name]["building"] = build_name 
        restaurants[name]["rating"] = rating 
    conn.close() 
    print(restaurants)
    return restaurants

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    #select the cat name and count the # of restaurants in each cat
    cursor.execute("SELECT categories.category, COUNT(restaurants.category_id) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category")
    #create empty dict to store the counts for each category 
    cat_counts = {}

    #iterate through the rows of the query: 
    for row in cursor.fetchall(): 
        #get cat name and count for each row
        category_name = row[0]
        count = row[1]
        #add the cat name and count to the dct 
        cat_counts[category_name] = count 
    conn.close()
    #sort the dct 
    cat_counts = dict(sorted(cat_counts.items(), key = lambda item: item[1], reverse = False))
    #create the bar chart 
    max_ct = max(cat_counts.values())
    plt.barh(range(len(cat_counts)), list(cat_counts.values()), align = "center")
    plt.yticks(range(len(cat_counts)), list(cat_counts.keys()))
    plt.xticks(range(0, max_ct+1, 1))
    plt.ylabel("Restaurant Category")
    plt.xlabel("Number of Restaurants")
    plt.title("Restaurants on South U")
    plt.show()
    print(cat_counts)
    return cat_counts


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    c = conn.cursor()
    # Retrieve the list of restaurant names in the specified building, sorted by rating
    c.execute('''SELECT restaurants.name FROM restaurants 
                 INNER JOIN buildings ON restaurants.building_id = buildings.id 
                 WHERE buildings.building = ? 
                 ORDER BY restaurants.rating DESC''', (building_num,))
    restaurant_names = [row[0] for row in c.fetchall()]
    # Close the database connection
    conn.close()
    return restaurant_names

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass
class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
