# -*- encoding: utf-8 -*-
from dna.views import (
    EveryCreateViewMixin,
    EveryUpdateViewMixin,
    EveryDeleteViewMixin,
    EveryEngageViewMixin,
    EveryListViewMixin,
    EveryManyViewMixin,
    EveryOptimizeViewMixin,
    EveryPageViewMixin,
    EveryHomeViewMixin,
)


class Criew(EveryCreateViewMixin):
    template_name = "molecule/thing_form.html"


class Uiew(EveryUpdateViewMixin):
    template_name = "molecule/thing_form.html"


class Diew(EveryDeleteViewMixin):
    template_name = "molecule/thing_delete.html"


class Eiew(EveryEngageViewMixin):
    template_name = "molecule/thing_engaged.html"


class Liew(EveryListViewMixin):
    template_name = "molecule/thing_listed.html"


class Miew(EveryManyViewMixin):
    template_name = "molecule/thing_many.html"


class Oiew(EveryOptimizeViewMixin):
    template_name = "molecule/thing_optimize.html"


class Piew(EveryPageViewMixin):
    template_name = "molecule/thing_page.html"


class Hiew(EveryHomeViewMixin):
    template_name = "molecule/home_page.html"
