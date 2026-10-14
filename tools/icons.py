# Bibliothèque d'icônes VERBUM (SVG en ligne, trait doré via currentColor).
# Règle absolue de la charte : aucune croix, aucun « + », aucune intersection
# perpendiculaire de deux traits. Utilisé par tools/build.py.

S = 'viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'

ICONS = {
    # Deux tables de pierre
    "tables": f'<svg {S}><path d="M8 56V22a10 10 0 0 1 20 0v34z"/><path d="M36 56V22a10 10 0 0 1 20 0v34z"/><path d="M13 27h10M13 33h10M13 39h7M41 27h10M41 33h10M41 39h7"/></svg>',
    # Plume de scribe et encrier
    "plume": f'<svg {S}><path d="M50 6C34 10 22 24 18 44l-2 8"/><path d="M50 6c-2 14-10 28-26 36"/><path d="M27 30c6-2 12-6 16-12"/><path d="M10 54h18l-2 6H12z"/></svg>',
    # Jarre de Qumrân et rouleau
    "jarre": f'<svg {S}><path d="M22 8h20a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H22a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2z"/><path d="M21 15c-6 8-6 32 0 43h22c6-11 6-35 0-43"/><path d="M24 26c5 2 11 2 16 0M23 44c6 2 12 2 18 0"/><ellipse cx="32" cy="35" rx="4" ry="2.5"/></svg>',
    # Codex ouvert
    "codex": f'<svg {S}><path d="M6 14c9-3 18-2 26 3 8-5 17-6 26-3v38c-9-3-18-2-26 3-8-5-17-6-26-3z"/><path d="M32 17v38"/><path d="M12 24c5-1 10-1 14 1M12 31c5-1 10-1 14 1M12 38c5-1 10-1 14 1M38 25c4-2 9-2 14-1M38 32c4-2 9-2 14-1M38 39c4-2 9-2 14-1"/></svg>',
    # Page fantôme sous la loupe multispectrale
    "spectre": f'<svg {S}><path d="M10 8h28l8 8v40H10z"/><path d="M38 8v8h8"/><path d="M16 22h16M16 28h20" stroke-dasharray="2 3"/><circle cx="36" cy="40" r="9"/><path d="M42.5 46.5L54 58"/><path d="M31 40c3-3 7-3 10 0" opacity=".7"/></svg>',
    # Rouleau déchiré (apocryphes)
    "dechire": f'<svg {S}><path d="M14 10h30a6 6 0 0 1 6 6v6"/><path d="M14 10a6 6 0 0 0-6 6v6h6"/><path d="M14 16v34l5-4 5 4 5-4 5 4 5-4 5 4V22"/><path d="M21 26h14M21 33h9" stroke-dasharray="3 3"/></svg>',
    # Langues : aleph hébreu et alpha grec
    "langues": f'<svg {S}><path d="M14 16l14 22M27 16c0 6-4 9-10 9M15 38c0-6 4-9 10-9"/><path d="M38 40l7-22 7 22M41 32h8"/><path d="M24 50c6 4 14 4 20 0" /><path d="M40 47l4 3-4 3"/></svg>',
    # Caractères mobiles (rangées décalées, aucune grille)
    "caracteres": f'<svg {S}><rect x="8" y="12" width="14" height="14" rx="2"/><rect x="25" y="12" width="14" height="14" rx="2"/><rect x="42" y="12" width="14" height="14" rx="2"/><rect x="16" y="32" width="14" height="14" rx="2"/><rect x="33" y="32" width="14" height="14" rx="2"/><path d="M12 22l3-7 3 7M29 22v-7h3a2 2 0 0 1 0 4h-3M49 15a3.5 3.5 0 1 0 0 7"/><path d="M8 54h48" opacity=".5"/></svg>',
    # Stèle inscrite
    "stele": f'<svg {S}><path d="M16 54V20C16 12 23 6 32 6s16 6 16 14v34z"/><path d="M22 20h20M22 26h20M22 32h16M22 38h20M22 44h12"/><path d="M8 59h48" opacity=".5"/></svg>',
    # Livre et flamme (résistance)
    "flamme": f'<svg {S}><path d="M32 6c6 7 9 12 9 17a9 9 0 0 1-18 0c0-3 1-5 3-7 0 3 2 5 4 5-1-6 0-10 2-15z"/><path d="M6 40c9-3 18-2 26 3 8-5 17-6 26-3v16c-9-3-18-2-26 3-8-5-17-6-26-3z"/><path d="M32 43v16"/></svg>',
    # Frise chronologique (losanges reliés, sans graduations)
    "frise": f'<svg {S}><path d="M4 32h7M21 32h10M41 32h10M60 32h1"/><path d="M16 26l5 6-5 6-5-6z"/><path d="M36 24l6 8-6 8-6-8z"/><path d="M55 26l5 6-5 6-5-6z"/><path d="M16 20v-4M36 16v-6M55 20v-4" opacity=".6"/></svg>',
    "livre-fr": f'<svg {S}><path d="M6 22c9-3 18-2 26 3 8-5 17-6 26-3v32c-9-3-18-2-26 3-8-5-17-6-26-3z"/><path d="M32 25v32"/><path d="M12 31c5-1 10-1 14 1M12 38c5-1 10-1 14 1M12 45c5-1 10-1 14 1M38 32c4-2 9-2 14-1M38 39c4-2 9-2 14-1M38 46c4-2 9-2 14-1"/><path d="M40 6c-6 2-10 7-11 13" /><path d="M40 6c0 6-3 10-8 12"/></svg>',
    "colonne": f'<svg {S}><path d="M14 10h36M18 10v4h28v-4M20 14v36M28 14v36M36 14v36M44 14v36M16 50h32v4H16zM12 58h40"/></svg>',
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h16M14 6l6 6-6 6"/></svg>'
CHEVRON_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>'
