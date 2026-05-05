import pygame
import json
import os

pygame.init()

FICHIER_SAUVEGARDE = "sauvegardes.json"
NB_SLOTS = 3


def _charger_json():
    if os.path.exists(FICHIER_SAUVEGARDE):
        with open(FICHIER_SAUVEGARDE, "r") as f:
            return json.load(f)
    return {}


def _ecrire_json(data):
    with open(FICHIER_SAUVEGARDE, "w") as f:
        json.dump(data, f, indent=2)


def sauvegarder(slot, player, liste_equipe, mon_inventaire, joueur_or):
    data = _charger_json()

    equipe_data = []
    for perso in liste_equipe:
        equipe_data.append({
            "nom": perso.nom,
            "pv": perso.pv,
            "pvmax": perso.pvmax,
            "mana": perso.mana,
            "manamax": perso.manamax,
        })

    items_data = []
    for it in mon_inventaire.items:
        chemin_image = ""
        for attr in ("image_path", "chemin", "path", "nom_image"):
            if hasattr(it, attr):
                chemin_image = getattr(it, attr)
                break
        if not chemin_image:
            from Boutique import CATALOGUE
            for article in CATALOGUE:
                if article["nom"] == it.nom:
                    chemin_image = article["image"]
                    break
        items_data.append({
            "nom": it.nom,
            "effet": it.effet,
            "image": chemin_image,
        })

    data[str(slot)] = {
        "joueur": {
            "x": float(player.position.x),
            "y": float(player.position.y),
            "pv": player.pv,
            "pvmax": player.pvmax,
        },
        "equipe": equipe_data,
        "inventaire": items_data,
        "or": joueur_or[0],
    }

    _ecrire_json(data)


def appliquer_chargement(save_data, player, liste_equipe, mon_inventaire, joueur_or):
    from Physique import item as PhysiqueItem
    from Boutique import CATALOGUE

    j = save_data["joueur"]
    player.position.x = j["x"]
    player.position.y = j["y"]
    player.rect.centerx = int(j["x"])
    player.rect.centery = int(j["y"])
    player.pv = j["pv"]
    player.pvmax = j["pvmax"]
    if hasattr(player, "velocity"):
        player.velocity.x = 0
        player.velocity.y = 0

    for i, perso_data in enumerate(save_data["equipe"]):
        if i < len(liste_equipe):
            liste_equipe[i].pv = perso_data["pv"]
            liste_equipe[i].pvmax = perso_data["pvmax"]
            liste_equipe[i].mana = perso_data["mana"]
            liste_equipe[i].manamax = perso_data["manamax"]

    mon_inventaire.items.clear()
    catalogue_par_nom = {a["nom"]: a for a in CATALOGUE}
    for it_data in save_data["inventaire"]:
        nom = it_data["nom"]
        effet = it_data["effet"]
        article = catalogue_par_nom.get(nom)
        chemin_image = article["image"] if article else (it_data.get("image") or "assets/potion_vie.png")
        mon_inventaire.ajouter(PhysiqueItem(nom, 50, 50, effet, (255, 200, 50), chemin_image))

    joueur_or[0] = save_data["or"]


