from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
        Extension("sxtweb.version",["sxtweb/version.py"]),
	Extension("common.choices",["common/choices.py"]),
	Extension("common.errcode",["common/errcode.py"]),
	Extension("protocols.TG61.BSF_Wat", ["protocols/TG61/BSF_Wat.py"]),
	Extension("protocols.TG61.BSF_BoneWat",["protocols/TG61/BSF_BoneWat.py"]),
	Extension("protocols.TG61.BSF_CloseCone",["protocols/TG61/BSF_CloseCone.py"]),
	Extension("protocols.TG61.CMedWat",["protocols/TG61/CMedWat.py"]),
	Extension("protocols.TG61.HVLAlCu",["protocols/TG61/HVLAlCu.py"]),
	Extension("protocols.TG61.Mu_WatAir_air",["protocols/TG61/Mu_WatAir_air.py"]),
	Extension("protocols.TG61.Mu_WatAir_wat",["protocols/TG61/Mu_WatAir_wat.py"]),
	Extension("protocols.TG61.tests",["protocols/TG61/tests.py"]),
	Extension("tegmine.admin",["tegmine/admin.py"]),
	Extension("tegmine.context_processors",["tegmine/context_processors.py"]),
	Extension("tegmine.curve_fitting",["tegmine/curve_fitting.py"]),
	Extension("tegmine.forms",["tegmine/forms.py"]),
	Extension("tegmine.models",["tegmine/models.py"]),
	Extension("tegmine.tests",["tegmine/tests.py"]),
        Extension("tegmine.views", ["tegmine/views.py"]),
	Extension("tegmine.views_general",["tegmine/views_general.py"]),
	Extension("tegmine.views_plan",["tegmine/views_plan.py"]),
	Extension("tegmine.views_export",["tegmine/views_export.py"]),
	Extension("tegmine.plancalc",["tegmine/plancalc.py"]),
	#Extension("tegmine.templatetags.sxt_filters",["tegmine/templatetags/sxt_filters.py"]),
	#Extension("tegmine.templatetags.admin_reorder_tag",["tegmine/templatetags/admin_reorder_tag.py"]),
	]
#print ext_modules

setup(
	name = 'sxtweb',
	version='1.0',
	description='SuperDoCS',
	author='Lixin Zhan',
	author_email='lixinzhan@gmail.com',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules,
)

