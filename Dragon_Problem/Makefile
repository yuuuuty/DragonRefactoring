PYCS	= $(shell find . -name "*.pyc")
PYOPENGL	= PyOpenGL-3.0.2
OPENGL	= OpenGL
TARGET	= dragon.py

all:
	@if [ ! -e $(PYOPENGL) ] ; then unzip $(PYOPENGL).zip ; fi
	@if [ ! -e $(OPENGL) ] ; then ln -s $(PYOPENGL)/$(OPENGL) $(OPENGL) ; fi

clean:
	@for each in ${PYCS} ; do echo "rm -f $${each}" ; rm -f $${each} ; done

wipe:
	if [ -e $(OPENGL) ] ; then rm -f $(OPENGL) ; fi
	if [ -e $(PYOPENGL) ] ; then rm -f -r $(PYOPENGL) ; fi

test: all
	python ${TARGET}