def _popup_confirmation(screen, ligne1, ligne2=""):
    width, height = screen.get_size()
    font_msg = pygame.font.Font(None, 36)
    font_btn = pygame.font.Font(None, 38)

    pw, ph = 460, 180
    px = width // 2 - pw // 2
    py = height // 2 - ph // 2
    rect_oui = pygame.Rect(px + 60, py + ph - 60, 130, 42)
    rect_non = pygame.Rect(px + 270, py + ph - 60, 130, 42)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (35, 25, 8), (px, py, pw, ph), border_radius=10)
        pygame.draw.rect(screen, (200, 160, 80), (px, py, pw, ph), 2, border_radius=10)

        txt1 = font_msg.render(ligne1, True, (255, 230, 150))
        screen.blit(txt1, (px + pw // 2 - txt1.get_width() // 2, py + 22))
        if ligne2:
            txt2 = font_msg.render(ligne2, True, (200, 180, 120))
            screen.blit(txt2, (px + pw // 2 - txt2.get_width() // 2, py + 58))

        survol_oui = rect_oui.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (70, 150, 70) if survol_oui else (50, 110, 50), rect_oui, border_radius=7)
        pygame.draw.rect(screen, (120, 200, 120), rect_oui, 2, border_radius=7)
        t_oui = font_btn.render("Oui", True, (255, 255, 255))
        screen.blit(t_oui, (rect_oui.centerx - t_oui.get_width() // 2, rect_oui.centery - t_oui.get_height() // 2))

        survol_non = rect_non.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (150, 60, 60) if survol_non else (110, 40, 40), rect_non, border_radius=7)
        pygame.draw.rect(screen, (200, 100, 100), rect_non, 2, border_radius=7)
        t_non = font_btn.render("Non", True, (255, 255, 255))
        screen.blit(t_non, (rect_non.centerx - t_non.get_width() // 2, rect_non.centery - t_non.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_oui.collidepoint(event.pos):
                    return True
                if rect_non.collidepoint(event.pos):
                    return False


def _dessiner_slot(screen, font, sx, sy, sw, sh, i, save):
    rect = pygame.Rect(sx, sy, sw, sh)
    survol = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, (90, 75, 30) if survol else (60, 50, 20), rect, border_radius=10)
    pygame.draw.rect(screen, (200, 160, 80), rect, 2, border_radius=10)

    txt_slot = font.render(f"Slot {i + 1}", True, (255, 215, 0))
    screen.blit(txt_slot, (sx + 16, sy + 12))

    if save:
        equipe = save.get("equipe", [])
        pv_total = sum(e["pv"] for e in equipe)
        pv_max = sum(e["pvmax"] for e in equipe)
        or_ = save.get("or", 0)
        nb_items = len(save.get("inventaire", []))
        line1 = font.render(f"PV equipe : {pv_total}/{pv_max}   Or : {or_}   Items : {nb_items}", True, (220, 220, 180))
        noms = ", ".join(e["nom"] for e in equipe[:2])
        line2 = font.render(f"Equipe : {noms}...", True, (160, 160, 140))
        screen.blit(line1, (sx + 16, sy + 48))
        screen.blit(line2, (sx + 16, sy + 78))
    else:
        vide = font.render("— vide —", True, (100, 100, 100))
        screen.blit(vide, (sx + 16, sy + 55))

    return rect


def afficher_sauvegarde(screen, font):
    width, height = screen.get_size()
    font_titre = pygame.font.Font(None, 60)
    font_slot = pygame.font.Font(None, 34)
    font_retour = pygame.font.Font(None, 36)
    data_saves = _charger_json()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill((10, 10, 40))

        titre = font_titre.render("— Sauvegardes —", True, (255, 215, 0))
        screen.blit(titre, (width // 2 - titre.get_width() // 2, 50))

        rects_slots = []
        for i in range(NB_SLOTS):
            rect = _dessiner_slot(screen, font_slot, width // 2 - 280, 150 + i * 150, 560, 110, i, data_saves.get(str(i)))
            rects_slots.append(rect)

        rect_retour = pygame.Rect(width // 2 - 80, height - 80, 160, 45)
        survol_retour = rect_retour.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (120, 50, 50) if survol_retour else (80, 30, 30), rect_retour, border_radius=8)
        pygame.draw.rect(screen, (180, 80, 80), rect_retour, 2, border_radius=8)
        txt_retour = font_retour.render("Retour", True, (255, 255, 255))
        screen.blit(txt_retour, (rect_retour.centerx - txt_retour.get_width() // 2,
                                  rect_retour.centery - txt_retour.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_retour.collidepoint(event.pos):
                    return "menu"
                for i, rect in enumerate(rects_slots):
                    if rect.collidepoint(event.pos):
                        save = data_saves.get(str(i))
                        if save:
                            return ("charger", i, save)


def afficher_sauvegarde_ingame(screen, font, player, liste_equipe, mon_inventaire, joueur_or):
    width, height = screen.get_size()
    font_titre = pygame.font.Font(None, 50)
    font_slot = pygame.font.Font(None, 32)
    data_saves = _charger_json()
    message = ""
    msg_timer = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pw, ph = 520, 380
        px = width // 2 - pw // 2
        py = height // 2 - ph // 2
        pygame.draw.rect(screen, (40, 30, 10), (px, py, pw, ph), border_radius=12)
        pygame.draw.rect(screen, (200, 160, 80), (px, py, pw, ph), 3, border_radius=12)

        titre = font_titre.render("Sauvegarder dans…", True, (255, 215, 0))
        screen.blit(titre, (px + pw // 2 - titre.get_width() // 2, py + 14))

        rects_slots = []
        for i in range(NB_SLOTS):
            sx = px + 20
            sy = py + 70 + i * 85
            rect = pygame.Rect(sx, sy, pw - 40, 70)
            rects_slots.append(rect)

            save = data_saves.get(str(i))
            survol = rect.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, (100, 80, 35) if survol else (70, 55, 25), rect, border_radius=8)
            pygame.draw.rect(screen, (160, 120, 60), rect, 2, border_radius=8)

            txt_slot = font_slot.render(f"Slot {i + 1}", True, (255, 215, 0))
            screen.blit(txt_slot, (sx + 10, sy + 8))

            if save:
                equipe = save.get("equipe", [])
                pv_total = sum(e["pv"] for e in equipe)
                pv_max = sum(e["pvmax"] for e in equipe)
                info = font_slot.render(
                    f"PV equipe : {pv_total}/{pv_max}   Or : {save.get('or', 0)}   Items : {len(save.get('inventaire', []))}",
                    True, (200, 190, 160))
                screen.blit(info, (sx + 10, sy + 38))
            else:
                vide = font_slot.render("— vide —", True, (100, 100, 100))
                screen.blit(vide, (sx + 10, sy + 38))

        if message and pygame.time.get_ticks() - msg_timer < 1500:
            txt_msg = font_slot.render(message, True, (100, 220, 100))
            screen.blit(txt_msg, (px + pw // 2 - txt_msg.get_width() // 2, py + ph - 55))

        rect_fermer = pygame.Rect(px + pw // 2 - 60, py + ph - 42, 120, 32)
        pygame.draw.rect(screen, (100, 40, 40), rect_fermer, border_radius=6)
        pygame.draw.rect(screen, (180, 80, 80), rect_fermer, 2, border_radius=6)
        txt_f = font_slot.render("Fermer", True, (255, 255, 255))
        screen.blit(txt_f, (rect_fermer.centerx - txt_f.get_width() // 2,
                              rect_fermer.centery - txt_f.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "ok"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "ok"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_fermer.collidepoint(event.pos):
                    return "ok"
                for i, rect in enumerate(rects_slots):
                    if rect.collidepoint(event.pos):
                        if data_saves.get(str(i)):
                            if not _popup_confirmation(screen, f"Écraser le slot {i + 1} ?", "Cette sauvegarde sera perdue."):
                                break
                        sauvegarder(i, player, liste_equipe, mon_inventaire, joueur_or)
                        data_saves = _charger_json()
                        message = f"✓ Sauvegardé dans le slot {i + 1} !"
                        msg_timer = pygame.time.get_ticks()
