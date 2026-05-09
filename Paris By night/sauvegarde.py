import pygame
import json
import os

pygame.init()

FICHIER_SAUVEGARDE = "sauvegardes.json"
NB_SLOTS = 3

fond = pygame.image.load("assets/bg_sauvegarde.png")
fond = pygame.transform.scale(fond, (1080, 720))


def _charger_json():
    if os.path.exists(FICHIER_SAUVEGARDE):
        with open(FICHIER_SAUVEGARDE, "r") as f:
            return json.load(f)
    return {}


def _ecrire_json(data):
    with open(FICHIER_SAUVEGARDE, "w") as f:
        json.dump(data, f, indent=2)


def sauvegarder(slot, player, liste_equipe, mon_inventaire, joueur_or, equipe_cles=None):
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

    if equipe_cles is None:
        equipe_cles = [p["nom"] for p in equipe_data]

    data[str(slot)] = {
        "joueur": {
            "x": float(player.position.x),
            "y": float(player.position.y),
            "pv": player.pv,
            "pvmax": player.pvmax,
        },
        "equipe": equipe_data,
        "equipe_cles": equipe_cles,
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

    return save_data.get("equipe_cles", None)


def _popup_confirmation(screen, ligne1, ligne2=""):
    width, height = screen.get_size()
    font_msg = pygame.font.Font(None, 36)
    font_btn = pygame.font.Font(None, 34)

    pw, ph = 460, 180
    px = width // 2 - pw // 2
    py = height // 2 - ph // 2
    rect_oui = pygame.Rect(px + 55, py + ph - 58, 130, 38)
    rect_non = pygame.Rect(px + 275, py + ph - 58, 130, 38)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        voile = pygame.Surface((width, height), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 180))
        screen.blit(voile, (0, 0))

        fond_panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        fond_panel.fill((18, 26, 48, 235))
        screen.blit(fond_panel, (px, py))
        pygame.draw.rect(screen, (65, 95, 148), (px, py, pw, ph), 1)

        txt1 = font_msg.render(ligne1, True, (185, 205, 240))
        screen.blit(txt1, (px + pw // 2 - txt1.get_width() // 2, py + 22))
        if ligne2:
            txt2 = font_msg.render(ligne2, True, (120, 145, 188))
            screen.blit(txt2, (px + pw // 2 - txt2.get_width() // 2, py + 58))

        survol_oui = rect_oui.collidepoint(pygame.mouse.get_pos())
        fond_oui = pygame.Surface((130, 38), pygame.SRCALPHA)
        fond_oui.fill((38, 62, 105, 220) if survol_oui else (25, 42, 75, 200))
        screen.blit(fond_oui, rect_oui)
        pygame.draw.rect(screen, (90, 130, 190) if survol_oui else (60, 95, 150), rect_oui, 1)
        t_oui = font_btn.render("oui", True, (195, 215, 250))
        screen.blit(t_oui, (rect_oui.centerx - t_oui.get_width() // 2, rect_oui.centery - t_oui.get_height() // 2))

        survol_non = rect_non.collidepoint(pygame.mouse.get_pos())
        fond_non = pygame.Surface((130, 38), pygame.SRCALPHA)
        fond_non.fill((80, 30, 30, 220) if survol_non else (55, 20, 20, 200))
        screen.blit(fond_non, rect_non)
        pygame.draw.rect(screen, (140, 65, 65) if survol_non else (100, 45, 45), rect_non, 1)
        t_non = font_btn.render("non", True, (220, 175, 175))
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

    fond_slot = pygame.Surface((sw, sh), pygame.SRCALPHA)
    fond_slot.fill((32, 48, 82, 200) if survol else (18, 28, 52, 175))
    screen.blit(fond_slot, rect)
    pygame.draw.rect(screen, (80, 115, 170) if survol else (50, 78, 128), rect, 1)

    txt_slot = font.render(f"slot {i + 1}", True, (155, 185, 230))
    screen.blit(txt_slot, (sx + 14, sy + 10))

    if save:
        equipe = save.get("equipe", [])
        pv_total = sum(e["pv"] for e in equipe)
        pv_max = sum(e["pvmax"] for e in equipe)
        or_ = save.get("or", 0)
        nb_items = len(save.get("inventaire", []))
        noms = ",  ".join(e["nom"] for e in equipe[:4])
        line1 = font.render(noms, True, (188, 205, 235))
        line2 = font.render(f"pv {pv_total}/{pv_max}    or {or_}    items {nb_items}", True, (105, 130, 170))
        screen.blit(line1, (sx + 14, sy + 46))
        screen.blit(line2, (sx + 14, sy + 76))
    else:
        vide = font.render("vide", True, (65, 85, 125))
        screen.blit(vide, (sx + 14, sy + sh // 2 - vide.get_height() // 2))

    return rect


def afficher_sauvegarde(screen, font):
    width, height = screen.get_size()
    font_titre  = pygame.font.Font(None, 58)
    font_slot   = pygame.font.Font(None, 32)
    font_retour = pygame.font.Font(None, 34)
    data_saves  = _charger_json()
    clock       = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.blit(fond, (0, 0))

        voile = pygame.Surface((width, height), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 100))
        screen.blit(voile, (0, 0))

        titre = font_titre.render("sauvegardes", True, (155, 185, 230))
        screen.blit(titre, (width // 2 - titre.get_width() // 2, 44))

        rects_slots = []
        for i in range(NB_SLOTS):
            rect = _dessiner_slot(screen, font_slot,
                                  width // 2 - 270, 130 + i * 148, 540, 108,
                                  i, data_saves.get(str(i)))
            rects_slots.append(rect)

        rect_retour = pygame.Rect(width // 2 - 70, height - 72, 140, 40)
        survol_retour = rect_retour.collidepoint(pygame.mouse.get_pos())
        fond_btn = pygame.Surface((140, 40), pygame.SRCALPHA)
        fond_btn.fill((32, 48, 82, 210) if survol_retour else (18, 28, 52, 185))
        screen.blit(fond_btn, rect_retour)
        pygame.draw.rect(screen, (80, 115, 170) if survol_retour else (50, 78, 128), rect_retour, 1)
        txt_retour = font_retour.render("retour", True, (175, 200, 240))
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


def afficher_sauvegarde_ingame(screen, font, player, liste_equipe, mon_inventaire, joueur_or, equipe_cles=None):
    width, height = screen.get_size()
    font_titre = pygame.font.Font(None, 46)
    font_slot  = pygame.font.Font(None, 30)
    data_saves = _charger_json()
    message    = ""
    msg_timer  = 0
    clock      = pygame.time.Clock()

    pw, ph = 500, 370
    px = width  // 2 - pw // 2
    py = height // 2 - ph // 2

    while True:
        clock.tick(60)

        voile = pygame.Surface((width, height), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 165))
        screen.blit(voile, (0, 0))

        fond_panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        fond_panel.fill((15, 22, 42, 235))
        screen.blit(fond_panel, (px, py))
        pygame.draw.rect(screen, (60, 90, 145), (px, py, pw, ph), 1)

        titre = font_titre.render("sauvegarder", True, (155, 185, 230))
        screen.blit(titre, (px + pw // 2 - titre.get_width() // 2, py + 14))

        rects_slots = []
        for i in range(NB_SLOTS):
            sx = px + 18
            sy = py + 62 + i * 82
            sw = pw - 36
            rect = pygame.Rect(sx, sy, sw, 68)
            rects_slots.append(rect)

            survol = rect.collidepoint(pygame.mouse.get_pos())
            fond_slot = pygame.Surface((sw, 68), pygame.SRCALPHA)
            fond_slot.fill((32, 48, 82, 200) if survol else (18, 28, 52, 170))
            screen.blit(fond_slot, rect)
            pygame.draw.rect(screen, (80, 115, 170) if survol else (48, 75, 125), rect, 1)

            save = data_saves.get(str(i))
            txt_slot = font_slot.render(f"slot {i + 1}", True, (155, 185, 230))
            screen.blit(txt_slot, (sx + 10, sy + 6))

            if save:
                equipe   = save.get("equipe", [])
                pv_total = sum(e["pv"]    for e in equipe)
                pv_max   = sum(e["pvmax"] for e in equipe)
                noms     = ",  ".join(e["nom"] for e in equipe[:4])
                info = font_slot.render(
                    f"{noms}   pv {pv_total}/{pv_max}   or {save.get('or', 0)}",
                    True, (140, 165, 210))
                screen.blit(info, (sx + 10, sy + 36))
            else:
                vide = font_slot.render("vide", True, (65, 85, 125))
                screen.blit(vide, (sx + 10, sy + 24))

        if message and pygame.time.get_ticks() - msg_timer < 1500:
            txt_msg = font_slot.render(message, True, (140, 200, 140))
            screen.blit(txt_msg, (px + pw // 2 - txt_msg.get_width() // 2, py + ph - 46))

        rect_fermer = pygame.Rect(px + pw // 2 - 52, py + ph - 38, 104, 28)
        survol_f = rect_fermer.collidepoint(pygame.mouse.get_pos())
        fond_f = pygame.Surface((104, 28), pygame.SRCALPHA)
        fond_f.fill((32, 48, 82, 210) if survol_f else (18, 28, 52, 185))
        screen.blit(fond_f, rect_fermer)
        pygame.draw.rect(screen, (80, 115, 170) if survol_f else (50, 78, 128), rect_fermer, 1)
        txt_f = font_slot.render("fermer", True, (175, 200, 240))
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
                            if not _popup_confirmation(screen, f"écraser le slot {i + 1} ?", "cette sauvegarde sera perdue."):
                                break
                        sauvegarder(i, player, liste_equipe, mon_inventaire, joueur_or, equipe_cles)
                        data_saves = _charger_json()
                        message    = f"sauvegardé dans le slot {i + 1}"
                        msg_timer  = pygame.time.get_ticks()
