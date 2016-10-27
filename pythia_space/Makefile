PYTHIA8_BIN=/Users/Yunjie/pythia8212/bin
PYTHIA8_INCLUDE=/Users/Yunjie/pythia8212/include
PYTHIA8_LIB=/Users/Yunjie/pythia8212/lib
PYTHIA8_SHARE=/Users/Yunjie/pythia8212/share/Pythia8


ENABLE_SHARED=true

CXX=g++
CXX_COMMON=-O2 -pedantic -W -Wall -Wshadow -fPIC
CXX_SHARED=-dynamiclib -flat_namespace -undefined suppress
CXX_SONAME=-Wl,-dylib_install_name
LIB_SUFFIX=.dylib

TARGET = pythia_gen

$(TARGET): $(TARGET).cc $(PYTHIA8_LIB)/libpythia8.a
	$(CXX) -std=c++11 $^ -o $(TARGET) -w -I$(PYTHIA8_INCLUDE) $(CXX_COMMON) 
clean:
	$(RM) $(TARGET)
