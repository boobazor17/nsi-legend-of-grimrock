import pygame
import math
import equipe
pygame.init()
height= 720
width = 1080

def dessiner_vision(screen, follow, player, rayon=200):
    masque = pygame.Surface((width, height), pygame.SRCALPHA)
    masque.fill((0, 0, 0, 100))
    pos_joueur = follow.appliquer(player.position)
    pygame.draw.circle(masque, (0, 0, 0, 0), pos_joueur, 300)
    screen.blit(masque, (0, 0))

def fade_out(screen,dessiner_scene_callback=None):
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))

    # fade out
    for alpha in range(0, 256, 4):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(20) 

def fade_in(screen, dessiner_scene_callback=None):
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))

    for alpha in range(255, -1, -4):
        if dessiner_scene_callback:
            dessiner_scene_callback()

        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)


def vide(screen, joueur_dans_vide, player, follow, map_manager, cam, temps_entree_vide, dessiner_scene_callback=None):
    if joueur_dans_vide:
        if temps_entree_vide is None:
            temps_entree_vide = pygame.time.get_ticks()

        if pygame.time.get_ticks() - temps_entree_vide > 100:
            fade_out(screen, dessiner_scene_callback)


            player.position = map_manager.spawnpoint_joueur.copy()
            player.rect.center = player.position

            cam.offset_float.x = player.rect.x + cam.CONST.x
            cam.offset_float.y = player.rect.y + cam.CONST.y
            cam.offset.x = int(cam.offset_float.x)
            cam.offset.y = int(cam.offset_float.y)

            fade_in(screen, dessiner_scene_callback)

            temps_entree_vide = None
    else:
        temps_entree_vide = None
    return temps_entree_vide

def dessiner_scene(screen, map_manager, follow, player, vases, mon_coffre,
                   liste_portes, liste_items_au_sol, list_ennemi,
                   rayon_vision, paused, inventory, liste_equipe):

    screen.fill((201, 158, 89))
    map_manager.draw(screen, follow)

    for vase in vases:
        screen.blit(vase.image, follow.appliquer(vase.position))

    if mon_coffre:
        screen.blit(mon_coffre.image, follow.appliquer(mon_coffre.position))

    for porte in liste_portes:
        if not porte.ouvert:
            screen.blit(porte.image, follow.appliquer(porte.position))

        if type(porte).__name__ == "Porte_plaque":
            image_plaque = porte.dessiner_plaque(screen, follow)
            screen.blit(
                image_plaque,
                follow.appliquer(pygame.math.Vector2(porte.rect_plaque.x, porte.rect_plaque.y))
            )

    for item in liste_items_au_sol:
        screen.blit(item.image, follow.appliquer(item.position))

    player.draw(screen, follow)

    for monstree in list_ennemi:
        dx = monstree.position.x - player.position.x
        dy = monstree.position.y - player.position.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance <= rayon_vision:
            monstree.draw(screen, follow, player)

    if not paused and player.pv > 0 and not inventory:
        equipe.afficher_equipe(liste_equipe, screen)
        equipe.afficher_pv(liste_equipe, screen)

    if not inventory and not paused:
        dessiner_vision(screen, follow, player, rayon_vision)
