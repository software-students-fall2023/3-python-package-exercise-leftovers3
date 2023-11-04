# petmagotchi/__main__.py
from pet import Pet

def main():
    # Create a pet instance
    my_pet = Pet(name='Fido', type='Dog')

    # Display pet status
    my_pet.print_status()

    # Feed the pet
    my_pet.feed_pet(food='meat', quantity=2)
    my_pet.print_status()

    # Play with the pet
    my_pet.play(toy='ball')
    my_pet.print_status()

    #Hydrate pet
    my_pet.hydrate_pet(drink='lemonade', quantity=3)
    my_pet.print_status()

    #See pet
    my_pet.see_pet()

    #Wash pet
    my_pet.wash()
    my_pet.print_status()

    #Pet pet
    my_pet.pet()
    my_pet.print_status()

    

if __name__ == '__main__':
    main()
