import requests
from deep_translator import GoogleTranslator

API_KEY = '3f807ffa26e6475cb0e27a17a745cf8a'
BASE_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_URL = 'https://api.spoonacular.com/recipes/{id}/information'

def search_recipes(query):
    response = requests.get(BASE_URL, params={
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
    })
    return response.json().get('results', [])

def get_recipe_details(recipe_id):
    response = requests.get(RECIPE_URL.format(id=recipe_id), params={
        'apiKey': API_KEY,
        'includeNutrition': False,
    })
    return response.json()

def get_suggested_recipes():
    response = requests.get(BASE_URL, params={
        'apiKey': API_KEY,
        'sort': 'popularity',
        'number': 5,
        'instructionsRequired': True,
        'addRecipeInformation': True,
    })
    return response.json().get('results', [])

def translate_text(text, target_language='es'):
    return GoogleTranslator(source='auto', target=target_language).translate(text)

def main():
    recipes = []
    while True:
        print('\n1. Buscar Recetas')
        print('2. Ver detalles de la receta')
        print('3. Ver platos sugeridos')
        print('4. Salir')
        choice = input('\nSeleccione una opción: ')

        if choice == '1':
            query = input('\nIngrese el nombre del plato: ')
            recipes = search_recipes(query)
            print('\nResultados de la búsqueda:')
            for idx, recipe in enumerate(recipes, start=1):
                title = translate_text(recipe.get('title', 'Sin título'))
                print(f'{idx}. {title} (ID: {recipe["id"]})')

        elif choice == '2':
            if recipes:
                selected_recipe_idx = int(input('\nIngrese el número de la receta que desea ver los detalles: ')) - 1
                selected_recipe_id = recipes[selected_recipe_idx]['id']
                recipe = get_recipe_details(selected_recipe_id)
                title = translate_text(recipe.get('title', 'Sin título'))
                print(f'\n Título: {title}')
                print('Ingredientes:')
                for ingredient in recipe.get('extendedIngredients', []):
                    print(f' - {translate_text(ingredient.get("original", ""))}')
                instructions = translate_text(recipe.get('instructions', 'No hay instrucciones disponibles'))
                print(f'Instrucciones: {instructions}')
                print(f'Fuente: {recipe.get("sourceUrl", "No disponible")}')
            else:
                print('\nPrimero debe buscar recetas ingresando la opción 1')

        elif choice == '3':
            suggested_recipes = get_suggested_recipes()
            print('\nPlatos sugeridos:')
            for idx, recipe in enumerate(suggested_recipes, start=1):
                title = translate_text(recipe.get('title', 'Sin título'))
                print(f'{idx}. {title} (ID: {recipe["id"]})')

        elif choice == '4':
            break

if __name__ == '__main__':
    main()
