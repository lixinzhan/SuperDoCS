from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = 	[Extension("BSF_Wat",["BSF_Wat.py"]),
		 Extension("BSF_BoneWat",["BSF_BoneWat.py"]),
		 Extension("CalibrationTable",["CalibrationTable.py"]),
		 Extension("TG61Data",["TG61Data.py"]),
		 Extension("CMedWat",["CMedWat.py"]),
		 Extension("HVLAlCu",["HVLAlCu.py"]),
		 Extension("Mu_WatAir_air",["Mu_WatAir_air.py"]),
		 Extension("Mu_WatAir_wat",["Mu_WatAir_wat.py"])
		]

print(ext_modules)

setup(
	name = 'django views module',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules
)

