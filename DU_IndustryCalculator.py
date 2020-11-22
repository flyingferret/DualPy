import math
import json

class Recipe:
    def __init__(self,name,init_data):
        self.name = name
        self.tier = init_data["tier"]
        self.type = init_data["type"]
        self.mass = init_data["mass"]
        self.volume = init_data["volume"]
        self.skill = init_data["skill"]
        self.industries = init_data["industries"]
        self.outputQuantity = init_data["outputQuantity"]

        self.raw_input = init_data["input"]
        self.raw_byproducts = init_data["byproducts"]

    #helper function finds object by name in recipes library
    def find_recipe(self,name,library):
        for r in library:
            if r.name == name:
                return r

    #populate input and outputs with objects from recipes library once initalised
    def populate(self,library):
        self.input = {}
        self.byproducts = {}
        for i in self.raw_input:
           self.input.update({self.find_recipe(i,library):self.raw_input[i]})
        for i in self.raw_byproducts:
           self.byproducts.update({self.find_recipe(i,library):self.raw_byproducts[i]})

    #return actual numbers per unit
    def requirements(self,quantity=0):
        if quantity == 0: quantity=self.outputQuantity
        requirements = {}
        for i in self.input:
            amount = self.input[i]*quantity/self.outputQuantity
            batchs = math.ceil(amount/i.outputQuantity)
            requirements.update({ i:{"amount":amount,"batchs":batchs}})
            sub_req = i.requirements(self.input[i]*quantity)
            for sr in sub_req:
                if sr in requirements:
                    requirements[sr]["amount"] = requirements[sr]["amount"] + sub_req[sr]["amount"]
                    requirements[sr]["batchs"] = requirements[sr]["batchs"] + sub_req[sr]["batchs"]
                else:
                    requirements.update({sr:sub_req[sr]})
        return requirements

    def crafting_que(self,quantity=0):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return  self.name

class RecipeLibrary:
    def __init__(self, recipes_json_file):
        res_file = open(recipes_json_file)
        recipes_json = json.load(res_file)
        self.recipes = []

        for key in recipes_json:
            self.recipes.append(Recipe(key, recipes_json[key]))

        for r in self.recipes:
            r.populate(self.recipes)
    #returns list of recipe by give item_name, searchType: 0 = Exact,1 = Contains
    def find_recipe_by_name(self,item_name,searchType=0):
        result = []
        for r in self.recipes:
            if searchType == 0:
                if r.name == item_name:
                    result.append(r)
            if searchType == 1:
                if r.name.lower().find(item_name.lower()) > -1:
                    result.append(r)
        return result

industy_types = {
 'ore',
 'Recycler M',
 'Refiner M',
 'Chemical Industry M',
 'Smelter M',
 '3D Printer M',
 'Glass Furnace M',
 'Electronics Industry M',
 'Metalwork Industry M',
 'Honeycomb Refinery M',
 'Assembly Line XS',
 'Assembly Line S',
 'Assembly Line S',
 'Assembly Line M',
 'Assembly Line L',
 'Assembly Line XL'
 }

##Testing area
library = RecipeLibrary("recipes.json")

while True:
    item_name = input("Name of item: ")

    results = library.find_recipe_by_name(item_name,1)
    i=0
    print("Select Item from search result")
    if results != None:
        for r in results:
            i = i+1
            print("{}. {}".format(i,r.name))
    else:
        print("Error item not found")

    choice = int(input("Select # :"))
    recipe = results[choice-1]
    quantity = int(input("Number of items: "))
    print(recipe.requirements())


