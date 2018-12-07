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
	Extension("xcalc.admin",["xcalc/admin.py"]),
	Extension("xcalc.context_processors",["xcalc/context_processors.py"]),
	Extension("xcalc.curve_fitting",["xcalc/curve_fitting.py"]),
	Extension("xcalc.forms",["xcalc/forms.py"]),
	Extension("xcalc.models",["xcalc/models.py"]),
	Extension("xcalc.tests",["xcalc/tests.py"]),
        Extension("xcalc.views", ["xcalc/views.py"]),
	Extension("xcalc.views_general",["xcalc/views_general.py"]),
	Extension("xcalc.views_plan",["xcalc/views_plan.py"]),
	Extension("xcalc.views_export",["xcalc/views_export.py"]),
	Extension("xcalc.plancalc",["xcalc/plancalc.py"]),
	#Extension("xcalc.templatetags.sxt_filters",["xcalc/templatetags/sxt_filters.py"]),
	#Extension("xcalc.templatetags.admin_reorder_tag",["xcalc/templatetags/admin_reorder_tag.py"]),
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

