import os
import requests
from PIL import Image
from io import BytesIO

# Create 'Output' directory if it doesn't exist
if not os.path.exists('Output'):
    os.makedirs('Output')

# Function to fetch card data from YuGiOhProdeck API
def fetch_card_data(card_name):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name.replace(' ', '+')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data:
            return data['data']
    return None

# Function to resize image to 114x94 using Bilinear scaling
def resize_image(image, size):
    return image.resize(size, Image.BILINEAR)

while True:
    # Card name to search for, taken as input from the user
    card_name = input("Enter the name of the card (or 'quit' to stop): ")
    
    if card_name.lower() == 'quit':
        break

    # Fetch card data from the API
    card_data = fetch_card_data(card_name)

    if card_data:
        # Get the card image URL
        image_url = card_data[0]['card_images'][0]['image_url']
        response = requests.get(image_url)

        # Open the image and crop it to the desired region (49,111) - (371,433)
        img = Image.open(BytesIO(response.content))
        img = img.crop((49, 111, 371, 433))

        # Save the cropped image
        img.save(f'Output/{card_name}_art.jpg')
        print(f"The card art of '{card_name}' has been saved in the Output folder.")

        # Shrink down the cropped image to 114x94 using Bilinear scaling
        resized_img = resize_image(img, (114, 94))
        resized_img.save(f'Output/{card_name}_shrunken.jpg')
        print(f"The shrunken image of '{card_name}' has been saved in the Output folder.")

        # Print card details
        card = card_data[0]
        print(f"Name: {card.get('name')}")
        print(f"Type: {card.get('type')}")
        print(f"Attribute: {card.get('attribute')}")
        print(f"Race (Typing): {card.get('race')}")
        print(f"Level/Rank: {card.get('level')}")
        print(f"ATK: {card.get('atk')}")
        print(f"DEF: {card.get('def')}")
        print(f"Archetype: {card.get('archetype')}")
        print(f"Card Text: {card.get('desc')}")
    else:
        print(f"No card found for '{card_name}'.")
