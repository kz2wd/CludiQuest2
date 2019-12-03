from Modules import menu
from Lore import biomes
from GameCore import all_kit


def choose_game_mode(authorized_ids, channel):
    return menu.BetterMenu(["Simple", "Hardcore", "Aventure libre"],
                           authorized_ids, channel, title="*Options de la partie*")


# when game enter state 3
def choose_kit(authorized_ids, channel):
    kit_handler = all_kit.KitHandler()
    return menu.BetterMenu([kit.name for kit in kit_handler.kits], authorized_ids, channel,
                           title="*Choisissez votre classe*")


def choose_start_biome(authorized_ids, channel):
    return menu.BetterMenu(biomes.start_zones, authorized_ids, channel, title="*Choisissez votre zone de départ*")


