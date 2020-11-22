import math
import json
byProducts = ['Hydrogen Pure', 'Oxygen Pure']
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
        self.time = init_data["time"]
        self.raw_input = init_data["input"]
        self.raw_byproducts = init_data["byproducts"]

    #helper function finds object by name in recipes library
    def find_recipe(self,name,library):
        for r in library:
            if r.name == name:
                return r

    #populate input and outputs with objects from recipes library once initalised
    def populate(self,library):
        self.input = []
        self.byproducts = {}
        for i in self.raw_input:
            r = self.find_recipe(i,library)
            quantity = self.raw_input[i]
            self.input.append(CraftingRequirment(r,quantity))
        for i in self.raw_byproducts:
           self.byproducts.update({self.find_recipe(i,library):self.raw_byproducts[i]})

    #return actual numbers per unit
    def requirements(self,quantity=0):
        if quantity == 0: quantity=self.outputQuantity
        craftingRequirments = []
        # craftingRequirments.append(CraftingRequirment(self,quantity))

        for i in self.input:
            craftingRequirments.append(CraftingRequirment(i.recipe,i.quantity*quantity))
            sub_req = i.recipe.requirements(i.quantity*quantity/i.recipe.outputQuantity)
            for r in sub_req:
                #if not already in craftreq add it
                found = False
                for c in craftingRequirments:
                    if c.recipe.name == r.recipe.name:
                        c.increaseQuanity(r.quantity)
                        found = True
                if not found :
                    craftingRequirments.append(r)
        return craftingRequirments

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

class CraftingRequirment:
    def __init__(self, recipe,quantity=0):
        self.recipe = recipe
        self.quantity = 0
        self.time = 0
        self.batchs = 0
        self.increaseQuanity(quantity)

    def increaseQuanity(self,quantity):
        if(self.recipe.name not in byProducts):
            self.quantity = self.quantity + quantity
            self.batchs = math.ceil(self.quantity / self.recipe.outputQuantity)
            self.time = self.recipe.time * self.batchs

    def __str__(self):
        return self.recipe.name

    def __repr__(self):
        return  self.recipe.name


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
if __name__ == "__main__":
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

        requirements = recipe.requirements(quantity)
        totalTime = 0
        for req in requirements:
            totalTime = totalTime + req.time
            print("{} Amount: {:.0f} # Batches: {} Time: {:.0f}".format(req.recipe.name,req.quantity,req.batchs,req.time))
        print("Total Time: {:.0f} sec".format(totalTime))


