import pygame
import os

pygame.init()

PERSONNAGES_DISPONIBLES = [
    {
        "nom":     "Fantôme",
        "cle":     "fantome",
        "image":   "assets/personnage log/fantome.png",
        "pvmax":   100,
        "attaque": "mage",
        "degat":   30,
        "portee":  200,
        "desc":    "Attaque de zone à distance",
    },
    {
        "nom":     "Rat",
        "cle":     "rat",
        "image":   "assets/personnage log/rat.png",
        "pvmax":   50,
        "attaque": "distance",
        "degat":   40,
        "portee":  300,
        "desc":    "Rapide, tire à distance",
    },
    {
        "nom":     "Pigeon",
        "cle":     "pigeon",
        "image":   "assets/personnage log/pigeon.png",
        "pvmax":   200,
        "attaque": "cac",
        "degat":   20,
        "portee":  200,
        "desc":    "Corps à corps robuste",
    },
    {
        "nom":     "Escargot",
        "cle":     "escargot",
        "image":   "assets/personnage log/escargot.png",
        "pvmax":   100,
        "attaque": "distance",
        "degat":   20,
        "portee":  300,
        "desc":    "Tireur solide",
    },
]

W, H = 1080, 720

fond = pygame.image.load("assets/bg_menu_equipe.png")
fond = pygame.transform.scale(fond, (W, H))


def _charger_image(chemin, taille):
    try:
        full = os.path.join(os.path.dirname(__file__), chemin)
        img  = pygame.image.load(full).convert_alpha()
        return pygame.transform.scale(img, taille)
    except Exception:
        surf = pygame.Surface(taille, pygame.SRCALPHA)
        surf.fill((40, 50, 80))
        return surf


