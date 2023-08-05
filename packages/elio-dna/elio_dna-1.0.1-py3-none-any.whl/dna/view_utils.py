# -*- encoding: utf-8 -*-
from django.urls import reverse_lazy


def get_page_dna(site_dna, current_page):
    """Find the details of the current page in the SITE_DNA."""
    for menu_key in site_dna.keys():
        if menu_key == current_page:
            return site_dna[menu_key]
    for menu_values in site_dna.values():
        if isinstance(menu_values, dict):
            rtn = get_page_dna(menu_values, current_page)
            if rtn:
                return rtn
    return {}


def get_model_dna(page_dna, thing_name):
    """Find the details of a model of the current page in the SITE_DNA."""
    if not isinstance(page_dna, dict):
        return {}
    for elio_type in ["engage", "list"]:
        if thing_name in list(page_dna.get(elio_type, {})):
            if isinstance(page_dna[elio_type], dict):
                return page_dna[elio_type].get(thing_name, {})
    return {}


def menuactivator(menu_dna, current_page):
    """A lookahead to return if a menu has sub menus activated."""
    for page_key in menu_dna.get("page", {}).keys():
        if page_key == current_page:
            return True
    for page_vals in menu_dna.get("page", {}).values():
        if page_vals.get("page"):
            return menuactivator(page_vals, current_page)
    return False


def get_page_menu(site_dna, current_page, site_things=[]):
    """Convert the SITE_DNA into a menu."""
    menu = dict()
    for page_key, page_vals in site_dna.get("page", {}).items():
        menu[page_key] = dict()
        menu[page_key]["url"] = reverse_lazy(
            "engage.page", kwargs={"page_key": page_key}
        )
        if page_vals.get("status"):
            menu[page_key]["status"] = page_vals.get("status")
        if page_key == current_page:
            menu[page_key]["status"] = "active"
        if menu[page_key].get("status") or menuactivator(
            page_vals, current_page
        ):
            if not menu[page_key].get("status"):
                menu[page_key]["status"] = "crumb"  # Make the breadcrumbs
            sub_menu = get_page_menu(page_vals, current_page)
            if sub_menu.get("page"):
                menu[page_key].update(sub_menu)
    if site_things:
        menu["Browse Things"] = {"status": "label", "page": {}}
        for thing in sorted(site_things):
            menu["Browse Things"]["page"][thing] = dict()
            menu["Browse Things"]["page"][thing]["url"] = reverse_lazy(
                "list.things", kwargs={"page_key": thing, "thing": thing}
            )
            if thing == current_page:
                menu["Browse Things"]["page"][thing]["status"] = "active"
    return {"page": menu}
