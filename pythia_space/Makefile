PYTHIA8_INCLUDE=$(PYTHIA8_HOME)/include
PYTHIA8_LIB=$(PYTHIA8_HOME)/lib

CXX=g++
CXX_COMMON=-O2 -pedantic -W -Wall -Wshadow -fPIC
CXX_SHARED=-dynamiclib -flat_namespace -undefined suppress
CXX_SONAME=-Wl,-dylib_install_name
LIB_SUFFIX=.dylib

TARGET = pythia_gen

$(TARGET): $(TARGET).cc $(PYTHIA8_LIB)/libpythia8.a
	$(CXX) -std=c++11 $^ -o $(TARGET) -w -I$(PYTHIA8_INCLUDE) $(CXX_COMMON) -ldl 
clean:
	$(RM) $(TARGET)