def afficher_menu_equipe(screen):
    clock   = pygame.time.Clock()
    f_titre = pygame.font.Font(None, 48)
    f_nom   = pygame.font.Font(None, 30)
    f_small = pygame.font.Font(None, 24)
    f_btn   = pygame.font.Font(None, 32)

    images = [_charger_image(p["image"], (80, 80)) for p in PERSONNAGES_DISPONIBLES]

    equipe     = [None, None, None, None]
    slot_actif = None

    SLOT_W, SLOT_H = 200, 95
    SLOT_GAP       = 12
    SLOTS_X        = W // 2 - (4 * SLOT_W + 3 * SLOT_GAP) // 2
    SLOTS_Y        = 88

    NB       = len(PERSONNAGES_DISPONIBLES)
    CARD_W   = min(210, (W - 80) // NB - 14)
    CARD_H   = 255
    CARD_GAP = max(10, (W - 80 - NB * CARD_W) // (NB - 1)) if NB > 1 else 0
    CARDS_Y  = 240

    BTN_W, BTN_H = 160, 38
    btn_start = pygame.Rect(W // 2 + 20,  H - 55, BTN_W, BTN_H)
    btn_back  = pygame.Rect(W // 2 - 180, H - 55, BTN_W, BTN_H)

    while True:
        clock.tick(60)
        souris = pygame.mouse.get_pos()

        screen.blit(fond, (0, 0))

        voile = pygame.Surface((W, H), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 115))
        screen.blit(voile, (0, 0))

        t = f_titre.render("choisissez votre équipe", True, (155, 185, 230))
        screen.blit(t, (W // 2 - t.get_width() // 2, 22))

        slot_rects = []
        for i in range(4):
            sx = SLOTS_X + i * (SLOT_W + SLOT_GAP)
            r  = pygame.Rect(sx, SLOTS_Y, SLOT_W, SLOT_H)
            slot_rects.append(r)

            actif  = (slot_actif == i)
            survol = r.collidepoint(souris)

            fond_slot = pygame.Surface((SLOT_W, SLOT_H), pygame.SRCALPHA)
            if actif:
                fond_slot.fill((38, 55, 95, 215))
            elif survol:
                fond_slot.fill((28, 42, 75, 195))
            else:
                fond_slot.fill((15, 22, 42, 175))
            screen.blit(fond_slot, r)

            idx = equipe[i]
            if idx is not None:
                p = PERSONNAGES_DISPONIBLES[idx]
                screen.blit(images[idx], (sx + 6, SLOTS_Y + 8))
                screen.blit(f_nom.render(p["nom"], True, (185, 205, 240)), (sx + 94, SLOTS_Y + 20))
                screen.blit(f_small.render(p["attaque"], True, (95, 120, 165)), (sx + 94, SLOTS_Y + 52))
            else:
                label = f_nom.render(f"{i + 1}", True, (55, 75, 118))
                screen.blit(label, (sx + SLOT_W // 2 - label.get_width() // 2,
                                    SLOTS_Y + SLOT_H // 2 - label.get_height() // 2))

        card_rects = []
        for i, p in enumerate(PERSONNAGES_DISPONIBLES):
            cx = 40 + i * (CARD_W + CARD_GAP)
            r  = pygame.Rect(cx, CARDS_Y, CARD_W, CARD_H)
            card_rects.append(r)

            survol = r.collidepoint(souris)
            sel    = (slot_actif is not None and equipe[slot_actif] == i)

            fond_card = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
            if sel:
                fond_card.fill((38, 55, 95, 215))
            elif survol:
                fond_card.fill((28, 42, 75, 195))
            else:
                fond_card.fill((15, 22, 42, 170))
            screen.blit(fond_card, r)

            screen.blit(images[i], (cx + CARD_W // 2 - 40, CARDS_Y + 10))

            nom_t = f_nom.render(p["nom"], True, (185, 205, 240))
            screen.blit(nom_t, (cx + CARD_W // 2 - nom_t.get_width() // 2, CARDS_Y + 96))

            for j, ligne in enumerate([
                f"pv      {p['pvmax']}",
                f"type    {p['attaque']}",
                f"dégâts  {p['degat']}",
            ]):
                screen.blit(f_small.render(ligne, True, (95, 120, 165)), (cx + 12, CARDS_Y + 122 + j * 20))

            desc_t = f_small.render(p["desc"], True, (70, 90, 130))
            screen.blit(desc_t, (cx + CARD_W // 2 - desc_t.get_width() // 2, CARDS_Y + CARD_H - 24))

        sur_back = btn_back.collidepoint(souris)
        fond_b = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        fond_b.fill((32, 48, 82, 210) if sur_back else (18, 28, 52, 185))
        screen.blit(fond_b, btn_back)
        tb = f_btn.render("retour", True, (155, 185, 230))
        screen.blit(tb, (btn_back.centerx - tb.get_width() // 2,
                         btn_back.centery - tb.get_height() // 2))

        pret      = all(s is not None for s in equipe)
        sur_start = btn_start.collidepoint(souris) and pret
        fond_s = pygame.Surface((BTN_W, BTN_H), pygame.SRCALPHA)
        fond_s.fill((32, 48, 82, 210) if sur_start else (18, 28, 52, 185) if pret else (12, 18, 32, 140))
        screen.blit(fond_s, btn_start)
        ts = f_btn.render("commencer", True, (155, 185, 230) if pret else (45, 58, 82))
        screen.blit(ts, (btn_start.centerx - ts.get_width() // 2,
                         btn_start.centery - ts.get_height() // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if btn_back.collidepoint(pos):
                    return None

                if btn_start.collidepoint(pos) and pret:
                    return [PERSONNAGES_DISPONIBLES[idx]["cle"] for idx in equipe]

                clique_slot = False
                for i, r in enumerate(slot_rects):
                    if r.collidepoint(pos):
                        slot_actif = i
                        clique_slot = True
                        break

                if not clique_slot and slot_actif is not None:
                    for i, r in enumerate(card_rects):
                        if r.collidepoint(pos):
                            equipe[slot_actif] = i
                            break
