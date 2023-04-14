# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

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
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    #extract the info from database and make queries 
    cur.execute("SELECT name, rating, category_id, building_id FROM restaurants")
    tableinfo = cur.fetchall()
    cur = conn.cursor()
    #get category info
    cur.execute("SELECT category, id FROM categories")
    cat_info = cur.fetchall()
    #get building info 
    cur.execute("SELECT building, id FROM buildings")
    build_info = cur.fetchall()
    #commit
    conn.commit()
    #create the dictionary 
    restaurant_lst = []
    res_dct = {}
    for tuple in tableinfo: 
        name = tuple[0]
        cat_id = tuple[2]
        building_id = tuple[3]
        rating = tuple[1]
        category = None 
        building = None
    #get the right category for each restaurant 
    for cats in cat_info: 
        #get category type by comparing cat ids
        if cats[1] == cat_id: 
            category = cats[0]
    #get the right building for each restaurant 
    for buildings in build_info: 
        #get category type by comparing cat ids
        if buildings[1] == building_id: 
            building = buildings[0]
    #create the nested dict with the info 
        #for tuple in range(tableinfo):
    for name in tableinfo[0]:
        res_dct[name] = {"category": category, "building": building, "rating": rating}
    print(res_dct)
    return res_dct
def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    # Execute a SQL query to count number in each category
    cur.execute("""
        SELECT category_type, COUNT(restaurant_id)
        FROM category 
        JOIN restaurant  ON category_id = category_id
        GROUP BY category_type
    """)
    # Fetch the results of the query as a list of tuples
    results = cur.fetchall()
    # Create a dictionary to store the count of restaurants in each category
    count_by_category = {}
    for row in results:
        count_by_category[row[0]] = row[1]
    conn.close()
    # Create a bar chart with the restaurant categories and the count of restaurants in each category
    fig, ax = plt.subplots()
    ax.bar(count_by_category.keys(), count_by_category.values())
    ax.set_xlabel('Category')
    ax.set_ylabel('Count')
    ax.set_title('Restaurant Count by Category')
    plt.show()
    # Return the dictionary with the count of restaurants in each category
    return count_by_category
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
