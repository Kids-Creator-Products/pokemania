def button_search_click(self, **event_args):
  name = self.text_box_search.text
  pokemon = anvil.server.call('get_pokemon_details', name)

  if pokemon:
    # Show the full API URL
    self.label_url.text = pokemon['api_url']

    # Display the sprite and name
    self.image_pokemon.source = pokemon['image']
    self.label_info.text = f"Name: {pokemon['name']}\nTypes: {', '.join(pokemon['types'])}"

    # Display the full list of attacks (moves)
    self.text_area_moves.text = "\n".join(pokemon['attacks'])
  else:
    self.label_info.text = "Error: Pokémon not found."
